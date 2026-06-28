"""
advanced_analysis.py -- Analise Avancada FEM-VOLUME ICRS

Modulo 1: Mapa 2D de Von Mises na secao transversal (Y~0)
Modulo 2: Calculo do Encurtamento Funcional de Arco (Arc Shortening)
Modulo 3: Dashboard de Validacao Completa
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import xml.etree.ElementTree as ET
import os


# ============================================================================
# Parsing
# ============================================================================

def parse_geometry_and_elements(feb_file):
    """Extrai nos e elementos hex8 com centroide e nodes do .feb."""
    tree = ET.parse(feb_file)
    root = tree.getroot()

    nodes = {}
    for node in root.findall(".//node"):
        nid_str = node.get("id")
        if nid_str is None:
            continue
        nid = int(nid_str)
        coords = [float(x) for x in node.text.split(",")]
        nodes[nid] = np.array(coords)

    elements = {}
    for elem in root.findall(".//elem"):
        eid_str = elem.get("id")
        if eid_str is None:
            continue
        eid = int(eid_str)
        try:
            node_ids = [int(x) for x in elem.text.split(",")]
            if len(node_ids) >= 6:
                coords = np.array([nodes[n] for n in node_ids if n in nodes])
                centroid = coords.mean(axis=0)
                elements[eid] = {"nodes": node_ids, "centroid": centroid}
        except (ValueError, KeyError):
            pass

    return nodes, elements


def parse_stress(stress_file):
    """Le o ultimo passo de stress do CSV do FEBio."""
    if not os.path.exists(stress_file):
        return None
    with open(stress_file, "r") as f:
        lines = f.readlines()

    last_step_idx = 0
    for i, line in enumerate(lines):
        if "Step = 10" in line:
            last_step_idx = i

    stress = {}
    skip = ("*", "=", "Step", "Time", "Data", "File")
    for line in lines[last_step_idx:]:
        if line.strip() and not any(line.startswith(p) for p in skip):
            parts = line.strip().split(",")
            if len(parts) >= 7:
                eid = int(parts[0])
                sx, sy, sz = float(parts[1]), float(parts[2]), float(parts[3])
                sxy, syz, sxz = float(parts[4]), float(parts[5]), float(parts[6])
                vm = np.sqrt(
                    0.5 * ((sx - sy)**2 + (sy - sz)**2 + (sz - sx)**2)
                    + 3.0 * (sxy**2 + syz**2 + sxz**2)
                )
                stress[eid] = {"vm": vm, "sx": sx, "sy": sy, "sz": sz}
    return stress


def parse_disp(disp_file):
    """Le o ultimo passo de deslocamento do CSV do FEBio."""
    if not os.path.exists(disp_file):
        return None
    with open(disp_file, "r") as f:
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
                disp[nid] = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
    return disp


# ============================================================================
# Modulo 1: Von Mises Cross-Section Map
# ============================================================================

def plot_vonmises_cross_section(feb_file, stress_dict, title_suffix=""):
    """Gera mapa 2D de Von Mises na secao transversal (plano Y~0)."""
    if stress_dict is None:
        print(f"  [SKIP] Sem dados de stress para {title_suffix}")
        return

    _, elements = parse_geometry_and_elements(feb_file)

    # Filtrar elementos no plano Y~0
    xs, zs, vms = [], [], []
    for eid, edata in elements.items():
        c = edata["centroid"]
        if abs(c[1]) < 0.3 and eid in stress_dict:
            xs.append(c[0])
            zs.append(c[2])
            vms.append(stress_dict[eid]["vm"])

    if not xs:
        print(f"  [SKIP] Sem elementos no plano Y~0 para {title_suffix}")
        return

    xs = np.array(xs)
    zs = np.array(zs)
    vms = np.array(vms)

    return xs, zs, vms


def generate_vonmises_dashboard():
    """Gera dashboard com 3 mapas de Von Mises lado a lado."""
    DARK_BG = "#161B22"
    DARK_FG = "#0D1117"
    SPINE_COLOR = "#6E7681"

    models = [
        ("model_baseline.feb", "stress_model_baseline.csv", "Baseline (Apenas PIO)"),
        ("model_triangular.feb", "stress_model_triangular.csv", "Anel Triangular (Ferrara)"),
        ("model_oval.feb", "stress_model_oval.csv", "Anel Oval (Keraring)"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor=DARK_BG)

    vmin_global, vmax_global = 1e9, 0

    all_data = []
    for feb, stress_csv, label in models:
        if not os.path.exists(feb):
            all_data.append(None)
            continue
        stress = parse_stress(stress_csv)
        result = plot_vonmises_cross_section(feb, stress, label)
        if result is not None:
            xs, zs, vms = result
            vmin_global = min(vmin_global, vms.min())
            vmax_global = max(vmax_global, np.percentile(vms, 95))
            all_data.append((xs, zs, vms, label))
        else:
            all_data.append(None)

    for idx, ax in enumerate(axes):
        ax.set_facecolor(DARK_FG)
        ax.tick_params(colors="white")
        for s in ax.spines.values():
            s.set_color(SPINE_COLOR)

        if all_data[idx] is not None:
            xs, zs, vms, label = all_data[idx]
            # Triangular interpolation for smooth colormap
            triang = mtri.Triangulation(xs, zs)
            tcf = ax.tricontourf(triang, vms, levels=30, cmap="inferno",
                                 vmin=vmin_global, vmax=vmax_global)
            ax.tricontour(triang, vms, levels=10, colors="white",
                          linewidths=0.3, alpha=0.3)
            ax.set_title(label, color="white", fontsize=11)
        else:
            ax.set_title(models[idx][2] + " (N/A)", color="white", fontsize=11)

        ax.set_xlabel("X (mm)", color="white")
        ax.set_ylabel("Z (mm)", color="white")
        ax.set_aspect("equal")

    # Colorbar
    if any(d is not None for d in all_data):
        cbar = fig.colorbar(tcf, ax=axes.ravel().tolist(), shrink=0.8)
        cbar.set_label("Von Mises (MPa)", color="white")
        cbar.ax.yaxis.set_tick_params(color="white")
        plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")

    fig.suptitle("Mapa de Von Mises -- Secao Transversal (Y=0)",
                 color="white", fontsize=14, y=0.98)
    fig.tight_layout(rect=[0, 0, 0.92, 0.95])
    fig.savefig("fem_vonmises_crosssection.png", dpi=150)
    print("  Saved: fem_vonmises_crosssection.png")


# ============================================================================
# Modulo 2: Arc Shortening Analysis
# ============================================================================

def compute_arc_length(nodes, disp, r_ant=7.8):
    """
    Calcula o comprimento funcional do arco anterior (R=0 ate R=4mm).

    O arco anterior eh a curva formada pelos nos da face anterior (maior Z)
    no plano Y~0. Calculamos a soma dos segmentos lineares entre nos
    adjacentes, antes e depois da deformacao.
    """
    if disp is None:
        return None, None

    # Coletar nos anteriores no plano Y~0
    pts_orig = []
    pts_def = []
    for nid, coord in nodes.items():
        x, y, z = coord
        if abs(y) < 0.2 and x >= 0 and nid in disp:
            pts_orig.append([x, z])
            pts_def.append([x, z + disp[nid][2]])

    if len(pts_orig) < 10:
        return None, None

    pts_orig = np.array(pts_orig)
    pts_def = np.array(pts_def)

    # Binning para pegar o no mais anterior (maior Z) por faixa radial
    bins = np.linspace(0, 4.0, 80)
    arc_orig_pts = []
    arc_def_pts = []
    for i in range(len(bins) - 1):
        mask = (pts_orig[:, 0] >= bins[i]) & (pts_orig[:, 0] < bins[i + 1])
        if np.any(mask):
            # Pegar o ponto com maior Z original (face anterior)
            max_idx = np.argmax(pts_orig[mask, 1])
            arc_orig_pts.append(pts_orig[mask][max_idx])
            arc_def_pts.append(pts_def[mask][max_idx])

    if len(arc_orig_pts) < 5:
        return None, None

    arc_orig_pts = np.array(arc_orig_pts)
    arc_def_pts = np.array(arc_def_pts)

    # Ordenar por X
    sort_idx = np.argsort(arc_orig_pts[:, 0])
    arc_orig_pts = arc_orig_pts[sort_idx]
    arc_def_pts = arc_def_pts[sort_idx]

    # Comprimento do arco = soma dos segmentos
    def arc_len(pts):
        diffs = np.diff(pts, axis=0)
        return np.sum(np.sqrt(diffs[:, 0]**2 + diffs[:, 1]**2))

    L_orig = arc_len(arc_orig_pts)
    L_def = arc_len(arc_def_pts)

    return L_orig, L_def


def analyze_arc_shortening():
    """Analisa o encurtamento de arco para todos os modelos."""
    print("\n--- ANALISE DE ENCURTAMENTO DE ARCO ---")

    models = {
        "Baseline": ("model_baseline.feb", "disp_model_baseline.csv"),
        "Triangular": ("model_triangular.feb", "disp_model_triangular.csv"),
        "Oval": ("model_oval.feb", "disp_model_oval.csv"),
    }

    results = {}
    for name, (feb, disp_csv) in models.items():
        if not os.path.exists(feb):
            continue
        nodes, _ = parse_geometry_and_elements(feb)
        disp = parse_disp(disp_csv)
        L_orig, L_def = compute_arc_length(nodes, disp)
        if L_orig is not None:
            delta_L = L_def - L_orig
            pct = (delta_L / L_orig) * 100
            results[name] = {
                "L_orig": L_orig, "L_def": L_def,
                "delta_L": delta_L, "pct": pct,
            }
            print(f"  {name:15s} | L_orig: {L_orig:.4f} mm | "
                  f"L_def: {L_def:.4f} mm | "
                  f"Delta: {delta_L*1000:+.2f} um ({pct:+.4f}%)")

    if "Baseline" in results:
        L_base = results["Baseline"]["L_def"]
        print("\n  --- ENCURTAMENTO RELATIVO (vs Baseline deformado) ---")
        for name in ["Triangular", "Oval"]:
            if name in results:
                rel = results[name]["L_def"] - L_base
                print(f"  {name:15s} | dL_rel = {rel*1000:+.3f} um "
                      f"({'ENCURTOU' if rel < 0 else 'ALONGOU'})")

    return results


# ============================================================================
# Modulo 3: Dashboard de Validacao
# ============================================================================

def generate_validation_dashboard():
    """Dashboard final: perfis + delta + Von Mises + Arc."""
    DARK_BG = "#161B22"
    DARK_FG = "#0D1117"
    SPINE_COLOR = "#6E7681"
    GRID_COLOR = "#21262D"
    C_BASE = "#6E7681"
    C_TRI = "#00D4AA"
    C_OVAL = "#F4C430"

    def _style(ax):
        ax.set_facecolor(DARK_FG)
        ax.tick_params(colors="white")
        for s in ax.spines.values():
            s.set_color(SPINE_COLOR)
        ax.grid(color=GRID_COLOR, linestyle="--", alpha=0.4)

    # Carregar dados
    models = {
        "baseline": ("model_baseline.feb", "disp_model_baseline.csv", "stress_model_baseline.csv"),
        "triangular": ("model_triangular.feb", "disp_model_triangular.csv", "stress_model_triangular.csv"),
        "oval": ("model_oval.feb", "disp_model_oval.csv", "stress_model_oval.csv"),
    }

    data = {}
    for name, (feb, disp_csv, stress_csv) in models.items():
        if not os.path.exists(feb):
            continue
        nodes, elements = parse_geometry_and_elements(feb)
        disp = parse_disp(disp_csv)
        stress = parse_stress(stress_csv)
        L_orig, L_def = compute_arc_length(nodes, disp)
        data[name] = {
            "nodes": nodes, "elements": elements,
            "disp": disp, "stress": stress,
            "L_orig": L_orig, "L_def": L_def,
        }

    if "baseline" not in data:
        print("  [ERRO] Baseline nao disponivel.")
        return

    # Extrair perfis
    def get_profile(name):
        d = data[name]
        r_vals, z_orig, z_def = [], [], []
        for nid, coord in d["nodes"].items():
            x, y, z = coord
            if abs(y) < 0.2 and x >= 0 and d["disp"] and nid in d["disp"]:
                r_vals.append(x)
                z_orig.append(z)
                z_def.append(z + d["disp"][nid][2])
        if not r_vals:
            return None, None
        r_vals, z_orig, z_def = np.array(r_vals), np.array(z_orig), np.array(z_def)
        bins = np.linspace(0, 5, 100)
        br, bz = [], []
        for i in range(len(bins) - 1):
            mask = (r_vals >= bins[i]) & (r_vals < bins[i + 1])
            if np.any(mask):
                mi = np.argmax(z_orig[mask])
                br.append(r_vals[mask][mi])
                bz.append(z_def[mask][mi])
        common_r = np.linspace(0, 4.5, 200)
        interp_z = np.interp(common_r, br, bz)
        return common_r, interp_z

    r_grid, z_base = get_profile("baseline")
    _, z_tri = get_profile("triangular") if "triangular" in data else (None, None)
    _, z_oval = get_profile("oval") if "oval" in data else (None, None)

    # ---- DASHBOARD: 2x2 ----
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), facecolor=DARK_BG)

    # Panel A: Perfis
    ax = axes[0, 0]
    _style(ax)
    ax.plot(r_grid, z_base * 1000, color=C_BASE, linestyle="--", linewidth=1.5,
            label="Baseline")
    if z_tri is not None:
        ax.plot(r_grid, z_tri * 1000, color=C_TRI, linewidth=2.5,
                label="Triangular")
    if z_oval is not None:
        ax.plot(r_grid, z_oval * 1000, color=C_OVAL, linewidth=2.5,
                label="Oval")
    ax.axvline(2.5, color=SPINE_COLOR, linestyle=":", alpha=0.5)
    ax.set_title("A. Perfis Anteriores Deformados", color="white", fontsize=11)
    ax.set_xlabel("R (mm)", color="white")
    ax.set_ylabel("Z (um)", color="white")
    ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=8)

    # Panel B: Delta Z
    ax = axes[0, 1]
    _style(ax)
    if z_tri is not None:
        ax.plot(r_grid, (z_tri - z_base) * 1000, color=C_TRI, linewidth=2.5,
                label="dZ Triangular")
    if z_oval is not None:
        ax.plot(r_grid, (z_oval - z_base) * 1000, color=C_OVAL, linewidth=2.5,
                label="dZ Oval")
    ax.axhline(0, color=SPINE_COLOR, linestyle="--", alpha=0.5)
    ax.axvline(2.5, color=SPINE_COLOR, linestyle=":", alpha=0.5)
    ax.set_title("B. Delta Z Relativo", color="white", fontsize=11)
    ax.set_xlabel("R (mm)", color="white")
    ax.set_ylabel("dZ (um)", color="white")
    ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=8)

    # Panel C: Von Mises Cross-Section (Triangular)
    ax = axes[1, 0]
    ax.set_facecolor(DARK_FG)
    ax.tick_params(colors="white")
    for s in ax.spines.values():
        s.set_color(SPINE_COLOR)

    if "triangular" in data and data["triangular"]["stress"]:
        xs, zs, vms = [], [], []
        for eid, edata in data["triangular"]["elements"].items():
            c = edata["centroid"]
            if abs(c[1]) < 0.3 and eid in data["triangular"]["stress"]:
                xs.append(c[0])
                zs.append(c[2])
                vms.append(data["triangular"]["stress"][eid]["vm"])
        if xs:
            xs, zs, vms = np.array(xs), np.array(zs), np.array(vms)
            triang = mtri.Triangulation(xs, zs)
            tcf = ax.tricontourf(triang, vms, levels=25, cmap="inferno")
            ax.tricontour(triang, vms, levels=8, colors="white",
                          linewidths=0.3, alpha=0.3)
            plt.colorbar(tcf, ax=ax, shrink=0.8, label="Von Mises (MPa)")
    ax.set_title("C. Von Mises -- Triangular (Y=0)", color="white", fontsize=11)
    ax.set_xlabel("X (mm)", color="white")
    ax.set_ylabel("Z (mm)", color="white")
    ax.set_aspect("equal")

    # Panel D: Arc Length Comparison (Bar Chart)
    ax = axes[1, 1]
    _style(ax)

    arc_names = []
    arc_deltas = []
    arc_colors = []

    L_base_def = data["baseline"]["L_def"] if data["baseline"]["L_def"] else 0
    for name, color in [("baseline", C_BASE), ("triangular", C_TRI), ("oval", C_OVAL)]:
        if name in data and data[name]["L_def"] is not None:
            delta = (data[name]["L_def"] - L_base_def) * 1000 if name != "baseline" else 0
            arc_names.append(name.capitalize())
            arc_deltas.append(delta)
            arc_colors.append(color)

    if arc_names:
        bars = ax.bar(arc_names, arc_deltas, color=arc_colors, width=0.5, edgecolor="white",
                      linewidth=0.5)
        for bar, val in zip(bars, arc_deltas):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f"{val:+.2f} um", ha="center", va="bottom",
                    color="white", fontsize=10)
    ax.axhline(0, color=SPINE_COLOR, linestyle="--", alpha=0.5)
    ax.set_title("D. Encurtamento de Arco Anterior (vs Baseline)", color="white", fontsize=11)
    ax.set_ylabel("Delta L (um)", color="white")

    fig.suptitle("Dashboard de Validacao: Lei de Redistribuicao Volumetrica (HGO)",
                 color="white", fontsize=15, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig("fem_validation_dashboard.png", dpi=150)
    print("  Saved: fem_validation_dashboard.png")


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 64)
    print("  ANALISE AVANCADA FEM-VOLUME ICRS (HGO)")
    print("=" * 64)

    # 1. Von Mises Cross-Section
    print("\n[1] Gerando mapa de Von Mises na secao transversal...")
    generate_vonmises_dashboard()

    # 2. Arc Shortening
    print("\n[2] Calculando encurtamento funcional de arco...")
    arc_results = analyze_arc_shortening()

    # 3. Dashboard
    print("\n[3] Gerando dashboard de validacao...")
    generate_validation_dashboard()

    print("\n" + "=" * 64)
    print("  Analise avancada concluida.")
    print("=" * 64)


if __name__ == "__main__":
    main()
