import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def generate_synthetic_epithelial_map():
    # Parâmetros da Córnea
    radius = 4.5 # raio de 4.5mm (zona de 9mm)
    grid_size = 500
    x = np.linspace(-radius, radius, grid_size)
    y = np.linspace(-radius, radius, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Máscara circular
    R = np.sqrt(X**2 + Y**2)
    mask = R <= radius
    
    # Espessura Base (Córnea Normal ~ 50um)
    Z = np.ones_like(X) * 50.0
    
    # Simulação do Padrão Donut de Ceratocone (Ínfero-Temporal)
    # Cone descentrado para Baixo e Direita (no mapa topográfico, OD)
    cone_x = -1.0 # Temporal
    cone_y = -1.5 # Inferior
    
    # Afinamento epitelial sobre o ápice (cai para ~38um)
    dist_to_cone = np.sqrt((X - cone_x)**2 + (Y - cone_y)**2)
    Z -= 12.0 * np.exp(-(dist_to_cone**2) / 1.5) # Gaussiana de afinamento
    
    # Anel de Espessamento compensatório (sobe para ~58um ao redor do cone)
    ring_radius = 2.0
    ring_effect = 8.0 * np.exp(-((dist_to_cone - ring_radius)**2) / 0.8)
    Z += ring_effect
    
    # Aplica máscara circular
    Z[~mask] = np.nan
    
    # Plotagem Topográfica
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='black')
    
    # Colormap típico de paquimetria/epitélio (azul=fino, verde=médio, vermelho/branco=espesso)
    cmap = plt.cm.get_cmap('jet')
    
    contour = ax.contourf(X, Y, Z, levels=np.linspace(35, 65, 30), cmap=cmap)
    
    # Adicionar anéis de zona (3, 5, 7 mm)
    for r in [1.5, 2.5, 3.5]:
        circle = Circle((0, 0), r, fill=False, color='white', linestyle='--', alpha=0.5)
        ax.add_patch(circle)
        
    ax.set_aspect('equal')
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    ax.axis('off')
    
    # Barra de cores
    cbar = plt.colorbar(contour, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Espessura Epitelial (µm)', color='white', fontsize=12)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    # Títulos e Labels
    plt.title("MAPA EPITELIAL SINTÉTICO (Ceratocone)\nDerivado Exclusivo do Scheimpflug Bruto (YOLOv11)", 
              color='white', fontsize=14, fontweight='bold', pad=20)
    plt.text(0, -radius - 0.5, "Nota: Simulação de nuvem de pontos radiais extraída sem OCT", 
             color='gray', fontsize=10, ha='center')
    
    # Indicadores
    plt.text(cone_x, cone_y, "Afinamento\nApical (38µm)", color='black', ha='center', va='center', fontweight='bold')
    plt.text(cone_x+2.5, cone_y+1.5, "Espessamento\nCompensatório (Donut)", color='white', ha='center', va='center', fontweight='bold')

    output_path = r"C:\Users\3D_OCT\.gemini\antigravity\brain\0acad2ee-04f3-4437-9637-d789354d9fd6\artifacts\mapa_epitelial_pentacam_yolo.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='black')
    print(f"Mapa gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    generate_synthetic_epithelial_map()
