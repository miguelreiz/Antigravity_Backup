"""
plot_parametric.py -- Gerar graficos parametricos a partir dos dados ja rodados.
"""
import numpy as np
import matplotlib.pyplot as plt

# Resultados extraidos do output do parametric_study.py
# Format: (label, diam, depth_pct, thick_um, dz_apex, dz_track)
data = [
    ("D5_d60_t150", 5.0, 60, 150,  18.05, -73.27),
    ("D5_d60_t200", 5.0, 60, 200,  17.95,  89.50),
    ("D5_d60_t250", 5.0, 60, 250,  17.95, 202.30),
    ("D5_d60_t300", 5.0, 60, 300,  17.95, 221.16),
    ("D5_d70_t150", 5.0, 70, 150,  17.95, -77.17),
    ("D5_d70_t200", 5.0, 70, 200,  17.58,  88.60),
    ("D5_d70_t250", 5.0, 70, 250,  17.95, 133.44),
    ("D5_d70_t300", 5.0, 70, 300,  17.94, 197.72),
    ("D5_d80_t150", 5.0, 80, 150,  17.92, -65.11),
    ("D5_d80_t200", 5.0, 80, 200,  17.92, -65.11),
    ("D5_d80_t250", 5.0, 80, 250,  17.92, -65.11),
    ("D5_d80_t300", 5.0, 80, 300,  17.96,  95.15),
    ("D6_d60_t150", 6.0, 60, 150,  18.04, -68.47),
    ("D6_d60_t200", 6.0, 60, 200,  17.89, 103.63),
    ("D6_d60_t250", 6.0, 60, 250,  17.87, 226.36),
    ("D6_d60_t300", 6.0, 60, 300,  17.77, 248.28),
    ("D6_d70_t150", 6.0, 70, 150,  17.93,   4.36),
    ("D6_d70_t200", 6.0, 70, 200,  17.89,  67.35),
    ("D6_d70_t250", 6.0, 70, 250,  17.87, 158.43),
    ("D6_d70_t300", 6.0, 70, 300,  17.67, 261.07),
]

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

DEPTHS = [60, 70, 80]
THICKNESSES = [150, 200, 250, 300]
DIAMETERS = [5.0, 6.0]
colors_depth = {60: "#FF7B72", 70: "#00D4AA", 80: "#BD93F9"}

# ---- Plot 1: Espessura vs Track Elevation ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=DARK_BG)
for ax_idx, diam in enumerate(DIAMETERS):
    ax = axes[ax_idx]
    _style(ax)
    ax.set_title(f"Diametro = {diam:.0f} mm", color="white", fontsize=12)
    for depth in DEPTHS:
        subset = [(d[3], d[5]) for d in data if d[1] == diam and d[2] == depth]
        if not subset:
            continue
        thicks = [s[0] for s in subset]
        tracks = [s[1] for s in subset]
        ax.plot(thicks, tracks, marker="o", linewidth=2.5, markersize=8,
                color=colors_depth[depth], label=f"Prof. {depth}%")
    ax.axhline(0, color=SPINE_COLOR, linestyle="--", alpha=0.5)
    ax.set_xlabel("Espessura do Anel (um)", color="white")
    ax.set_ylabel("Elevacao Track (um)", color="white")
    ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)
fig.suptitle("Sensibilidade Parametrica: Espessura x Elevacao do Track (HGO)",
             color="white", fontsize=14)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig("parametric_track_elevation.png", dpi=150)
print("Saved: parametric_track_elevation.png")

# ---- Plot 2: Heatmaps ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=DARK_BG)
for ax_idx, diam in enumerate(DIAMETERS):
    ax = axes[ax_idx]
    _style(ax)
    ax.set_title(f"Diametro = {diam:.0f} mm", color="white", fontsize=12)
    grid = np.full((len(DEPTHS), len(THICKNESSES)), np.nan)
    for d in data:
        if d[1] == diam:
            try:
                di = DEPTHS.index(d[2])
                ti = THICKNESSES.index(d[3])
                grid[di, ti] = d[5]
            except ValueError:
                pass
    im = ax.imshow(grid, aspect="auto", cmap="inferno", origin="lower",
                   extent=[125, 325, 55, 85])
    for di, depth in enumerate(DEPTHS):
        for ti, thick in enumerate(THICKNESSES):
            if not np.isnan(grid[di, ti]):
                ax.text(thick, depth, f"{grid[di, ti]:.0f}",
                        ha="center", va="center",
                        color="white", fontsize=10, fontweight="bold")
    ax.set_xlabel("Espessura (um)", color="white")
    ax.set_ylabel("Profundidade (%)", color="white")
    plt.colorbar(im, ax=ax, label="Track Elevation (um)")
fig.suptitle("Mapa Parametrico: Elevacao do Track (um) — HGO Anisotropico",
             color="white", fontsize=14)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig("parametric_heatmap.png", dpi=150)
print("Saved: parametric_heatmap.png")

# ---- Plot 3: Comparacao D5 vs D6 ----
fig, ax = plt.subplots(figsize=(10, 5), facecolor=DARK_BG)
_style(ax)
for diam, ls, marker in [(5.0, "-", "o"), (6.0, "--", "s")]:
    for depth in [60, 70]:
        subset = [(d[3], d[5]) for d in data if d[1] == diam and d[2] == depth]
        if not subset:
            continue
        thicks = [s[0] for s in subset]
        tracks = [s[1] for s in subset]
        ax.plot(thicks, tracks, marker=marker, linewidth=2, markersize=7,
                linestyle=ls, color=colors_depth[depth],
                label=f"D={diam:.0f}mm, Prof.{depth}%")
ax.axhline(0, color=SPINE_COLOR, linestyle="--", alpha=0.5)
ax.set_xlabel("Espessura do Anel (um)", color="white")
ax.set_ylabel("Elevacao Track (um)", color="white")
ax.set_title("Efeito do Diametro na Elevacao do Track", color="white", fontsize=13)
ax.legend(facecolor=DARK_BG, labelcolor="white", fontsize=9)
fig.tight_layout()
fig.savefig("parametric_diameter_comparison.png", dpi=150)
print("Saved: parametric_diameter_comparison.png")
