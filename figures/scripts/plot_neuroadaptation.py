#!/usr/bin/env python3
"""
Curva de Neuroadaptação - Capítulo 10
Gráfico: Satisfação e Halos ao longo de 12 meses
"""

import matplotlib.pyplot as plt
import numpy as np

# Dados do Capítulo 10
tempo_labels = ['Sem 1', 'Mês 1', 'Mês 3', 'Mês 6', 'Mês 12']
tempo_numeric = [0.25, 1, 3, 6, 12]  # Em meses

satisfacao = [3.0, 5.5, 7.8, 8.7, 9.1]
halos_severos = [85, 60, 25, 12, 8]
insatisfacao = [35, 15, 8, 5, 3]

# Criar figura com 2 subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot 1: Satisfação ao longo do tempo
ax1.plot(tempo_numeric, satisfacao, marker='o', linewidth=2.5, 
         markersize=8, color='#2e7d32', label='Satisfação (0-10)')
ax1.axhline(y=8, color='gray', linestyle='--', alpha=0.5, label='Target Clínico (≥8/10)')
ax1.axvspan(0, 1, alpha=0.2, color='#ffcdd2', label='"Vale do Desespero"')

ax1.set_ylabel('Score Satisfação (0-10)', fontsize=12, fontweight='bold')
ax1.set_ylim(0, 10)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='lower right')
ax1.set_title('Evolução de Satisfação e Sintomas Pós-Cirurgia Presbiópica\n(Dados Agregados Literatura)', 
              fontsize=14, fontweight='bold')

# Adicionar anotações
ax1.annotate('Arrependimento\n35%', xy=(0.25, 3), xytext=(1.5, 2),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            fontsize=10, color='red', ha='center')
ax1.annotate('Platô\nNeuroadaptação', xy=(6, 8.7), xytext=(8, 7),
            arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5),
            fontsize=10, color='darkgreen', ha='center')

# Plot 2: Halos Severos (%)
ax2.plot(tempo_numeric, halos_severos, marker='s', linewidth=2.5, 
         markersize=8, color='#e65100', label='% Halos Severos (>7/10)')
ax2.fill_between(tempo_numeric, halos_severos, alpha=0.3, color='#ff9800')

ax2.set_xlabel('Tempo Pós-Operatório', fontsize=12, fontweight='bold')
ax2.set_ylabel('% Pacientes', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 100)
ax2.set_xticks(tempo_numeric)
ax2.set_xticklabels(tempo_labels)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right')

# Adicionar anotação supressão
ax2.annotate('Supressão cortical\nativa', xy=(3, 25), xytext=(6, 50),
            arrowprops=dict(arrowstyle='->', color='#e65100', lw=1.5),
            fontsize=10, color='#e65100', ha='center')

plt.tight_layout()
plt.savefig('figures/chapter10/plot_neuroadaptation_curve.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo: figures/chapter10/plot_neuroadaptation_curve.png")
plt.close()
