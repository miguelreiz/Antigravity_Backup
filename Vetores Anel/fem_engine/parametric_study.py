"""
parametric_study.py -- Estudo Paramétrico Automatizado FEM-VOLUME ICRS.

Varia sistematicamente os parâmetros do anel (espessura, profundidade, diâmetro)
e registra o aplainamento apical e a elevação no track para cada configuração.

Gera curvas de sensibilidade biomecânica -- a base de um nomograma computacional.
"""

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import json

# ============================================================================
# Configuração do Estudo
# ============================================================================

FEBIO_PATH = r"C:\Program Files\FEBioStudio\bin\febio4.exe"

# Parâmetros fixos
RING_PROFILE = "triangular"
RING_BASE = 0.600  # mm

# Varreduras
THICKNESSES = [0.150, 0.200, 0.250, 0.300]  # mm
DEPTHS = [0.60, 0.70, 0.80]                  # fração da espessura
DIAMETERS = [5.0, 6.0]                        # mm


# ============================================================================
# Funções auxiliares (importadas do pipeline principal)
# ============================================================================

def generate_and_solve(label, has_ring, ring_thick, ring_depth_frac, ring_diam):
    """Gera malha, exporta FEBio, roda o solver."""
    import gmsh
    from mesh_generator import generate_cornea_ring_mesh
    from febio_builder import export_to_febio

    msh_file = f"param_{label}.msh"
    feb_file = f"param_{label}.feb"

    # Gerar malha
    generate_cornea_ring_mesh(
        output_filename=msh_file,
        has_ring=has_ring,
        ring_profile=RING_PROFILE,
        ring_thick=ring_thick,
        ring_base=RING_BASE,
        ring_depth_frac=ring_depth_frac,
        ring_diam=ring_diam,
    )
    gmsh.finalize()

    # Exportar FEBio
    gmsh.initialize()
    gmsh.open(msh_file)
    export_to_febio(output_feb_file=feb_file, baseline=(not has_ring))
    gmsh.finalize()

    # Rodar solver
    result = subprocess.run(
        [FEBIO_PATH, "-i", feb_file],
        capture_output=True, text=True,
    )
    converged = result.returncode == 0
    return feb_file, converged


def extract_apex_and_track(feb_file, disp_csv, r_ring):
    """Extrai Z deformado no ápice e no track."""
    if not os.path.exists(disp_csv):
        return None, None

    # Parsing geometry
    tree = ET.parse(feb_file)
    root = tree.getroot()
    nodes = {}
    for node in root.findall(".//node"):
        nid = int(node.get("id"))
        coords = [float(x) for x in node.text.split(",")]
        nodes[nid] = coords

    # Parsing displacement (last step)
    with open(disp_csv, "r") as f:
        lines = f.readlines()

    last_step_idx = 0
    for i, line in enumerate(lines):
        if "Step = 10" in line:
            last_step_idx = i

    disp = {}
    skip = ("*", "=", "Step", "Time", "Data", "File")
    for line in lines[last_step_idx:]:
        if line.strip() and not any(line.startswith(p) for p in skip):
            parts = line.strip().split(",")
            if len(parts) >= 4:
                nid = int(parts[0])
                disp[nid] = (float(parts[1]), float(parts[2]), float(parts[3]))

    # Extrair perfil anterior (Y~0, X>=0)
    r_vals, z_orig, z_def = [], [], []
    for nid, (x, y, z) in nodes.items():
        if abs(y) < 0.2 and x >= 0 and nid in disp:
            r_vals.append(x)
            z_orig.append(z)
            z_def.append(z + disp[nid][2])

    if not r_vals:
        return None, None

    r_vals = np.array(r_vals)
    z_orig = np.array(z_orig)
    z_def = np.array(z_def)

    # Binning
    bins = np.linspace(0, 5, 100)
    binned_r, binned_z = [], []
    for i in range(len(bins) - 1):
        mask = (r_vals >= bins[i]) & (r_vals < bins[i + 1])
        if np.any(mask):
            max_idx = np.argmax(z_orig[mask])
            binned_r.append(r_vals[mask][max_idx])
            binned_z.append(z_def[mask][max_idx])

    common_r = np.linspace(0, 4.5, 200)
    interp_z = np.interp(common_r, binned_r, binned_z)

    z_apex = interp_z[0]
    track_idx = np.argmin(np.abs(common_r - r_ring))
    z_track = interp_z[track_idx]

    return z_apex, z_track


