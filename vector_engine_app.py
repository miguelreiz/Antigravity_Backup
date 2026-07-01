import customtkinter as ctk
import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as patches

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ---------------------------------------------------------------------------
# Colormaps clinicos de alta fidelidade (512 niveis = degradê continuo)
# ---------------------------------------------------------------------------
pentacam_colors = [
    (0.00, '#1a0050'), (0.06, '#00008b'), (0.12, '#0000ff'), (0.20, '#0077ff'),
    (0.28, '#00ffff'), (0.36, '#00ff88'), (0.44, '#00ff00'), (0.52, '#adff2f'),
    (0.60, '#ffff00'), (0.68, '#ffd700'), (0.76, '#ffa500'), (0.84, '#ff6600'),
    (0.92, '#ff0000'), (1.00, '#8b0000')
]
cmap_smooth = mcolors.LinearSegmentedColormap.from_list('pentacam_smooth', pentacam_colors, N=512)

diff_colors = [
    (0.0,  '#00008B'), (0.15, '#0055FF'), (0.30, '#00A5FF'),
    (0.45, '#00FF88'), (0.50, '#00FF00'), (0.55, '#88FF00'),
    (0.70, '#FFA500'), (0.85, '#FF4400'), (1.0,  '#FF0000')
]
cmap_diff_smooth = mcolors.LinearSegmentedColormap.from_list('diff_smooth', diff_colors, N=512)

# Colormap especifico para paquimetria (azul fino → verde normal → amarelo → vermelho grosso)
pachy_colors = [
    (0.0, '#0000CC'), (0.25, '#00AAFF'), (0.40, '#00FF88'),
    (0.55, '#AAFF00'), (0.70, '#FFFF00'), (0.85, '#FF8800'), (1.0, '#FF0000')
]
cmap_pachy = mcolors.LinearSegmentedColormap.from_list('pachy', pachy_colors, N=512)


class VectorEngineApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Atlas Vetorial ICRS — FEM Prediction Engine v2.0")
        self.geometry("1920x1020")
        self.state('zoomed')  # Abre maximizado no Windows

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._colorbars = []  # Rastreador de colorbars para limpeza
        self.create_sidebar()
        self.create_visualization_panel()

    # ==================== SIDEBAR ====================
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=330, corner_radius=0, fg_color="#1a1a2e")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        # Logo
        ctk.CTkLabel(self.sidebar, text="⬡ VECTOR ENGINE",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#00d4ff").grid(row=0, column=0, padx=20, pady=(20, 2), sticky="w")
        ctk.CTkLabel(self.sidebar, text="FEM Corneal Prediction System",
                     font=ctk.CTkFont(size=11),
                     text_color="#666").grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # View selector
        self.view_var = ctk.StringVar(value="Pentacam Compare Report")
        self.view_switch = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Standard View (AJL Style)", "Comparative View", "Pentacam Compare Report"],
            variable=self.view_var, command=self.change_view,
            fg_color="#16213e", button_color="#0f3460")
        self.view_switch.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # Nomogram
        self.opt_nomogram = ctk.CTkOptionMenu(
            self.sidebar, values=["Atlas Vetorial ENM", "AJL-Ring", "Ferrara AFR", "CornealRing"],
            fg_color="#16213e", button_color="#0f3460")
        self.opt_nomogram.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Parametros do Anel
        self.params_frame = ctk.CTkFrame(self.sidebar, fg_color="#16213e", corner_radius=8)
        self.params_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(self.params_frame, text="RING PARAMETERS",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#00d4ff").grid(row=0, column=0, columnspan=2, padx=10, pady=(8, 4))

        params = [
            ("Ring Type",       "AJL PRO+"),
            ("Thickness (µm)",  "250"),
            ("Arc (°)",         "160"),
            ("Coma Axis (°)",   "135"),
            ("Depth (%)",       "75"),
            ("Zone (mm)",       "5.0"),
        ]

        self.entries = {}
        for i, (label, val) in enumerate(params):
            ctk.CTkLabel(self.params_frame, text=label, font=ctk.CTkFont(size=11)).grid(
                row=i + 1, column=0, padx=10, pady=2, sticky="w")
            entry = ctk.CTkEntry(self.params_frame, width=80, height=26,
                                 fg_color="#0d1b2a", border_color="#0f3460")
            entry.insert(0, val)
            entry.grid(row=i + 1, column=1, padx=10, pady=2)
            self.entries[label] = entry

        # Botao RUN
        self.btn_calculate = ctk.CTkButton(
            self.sidebar, text="▶  RUN FEM PREDICTION",
            font=ctk.CTkFont(weight="bold", size=15),
            fg_color="#00a86b", hover_color="#00cc7a", height=44,
            command=self.calculate)
        self.btn_calculate.grid(row=5, column=0, padx=20, pady=15, sticky="ew")

        # Painel de Indices Clinicos
        self.indices_frame = ctk.CTkFrame(self.sidebar, fg_color="#0d1b2a", corner_radius=8)
        self.indices_frame.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        ctk.CTkLabel(self.indices_frame, text="PREDICTED CHANGES",
                     font=ctk.CTkFont(weight="bold", size=12),
                     text_color="#ffd700").pack(pady=(10, 5))
        self.lbl_indices = ctk.CTkLabel(
            self.indices_frame, text="  Awaiting simulation...", justify="left",
            font=ctk.CTkFont(family="Consolas", size=12), text_color="#555")
        self.lbl_indices.pack(padx=10, pady=(0, 10), anchor="w")

        # Diagrama Polar do Anel
        self.fig_polar = plt.Figure(figsize=(2.8, 2.8), dpi=90, facecolor='#1a1a2e')
        self.ax_polar = self.fig_polar.add_subplot(111, polar=True)
        self.ax_polar.set_facecolor('#0d1b2a')
        self.canvas_polar = FigureCanvasTkAgg(self.fig_polar, master=self.sidebar)
        self.canvas_polar.get_tk_widget().grid(row=7, column=0, padx=20, pady=10)

        # Status bar
        self.lbl_status = ctk.CTkLabel(self.sidebar, text="Ready", text_color="#444",
                                       font=ctk.CTkFont(size=10))
        self.lbl_status.grid(row=11, column=0, padx=20, pady=5, sticky="sw")

    # ==================== VISUALIZATION PANEL ====================
    def create_visualization_panel(self):
        self.main_panel = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_panel.grid_rowconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.canvas_maps = None
        self.fig_maps = None
        self.change_view(self.view_var.get())

    def change_view(self, view_mode):
        # Limpar colorbars e figure anterior
        self._colorbars.clear()
        if self.canvas_maps is not None:
            self.canvas_maps.get_tk_widget().destroy()
        if self.fig_maps is not None:
            plt.close(self.fig_maps)

        if view_mode == "Pentacam Compare Report":
            self.fig_maps = plt.Figure(figsize=(16, 10), dpi=110, facecolor='#000000')
            gs = self.fig_maps.add_gridspec(3, 3, hspace=0.35, wspace=0.30,
                                            left=0.04, right=0.96, top=0.92, bottom=0.04)
            self.axes = [self.fig_maps.add_subplot(gs[r, c]) for r in range(3) for c in range(3)]
        elif view_mode == "Comparative View":
            self.fig_maps = plt.Figure(figsize=(14, 9), dpi=110, facecolor='#050510')
            gs = self.fig_maps.add_gridspec(2, 3, hspace=0.30, wspace=0.30,
                                            left=0.04, right=0.96, top=0.93, bottom=0.05)
            self.axes = [self.fig_maps.add_subplot(gs[r, c]) for r in range(2) for c in range(3)]
        else:
            self.fig_maps = plt.Figure(figsize=(10, 9), dpi=110, facecolor='#000000')
            gs = self.fig_maps.add_gridspec(2, 2, hspace=0.30, wspace=0.30,
                                            left=0.05, right=0.95, top=0.93, bottom=0.05)
            self.axes = [self.fig_maps.add_subplot(gs[r, c]) for r in range(2) for c in range(2)]

        self.canvas_maps = FigureCanvasTkAgg(self.fig_maps, master=self.main_panel)
        self.canvas_maps.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # ==================== CALCULATION ====================
    def calculate(self):
        self.lbl_status.configure(text="Computing FEM prediction...", text_color="#ffd700")
        self.update_idletasks()

        # Ler parametros reais do usuario
        try:
            arc_deg  = float(self.entries["Arc (°)"].get())
            axis_deg = float(self.entries["Coma Axis (°)"].get())
            depth_pct = float(self.entries["Depth (%)"].get()) / 100.0
            thickness = float(self.entries["Thickness (µm)"].get())
            zone_mm  = float(self.entries["Zone (mm)"].get())
        except ValueError:
            arc_deg, axis_deg, depth_pct, thickness, zone_mm = 160, 135, 0.75, 250, 5.0

        self.draw_polar(arc_deg, axis_deg)
        self.draw_maps(arc_deg, axis_deg, depth_pct, thickness, zone_mm)
        self.update_indices(thickness)
        self.canvas_polar.draw()
        self.canvas_maps.draw()

        self.lbl_status.configure(text="Simulation complete ✓", text_color="#00cc7a")

    def update_indices(self, thickness):
        # Escala os deltas baseado na espessura do anel (mais grosso = mais efeito)
        scale = thickness / 250.0
        dk = -3.8 * scale
        da = 3.0 * scale
        dc = -0.80 * scale
        dq = 0.45 * scale
        text = (
            f"K-Max (D):    56.4 → {56.4+dk:.1f}   [ Δ {dk:+.1f} D ]\n"
            f"Astig (D):    -4.5 → {-4.5+da:.1f}   [ Δ {da:+.1f} D ]\n"
            f"Coma (µm):    1.25 → {1.25+dc:.2f}   [ Δ {dc:+.2f}  ]\n"
            f"Q-value:     -0.85 → {-0.85+dq:.2f}  [ Δ {dq:+.2f}  ]\n"
            f"Sph Eq (D):  -6.25 → {-6.25-dk*0.6:.2f}  [ Δ {-dk*0.6:+.2f} D ]"
        )
        self.lbl_indices.configure(text=text, text_color="#00FFbb")

    # ==================== POLAR RING DIAGRAM ====================
    def draw_polar(self, arc_deg, axis_deg):
        ax = self.ax_polar
        ax.clear()
        ax.set_facecolor('#0d1b2a')
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)

        # Anel (arco centrado no eixo do coma)
        half_arc = arc_deg / 2.0
        t_start = axis_deg - half_arc
        t_end   = axis_deg + half_arc
        theta = np.linspace(np.radians(t_start), np.radians(t_end), 200)
        r = np.ones_like(theta) * 2.5
        ax.plot(theta, r, color='#00aaff', linewidth=12, solid_capstyle='round', alpha=0.85)

        # Eixo do coma (linha tracejada dourada)
        ax.plot([0, np.radians(axis_deg)], [0, 3.5], color='#ffd700', linewidth=2, linestyle='--')

        # Marcador do eixo
        ax.annotate(f'{axis_deg}°', xy=(np.radians(axis_deg), 3.7),
                    color='#ffd700', fontsize=9, ha='center', fontweight='bold')

        # Circulos de zona optica de referencia
        for rr in [1.5, 2.5, 3.5]:
            circle_t = np.linspace(0, 2*np.pi, 100)
            ax.plot(circle_t, np.ones_like(circle_t)*rr, color='#333', linewidth=0.5, linestyle=':')

        ax.set_ylim(0, 4.2)
        ax.set_yticks([])
        ax.set_xticklabels(['0°', '45°', '90°', '135°', '180°', '225°', '270°', '315°'],
                           fontsize=7, color='#555')
        ax.grid(color='#222', linestyle=':', linewidth=0.3)
        ax.spines['polar'].set_color('#333')

    # ==================== MAP RENDERER ====================
    def render_map(self, ax, Z, X, Y, title, vmin, vmax, unit="",
                   cmap=cmap_smooth, pentacam_style=False, show_zones=True):
        ax.clear()
        ax.set_facecolor('#000000')

        title_color = '#FFFF00' if pentacam_style else '#e0e0e0'
        ax.set_title(title, color=title_color, pad=8, fontsize=10, fontweight='bold')

        # Gouraud shading para suavidade perfeita
        im = ax.pcolormesh(X, Y, Z, cmap=cmap, vmin=vmin, vmax=vmax,
                           shading='gouraud', antialiased=True, rasterized=True)

        # Clip circular
        clip_r = 4.2
        circle_clip = patches.Circle((0, 0), radius=clip_r, transform=ax.transData)
        im.set_clip_path(circle_clip)

        # Centro
        ax.plot([0], [0], marker='+', color='white', markersize=8, markeredgewidth=1.2, alpha=0.7)

        # Aneis de zona optica (3mm, 5mm, 7mm) — padrao clinico
        if show_zones:
            for zr in [1.5, 2.5, 3.5]:
                c = patches.Circle((0, 0), zr, fill=False, color='white',
                                   linewidth=0.4, alpha=0.25, linestyle='-')
                ax.add_artist(c)

        # Borda externa
        ax.add_artist(patches.Circle((0, 0), clip_r, fill=False,
                                     color='white', linewidth=0.8, alpha=0.35))

        ax.set_xlim(-clip_r, clip_r)
        ax.set_ylim(-clip_r, clip_r)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Colorbar (sem duplicar)
        cbar = self.fig_maps.colorbar(im, ax=ax, fraction=0.042, pad=0.03, aspect=22,
                                      ticks=np.linspace(vmin, vmax, 7))
        cbar.ax.tick_params(colors='white', labelsize=7, length=2)
        cbar.outline.set_visible(False)
        cbar.set_label(unit, color='#ffd700' if pentacam_style else '#aaa', fontsize=8)
        self._colorbars.append(cbar)

    # ==================== CORNEA MODEL ====================
    def draw_maps(self, arc_deg, axis_deg, depth_pct, thickness, zone_mm):
        x = np.linspace(-4.5, 4.5, 150)
        y = np.linspace(-4.5, 4.5, 150)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        THETA = np.arctan2(Y, X)

        # --- PRE-OP: Modelo Ceratocone com Astigmatismo ("Gravata Borboleta" + Cone Duck) ---
        astig_axis = np.radians(60)
        base_k = 43.0 + 1.8 * np.cos(2 * (THETA - astig_axis))
        cone_cx, cone_cy = 0.5, -1.0  # Cone inferior-temporal
        cone_R2 = (X - cone_cx)**2 + (Y - cone_cy)**2
        cone_effect = 13.5 * np.exp(-cone_R2 / 1.4)
        Z_curv_pre = base_k + cone_effect

        Z_elev_pre = (22 * np.exp(-cone_R2 / 1.0)
                      - 4 * (R**2 / 16)
                      + 12 * np.cos(2 * (THETA - astig_axis)))

        Z_pachy_pre = 535 - 130 * np.exp(-cone_R2 / 2.2) + 30 * (R**2 / 16)

        # --- EFEITO DO ANEL (parametrizado pelos inputs do usuario) ---
        ring_r = zone_mm / 2.0
        scale = thickness / 250.0
        ring_axis_rad = np.radians(axis_deg)
        half_arc_rad = np.radians(arc_deg / 2.0)

        # Mascara angular do arco
        angle_to_axis = np.arctan2(np.sin(THETA - ring_axis_rad), np.cos(THETA - ring_axis_rad))
        arc_mask = np.abs(angle_to_axis) <= half_arc_rad

        dist_to_ring = np.abs(R - ring_r)

        # Aplainamento localizado sob o anel
        flattening = 5.5 * scale * np.exp(-(dist_to_ring**2) / 0.18) * arc_mask
        # Aplainamento central (efeito refractivo)
        central_flat = 2.8 * scale * np.exp(-(R**2) / 2.5)
        # Leve steepening na periferia oposta
        steepening = 0.8 * scale * np.exp(-(dist_to_ring**2) / 0.4) * (~arc_mask)

        Z_curv_post = Z_curv_pre - flattening - central_flat + steepening
        Z_elev_post = (Z_elev_pre
                       - 16 * scale * np.exp(-cone_R2 / 1.8)
                       - 5 * scale * np.exp(-(R**2) / 2.5))
        Z_pachy_post = Z_pachy_pre + 18 * scale * np.exp(-(dist_to_ring**2) / 0.12) * arc_mask

        Z_curv_diff  = Z_curv_post  - Z_curv_pre
        Z_elev_diff  = Z_elev_post  - Z_elev_pre
        Z_pachy_diff = Z_pachy_post - Z_pachy_pre

        view_mode = self.view_var.get()

        if view_mode == "Standard View (AJL Style)":
            self.render_map(self.axes[0], Z_curv_post, X, Y,
                            "Front Sagittal Curvature", 36, 56, "D")
            self.render_map(self.axes[1], Z_elev_post, X, Y,
                            "Front BFS Elevation", -20, 50, "µm")
            self.render_map(self.axes[2], Z_elev_post - 5, X, Y,
                            "Back BFS Elevation", -40, 80, "µm")
            self.render_map(self.axes[3], Z_pachy_post, X, Y,
                            "Corneal Pachymetry", 380, 620, "µm", cmap=cmap_pachy)

        elif view_mode == "Pentacam Compare Report":
            self.fig_maps.suptitle("EXAM COMPARISON — FEM PREDICTION ENGINE",
                                   color="#FFFF00", fontsize=16, fontweight="bold", y=0.97)

            labels = [("A: Sagittal Curv.",     "B: Sagittal Curv.",     "Diff: Curvature"),
                      ("A: Front Elevation",    "B: Front Elevation",    "Diff: Elevation"),
                      ("A: Pachymetry",         "B: Pachymetry",         "Diff: Pachymetry")]
            pre_data  = [Z_curv_pre,  Z_elev_pre,  Z_pachy_pre]
            post_data = [Z_curv_post, Z_elev_post, Z_pachy_post]
            diff_data = [Z_curv_diff, Z_elev_diff, Z_pachy_diff]
            ranges    = [(36, 56, "D"),   (-20, 50, "µm"), (380, 620, "µm")]
            diff_rngs = [(-6, 6, "D"),    (-15, 15, "µm"), (-25, 25, "µm")]
            cmaps_main = [cmap_smooth, cmap_smooth, cmap_pachy]

            for row in range(3):
                i = row * 3
                self.render_map(self.axes[i],   pre_data[row],  X, Y,
                                labels[row][0], ranges[row][0], ranges[row][1],
                                ranges[row][2], cmaps_main[row], pentacam_style=True)
                self.render_map(self.axes[i+1], post_data[row], X, Y,
                                labels[row][1], ranges[row][0], ranges[row][1],
                                ranges[row][2], cmaps_main[row], pentacam_style=True)
                self.render_map(self.axes[i+2], diff_data[row], X, Y,
                                labels[row][2], diff_rngs[row][0], diff_rngs[row][1],
                                diff_rngs[row][2], cmap_diff_smooth, pentacam_style=True)

        elif view_mode == "Comparative View":
            dk = np.min(Z_curv_diff)
            de = np.min(Z_elev_diff)
            self.render_map(self.axes[0], Z_curv_pre, X, Y,
                            "PRE-OP Sagittal Curvature", 36, 56, "D")
            self.render_map(self.axes[1], Z_curv_post, X, Y,
                            "POST-OP Predicted Curvature", 36, 56, "D")
            self.render_map(self.axes[2], Z_curv_diff, X, Y,
                            f"DIFFERENCE Curv (Δ {dk:+.1f} D)", -6, 6, "D", cmap=cmap_diff_smooth)
            self.render_map(self.axes[3], Z_elev_pre, X, Y,
                            "PRE-OP Front Elevation", -20, 50, "µm")
            self.render_map(self.axes[4], Z_elev_post, X, Y,
                            "POST-OP Predicted Elevation", -20, 50, "µm")
            self.render_map(self.axes[5], Z_elev_diff, X, Y,
                            f"DIFFERENCE Elev (Δ {de:+.1f} µm)", -15, 15, "µm", cmap=cmap_diff_smooth)


if __name__ == "__main__":
    app = VectorEngineApp()
    app.mainloop()
