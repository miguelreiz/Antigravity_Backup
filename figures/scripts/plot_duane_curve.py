import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

# Set style
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

# Data generation (Hofstetter formulas)
age = np.linspace(10, 80, 100)
min_amplitude = np.maximum(15 - 0.25 * age, 0)
avg_amplitude = np.maximum(18.5 - 0.3 * age, 0)
max_amplitude = np.maximum(25 - 0.4 * age, 0)

# Adjust for "absolute presbyopia" plateau at ~0.5D after 60
avg_amplitude[age > 60] = 0.5
min_amplitude[age > 60] = 0.0
max_amplitude[age > 60] = 1.0

# Plot Curves
ax.plot(age, avg_amplitude, color='#00aaff', linewidth=3, label='Amplitude Média (Hofstetter)')
ax.fill_between(age, min_amplitude, max_amplitude, color='#00aaff', alpha=0.1, label='Faixa Fisiológica (Min-Max)')

# Critical Zones (Vertical Shading)
# Zone 1: Physiological Reserve (10-35)
ax.axvspan(10, 35, color='#00ff00', alpha=0.05, label='Reserva Fisiológica')
# Zone 2: Pre-Presbyopia (35-42)
ax.axvspan(35, 42, color='#ffff00', alpha=0.05, label='Declínio Subclínico')
# Zone 3: Symptomatic Onset (42-50)
ax.axvspan(42, 50, color='#ff9900', alpha=0.05, label='Presbiopia Sintomática (Janela Cirúrgica)')
# Zone 4: Absolute Presbyopia (50+)
ax.axvspan(50, 80, color='#ff0000', alpha=0.05, label='Presbiopia Absoluta / DLS')

# Threshold Lines
ax.axhline(6.0, color='#ffff00', linestyle='--', linewidth=1.5, alpha=0.8)
ax.text(78, 6.2, 'Limiar Sintomático (6D)', color='#ffff00', ha='right', fontsize=9)

ax.axhline(3.0, color='#ff0000', linestyle='--', linewidth=1.5, alpha=0.8)
ax.text(78, 3.2, 'Mínimo Leitura (3D)', color='#ff0000', ha='right', fontsize=9)

# Clinical Annotations (Milestones)
milestones = [
    (40, 6.0, "Primeira Adição\n(+1.00)"),
    (50, 2.5, "Dependência Total\n(Multifocais)"),
    (60, 0.5, "Catarata/DLS 2-3\n(RLE Mandatória)")
]

for ma, my, txt in milestones:
    ax.plot(ma, my, 'o', color='white', markeredgecolor='#00aaff', markersize=8)
    ax.annotate(txt, xy=(ma, my), xytext=(ma+2, my+2),
                arrowprops=dict(arrowstyle='->', color='white', lw=1),
                color='white', fontsize=10, fontweight='bold',
                path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])

# Labels and Title
ax.set_title('Curva de Duane & Progressão Clínica da Presbiopia', fontsize=20, color='white', pad=20, fontweight='bold')
ax.set_xlabel('Idade (Anos)', fontsize=14, color='#c9d1d9')
ax.set_ylabel('Amplitude de Acomodação (Dioptrias)', fontsize=14, color='#c9d1d9')

# Grid and Ticks
ax.grid(True, linestyle='--', color='#30363d', alpha=0.6)
ax.spines['bottom'].set_color('#30363d')
ax.spines['left'].set_color('#30363d')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', colors='#c9d1d9')

# Legend
ax.legend(loc='upper right', facecolor='#0d1117', edgecolor='#30363d', labelcolor='#c9d1d9')

# Save
plt.tight_layout()
plt.savefig('figures/chapter1/duane_curve.png', dpi=300, bbox_inches='tight', facecolor='#0d1117')
plt.close()