# ============================================================================
# Pipeline Paramétrico
# ============================================================================

def run_parametric_study():
    print("=" * 64)
    print("  ESTUDO PARAMETRICO FEM-VOLUME ICRS (HGO)")
    print("=" * 64)

    # 1. Gerar e rodar o BASELINE (uma única vez)
    print("\n[BASELINE] Gerando cornea intacta...")
    base_feb, base_ok = generate_and_solve(
        "baseline", has_ring=False,
        ring_thick=0.200, ring_depth_frac=0.70, ring_diam=5.0,
    )
    if not base_ok:
        print("  FALHA no baseline. Abortando.")
        return

    base_disp = f"disp_param_baseline.csv"
    z_apex_base, _ = extract_apex_and_track(base_feb, base_disp, r_ring=2.5)
    if z_apex_base is None:
        print("  Sem dados do baseline. Abortando.")
        return

    print(f"  Baseline Z_apex = {z_apex_base*1000:.2f} um")

    # 2. Varredura paramétrica
    results = []

    total = len(THICKNESSES) * len(DEPTHS) * len(DIAMETERS)
    count = 0

    for diam in DIAMETERS:
        r_ring = diam / 2.0
        for depth in DEPTHS:
            for thick in THICKNESSES:
                count += 1
                label = f"D{diam:.0f}_d{int(depth*100)}_t{int(thick*1000)}"
                print(f"\n[{count}/{total}] {label}")

                feb_file, converged = generate_and_solve(
                    label, has_ring=True,
                    ring_thick=thick, ring_depth_frac=depth, ring_diam=diam,
                )

                if not converged:
                    print(f"  FALHA: {label}")
                    results.append({
                        "label": label, "diam": diam, "depth": depth,
                        "thick": thick, "converged": False,
                        "dz_apex": None, "dz_track": None,
                    })
                    continue

                disp_csv = f"disp_param_{label}.csv"
                z_apex, z_track = extract_apex_and_track(feb_file, disp_csv, r_ring)

                if z_apex is not None and z_apex_base is not None:
                    dz_apex = (z_apex - z_apex_base) * 1000  # um
                    # Para track, comparamos com o baseline no mesmo R
                    _, z_track_base = extract_apex_and_track(
                        base_feb, base_disp, r_ring
                    )
                    dz_track = (z_track - z_track_base) * 1000 if z_track_base else None
                else:
                    dz_apex = None
                    dz_track = None

                results.append({
                    "label": label, "diam": diam, "depth": depth,
                    "thick": thick, "converged": True,
                    "dz_apex": dz_apex, "dz_track": dz_track,
                })

                if dz_apex is not None:
                    print(f"  dZ_apex = {dz_apex:+.2f} um | dZ_track = {dz_track:+.2f} um")

    # 3. Salvar resultados brutos
    with open("parametric_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResultados salvos em parametric_results.json")

    # 4. Gerar gráficos de sensibilidade
    plot_sensitivity(results)


# ============================================================================
# Visualização
# ============================================================================

DARK_BG = "#161B22"
DARK_FG = "#0D1117"
GRID_COLOR = "#21262D"
SPINE_COLOR = "#6E7681"

def _style(ax):
    ax.set_facecolor(DARK_FG)
    ax.tick_params(colors="white")
    for s in ax.spines.values():
        s.set_color(SPINE_COLOR)
    ax.grid(color=GRID_COLOR, linestyle="--", alpha=0.5)


