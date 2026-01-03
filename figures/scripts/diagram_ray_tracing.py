#!/usr/bin/env python3
"""
Ray Tracing - EDOF Demonstration
Capítulo 2 - Visualização profundidade de campo
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(figsize=(14, 8))

# Perfil corneano hiperprolato (simplificado)
cornea_x = np.array([0, 0.5, 1.5, 2.5, 3])
cornea_y = np.array([0, 0.3, 0.6, 0.8, 0.9])

# Desenhar córnea
ax.plot(cornea_x, cornea_y, 'b-', linewidth=3, label='Córnea Hiper-prolata (Q=-0.80)')
ax.plot(cornea_x, -cornea_y, 'b-', linewidth=3)

# Raios de luz paralelos
ray_starts = [(-2, y) for y in [0, 0.5, 1.0, 1.5, 2.0]]
colors = ['#ff6b6b', '#feca57', '#48dbfb', '#1dd1a1', '#ee5a6f']
labels_done = set()

for i, (start, color) in enumerate(zip(ray_starts, colors)):
    # Raio incidente (paralelo)
    ax.arrow(start[0], start[1], 2-start[0], 0, head_width=0.15, head_length=0.1,
             fc=color, ec=color, alpha=0.7, linewidth=1.5)
    
    # Ponto de refração na córnea
    refract_x = 0
    refract_y = start[1]
    
    # Raios refratados - diferentes focos conforme altura
    if abs(start[1]) < 0.6:  # Central
        focus_x = 20
        focus_y = 0.3  # Foco perto (+2.00D)
        label = 'Raios Centrais → Foco Perto' if 'central' not in labels_done else ''
        labels_done.add('central')
    elif abs(start[1]) < 1.2:  # Paracentral
        focus_x = 23
        focus_y = 0.15  # Foco intermediário
        label = 'Raios Paracentrais → Intermediário' if 'para' not in labels_done else ''
        labels_done.add('para')
    else:  # Periférico
        focus_x = 26
        focus_y = 0  # Foco longe (emetropia)
        label = 'Raios Periféricos → Foco Longe' if 'peri' not in labels_done else ''
        labels_done.add('peri')
    
    # Desenhar raio refratado
    ax.plot([refract_x, focus_x], [refract_y, focus_y], color=color, 
            linewidth=2, alpha=0.7, label=label)

# EDOF Zone (zona focal estendida)
edof_rect = patches.Rectangle((19.5, -0.5), 7, 1, linewidth=2, 
                               edgecolor='green', facecolor='green', alpha=0.2)
ax.add_patch(edof_rect)
ax.text(23, -1.2, 'EDOF Zone\n(Foco Estendido)', fontsize=11, 
        fontweight='bold', color='green', ha='center')

# Retina (simplificada)
ax.plot([28, 28], [-3, 3], 'k--', linewidth=2, alpha=0.5, label='Retina')

# Distâncias focais
ax.annotate('40 cm\n(Perto)', xy=(20, 0.3), xytext=(20, 1.5),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            fontsize=10, color='red', ha='center', fontweight='bold')

ax.annotate('60-100 cm\n(Intermediário)', xy=(23, 0.15), xytext=(23, -2),
            arrowprops=dict(arrowstyle='->', color='orange', lw=1.5),
            fontsize=10, color='orange', ha='center', fontweight='bold')

ax.annotate('6 m\n(Longe)', xy=(26, 0), xytext=(26, -2.5),
            arrowprops=dict(arrowstyle='->', color='blue', lw=1.5),
            fontsize=10, color='blue', ha='center', fontweight='bold')

# Configurações
ax.set_xlim(-3, 30)
ax.set_ylim(-3.5, 3)
ax.set_xlabel('Distância Óptica (escala não-linear)', fontsize=12, fontweight='bold')
ax.set_ylabel('Altura (mm)', fontsize=12, fontweight='bold')
ax.set_title('Ray Tracing - Demonstração EDOF com Córnea Hiper-prolata\n' + 
             '(Conceito: Múltiplos focos = Profundidade campo estendida)',
             fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.2)
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig('figures/chapter2/diagram_ray_tracing_edof.png', dpi=300, bbox_inches='tight')
print("✅ Diagrama salvo: figures/chapter2/diagram_ray_tracing_edof.png")
plt.close()
