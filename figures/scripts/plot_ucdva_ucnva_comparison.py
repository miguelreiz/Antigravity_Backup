#!/usr/bin/env python3
"""
Comparação UCDVA/UCNVA por Técnica - Capítulo 12
Gráfico de barras comparando outcomes visuais
"""

import matplotlib.pyplot as plt
import numpy as np

# Dados do Capítulo 12

técnicas = ['Custom-Q', 'PRESBYOND', 'PresbyMAX\nHybrid', 'RLE\nEDOF', 'RLE\nTrifocal']
ucdva_20_25 = [85, 92, 90, 95, 88]  # % atingem ≥20/25
ucnva_j2 = [80, 88, 90, 75, 96]    # % atingem ≥J2

x = np.arange(len(técnicas))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

bars1 = ax.bar(x - width/2, ucdva_20_25, width, label='UCDVA ≥20/25',
               color='#1565c0', alpha=0.8)
bars2 = ax.bar(x + width/2, ucnva_j2, width, label='UCNVA ≥J2',
               color='#2e7d32', alpha=0.8)

# Adicionar valores nas barras
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}%', ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}%', ha='center', va='bottom', fontsize=9)

# Adicionar linha target
ax.axhline(y=85, color='gray', linestyle='--', alpha=0.5, linewidth=1.5, 
           label='Target Clínico (85%)')

ax.set_ylabel('% Pacientes Atingindo Target', fontsize=12, fontweight='bold')
ax.set_title('Comparação Outcomes Visuais por Técnica Presbiópica\n(12 meses pós-operatório)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(técnicas, fontsize=10)
ax.set_ylim(60, 105)
ax.legend(loc='lower left')
ax.grid(axis='y', alpha=0.3)

# Adicionar anotações
ax.annotate('Melhor longe', xy=(3, 95), xytext=(3.5, 98),
            arrowprops=dict(arrowstyle='->', color='#1565c0', lw=1.5),
            fontsize=9, color='#1565c0')
ax.annotate('Melhor perto', xy=(4, 96), xytext=(3.5, 90),
            arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.5),
            fontsize=9, color='#2e7d32')

plt.tight_layout()
plt.savefig('figures/chapter12/plot_ucdva_ucnva_comparison.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: figures/chapter12/plot_ucdva_ucnva_comparison.png")
plt.close()
