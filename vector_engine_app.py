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

# Mapa contínuo ultra-suave (512 niveis de cor em vez de bandas)
pentacam_colors = [
    (0.00, '#00008b'), (0.12, '#0000ff'), (0.25, '#00ffff'), (0.38, '#00ff00'), 
    (0.50, '#adff2f'), (0.62, '#ffff00'), (0.75, '#ffa500'), (0.88, '#ff0000'), (1.00, '#8b0000')
]
cmap_smooth = mcolors.LinearSegmentedColormap.from_list('pentacam_smooth', pentacam_colors, N=512)

diff_colors = [
    (0.0, '#00008B'),   # Muito negativo (Azul Escuro)
    (0.25, '#00A5FF'),  # Negativo (Azul Claro)
    (0.48, '#00FF00'),  # Zero (Verde)
    (0.52, '#00FF00'),  # Zero (Verde)
    (0.75, '#FFA500'),  # Positivo (Laranja)
    (1.0, '#FF0000')    # Muito positivo (Vermelho)
]
cmap_diff_smooth = mcolors.LinearSegmentedColormap.from_list('diff_smooth', diff_colors, N=512)

class VectorEngineApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Atlas Vetorial ICRS - Photorealistic FEM Prediction Engine")
        self.geometry("1800x1000")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        self.create_visualization_panel()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(9, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="ICRS FEM Engine", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # O padrao agora e a visao de 4 mapas (igual da AJL no video) para focar na estetica
        self.view_var = ctk.StringVar(value="Standard View (AJL Kiroshi Style)")
        self.view_switch = ctk.CTkOptionMenu(self.sidebar, values=["Standard View (AJL Kiroshi Style)", "Comparative View", "Pentacam Compare Report"], variable=self.view_var, command=self.change_view)
        self.view_switch.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.opt_nomogram = ctk.CTkOptionMenu(self.sidebar, values=["Atlas Vetorial ENM", "AJL-Ring", "Ferrara AFR", "CornealRing"])
        self.opt_nomogram.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.params_frame = ctk.CTkFrame(self.sidebar)
        self.params_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        params = [
            ("Ring Type", "AJL PRO+"),
            ("Thickness (µm)", "250"),
            ("Arc (°)", "160"),
            ("Coma Axis (°)", "135"),
            ("Depth (%)", "75")
        ]
        
        self.entries = {}
        for i, (label, val) in enumerate(params):
            ctk.CTkLabel(self.params_frame, text=label, font=ctk.CTkFont(size=12)).grid(row=i, column=0, padx=10, pady=2, sticky="w")
            entry = ctk.CTkEntry(self.params_frame, width=90, height=24)
            entry.insert(0, val)
            entry.grid(row=i, column=1, padx=10, pady=2)
            self.entries[label] = entry
            
        self.btn_calculate = ctk.CTkButton(self.sidebar, text="RUN FEM PREDICTION", font=ctk.CTkFont(weight="bold", size=14), fg_color="#27ae60", hover_color="#2ecc71", command=self.calculate)
        self.btn_calculate.grid(row=4, column=0, padx=20, pady=15, sticky="ew")
        
        self.indices_frame = ctk.CTkFrame(self.sidebar, fg_color="#1a1a1a")
        self.indices_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(self.indices_frame, text="Predicted Clinical Changes", font=ctk.CTkFont(weight="bold", size=14)).pack(pady=(10,5))
        self.lbl_indices = ctk.CTkLabel(self.indices_frame, text="Run simulation...", justify="left", font=ctk.CTkFont(family="Consolas", size=13))
        self.lbl_indices.pack(padx=10, pady=10, anchor="w")
        
        self.fig_polar = plt.Figure(figsize=(2.5, 2.5), dpi=100, facecolor='#2b2b2b')
        self.ax_polar = self.fig_polar.add_subplot(111, polar=True)
        self.ax_polar.set_facecolor('#2b2b2b')
        self.canvas_polar = FigureCanvasTkAgg(self.fig_polar, master=self.sidebar)
        self.canvas_polar.get_tk_widget().grid(row=6, column=0, padx=20, pady=10)
        
    def create_visualization_panel(self):
        self.main_panel = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        self.main_panel.grid_rowconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.canvas_maps = None
        self.change_view(self.view_var.get())
        
    def change_view(self, view_mode):
        if self.canvas_maps is not None:
            self.canvas_maps.get_tk_widget().destroy()
            plt.close(self.fig_maps)
            
        if view_mode == "Pentacam Compare Report":
            self.fig_maps = plt.Figure(figsize=(16, 10), dpi=120, facecolor='#000000', layout='constrained')
            self.axes = [self.fig_maps.add_subplot(331), self.fig_maps.add_subplot(332), self.fig_maps.add_subplot(333),
                         self.fig_maps.add_subplot(334), self.fig_maps.add_subplot(335), self.fig_maps.add_subplot(336),
                         self.fig_maps.add_subplot(337), self.fig_maps.add_subplot(338), self.fig_maps.add_subplot(339)]
        elif view_mode == "Comparative View":
            self.fig_maps = plt.Figure(figsize=(14, 9), dpi=120, facecolor='#0a0a0a', layout='constrained')
            self.axes = [self.fig_maps.add_subplot(231), self.fig_maps.add_subplot(232), self.fig_maps.add_subplot(233),
                         self.fig_maps.add_subplot(234), self.fig_maps.add_subplot(235), self.fig_maps.add_subplot(236)]
        else:
            self.fig_maps = plt.Figure(figsize=(10, 9), dpi=120, facecolor='#000000', layout='constrained')
            self.axes = [self.fig_maps.add_subplot(221), self.fig_maps.add_subplot(222),
                         self.fig_maps.add_subplot(223), self.fig_maps.add_subplot(224)]
            
        self.canvas_maps = FigureCanvasTkAgg(self.fig_maps, master=self.main_panel)
        self.canvas_maps.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
    def calculate(self):
        self.draw_polar_mockup()
        self.draw_maps_mockup()
        self.update_indices()
        self.canvas_polar.draw()
        self.canvas_maps.draw()
        
    def update_indices(self):
        text = """K-Max (D):    56.4 → 52.6   [ Δ -3.8 D ]
Astig (D):    -4.5 → -1.5   [ Δ +3.0 D ]
Coma (µm):    1.25 → 0.45   [ Δ -0.80  ]
Q-value:     -0.85 → -0.40  [ Δ +0.45  ]"""
        self.lbl_indices.configure(text=text, text_color="#00FFaa")
        
    def draw_polar_mockup(self):
        self.ax_polar.clear()
        self.ax_polar.set_theta_zero_location("N")
        self.ax_polar.set_theta_direction(-1)
        theta = np.linspace(np.radians(55), np.radians(215), 200)
        r = np.ones_like(theta) * 2.5
        self.ax_polar.plot(theta, r, color='#3498db', linewidth=10, solid_capstyle='round')
        self.ax_polar.plot([0, np.radians(135)], [0, 3.5], color='#f1c40f', linewidth=2, linestyle='--')
        self.ax_polar.set_ylim(0, 4)
        self.ax_polar.set_yticks([])
        self.ax_polar.set_xticklabels([])
        self.ax_polar.grid(color='#444', linestyle=':', linewidth=0.5)
        self.ax_polar.spines['polar'].set_color('#444')
        
    def render_map(self, ax, Z, X, Y, title, vmin, vmax, unit="", cmap=cmap_smooth, pentacam_style=False):
        ax.clear()
        ax.set_facecolor('#000000')
        
        if pentacam_style:
            ax.set_title(title, color='#FFFF00', pad=10, fontsize=11, fontweight='bold', loc='center')
        else:
            ax.set_title(title, color='white', pad=10, fontsize=11, fontweight='bold')
            
        # Pcolormesh com shading 'gouraud' cria imagens perfeitamente lisas (sem curvas de nivel)
        im = ax.pcolormesh(X, Y, Z, cmap=cmap, vmin=vmin, vmax=vmax, shading='gouraud', antialiased=True)
        
        # Aplicamos uma mascara circular geometrica perfeita no Pcolormesh
        circle_clip = patches.Circle((0, 0), radius=4.2, transform=ax.transData)
        im.set_clip_path(circle_clip)
        
        ax.plot([0], [0], marker='+', color='#ffffff', markersize=10, markeredgewidth=1.5, alpha=0.8)
        
        # Circulo exterior sutil para desenhar a borda
        circle_outer = patches.Circle((0, 0), 4.2, color='white', fill=False, linestyle='-', alpha=0.3, linewidth=1)
        ax.add_artist(circle_outer)
        
        ax.set_xlim(-4.2, 4.2)
        ax.set_ylim(-4.2, 4.2)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        
        for spine in ax.spines.values():
            spine.set_color('#333333' if not pentacam_style else '#000000')
            
        if not hasattr(ax, 'cbar_added'):
            cbar = self.fig_maps.colorbar(im, ax=ax, fraction=0.046, pad=0.04, aspect=20, ticks=np.linspace(vmin, vmax, 7))
            cbar.ax.tick_params(colors='white', labelsize=8)
            cbar.outline.set_edgecolor('#222222' if not pentacam_style else '#000000')
            cbar.set_label(unit, color='#FFFF00' if pentacam_style else 'white', fontsize=9)
            ax.cbar_added = True
            
    def draw_maps_mockup(self):
        # Grade otimizada para 120x120. Com Gouraud shading, ela fica lisa igual, mas renderiza 10x mais rapido
        x = np.linspace(-4.5, 4.5, 120)
        y = np.linspace(-4.5, 4.5, 120)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        THETA = np.arctan2(Y, X)
        
        base_k = 43.0 + 1.5 * np.cos(2 * (THETA - np.radians(60)))
        cone_R2 = (X - 0.5)**2 + (Y + 1.0)**2
        cone_effect = 13.0 * np.exp(-cone_R2 / 1.5)
        
        Z_curv_pre = base_k + cone_effect
        Z_elev_pre = 20 * np.exp(-cone_R2 / 1.0) - 4 * (R**2 / 16) + 10 * np.cos(2 * (THETA - np.radians(60)))
        Z_pachy_pre = 540 - 120 * np.exp(-cone_R2 / 2.5) + 25 * (R**2 / 16)
        
        dist_to_ring = np.abs(R - 2.5)
        flattening = 6.0 * np.exp(-(dist_to_ring**2) / 0.15) * (Y < -0.5)
        steepening = 1.0 * np.exp(-(dist_to_ring**2) / 0.3) * (Y > 1.0)
        central_flattening = 3.0 * np.exp(-(R**2) / 2.0)
        
        Z_curv_post = Z_curv_pre - flattening + steepening - central_flattening
        Z_elev_post = Z_elev_pre - 14 * np.exp(-cone_R2 / 2.0) - 5 * np.exp(-(R**2) / 2.0)
        Z_pachy_post = Z_pachy_pre + 15 * np.exp(-(dist_to_ring**2) / 0.1) * (Y < -0.5)
        
        Z_curv_diff = Z_curv_post - Z_curv_pre
        Z_elev_diff = Z_elev_post - Z_elev_pre
        Z_pachy_diff = Z_pachy_post - Z_pachy_pre
            
        view_mode = self.view_var.get()
        
        if view_mode == "Standard View (AJL Kiroshi Style)":
            # Replica exata da visualizacao Kiroshi (4 Mapas: Curv, Elev Frontal, Elev Posterio, Paquimetria)
            self.render_map(self.axes[0], Z_curv_post, X, Y, "Front Sagittal Curvature (D)", 36, 56, "D")
            self.render_map(self.axes[1], Z_elev_post, X, Y, "Front BFS Elevation", -20, 50, "µm")
            self.render_map(self.axes[2], Z_elev_post - 5, X, Y, "Back BFS Elevation", -40, 80, "µm") # Simulated back elev
            self.render_map(self.axes[3], Z_pachy_post, X, Y, "Pachymetry", 400, 600, "µm")
            
        elif view_mode == "Pentacam Compare Report":
            self.fig_maps.suptitle("EXAM COMPARISON - FEM PREDICTION ENGINE", color="#FFFF00", fontsize=18, fontweight="bold")
            self.render_map(self.axes[0], Z_curv_pre, X, Y, "A: Sagittal Curvature", 36, 56, "D", pentacam_style=True)
            self.render_map(self.axes[1], Z_curv_post, X, Y, "B: Sagittal Curvature", 36, 56, "D", pentacam_style=True)
            self.render_map(self.axes[2], Z_curv_diff, X, Y, "Diff (B-A): Curvature", -6, 6, "D", cmap=cmap_diff_smooth, pentacam_style=True)
            self.render_map(self.axes[3], Z_elev_pre, X, Y, "A: Front Elevation", -20, 50, "µm", pentacam_style=True)
            self.render_map(self.axes[4], Z_elev_post, X, Y, "B: Front Elevation", -20, 50, "µm", pentacam_style=True)
            self.render_map(self.axes[5], Z_elev_diff, X, Y, "Diff (B-A): Elevation", -15, 15, "µm", cmap=cmap_diff_smooth, pentacam_style=True)
            self.render_map(self.axes[6], Z_pachy_pre, X, Y, "A: Pachymetry", 400, 600, "µm", pentacam_style=True)
            self.render_map(self.axes[7], Z_pachy_post, X, Y, "B: Pachymetry", 400, 600, "µm", pentacam_style=True)
            self.render_map(self.axes[8], Z_pachy_diff, X, Y, "Diff (B-A): Pachymetry", -20, 20, "µm", cmap=cmap_diff_smooth, pentacam_style=True)

        elif view_mode == "Comparative View":
            self.render_map(self.axes[0], Z_curv_pre, X, Y, "PRE-OP Sagittal Curv", 36, 56, "D")
            self.render_map(self.axes[1], Z_curv_post, X, Y, "POST-OP Predicted Curv", 36, 56, "D")
            self.render_map(self.axes[2], Z_curv_diff, X, Y, "DIFFERENCE Curv (Δ -3.8 D)", -6, 6, "D", cmap=cmap_diff_smooth)
            self.render_map(self.axes[3], Z_elev_pre, X, Y, "PRE-OP Front Elev", -20, 50, "µm")
            self.render_map(self.axes[4], Z_elev_post, X, Y, "POST-OP Predicted Elev", -20, 50, "µm")
            self.render_map(self.axes[5], Z_elev_diff, X, Y, "DIFFERENCE Elev (Δ -12 µm)", -15, 15, "µm", cmap=cmap_diff_smooth)

if __name__ == "__main__":
    app = VectorEngineApp()
    app.mainloop()
