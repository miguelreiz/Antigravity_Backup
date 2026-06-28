"""
analyze_ant_post_coupling.py — Anterior-Posterior Biomechanical Coupling Analysis.

Loads all FEM models (baseline + parametric D5/D6 × d60/d70/d80 × t150–t300,
plus model_baseline, model_triangular, model_oval), extracts both anterior
and posterior deformed profiles, and analyses the mechanical coupling between
the two corneal surfaces.

Outputs
-------
- fem_antpost_profiles_baseline.png   : overlay of ant / post for baseline
- fem_antpost_scatter_apex.png        : ΔZ_ant vs ΔZ_post scatter (all param)
- fem_antpost_coupling_heatmap.png    : coupling-ratio heatmap (thickness × depth)
- fem_antpost_vonmises_split.png      : ant vs post Von Mises radial profiles
- Console summary table
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------
# Import shared utilities from post_processor
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from post_processor import (
    parse_febio_geometry,
    parse_disp,
    parse_stress,
    extract_anterior_profile,
    extract_posterior_profile,
    _style_axis,
    DARK_BG,
    DARK_FG,
    GRID_COLOR,
    SPINE_COLOR,
    C_BASE,
    C_TRI,
    C_OVAL,
    C_DELTA,
    C_VM,
)

# Additional palette for coupling plots
C_ANT = "#58A6FF"   # anterior – blue
C_POST = "#F97583"  # posterior – red/pink
C_SCATTER = "#79C0FF"
C_HEATMAP = "magma"

FEM_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# Helpers
# ============================================================================

def _extract_original_profiles(nodes):
    """Return (common_r, z_orig_ant, z_orig_post) for undeformed geometry.

    Uses the same radial binning as the profile extractors but applied
    to the original (zero-displacement) geometry.
    """
    r_vals, z_vals = [], []
    for nid, (x, y, z) in nodes.items():
        if abs(y) < 0.2 and x >= 0:
            r_vals.append(x)
            z_vals.append(z)

    if not r_vals:
        return None, None, None

    r_vals = np.array(r_vals)
    z_vals = np.array(z_vals)

    bins = np.linspace(0, 5, 100)
    binned_r_ant, binned_z_ant = [], []
    binned_r_post, binned_z_post = [], []
    for i in range(len(bins) - 1):
        mask = (r_vals >= bins[i]) & (r_vals < bins[i + 1])
        if np.any(mask):
            max_idx = np.argmax(z_vals[mask])
            binned_r_ant.append(r_vals[mask][max_idx])
            binned_z_ant.append(z_vals[mask][max_idx])

            min_idx = np.argmin(z_vals[mask])
            binned_r_post.append(r_vals[mask][min_idx])
            binned_z_post.append(z_vals[mask][min_idx])

    common_r = np.linspace(0, 4.5, 200)
    z_ant = np.interp(common_r, binned_r_ant, binned_z_ant)
    z_post = np.interp(common_r, binned_r_post, binned_z_post)
    return common_r, z_ant, z_post


def _vonmises_split(feb_file, stress_dict, nodes):
    """Split Von Mises into anterior-half and posterior-half radial profiles.

    Elements whose centroid Z > Z_mid are assigned to the anterior half;
    elements with Z <= Z_mid to the posterior half, where Z_mid is the
    mid-thickness at each radial bin.
    """
    if stress_dict is None:
        return None, None, None, None

    tree = ET.parse(feb_file)
    root = tree.getroot()

    # Parse element connectivity
    elem_centroids = {}
    for elem in root.findall(".//elem"):
        eid_str = elem.get("id")
        if eid_str is None:
            continue
        eid = int(eid_str)
        node_ids = [int(x) for x in elem.text.split(",")]
        if eid in stress_dict:
            coords = np.array([nodes[nid] for nid in node_ids if nid in nodes])
            if len(coords) > 0:
                elem_centroids[eid] = coords.mean(axis=0)

    if not elem_centroids:
        return None, None, None, None

    # Compute per-element radial distance and Z
    eids = list(elem_centroids.keys())
    e_r = np.array([np.sqrt(elem_centroids[e][0]**2 + elem_centroids[e][1]**2) for e in eids])
    e_z = np.array([elem_centroids[e][2] for e in eids])
    e_vm = np.array([stress_dict[e] for e in eids])

    # Z_mid per radial bin
    bins = np.linspace(0, 5, 50)
    ant_r, ant_vm, post_r, post_vm = [], [], [], []
    for i in range(len(bins) - 1):
        mask_bin = (e_r >= bins[i]) & (e_r < bins[i + 1])
        if not np.any(mask_bin):
            continue
        z_mid = (e_z[mask_bin].max() + e_z[mask_bin].min()) / 2.0
        r_center = (bins[i] + bins[i + 1]) / 2.0

        ant_mask = mask_bin & (e_z > z_mid)
        post_mask = mask_bin & (e_z <= z_mid)

        if np.any(ant_mask):
            ant_r.append(r_center)
            ant_vm.append(np.mean(e_vm[ant_mask]))
        if np.any(post_mask):
            post_r.append(r_center)
            post_vm.append(np.mean(e_vm[post_mask]))

    return (np.array(ant_r) if ant_r else None,
            np.array(ant_vm) if ant_vm else None,
            np.array(post_r) if post_r else None,
            np.array(post_vm) if post_vm else None)


def _find_closest_idx(arr, value):
    """Index of the element in *arr* closest to *value*."""
    return int(np.argmin(np.abs(arr - value)))


# ============================================================================
# Model Discovery
# ============================================================================

def discover_models():
    """Return dict {name: (feb_path, disp_path, stress_path)}."""
    models = {}

    # Parametric baseline
    for prefix in ("param_baseline", ):
        feb = os.path.join(FEM_DIR, f"{prefix}.feb")
        if os.path.exists(feb):
            models[prefix] = (
                feb,
                os.path.join(FEM_DIR, f"disp_{prefix}.csv"),
                os.path.join(FEM_DIR, f"stress_{prefix}.csv"),
            )

    # Parametric ring variants
    for D in ("D5", "D6"):
        for d in ("d60", "d70", "d80"):
            for t in ("t150", "t200", "t250", "t300"):
                name = f"param_{D}_{d}_{t}"
                feb = os.path.join(FEM_DIR, f"{name}.feb")
                if os.path.exists(feb):
                    models[name] = (
                        feb,
                        os.path.join(FEM_DIR, f"disp_{name}.csv"),
                        os.path.join(FEM_DIR, f"stress_{name}.csv"),
                    )

    # Morphological models
    for shape in ("baseline", "triangular", "oval"):
        name = f"model_{shape}"
        feb = os.path.join(FEM_DIR, f"{name}.feb")
        if os.path.exists(feb):
            models[name] = (
                feb,
                os.path.join(FEM_DIR, f"disp_{name}.csv"),
                os.path.join(FEM_DIR, f"stress_{name}.csv"),
            )

    return models


# ============================================================================
# Main Analysis
# ============================================================================

def main():
    print("=" * 70)
    print("  ANTERIOR-POSTERIOR COUPLING ANALYSIS")
    print("=" * 70)

    models = discover_models()
    print(f"\n  Discovered {len(models)} models.\n")

    # ------------------------------------------------------------------
    # Load all models
    # ------------------------------------------------------------------
    data = {}
    for name, (feb, disp_csv, stress_csv) in models.items():
        print(f"  Loading {name} …", end=" ")
        nodes = parse_febio_geometry(feb)
        disp = parse_disp(disp_csv)
        stress = parse_stress(stress_csv)

        r_ant, z_ant = extract_anterior_profile(nodes, disp)
        r_post, z_post = extract_posterior_profile(nodes, disp)
        r_orig, z_orig_ant, z_orig_post = _extract_original_profiles(nodes)

        data[name] = {
            "nodes": nodes,
            "disp": disp,
            "stress": stress,
            "feb": feb,
            "r_ant": r_ant, "z_ant": z_ant,
            "r_post": r_post, "z_post": z_post,
            "r_orig": r_orig, "z_orig_ant": z_orig_ant, "z_orig_post": z_orig_post,
        }
        status = "OK" if (z_ant is not None and z_post is not None) else "PARTIAL"
        print(status)

    # ------------------------------------------------------------------
    # Compute ΔZ for every model
    # ------------------------------------------------------------------
    for name, d in data.items():
        if d["z_ant"] is not None and d["z_orig_ant"] is not None:
            d["dz_ant"] = d["z_ant"] - d["z_orig_ant"]
        else:
            d["dz_ant"] = None
        if d["z_post"] is not None and d["z_orig_post"] is not None:
            d["dz_post"] = d["z_post"] - d["z_orig_post"]
        else:
            d["dz_post"] = None

    # Coupling ratio at apex (R≈0), mid (R=2.5), periphery (R=4)
    radii_of_interest = {"apex": 0.0, "mid": 2.5, "periph": 4.0}
    coupling = {}
    for name, d in data.items():
        if d["dz_ant"] is None or d["dz_post"] is None:
            continue
        r = d["r_ant"]
        cr = {}
        for label, r_val in radii_of_interest.items():
            idx = _find_closest_idx(r, r_val)
            dz_a = d["dz_ant"][idx]
            dz_p = d["dz_post"][idx]
            cr[label] = dz_a / dz_p if abs(dz_p) > 1e-9 else np.nan
        coupling[name] = cr

    # ------------------------------------------------------------------
    # Console summary table
    # ------------------------------------------------------------------
    print("\n" + "=" * 90)
    print(f"  {'Model':30s} | {'dZ_ant apex':>12s} | {'dZ_post apex':>12s} | "
          f"{'Ratio apex':>10s} | {'Ratio mid':>10s} | {'Ratio peri':>10s}")
    print("-" * 90)
    for name in sorted(data.keys()):
        d = data[name]
        if d["dz_ant"] is None:
            continue
        r = d["r_ant"]
        idx_apex = _find_closest_idx(r, 0.0)
        dz_a = d["dz_ant"][idx_apex] * 1000  # um
        dz_p = d["dz_post"][idx_apex] * 1000 if d["dz_post"] is not None else float("nan")
        cr = coupling.get(name, {})
        print(f"  {name:30s} | {dz_a:+12.2f} um | {dz_p:+12.2f} um | "
              f"{cr.get('apex', float('nan')):10.3f} | "
              f"{cr.get('mid', float('nan')):10.3f} | "
              f"{cr.get('periph', float('nan')):10.3f}")
    print("=" * 90)

    # ------------------------------------------------------------------
    # Export coupling results as CSV for integration with hypothesis dashboard
    # ------------------------------------------------------------------
    rows = []
    for name in sorted(data.keys()):
        d = data[name]
        if d["dz_ant"] is None:
            continue
        r = d["r_ant"]
        idx_apex = _find_closest_idx(r, 0.0)
        idx_mid = _find_closest_idx(r, 2.5)
        idx_peri = _find_closest_idx(r, 4.0)
        cr = coupling.get(name, {})
        rows.append({
            'model': name,
            'dz_ant_apex': d["dz_ant"][idx_apex] * 1000,
            'dz_post_apex': d["dz_post"][idx_apex] * 1000 if d["dz_post"] is not None else np.nan,
            'dz_ant_mid': d["dz_ant"][idx_mid] * 1000,
            'dz_post_mid': d["dz_post"][idx_mid] * 1000 if d["dz_post"] is not None else np.nan,
            'dz_ant_peri': d["dz_ant"][idx_peri] * 1000,
            'dz_post_peri': d["dz_post"][idx_peri] * 1000 if d["dz_post"] is not None else np.nan,
            'coupling_apex': cr.get('apex', np.nan),
            'coupling_mid': cr.get('mid', np.nan),
            'coupling_periph': cr.get('periph', np.nan),
        })
    
    import pandas as pd
    df_coupling = pd.DataFrame(rows)
    csv_path = os.path.join(FEM_DIR, 'ant_post_coupling_results.csv')
    df_coupling.to_csv(csv_path, index=False, sep=';')
    print(f"\n  Coupling CSV salvo: {csv_path}")

    # ==================================================================
    # PLOT 1 — Anterior vs Posterior deformed profiles (baseline)
    # ==================================================================
    baseline_key = "param_baseline" if "param_baseline" in data else "model_baseline"
    bl = data.get(baseline_key)

    if bl and bl["z_ant"] is not None and bl["z_post"] is not None:
        fig, ax = plt.subplots(figsize=(11, 6), facecolor=DARK_BG)
        _style_axis(ax)

        ax.plot(bl["r_ant"], bl["z_ant"] * 1000,
                color=C_ANT, linewidth=2.5, label="Anterior (deformado)")
        ax.plot(bl["r_post"], bl["z_post"] * 1000,
                color=C_POST, linewidth=2.5, label="Posterior (deformado)")

        # Original profiles
        if bl["z_orig_ant"] is not None:
            ax.plot(bl["r_orig"], bl["z_orig_ant"] * 1000,
                    color=C_ANT, linewidth=1, linestyle="--", alpha=0.5,
                    label="Anterior (original)")
        if bl["z_orig_post"] is not None:
            ax.plot(bl["r_orig"], bl["z_orig_post"] * 1000,
                    color=C_POST, linewidth=1, linestyle="--", alpha=0.5,
                    label="Posterior (original)")

        ax.axvline(2.5, color=SPINE_COLOR, linestyle=":", alpha=0.6,
                   label="Track do Anel (R=2.5 mm)")
        ax.set_title("Baseline: Perfis Anterior e Posterior",
                     color="white", fontsize=14)
        ax.set_xlabel("Distância Radial (mm)", color="white")
        ax.set_ylabel("Elevação Z (µm)", color="white")
        ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)
        fig.tight_layout()
        outpath = os.path.join(FEM_DIR, "fem_antpost_profiles_baseline.png")
        fig.savefig(outpath, dpi=150)
        plt.close(fig)
        print(f"\n  Saved: {outpath}")

    # ==================================================================
    # PLOT 2 — Scatter: ΔZ_anterior vs ΔZ_posterior at apex (parametric)
    # ==================================================================
    param_names = [n for n in data if n.startswith("param_") and n != "param_baseline"]
    scatter_ant, scatter_post, scatter_labels = [], [], []
    for name in param_names:
        d = data[name]
        if d["dz_ant"] is None or d["dz_post"] is None:
            continue
        idx = _find_closest_idx(d["r_ant"], 0.0)
        scatter_ant.append(d["dz_ant"][idx] * 1000)
        scatter_post.append(d["dz_post"][idx] * 1000)
        scatter_labels.append(name.replace("param_", ""))

    if scatter_ant:
        fig, ax = plt.subplots(figsize=(8, 8), facecolor=DARK_BG)
        _style_axis(ax)

        ax.scatter(scatter_post, scatter_ant, c=C_SCATTER, s=80,
                   edgecolors="white", linewidths=0.5, zorder=5)

        # Annotate each point
        for i, lbl in enumerate(scatter_labels):
            ax.annotate(lbl, (scatter_post[i], scatter_ant[i]),
                        textcoords="offset points", xytext=(6, 6),
                        color="white", fontsize=7, alpha=0.85)

        # Reference line y=x
        all_vals = scatter_ant + scatter_post
        lo, hi = min(all_vals), max(all_vals)
        margin = (hi - lo) * 0.1
        ref = np.linspace(lo - margin, hi + margin, 50)
        ax.plot(ref, ref, "--", color=SPINE_COLOR, alpha=0.5, label="1:1")

        ax.set_title("Acoplamento Anterior-Posterior no Ápex",
                     color="white", fontsize=14)
        ax.set_xlabel("ΔZ Posterior no Ápex (µm)", color="white")
        ax.set_ylabel("ΔZ Anterior no Ápex (µm)", color="white")
        ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)
        fig.tight_layout()
        outpath = os.path.join(FEM_DIR, "fem_antpost_scatter_apex.png")
        fig.savefig(outpath, dpi=150)
        plt.close(fig)
        print(f"  Saved: {outpath}")

    # ==================================================================
    # PLOT 3 — Coupling ratio heatmap (thickness × depth)
    # ==================================================================
    depths = ["d60", "d70", "d80"]
    thicknesses = ["t150", "t200", "t250", "t300"]
    diameters = ["D5", "D6"]

    # Build one heatmap per diameter
    for D in diameters:
        matrix = np.full((len(thicknesses), len(depths)), np.nan)
        for j, d in enumerate(depths):
            for i, t in enumerate(thicknesses):
                key = f"param_{D}_{d}_{t}"
                if key in coupling:
                    matrix[i, j] = coupling[key].get("apex", np.nan)

        if np.all(np.isnan(matrix)):
            continue

        fig, ax = plt.subplots(figsize=(7, 5), facecolor=DARK_BG)
        _style_axis(ax)

        im = ax.imshow(matrix, cmap=C_HEATMAP, aspect="auto",
                       origin="lower")
        ax.set_xticks(range(len(depths)))
        ax.set_xticklabels([x.replace("d", "") + "%" for x in depths], color="white")
        ax.set_yticks(range(len(thicknesses)))
        ax.set_yticklabels([x.replace("t", "") + " µm" for x in thicknesses], color="white")
        ax.set_xlabel("Profundidade de Implantação", color="white")
        ax.set_ylabel("Espessura do Anel", color="white")
        ax.set_title(f"Coupling Ratio no Ápex — Ø{D.replace('D','')} mm",
                     color="white", fontsize=14)

        # Annotate cells
        for i in range(len(thicknesses)):
            for j in range(len(depths)):
                val = matrix[i, j]
                if not np.isnan(val):
                    txt_color = "white" if val < np.nanmedian(matrix) else "black"
                    ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                            color=txt_color, fontsize=11, fontweight="bold")

        cbar = fig.colorbar(im, ax=ax, shrink=0.85)
        cbar.ax.yaxis.set_tick_params(color="white")
        cbar.ax.tick_params(labelcolor="white")
        cbar.set_label("ΔZ_ant / ΔZ_post", color="white")

        fig.tight_layout()
        outpath = os.path.join(FEM_DIR, f"fem_antpost_coupling_heatmap_{D}.png")
        fig.savefig(outpath, dpi=150)
        plt.close(fig)
        print(f"  Saved: {outpath}")

    # ==================================================================
    # PLOT 4 — Anterior vs Posterior Von Mises radial profiles
    # ==================================================================
    vm_models = {
        "model_baseline":    (C_BASE, "Baseline"),
        "model_triangular":  (C_TRI,  "Triangular"),
        "model_oval":        (C_OVAL, "Oval"),
    }

    has_any_vm = False
    vm_data = {}
    for name, (color, label) in vm_models.items():
        if name not in data or data[name]["stress"] is None:
            continue
        ar, avm, pr, pvm = _vonmises_split(
            data[name]["feb"], data[name]["stress"], data[name]["nodes"])
        if ar is not None:
            vm_data[name] = {"ar": ar, "avm": avm, "pr": pr, "pvm": pvm,
                             "color": color, "label": label}
            has_any_vm = True

    if has_any_vm:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6),
                                       facecolor=DARK_BG, sharey=True)
        _style_axis(ax1)
        _style_axis(ax2)

        for name, vd in vm_data.items():
            if vd["ar"] is not None:
                ax1.plot(vd["ar"], vd["avm"], color=vd["color"],
                         linewidth=2, label=vd["label"])
            if vd["pr"] is not None:
                ax2.plot(vd["pr"], vd["pvm"], color=vd["color"],
                         linewidth=2, label=vd["label"])

        ax1.axvline(2.5, color=SPINE_COLOR, linestyle=":", alpha=0.6)
        ax2.axvline(2.5, color=SPINE_COLOR, linestyle=":", alpha=0.6)

        ax1.set_title("Von Mises — Metade Anterior", color="white", fontsize=13)
        ax2.set_title("Von Mises — Metade Posterior", color="white", fontsize=13)
        ax1.set_xlabel("Distância Radial (mm)", color="white")
        ax2.set_xlabel("Distância Radial (mm)", color="white")
        ax1.set_ylabel("Von Mises (MPa)", color="white")
        ax1.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)
        ax2.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)

        fig.tight_layout()
        outpath = os.path.join(FEM_DIR, "fem_antpost_vonmises_split.png")
        fig.savefig(outpath, dpi=150)
        plt.close(fig)
        print(f"  Saved: {outpath}")

    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  Anterior-Posterior coupling analysis complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
