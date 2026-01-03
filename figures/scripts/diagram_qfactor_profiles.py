#!/usr/bin/env python3
"""
Q-Factor Corneal Profiles - Visual Comparison
Capítulo 2 - Demonstração conceito asfericidade
"""

import matplotlib.pyplot as plt
import numpy as np

# Criar perfis corneanos com diferentes Q-factors
x = np.linspace(0, 6, 100)  # Raio 0-6mm

# Função para calcular perfil corneano (equação cônica)
def corneal_profile(x, R, Q):
    """
    R = raio de curvatura apical (mm)
    Q = fator de asfericidade
    """
    y = (x**2 / R) / (1 + np.sqrt(1 - (1+Q)*(x**2/R**2)))
    return y

R = 7.8  # Raio típico córnea

# Perfis
y_prolate = corneal_profile(x, R, -0.26)      # Normal
y_hyperprolate = corneal_profile(x, R, -0.80)  # PresbyCor
y_oblate = corneal_profile(x, R, +0.50)       # Pós-LASIK

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Perfis Sobrepostos
ax1.plot(x, y_prolate, 'g-', linewidth=2.5, label='Prolata (Q = -0.26) Normal')
ax1.plot(x, y_hyperprolate, 'b-', linewidth=2.5, label='Hiper-prolata (Q = -0.80) PresbyCor')
ax1.plot(x, y_oblate, 'r-', linewidth=2.5, label='Oblata (Q = +0.50) Pós-LASIK')

ax1.fill_between(x, y_prolate, y_hyperprolate, where=(y_hyperprolate > y_prolate), 
                  alpha=0.3, color='blue', label='Ablação PresbyCor')

ax1.set_xlabel('Distância Radial do Centro (mm)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Elevação Corneana (mm)', fontsize=12, fontweight='bold')
ax1.set_title('Perfis Corneanos - Comparação Q-Factor', fontsize=14, fontweight='bold')
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 6)
ax1.invert_yaxis()  # Inverte para mostrar curvatura correta

# Anotar características
ax1.annotate('Centro íngreme\nPeriferia plana', xy=(4.5, y_hyperprolate[75]), 
             xytext=(3, 0.5), arrowprops=dict(arrowstyle='->', color='blue', lw=1.5),
             fontsize=9, color='blue')

# Plot 2: Curvatura Local (derivada)
def curvature(x, R, Q):
    """Curvatura local (K = 1/raio de curvatura local)"""
    # Simplificação: K ≈ x * (1+Q) / R^2
    return 337.5 / (R * (1 - ((1+Q)*x**2)/(2*R**2)))  # Em dioptrias

K_prolate = curvature(x, R, -0.26)
K_hyperprolate = curvature(x, R, -0.80)
K_oblate = curvature(x, R, +0.50)

ax2.plot(x, K_prolate, 'g-', linewidth=2.5, label='Prolata (Normal)')
ax2.plot(x, K_hyperprolate, 'b-', linewidth=2.5, label='Hiper-prolata (PresbyCor)')
ax2.plot(x, K_oblate, 'r-', linewidth=2.5, label='Oblata (Pós-LASIK)')

ax2.axhspan(42, 44, alpha=0.2, color='green', label='Range Normal (42-44 D)')

ax2.set_xlabel('Distância Radial (mm)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Poder Refrativo Local (D)', fontsize=12, fontweight='bold')
ax2.set_title('Distribuição de Poder Refrativo', fontsize=14, fontweight='bold')
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 6)
ax2.set_ylim(38, 48)

# Anotar zona multifocal
ax2.annotate('Variação poder\ncria EDOF', xy=(3, K_hyperprolate[50]), 
             xytext=(4.5, 46), arrowprops=dict(arrowstyle='->', color='blue', lw=1.5),
             fontsize=9, color='blue')

plt.tight_layout()
plt.savefig('figures/chapter2/diagram_qfactor_profiles.png', dpi=300, bbox_inches='tight')
print("✅ Diagrama salvo: figures/chapter2/diagram_qfactor_profiles.png")
plt.close()
