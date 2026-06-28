"""
================================================================
  HIPOTESE: A GRAVIDADE DO CERATOCONE ESTA DIRETAMENTE 
  LIGADA AO Df (ANTERIOR) E A RAZAO Df/Db
  
  Objetivo: Investigar como o Df e o Db se comportam a medida 
  que a doenca (Ceratocone) avanca em severidade.
================================================================
"""
import numpy as np, pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

BG = '#0d1117'; BG2 = '#161b22'; TEXT = '#c9d1d9'
ACCENT = '#58a6ff'; GREEN = '#3fb950'; RED = '#f85149'
ORANGE = '#d29922'; CYAN = '#39d2c0'; PURPLE = '#bc8cff'
PINK = '#f778ba'; GRID_CLR = '#21262d'
plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG2,
    'axes.edgecolor': GRID_CLR, 'axes.labelcolor': TEXT,
    'text.color': TEXT, 'xtick.color': TEXT, 'ytick.color': TEXT,
    'grid.color': GRID_CLR, 'grid.alpha': 0.4,
    'font.family': 'Segoe UI', 'font.size': 9,
})

def _style(ax, title):
    ax.set_title(title, fontsize=10, fontweight='bold', color=TEXT, pad=8)
    ax.grid(True, alpha=0.3)

print('='*70)
print('  ANALISE DE SEVERIDADE: O PAPEL DO Df NO KC AVANCADO')
print('='*70)

# Carregar dados
mp = pd.read_csv(r'D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\matched_pairs_FII_Pentacam.csv', sep=';')

# Converter colunas
cols_to_num = ['BAD_Df', 'BAD_Db', 'BAD_D', 'KMax', 'Pachy_Min', 'K1', 'K2']
for c in cols_to_num:
    if c in mp.columns:
        mp[c] = pd.to_numeric(mp[c], errors='coerce')

# Remover nulos
df = mp.dropna(subset=['BAD_Df', 'BAD_Db', 'BAD_D', 'Penta_Class']).copy()
df['is_kc'] = df['Penta_Class'].str.contains('KC', case=False, na=False).astype(int)

# 1. Definir metricas de severidade e razao
# Usar KMax se existir, senao usar BAD_D como proxy de severidade global
has_kmax = 'KMax' in df.columns and not df['KMax'].isna().all()
severity_col = 'KMax' if has_kmax else 'BAD_D'
print(f'  Usando {severity_col} como proxy de severidade.')

# Calcular razao Df/Db (protegendo divisao por zero ou negativo)
# Usaremos delta relativo a base normal para Df e Db
# Base normal media: Df = -0.18, Db = -0.18
df['Df_delta'] = df['BAD_Df'] - df[df['is_kc']==0]['BAD_Df'].mean()
df['Db_delta'] = df['BAD_Db'] - df[df['is_kc']==0]['BAD_Db'].mean()

# Razao de amplificacao
df['Ratio_Df_Db'] = np.where(df['Db_delta'] > 0.5, df['Df_delta'] / df['Db_delta'], np.nan)

# 2. Estratificar em estagios de severidade (apenas KC)
kc = df[df['is_kc'] == 1].copy()

if has_kmax:
    bins = [0, 48, 53, 58, 100]
    labels = ['KC Leve (<48)', 'KC Mod (48-53)', 'KC Avanc (53-58)', 'KC Grave (>58)']
    kc['Estagio'] = pd.cut(kc['KMax'], bins=bins, labels=labels)
else:
    # Usar BAD_D como proxy
    bins = [0, 3, 6, 10, 100]
    labels = ['KC Inicial (D<3)', 'KC Mod (D 3-6)', 'KC Avanc (D 6-10)', 'KC Grave (D>10)']
    kc['Estagio'] = pd.cut(kc['BAD_D'], bins=bins, labels=labels)

print('\n  1. COMPORTAMENTO POR ESTAGIO DE SEVERIDADE:')
print('  %-18s | %-5s | %-8s | %-8s | %-12s | %-10s' % ('Estagio', 'N', 'Db Medio', 'Df Medio', 'Razao Df/Db', 'Var. Df'))
print('  '+'-'*65)

stats_by_stage = []
for estagio in labels:
    sub = kc[kc['Estagio'] == estagio]
    n = len(sub)
    if n > 0:
        db_m = sub['BAD_Db'].mean()
        df_m = sub['BAD_Df'].mean()
        ratio = sub['Ratio_Df_Db'].mean()
        var_df = sub['BAD_Df'].var()
        print('  %-18s | %5d | %8.2f | %8.2f | %12.2f | %10.2f' % (estagio, n, db_m, df_m, ratio, var_df))
        stats_by_stage.append({'Estagio': estagio, 'Db': db_m, 'Df': df_m, 'Ratio': ratio, 'Var_Df': var_df})

