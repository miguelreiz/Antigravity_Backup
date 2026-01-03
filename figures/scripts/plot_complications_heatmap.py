#!/usr/bin/env python3
"""
Complicações por Técnica - Heatmap Visual
Capítulo 11 - Taxas comparativas
"""

import matplotlib.pyplot as plt
import numpy as np

# Dados Capítulo 11 (%)
técnicas = ['Custom-Q', 'PresbyMAX', 'PRESBYOND', 'SUPRACOR']
complicacoes = ['Descentramento', 'Halos >1 ano', 'Regressão Add', 
                'Olho Seco', 'Reversão', 'Enhancement']

# Matriz dados (%)
data = np.array([
    [3, 4, 2, 5],      # Descentramento
    [3, 8, 5, 15],     # Halos severos
    [15, 18, 10, 25],  # Regressão
    [28, 30, 25, 35],  # Olho seco
    [3, 6, 2, 12],     # Reversão
    [15, 12, 10, 18]   # Enhancement
])

fig, ax = plt.subplots(figsize=(10, 7))

# Criar heatmap
im = ax.imshow(data, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=35)

# Configurar ticks
ax.set_xticks(np.arange(len(técnicas)))
ax.set_yticks(np.arange(len(complicacoes)))
ax.set_xticklabels(técnicas, fontsize=11)
ax.set_yticklabels(complicacoes, fontsize=10)

# Rotar labels
plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

# Loop sobre dados para criar anotações
for i in range(len(complicacoes)):
    for j in range(len(técnicas)):
        text = ax.text(j, i, f'{data[i, j]}%',
                      ha="center", va="center", color="black", fontsize=10, fontweight='bold')

ax.set_title('Taxas de Complicações por Técnica Presbiópica\n(% Pacientes aos 12 meses)', 
             fontsize=13, fontweight='bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('% Pacientes', rotation=270, labelpad=20, fontsize=11)

# Adicionar legenda de cores
ax.text(len(técnicas) + 0.2, -0.8, 'Verde = Baixo\nAmarelo = Moderado\nVermelho = Alto',
        fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('figures/chapter11/heatmap_complications.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: figures/chapter11/heatmap_complications.png")
plt.close()
