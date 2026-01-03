#!/usr/bin/env python3
"""
Satisfação por Técnica - Comparação Final
Gráfico radar/comparação multi-dimensional
"""

import matplotlib.pyplot as plt
import numpy as np

# Dados satisfação 12 meses (%)
técnicas = ['Custom-Q', 'PresbyMAX', 'PRESBYOND', 'SUPRACOR', 'RLE EDOF', 'RLE Trifocal']
satisfacao_12m = [87, 85, 93, 78, 90, 92]
taxa_enhancement = [15, 12, 10, 18, 5, 8]
taxa_reversao = [3, 6, 2, 12, 0, 0]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Satisfação
colors_sat = ['#1565c0', '#7b1fa2', '#2e7d32', '#ff6f00', '#00838f', '#004d40']
bars1 = ax1.bar(range(len(técnicas)), satisfacao_12m, color=colors_sat, alpha=0.8)

for i, (bar, val) in enumerate(zip(bars1, satisfacao_12m)):
    ax1.text(i, val + 1, f'{val}%', ha='center', fontsize=10, fontweight='bold')

ax1.axhline(y=85, color='gray', linestyle='--', alpha=0.5, linewidth=2, label='Target (85%)')
ax1.set_ylabel('% Satisfação ≥8/10', fontsize=12, fontweight='bold')
ax1.set_title('Satisfação aos 12 Meses', fontsize=13, fontweight='bold')
ax1.set_xticks(range(len(técnicas)))
ax1.set_xticklabels(técnicas, rotation=45, ha='right', fontsize=9)
ax1.set_ylim(70, 100)
ax1.grid(axis='y', alpha=0.3)
ax1.legend()

# Plot 2: Enhancement + Reversão
x = np.arange(len(técnicas))
width = 0.35

bars_enh = ax2.bar(x - width/2, taxa_enhancement, width, label='Enhancement',
                   color='#ff9800', alpha=0.7)
bars_rev = ax2.bar(x + width/2, taxa_reversao, width, label='Reversão',
                   color='#f44336', alpha=0.7)

ax2.set_ylabel('% Pacientes', fontsize=12, fontweight='bold')
ax2.set_title('Taxas Enhancement e Reversão', fontsize=13, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(técnicas, rotation=45, ha='right', fontsize=9)
ax2.set_ylim(0, 20)
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# Adicionar anotação SUPRACOR
ax2.annotate('SUPRACOR:\nMaior taxa\nreversão',  xy=(3, 12), xytext=(4.5, 15),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            fontsize=9, color='red', ha='center')

plt.tight_layout()
plt.savefig('figures/comparative/plot_satisfaction_enhancement.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: figures/comparative/plot_satisfaction_enhancement.png")
plt.close()