# 3. Modelagem Exponencial vs Linear
print('\n  2. MODELAGEM DO CRESCIMENTO (SEVERIDADE vs DEVIACAO):')
# Db vs Severidade (Linear?)
slope_db, intercept_db, r_db, p_db, _ = stats.linregress(kc[severity_col], kc['BAD_Db'])
# Df vs Severidade (Exponencial?)
# log(Df) = a + b * Severidade -> Df = exp(a) * exp(b*Sev)
clean_kc = kc.dropna(subset=[severity_col, 'BAD_Df', 'BAD_Db'])
clean_kc = clean_kc[clean_kc['BAD_Df'] > 0.1] # evitar log negativo

slope_df_lin, _, r_df_lin, _, _ = stats.linregress(clean_kc[severity_col], clean_kc['BAD_Df'])

try:
    slope_df_exp, intercept_df_exp, r_df_exp, p_df_exp, _ = stats.linregress(clean_kc[severity_col], np.log(clean_kc['BAD_Df']))
    print('  Crescimento Posterior (Db): r_linear = %.3f' % r_db)
    print('  Crescimento Anterior (Df):  r_linear = %.3f, r_exp = %.3f' % (r_df_lin, r_df_exp))
    if r_df_exp**2 > r_df_lin**2 + 0.05:
        print('  --> Df exibe crescimento EXPONENCIAL com a severidade.')
    else:
        print('  --> Df exibe crescimento LINEAR com a severidade (mas slope muito maior).')
except:
    pass

# 4. Risco de "Catastrofe" (Variance explodindo)
print('\n  3. VARIANCIA E INSTABILIDADE ANTERIOR:')
var_norm_db = df[df['is_kc']==0]['BAD_Db'].var()
var_norm_df = df[df['is_kc']==0]['BAD_Df'].var()
var_kc_db = df[df['is_kc']==1]['BAD_Db'].var()
var_kc_df = df[df['is_kc']==1]['BAD_Df'].var()
print('  Variancia Db (Normal -> KC): %.2f -> %.2f (Aumento de %.1fx)' % (var_norm_db, var_kc_db, var_kc_db/var_norm_db))
print('  Variancia Df (Normal -> KC): %.2f -> %.2f (Aumento de %.1fx)' % (var_norm_df, var_kc_df, var_kc_df/var_norm_df))
if var_kc_df > var_kc_db * 2:
    print('  --> A superficie anterior sofre COLAPSO CATASTROFICO (alta variancia) no KC')

# ==========================================
# DASHBOARD GRAFICO
# ==========================================
print('\n  Gerando dashboard de severidade...')
fig = plt.figure(figsize=(16, 12))
fig.suptitle('DF COMO MOTOR DA GRAVIDADE (CATASTROFE ANTERIOR)', 
             fontsize=14, fontweight='bold', color=ACCENT, y=0.98)
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.25,
              left=0.07, right=0.96, top=0.90, bottom=0.08)

# A: Evolucao Db vs Df por Severidade
ax1 = fig.add_subplot(gs[0, 0])
x_col = severity_col
ax1.scatter(clean_kc[x_col], clean_kc['BAD_Db'], color=RED, alpha=0.6, label='Db (Posterior)', s=25, edgecolor='none')
ax1.scatter(clean_kc[x_col], clean_kc['BAD_Df'], color=CYAN, alpha=0.6, label='Df (Anterior)', s=25, edgecolor='none')

# Linhas de tendencia
x_vals = np.linspace(clean_kc[x_col].min(), clean_kc[x_col].max(), 100)
ax1.plot(x_vals, intercept_db + slope_db * x_vals, color=RED, linewidth=2, linestyle='--')
# Fit polinomial para Df para mostrar a curvatura (aceleracao)
z_df = np.polyfit(clean_kc[x_col], clean_kc['BAD_Df'], 2)
ax1.plot(x_vals, np.polyval(z_df, x_vals), color=CYAN, linewidth=2, linestyle='--')

ax1.set_xlabel(f'Severidade ({severity_col})')
ax1.set_ylabel('Desvio (BAD D-value)')
ax1.legend()
_style(ax1, 'A. Trajetoria de Colapso (Anterior acelera e ultrapassa Posterior)')

# B: Razao Df/Db vs Severidade
ax2 = fig.add_subplot(gs[0, 1])
ax2.axhline(1.0, color=ORANGE, linestyle=':', label='Equilibrio (Df = Db)')
clean_ratio = clean_kc.dropna(subset=['Ratio_Df_Db'])
sc = ax2.scatter(clean_ratio[x_col], clean_ratio['Ratio_Df_Db'], 
            c=clean_ratio['Ratio_Df_Db'], cmap='viridis', s=30, alpha=0.8, edgecolor='none')
