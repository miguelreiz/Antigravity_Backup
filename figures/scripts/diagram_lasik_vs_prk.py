#!/usr/bin/env python3
"""
LASIK vs PRK - Comparação Anatómica Simplificada
Capítulo 4
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Cores das camadas
colors = {
    'epithelium': '#ffeaa7',
    'bowman': '#fdcb6e',
    'stroma': '#74b9ff',
    'endothelium': '#a29bfe'
}

### LASIK ###
layers_lasik = [
    ('Epitélio', 0, 0.05, colors['epithelium']),
    ('Bowman', 0.05, 0.07, colors['bowman']),
    ('Flap (110μm)', 0.07, 0.18, '#81ecec'),  # Flap destacado
    ('Estroma\n(Ablação)', 0.18, 0.28, '#ff7675'),  # Ablated
    ('Estroma\n(RSB 360μm)', 0.28, 0.64, colors['stroma']),
    ('Endotélio', 0.64, 0.65, colors['endothelium'])
]

y_pos = 0
for label, start, end, color in layers_lasik:
    height = end - start
    rect = patches.Rectangle((0, start), 1, height, 
                             linewidth=2, edgecolor='black', 
                             facecolor=color, alpha=0.8)
    ax1.add_patch(rect)
    ax1.text(1.1, (start+end)/2, label, fontsize=9, va='center')

# Flap levantado (seta)
arrow = patches.FancyArrowPatch((0.5, 0.18), (0.8, 0.25),
                               arrowstyle='->', mutation_scale=20, 
                               linewidth=2, color='red')
ax1.add_patch(arrow)
ax1.text(0.85, 0.25, 'Flap\nLevantado', fontsize=9, color='red', fontweight='bold')

ax1.set_xlim(-0.2, 1.8)
ax1.set_ylim(0, 0.7)
ax1.set_title('LASIK\n(Flap 110μm + Ablação Estromal)', 
             fontsize=13, fontweight='bold')
ax1.axis('off')
ax1.invert_yaxis()

### PRK ###
layers_prk = [
    ('Epitélio\nREMOVIDO', 0, 0.05, '#fab1a0'),  # Removido
    ('Bowman +\nEstroma Anterior\n(Ablação)', 0.05, 0.15, '#ff7675'),
    ('Estroma\n(RSB 410μm)', 0.15, 0.56, colors['stroma']),
    ('Endotélio', 0.56, 0.57, colors['endothelium'])
]

for label, start, end, color in layers_prk:
    height = end - start
    rect = patches.Rectangle((0, start), 1, height, 
                             linewidth=2, edgecolor='black', 
                             facecolor=color, alpha=0.8)
    ax2.add_patch(rect)
    ax2.text(1.1, (start+end)/2, label, fontsize=9, va='center')

# Laser direto
arrow2 = patches.FancyArrowPatch((0.5, -0.05), (0.5, 0.05),
                                arrowstyle='->', mutation_scale=20, 
                                linewidth=2, color='orange')
ax2.add_patch(arrow2)
ax2.text(0.6, -0.05, 'Laser\nDireto', fontsize=9, color='orange', fontweight='bold')

# Regeneração epitélio
ax2.annotate('Regenera\n5-7 dias', xy=(0.5, 0.025), xytext=(1.5, 0.025),
            arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
            fontsize=9, color='green', ha='left')

ax2.set_xlim(-0.2, 2.2)
ax2.set_ylim(-0.1, 0.6)
ax2.set_title('PRK\n(Sem Flap, Ablação Superficial)', 
             fontsize=13, fontweight='bold')
ax2.axis('off')
ax2.invert_yaxis()

# Tabela comparativa
table_data = [
    ['Recuperação', '1-2 dias', '5-7 dias'],
    ['Dor', 'Mínima', 'Moderada'],
    ['RSB (exemplo)', '360 μm', '410 μm'],
    ['Biomecânica', 'Flap weakness', 'Mais forte']
]

table = ax2.table(cellText=table_data, colLabels=['', 'LASIK', 'PRK'],
                 cellLoc='left', loc='bottom',
                 bbox=[0, -0.5, 2, 0.3])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.5)

# Colorir header
for i in range(3):
    table[(0, i)].set_facecolor('#dfe6e9')
    table[(0, i)].set_text_props(weight='bold')

plt.suptitle('Comparação Anatómica LASIK vs PRK\n(Espessuras Aproximadas)', 
            fontsize=15, fontweight='bold')
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig('figures/chapter4/diagram_lasik_vs_prk.png', dpi=300, bbox_inches='tight')
print("✅ Diagrama salvo: figures/chapter4/diagram_lasik_vs_prk.png")
plt.close()