def plot_sensitivity(results):
    """Gera gráficos de sensibilidade: Espessura × Aplainamento."""
    valid = [r for r in results if r["converged"] and r["dz_track"] is not None]
    if not valid:
        print("Sem resultados validos para plotar.")
        return

    # --- Plot 1: Espessura vs Track Elevation (por profundidade, D=5mm) ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=DARK_BG)

    colors_depth = {0.60: "#FF7B72", 0.70: "#00D4AA", 0.80: "#BD93F9"}
    labels_depth = {0.60: "60%", 0.70: "70%", 0.80: "80%"}

    for ax_idx, diam in enumerate(DIAMETERS):
        ax = axes[ax_idx]
        _style(ax)
        ax.set_title(f"Diametro = {diam:.0f} mm", color="white", fontsize=12)

        for depth in DEPTHS:
            subset = [
                r for r in valid
                if r["diam"] == diam and r["depth"] == depth
            ]
            if not subset:
                continue

            thicks = [r["thick"] * 1000 for r in subset]  # um
            tracks = [r["dz_track"] for r in subset]

            ax.plot(
                thicks, tracks,
                marker="o", linewidth=2, markersize=8,
                color=colors_depth[depth],
                label=f"Prof. {labels_depth[depth]}",
            )

        ax.set_xlabel("Espessura do Anel (um)", color="white")
        ax.set_ylabel("Elevacao Track (um)", color="white")
        ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)

    fig.suptitle(
        "Sensibilidade: Espessura x Elevacao do Track (HGO)",
        color="white", fontsize=14,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig("parametric_track_elevation.png", dpi=150)
    print("Saved: parametric_track_elevation.png")

    # --- Plot 2: Espessura vs Apex Flattening ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=DARK_BG)

    for ax_idx, diam in enumerate(DIAMETERS):
        ax = axes[ax_idx]
        _style(ax)
        ax.set_title(f"Diametro = {diam:.0f} mm", color="white", fontsize=12)

        for depth in DEPTHS:
            subset = [
                r for r in valid
                if r["diam"] == diam and r["depth"] == depth
            ]
            if not subset:
                continue

            thicks = [r["thick"] * 1000 for r in subset]
            apexes = [r["dz_apex"] for r in subset]

            ax.plot(
                thicks, apexes,
                marker="s", linewidth=2, markersize=8,
                color=colors_depth[depth],
                label=f"Prof. {labels_depth[depth]}",
            )

        ax.axhline(0, color=SPINE_COLOR, linestyle="--", alpha=0.5)
        ax.set_xlabel("Espessura do Anel (um)", color="white")
        ax.set_ylabel("Delta Z Apex (um)", color="white")
        ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)

    fig.suptitle(
        "Sensibilidade: Espessura x Resposta Apical (HGO)",
        color="white", fontsize=14,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig("parametric_apex_response.png", dpi=150)
    print("Saved: parametric_apex_response.png")

    # --- Plot 3: Heatmap Depth x Thickness (D=5mm) ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=DARK_BG)

    for ax_idx, diam in enumerate(DIAMETERS):
        ax = axes[ax_idx]
        _style(ax)
        ax.set_title(f"Diametro = {diam:.0f} mm", color="white", fontsize=12)

        # Montar grid
        grid = np.full((len(DEPTHS), len(THICKNESSES)), np.nan)
        for r in valid:
            if r["diam"] == diam and r["dz_track"] is not None:
                di = DEPTHS.index(r["depth"])
                ti = THICKNESSES.index(r["thick"])
                grid[di, ti] = r["dz_track"]

        im = ax.imshow(
            grid, aspect="auto", cmap="inferno", origin="lower",
            extent=[
                THICKNESSES[0] * 1000 - 25, THICKNESSES[-1] * 1000 + 25,
                DEPTHS[0] * 100 - 5, DEPTHS[-1] * 100 + 5,
            ],
        )
        # Anotações
        for di, depth in enumerate(DEPTHS):
            for ti, thick in enumerate(THICKNESSES):
                if not np.isnan(grid[di, ti]):
                    ax.text(
                        thick * 1000, depth * 100,
                        f"{grid[di, ti]:.0f}",
                        ha="center", va="center",
                        color="white", fontsize=10, fontweight="bold",
                    )

        ax.set_xlabel("Espessura (um)", color="white")
        ax.set_ylabel("Profundidade (%)", color="white")
        plt.colorbar(im, ax=ax, label="Elevacao Track (um)")

    fig.suptitle(
        "Mapa Parametrico: Elevacao do Track (um)",
        color="white", fontsize=14,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig("parametric_heatmap.png", dpi=150)
    print("Saved: parametric_heatmap.png")


if __name__ == "__main__":
    run_parametric_study()