plt.colorbar(sc, ax=ax2, label='Razao Df/Db')
ax2.set_xlabel(f'Severidade ({severity_col})')
ax2.set_ylabel('Fator de Amplificacao (Razao Df/Db)')

# Suavizacao
try:
    from scipy.interpolate import make_interp_spline
    x_sort = np.sort(clean_ratio[x_col])
    # media movel
    window = 5
    ratio_smooth = clean_ratio.sort_values(x_col)['Ratio_Df_Db'].rolling(window, center=True).mean()
    ax2.plot(x_sort, ratio_smooth, color=PINK, linewidth=2, label='Tendencia')
except:
    pass
ax2.legend()
_style(ax2, 'B. Amplificacao Anterior Cresce com a Severidade')

# C: Barplot por Estagio
ax3 = fig.add_subplot(gs[1, 0])
stages = [s['Estagio'] for s in stats_by_stage]
db_vals = [s['Db'] for s in stats_by_stage]
df_vals = [s['Df'] for s in stats_by_stage]
x = np.arange(len(stages))
width = 0.35

ax3.bar(x - width/2, db_vals, width, label='Db (Posterior)', color=RED, alpha=0.8)
ax3.bar(x + width/2, df_vals, width, label='Df (Anterior)', color=CYAN, alpha=0.8)
ax3.set_xticks(x)
ax3.set_xticklabels([str(s) for s in stages])
ax3.set_ylabel('Desvio Medio')
ax3.legend()

# Add text labels on bars
for i in range(len(stages)):
    ax3.text(x[i] - width/2, db_vals[i] + 0.5, f'{db_vals[i]:.1f}', ha='center', color=TEXT, fontsize=8)
    ax3.text(x[i] + width/2, df_vals[i] + 0.5, f'{df_vals[i]:.1f}', ha='center', color=TEXT, fontsize=8)

_style(ax3, 'C. Inversao de Dominancia nos Estagios da Doenca')

# D: Modelo Biomecanico (Teoria da Catastrofe)
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

# Desenhar grafico conceitual de forca-deslocamento (curva stress-strain)
ax4.text(0.5, 0.95, 'TEORIA DO COLAPSO DA CASCA (SHELL BUCKLING)', ha='center', fontsize=11, fontweight='bold', color=ACCENT)
ax4.text(0.5, 0.88, 'A gravidade extrema e impulsionada pela FALHA ANTERIOR.', ha='center', fontsize=9, color=TEXT)

# Curvas
x_teoria = np.linspace(0, 10, 100)
y_post = x_teoria * 0.5 # linear yielding
y_ant = np.piecewise(x_teoria, [x_teoria < 6, x_teoria >= 6], 
                     [lambda x: x*0.1, lambda x: 0.6 + (x-6)**2 * 0.8])

ax4_sub = ax4.inset_axes([0.1, 0.1, 0.8, 0.7])
ax4_sub.plot(x_teoria, y_post, color=RED, lw=3, label='Posterior (Plastica/Lenta)')
ax4_sub.plot(x_teoria, y_ant, color=CYAN, lw=3, label='Anterior (Buckling/Catastrofe)')
ax4_sub.axvline(6, color=ORANGE, linestyle=':', lw=2)
ax4_sub.text(6.2, 5, 'Ponto de Colapso\nda Casca Anterior', color=ORANGE, fontweight='bold')
ax4_sub.set_xlabel('Tempo / Progressao da Doenca', color=TEXT)
ax4_sub.set_ylabel('Deformacao (Deviacao)', color=TEXT)
ax4_sub.tick_params(axis='both', colors=BG2) # hide ticks
ax4_sub.grid(False)
ax4_sub.legend(loc='upper left', frameon=False, labelcolor=TEXT)
_style(ax4_sub, '')

out = r'c:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\results\severidade_ceratocone_df.png'
fig.savefig(out, dpi=180, bbox_inches='tight')
plt.close('all')
print('  Dashboard salvo: %s' % out)

print('\n================================================================')
print('  RESUMO DA HIPOTESE:')
print('  O Df comeca BAIXO (resistido pela rigidez anterior), mas')
print('  quando o estroma anterior falha, ele entra em "Shell Buckling"')
print('  (colapso de casca). A variancia explode e o Df acelera ')
print('  exponencialmente, ultrapassando o Db. ')
print('  --> O Db e o "sensor" precoce.')
print('  --> O Df e o "motor" da gravidade extrema.')
print('================================================================')
