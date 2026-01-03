#!/usr/bin/env python3
"""
Q-Factor vs Add - Relação matemática PresbyCor
Capítulo 5 - Nomograma visual
"""

import matplotlib.pyplot as plt
import numpy as np

# Dados Tabela 5.3.1 (Add → Q-target)
add_values = [1.25, 1.50, 1.75, 2.00, 2.25, 2.50]
q_target_dominante = [-0.50, -0.60, -0.70, -0.80, -0.90, -1.00]
q_target_nao_dominante = [-0.60, -0.70, -0.80, -0.90, -1.00, -1.10]

fig, ax = plt.subplots(figsize=(10, 6))

# Plot relações
ax.plot(add_values, q_target_dominante, marker='o', linewidth=2.5, markersize=8,
        color='#1565c0', label='Olho Dominante', linestyle='-')
ax.plot(add_values, q_target_nao_dominante, marker='s', linewidth=2.5, markersize=8,
        color='#d32f2f', label='Olho Não-Dominante', linestyle='--')

# Área fisiológica normal
ax.axhspan(-0.35, -0.15, alpha=0.2, color='green', label='Córnea Normal (Q ~ -0.26)')

# Área hyperprolata
ax.axhspan(-1.10, -0.60, alpha=0.15, color='orange', label='Hiperprolata Zone')

# Adicionar grid e labels
ax.set_xlabel('Add Desejada (D)', fontsize=12, fontweight='bold')
ax.set_ylabel('Q-Target', fontsize=12, fontweight='bold')
ax.set_title('Relação Add vs Q-Target - Nomograma PresbyCor\n(Algoritmo Ghenassia)', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper right', framealpha=0.9)

# Adicionar anotações
ax.annotate('Micro-monovisão\nOlho ND mais negativo', xy=(1.75, -0.80), xytext=(2.2, -0.65),
            arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=1.5),
            fontsize=9, color='#d32f2f', ha='center')

ax.annotate('Q normal\nCórnea humana', xy=(1.25, -0.26), xytext=(0.8, -0.15),
            arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
            fontsize=9, color='green', ha='right')

# Inverter eixo Y para mostrar valores mais negativos em baixo
ax.invert_yaxis()
ax.set_ylim(-1.15, -0.10)
ax.set_xlim(1.15, 2.60)

plt.tight_layout()
plt.savefig('figures/chapter5/plot_qfactor_vs_add.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: figures/chapter5/plot_qfactor_vs_add.png")
plt.close()
