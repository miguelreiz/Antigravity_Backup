"""
post_processor.py — Análise comparativa dos resultados FEM-VOLUME ICRS.

Extrai perfis anteriores deformados de cada simulação (Baseline, Triangular, Oval),
calcula a diferença relativa (ΔZ = Ring − Baseline), e gera gráficos de alta fidelidade
para validação do Paradoxo do Anel e da Lei de Redistribuição Volumétrica.
"""

import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import os


# ============================================================================
# Parsing
# ============================================================================

def parse_febio_geometry(xml_file):
    """Extrai coordenadas nodais do arquivo .feb."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    nodes = {}
    for node in root.findall(".//node"):
        nid = int(node.get("id"))
        coords = [float(x) for x in node.text.split(",")]
        nodes[nid] = coords
    return nodes


def parse_disp(disp_file):
    """Lê o último passo de deslocamento do CSV de saída do FEBio."""
    if not os.path.exists(disp_file):
        return None
    with open(disp_file, "r") as f:
        lines = f.readlines()

    # Encontrar o último "Step = 10"
    last_step_idx = 0
    for i, line in enumerate(lines):
        if "Step = 10" in line:
            last_step_idx = i

    disp = {}
    skip_prefixes = ("*", "=", "Step", "Time", "Data", "File")
    for line in lines[last_step_idx:]:
        if line.strip() and not any(line.startswith(p) for p in skip_prefixes):
            parts = line.strip().split(",")
            if len(parts) >= 4:
                nid = int(parts[0])
                disp[nid] = (float(parts[1]), float(parts[2]), float(parts[3]))
    return disp


def parse_stress(stress_file):
    """Lê o último passo de stress do CSV de saída do FEBio."""
    if not os.path.exists(stress_file):
        return None
    with open(stress_file, "r") as f:
        lines = f.readlines()

    last_step_idx = 0
    for i, line in enumerate(lines):
        if "Step = 10" in line:
            last_step_idx = i

    stress = {}
    skip_prefixes = ("*", "=", "Step", "Time", "Data", "File")
    for line in lines[last_step_idx:]:
        if line.strip() and not any(line.startswith(p) for p in skip_prefixes):
            parts = line.strip().split(",")
            if len(parts) >= 7:
                eid = int(parts[0])
                sx, sy, sz = float(parts[1]), float(parts[2]), float(parts[3])
                sxy, syz, sxz = float(parts[4]), float(parts[5]), float(parts[6])
                # Von Mises
                vm = np.sqrt(
                    0.5
                    * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2)
                    + 3.0 * (sxy**2 + syz**2 + sxz**2)
                )
                stress[eid] = vm
    return stress


# ============================================================================
# Anterior Profile Extraction
# ============================================================================

def extract_anterior_profile(nodes, disp):
    """Extrai o perfil anterior deformado no plano Y≈0, X≥0."""
    if disp is None:
        return None, None

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

    # Binning: pegar o nó mais anterior (maior Z original) em cada faixa radial
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
    return common_r, interp_z


# ============================================================================
# Posterior Profile Extraction
# ============================================================================

def extract_posterior_profile(nodes, disp):
    """Extrai o perfil posterior deformado no plano Y≈0, X≥0.

    Análogo a extract_anterior_profile(), mas seleciona o nó com o
    MENOR Z (mais posterior) em cada faixa radial.
    """
    if disp is None:
        return None, None

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

    # Binning: pegar o nó mais posterior (menor Z original) em cada faixa radial
    bins = np.linspace(0, 5, 100)
    binned_r, binned_z = [], []
    for i in range(len(bins) - 1):
        mask = (r_vals >= bins[i]) & (r_vals < bins[i + 1])
        if np.any(mask):
            min_idx = np.argmin(z_orig[mask])
            binned_r.append(r_vals[mask][min_idx])
            binned_z.append(z_def[mask][min_idx])

    common_r = np.linspace(0, 4.5, 200)
    interp_z = np.interp(common_r, binned_r, binned_z)
    return common_r, interp_z


# ============================================================================
# Von Mises Radial Profile
# ============================================================================

def extract_vonmises_radial(feb_file, stress_dict):
    """Extrai perfil radial médio de Von Mises por faixa de raio."""
    if stress_dict is None:
        return None, None

    tree = ET.parse(feb_file)
    root = tree.getroot()

    # Mapear nós
    nodes = {}
    for node in root.findall(".//node"):
        nid = int(node.get("id"))
        coords = [float(x) for x in node.text.split(",")]
        nodes[nid] = coords

    # Mapear centróides dos elementos hex8
    elem_centroids = {}
    for elem in root.findall(".//elem"):
        eid_str = elem.get("id")
        if eid_str is None:
            continue  # skip MeshData <elem lid="..."> entries
        eid = int(eid_str)
        node_ids = [int(x) for x in elem.text.split(",")]
        if eid in stress_dict:
            coords = np.array([nodes[nid] for nid in node_ids if nid in nodes])
            if len(coords) > 0:
                centroid = coords.mean(axis=0)
                elem_centroids[eid] = centroid

    # Binning radial de Von Mises
    bins = np.linspace(0, 5, 50)
    bin_r, bin_vm = [], []
    for i in range(len(bins) - 1):
        vms = []
        for eid, c in elem_centroids.items():
            r = np.sqrt(c[0] ** 2 + c[1] ** 2)
            if bins[i] <= r < bins[i + 1]:
                vms.append(stress_dict[eid])
        if vms:
            bin_r.append((bins[i] + bins[i + 1]) / 2)
            bin_vm.append(np.mean(vms))

    return np.array(bin_r), np.array(bin_vm)


# ============================================================================
# Visualização
# ============================================================================

DARK_BG = "#161B22"
DARK_FG = "#0D1117"
GRID_COLOR = "#21262D"
SPINE_COLOR = "#6E7681"
C_BASE = "#6E7681"
C_TRI = "#00D4AA"
C_OVAL = "#F4C430"
C_DELTA = "#FF7B72"
C_VM = "#BD93F9"


def _style_axis(ax):
    ax.set_facecolor(DARK_FG)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color(SPINE_COLOR)
    ax.grid(color=GRID_COLOR, linestyle="--", alpha=0.5)


def analyze_results():
    print("=" * 60)
    print("  POST PROCESSOR  (Fase 4 — HGO Anisotrópico)")
    print("=" * 60)

    # ---- Carregar geometrias e deslocamentos ----
    models = {
        "baseline": ("model_baseline.feb", "disp_model_baseline.csv", "stress_model_baseline.csv"),
        "triangular": ("model_triangular.feb", "disp_model_triangular.csv", "stress_model_triangular.csv"),
        "oval": ("model_oval.feb", "disp_model_oval.csv", "stress_model_oval.csv"),
    }

    data = {}
    for name, (feb, disp_csv, stress_csv) in models.items():
        if not os.path.exists(feb):
            print(f"  [SKIP] {feb} não encontrado.")
            continue
        nodes = parse_febio_geometry(feb)
        disp = parse_disp(disp_csv)
        stress = parse_stress(stress_csv)
        r_grid, z_profile = extract_anterior_profile(nodes, disp)
        r_vm, vm_profile = extract_vonmises_radial(feb, stress)
        data[name] = {
            "r": r_grid, "z": z_profile,
            "r_vm": r_vm, "vm": vm_profile,
        }

    if "baseline" not in data or data["baseline"]["z"] is None:
        print("  [ERRO] Baseline não disponível.")
        return

    r_grid = data["baseline"]["r"]
    z_base = data["baseline"]["z"]

    # ---- Calcular deltas ----
    results = {}
    for name in ["triangular", "oval"]:
        if name in data and data[name]["z"] is not None:
            delta = data[name]["z"] - z_base
            apex_dz = delta[0] * 1000  # µm
            track_idx = np.argmin(np.abs(r_grid - 2.5))
            track_dz = delta[track_idx] * 1000  # µm
            results[name] = {"delta": delta, "apex": apex_dz, "track": track_dz}

    # ---- Imprimir resultados ----
    print("\n--- RESULTADOS RELATIVOS (HGO Anisotrópico) ---")
    labels = {"triangular": "TRIANGULAR (Ferrara)", "oval": "OVAL (Keraring)"}
    for name, res in results.items():
        status = "[PARADOXO OK]" if res["apex"] < 0 and res["track"] > 0 else "[VERIFICAR]"
        print(
            f"  {labels[name]:25s} | Apex: {res['apex']:+7.2f} µm | "
            f"Track: {res['track']:+7.2f} µm | {status}"
        )

    # ---- Gráfico 1: Perfis de Elevação ----
    fig, ax = plt.subplots(figsize=(11, 6), facecolor=DARK_BG)
    _style_axis(ax)

    ax.plot(r_grid, z_base * 1000, label="Baseline (Apenas PIO)",
            color=C_BASE, linestyle="--", linewidth=1.5)

    if "triangular" in data and data["triangular"]["z"] is not None:
        ax.plot(r_grid, data["triangular"]["z"] * 1000,
                label="Anel Triangular (Ferrara)", color=C_TRI, linewidth=2.5)
    if "oval" in data and data["oval"]["z"] is not None:
        ax.plot(r_grid, data["oval"]["z"] * 1000,
                label="Anel Oval (Keraring)", color=C_OVAL, linewidth=2.5)

    ax.axvline(2.5, color=SPINE_COLOR, linestyle=":", alpha=0.6,
               label="Track do Anel (R=2.5mm)")

    ax.set_title("FEM HGO: Perfil Anterior Deformado", color="white", fontsize=14)
    ax.set_xlabel("Distância Radial (mm)", color="white")
    ax.set_ylabel("Elevação Z Anterior (µm)", color="white")
    ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)
    fig.tight_layout()
    fig.savefig("fem_hgo_profiles.png", dpi=150)
    print("\n  Saved: fem_hgo_profiles.png")

    # ---- Gráfico 2: Delta Z Relativo ----
    fig, ax = plt.subplots(figsize=(11, 4), facecolor=DARK_BG)
    _style_axis(ax)

    if "triangular" in results:
        ax.plot(r_grid, results["triangular"]["delta"] * 1000,
                color=C_TRI, linewidth=2.5, label="ΔZ Triangular")
    if "oval" in results:
        ax.plot(r_grid, results["oval"]["delta"] * 1000,
                color=C_OVAL, linewidth=2.5, label="ΔZ Oval")

    ax.axhline(0, color=SPINE_COLOR, linestyle="--", alpha=0.5)
    ax.axvline(2.5, color=SPINE_COLOR, linestyle=":", alpha=0.6)

    ax.set_title("Diferencial de Elevação (ΔZ Relativo ao Baseline)",
                 color="white", fontsize=14)
    ax.set_xlabel("Distância Radial (mm)", color="white")
    ax.set_ylabel("ΔZ (µm)", color="white")
    ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)
    fig.tight_layout()
    fig.savefig("fem_hgo_delta.png", dpi=150)
    print("  Saved: fem_hgo_delta.png")

    # ---- Gráfico 3: Von Mises Radial ----
    has_vm = any(
        name in data and data[name]["vm"] is not None
        for name in ["baseline", "triangular", "oval"]
    )
    if has_vm:
        fig, ax = plt.subplots(figsize=(11, 5), facecolor=DARK_BG)
        _style_axis(ax)

        vm_colors = {"baseline": C_BASE, "triangular": C_TRI, "oval": C_OVAL}
        vm_labels = {
            "baseline": "Baseline",
            "triangular": "Triangular (Ferrara)",
            "oval": "Oval (Keraring)",
        }
        for name in ["baseline", "triangular", "oval"]:
            if name in data and data[name]["vm"] is not None:
                ax.plot(
                    data[name]["r_vm"], data[name]["vm"],
                    color=vm_colors[name], linewidth=2,
                    label=vm_labels[name],
                    linestyle="--" if name == "baseline" else "-",
                )

        ax.axvline(2.5, color=SPINE_COLOR, linestyle=":", alpha=0.6)
        ax.set_title("Distribuição Radial de Von Mises (HGO)",
                     color="white", fontsize=14)
        ax.set_xlabel("Distância Radial (mm)", color="white")
        ax.set_ylabel("Von Mises (MPa)", color="white")
        ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)
        fig.tight_layout()
        fig.savefig("fem_hgo_vonmises.png", dpi=150)
        print("  Saved: fem_hgo_vonmises.png")

    print("\n" + "=" * 60)
    print("  Análise concluída.")
    print("=" * 60)


if __name__ == "__main__":
    analyze_results()
