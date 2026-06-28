"""
================================================================
  PONTE FII x CURVATURA ANTERIOR/POSTERIOR
  Analise cruzada: 444 pares matched OCT-Triton x Pentacam
================================================================
Preenche o GAP: correlaciona o biomarcador radiometrico (FII)
com os indices geometricos anterior/posterior do Pentacam.

  FII = B_ant / B_post  (radiometria estromal profunda)
  BAD_Df = desvio anterior  (geometria Pentacam)
  BAD_Db = desvio posterior (geometria Pentacam)

Hipotese: se o FII mede colapso fibrilar ant/post, deve existir
correlacao com os indices geometricos ant/post do Pentacam.
================================================================
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import cross_val_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# -- DARK THEME --
BG       = '#0d1117'
BG2      = '#161b22'
TEXT     = '#c9d1d9'
ACCENT   = '#58a6ff'
GREEN    = '#3fb950'
RED      = '#f85149'
ORANGE   = '#d29922'
PURPLE   = '#bc8cff'
CYAN     = '#39d2c0'
PINK     = '#f778ba'
GRID_CLR = '#21262d'
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

# -- LOAD DATA --
CSV = r"D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\matched_pairs_FII_Pentacam.csv"
OUT_DIR = r"c:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\results"
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV, sep=';')
print(f"  Loaded: {len(df)} matched pairs")
print(f"  Columns: {list(df.columns)}")

# -- NUMERIC CLEANUP --
num_cols = ['FII_Central','FII_IT','FII_IC','FII_IN','BAD_D','K1','K2',
            'Astig','ART_Max','Pachy_Min','BAD_Df','BAD_Db']
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Derived features
df['FII_IAS'] = df['FII_Central'] - df['FII_IT']
df['BAD_Ratio'] = df['BAD_Df'] / df['BAD_Db'].replace(0, np.nan)
df['Kmax'] = df[['K1','K2']].max(axis=1)
df['Kmean'] = (df['K1'] + df['K2']) / 2

# Binary outcome
df['is_kc'] = (df['Penta_Class'].str.contains('KC', case=False, na=False)).astype(int)

# Clean
clean = df.dropna(subset=['FII_IT','FII_Central','BAD_Df','BAD_Db','BAD_D'])
clean = clean[(clean['BAD_Db'] != 0)]
print(f"  Clean pairs: {len(clean)}")
print(f"  KC: {clean['is_kc'].sum()} | Normal: {(~clean['is_kc'].astype(bool)).sum()}")

# -- 1. CORRELATION MATRIX --
print("\n" + "="*70)
print("  1. CORRELACOES FII x PENTACAM ANT/POST")
print("="*70)

pairs = [
    ('FII_IT',      'BAD_Db',    'FII_IT vs BAD_Db (posterior)'),
    ('FII_IT',      'BAD_Df',    'FII_IT vs BAD_Df (anterior)'),
    ('FII_Central', 'BAD_Db',    'FII_Central vs BAD_Db (posterior)'),
    ('FII_Central', 'BAD_Df',    'FII_Central vs BAD_Df (anterior)'),
    ('FII_IT',      'BAD_D',     'FII_IT vs BAD_D (composto)'),
    ('FII_Central', 'BAD_D',     'FII_Central vs BAD_D (composto)'),
    ('FII_IAS',     'BAD_Db',    'IAS (C-IT) vs BAD_Db (posterior)'),
    ('FII_IT',      'Pachy_Min', 'FII_IT vs Pachy_Min'),
    ('FII_IT',      'K2',        'FII_IT vs K2'),
    ('FII_IT',      'Kmax',      'FII_IT vs Kmax'),
    ('BAD_Df',      'BAD_Db',    'BAD_Df vs BAD_Db (ant vs post Pentacam)'),
    ('FII_IAS',     'BAD_D',     'IAS vs BAD_D'),
]

results = []
for x_col, y_col, label in pairs:
    valid = clean.dropna(subset=[x_col, y_col])
    if len(valid) < 10:
        continue
    r, p = stats.pearsonr(valid[x_col], valid[y_col])
    rho, p_sp = stats.spearmanr(valid[x_col], valid[y_col])
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
    print(f"  {label:45s}  Pearson r={r:+.4f} p={p:.2e} {sig}  | Spearman rho={rho:+.4f}")
    results.append({'pair': label, 'x': x_col, 'y': y_col,
                    'r': r, 'p': p, 'rho': rho, 'sig': sig, 'n': len(valid)})

results_df = pd.DataFrame(results)

# -- 2. LOGISTIC REGRESSION: FII + Pentacam AntPost --
print("\n" + "="*70)
print("  2. REGRESSAO LOGISTICA: FII + PENTACAM ANT/POST")
print("="*70)

model_data = clean.dropna(subset=['FII_IT','FII_Central','BAD_Df','BAD_Db',
                                   'K2','Pachy_Min','is_kc'])
model_data = model_data.replace([np.inf, -np.inf], np.nan).dropna(
    subset=['FII_IT','BAD_Df','BAD_Db','K2','Pachy_Min','is_kc'])

roc_results = {}
if model_data['is_kc'].sum() >= 5:
    models = {
        'BAD_D sozinho':                ['BAD_D'],
        'BAD_Df + BAD_Db':              ['BAD_Df', 'BAD_Db'],
        'FII_IT sozinho':               ['FII_IT'],
        'FII_IT + BAD_Db':              ['FII_IT', 'BAD_Db'],
        'FII_IT + BAD_Df + BAD_Db':     ['FII_IT', 'BAD_Df', 'BAD_Db'],
        'FII_IT + FII_C + BAD_Df + BAD_Db': ['FII_IT', 'FII_Central', 'BAD_Df', 'BAD_Db'],
        'Full (FII+Penta)':             ['FII_IT','FII_Central','BAD_Df','BAD_Db','K2','Pachy_Min'],
    }
    
    y = model_data['is_kc'].values
    
    for name, features in models.items():
        try:
            X = model_data[features].values
            X_std = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)
            lr = LogisticRegression(max_iter=1000, random_state=42)
            auc_cv = cross_val_score(lr, X_std, y, cv=5, scoring='roc_auc')
            lr.fit(X_std, y)
            y_prob = lr.predict_proba(X_std)[:,1]
            auc_full = roc_auc_score(y, y_prob)
            fpr, tpr, _ = roc_curve(y, y_prob)
            roc_results[name] = {'auc_cv': auc_cv.mean(), 'auc_std': auc_cv.std(),
                                 'auc_full': auc_full, 'fpr': fpr, 'tpr': tpr,
                                 'coefs': dict(zip(features, lr.coef_[0]))}
            print(f"  {name:40s}  AUC_CV={auc_cv.mean():.3f} +/- {auc_cv.std():.3f}  AUC_full={auc_full:.3f}")
            for f, c in zip(features, lr.coef_[0]):
                print(f"    {f:20s}: beta={c:+.3f}")
        except Exception as e:
            print(f"  {name:40s}  ERRO: {e}")
else:
    print(f"  INSUFICIENTE: apenas {model_data['is_kc'].sum()} KC positivos")

# -- 3. T-TESTS: KC vs Normal --
print("\n" + "="*70)
print("  3. T-TESTS: KC vs NORMAL")
print("="*70)

kc = clean[clean['is_kc'] == 1]
nl = clean[clean['is_kc'] == 0]

for col in ['FII_IT','FII_Central','FII_IAS','BAD_Df','BAD_Db','BAD_D','Pachy_Min','K2']:
    kc_vals = kc[col].dropna()
    nl_vals = nl[col].dropna()
    if len(kc_vals) > 2 and len(nl_vals) > 2:
        t, p = stats.ttest_ind(kc_vals, nl_vals, equal_var=False)
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        d = (kc_vals.mean() - nl_vals.mean()) / np.sqrt((kc_vals.std()**2 + nl_vals.std()**2)/2)
        print(f"  {col:15s}: KC={kc_vals.mean():.3f}+/-{kc_vals.std():.3f}  "
              f"NL={nl_vals.mean():.3f}+/-{nl_vals.std():.3f}  "
              f"d={d:+.2f}  t={t:+.2f}  p={p:.2e} {sig}")

# -- 4. GENERATE DASHBOARD --
print("\n  Gerando dashboard...")

fig = plt.figure(figsize=(20, 14))
fig.suptitle("PONTE FII x CURVATURA ANTERIOR/POSTERIOR - 444 Pares Matched",
             fontsize=14, fontweight='bold', color=ACCENT, y=0.98)

gs = GridSpec(3, 4, figure=fig, hspace=0.35, wspace=0.35,
              left=0.06, right=0.97, top=0.93, bottom=0.05)

# Panel A: FII_IT vs BAD_Db (POSTERIOR)
ax1 = fig.add_subplot(gs[0, 0])
kc_mask = clean['is_kc'] == 1
ax1.scatter(clean.loc[~kc_mask, 'FII_IT'], clean.loc[~kc_mask, 'BAD_Db'],
            c=CYAN, alpha=0.4, s=12, label='Normal', edgecolors='none')
ax1.scatter(clean.loc[kc_mask, 'FII_IT'], clean.loc[kc_mask, 'BAD_Db'],
            c=RED, alpha=0.8, s=25, label='KC', edgecolors='white', linewidths=0.5)
valid_fit = clean.dropna(subset=['FII_IT','BAD_Db'])
z = np.polyfit(valid_fit['FII_IT'], valid_fit['BAD_Db'], 1)
xline = np.linspace(valid_fit['FII_IT'].min(), valid_fit['FII_IT'].max(), 100)
ax1.plot(xline, np.polyval(z, xline), '--', color=ORANGE, linewidth=1.5)
r_val = results_df[results_df['y']=='BAD_Db']
r_val = r_val[r_val['x']=='FII_IT']['r'].values
r_str = f"r={r_val[0]:.3f}" if len(r_val) > 0 else ""
ax1.set_xlabel('FII_IT (radiometria)')
ax1.set_ylabel('BAD_Db (desvio posterior)')
ax1.legend(fontsize=7, loc='upper right')
_style(ax1, f'A. FII_IT vs BAD_Db (Post)\n{r_str}')

# Panel B: FII_IT vs BAD_Df (ANTERIOR)
ax2 = fig.add_subplot(gs[0, 1])
ax2.scatter(clean.loc[~kc_mask, 'FII_IT'], clean.loc[~kc_mask, 'BAD_Df'],
            c=CYAN, alpha=0.4, s=12, label='Normal', edgecolors='none')
ax2.scatter(clean.loc[kc_mask, 'FII_IT'], clean.loc[kc_mask, 'BAD_Df'],
            c=RED, alpha=0.8, s=25, label='KC', edgecolors='white', linewidths=0.5)
valid_fit2 = clean.dropna(subset=['FII_IT','BAD_Df'])
z2 = np.polyfit(valid_fit2['FII_IT'], valid_fit2['BAD_Df'], 1)
ax2.plot(xline, np.polyval(z2, xline), '--', color=ORANGE, linewidth=1.5)
r_val2 = results_df[results_df['y']=='BAD_Df']
r_val2 = r_val2[r_val2['x']=='FII_IT']['r'].values
r_str2 = f"r={r_val2[0]:.3f}" if len(r_val2) > 0 else ""
ax2.set_xlabel('FII_IT (radiometria)')
ax2.set_ylabel('BAD_Df (desvio anterior)')
ax2.legend(fontsize=7, loc='upper right')
_style(ax2, f'B. FII_IT vs BAD_Df (Ant)\n{r_str2}')

# Panel C: BAD_Df vs BAD_Db (Ant vs Post PENTACAM)
ax3 = fig.add_subplot(gs[0, 2])
ax3.scatter(clean.loc[~kc_mask, 'BAD_Df'], clean.loc[~kc_mask, 'BAD_Db'],
            c=CYAN, alpha=0.4, s=12, label='Normal', edgecolors='none')
ax3.scatter(clean.loc[kc_mask, 'BAD_Df'], clean.loc[kc_mask, 'BAD_Db'],
            c=RED, alpha=0.8, s=25, label='KC', edgecolors='white', linewidths=0.5)
valid_fit3 = clean.dropna(subset=['BAD_Df','BAD_Db'])
z3 = np.polyfit(valid_fit3['BAD_Df'], valid_fit3['BAD_Db'], 1)
xline3 = np.linspace(valid_fit3['BAD_Df'].min(), valid_fit3['BAD_Df'].max(), 100)
ax3.plot(xline3, np.polyval(z3, xline3), '--', color=ORANGE, linewidth=1.5)
r_val3 = results_df[results_df['y']=='BAD_Db']
r_val3 = r_val3[r_val3['x']=='BAD_Df']['r'].values
r_str3 = f"r={r_val3[0]:.3f}" if len(r_val3) > 0 else ""
ax3.set_xlabel('BAD_Df (ant)')
ax3.set_ylabel('BAD_Db (post)')
ax3.legend(fontsize=7, loc='upper left')
_style(ax3, f'C. BAD_Df vs BAD_Db\n{r_str3}')

# Panel D: IAS vs BAD_D
ax4 = fig.add_subplot(gs[0, 3])
sc = ax4.scatter(clean['FII_IAS'], clean['BAD_D'],
                 c=clean['BAD_Db'], cmap='RdYlGn_r', alpha=0.6, s=15,
                 edgecolors='none', vmin=-2, vmax=10)
plt.colorbar(sc, ax=ax4, label='BAD_Db', shrink=0.8)
ax4.set_xlabel('IAS = FII_C - FII_IT')
ax4.set_ylabel('BAD_D (composto)')
ax4.axvline(0, color=GRID_CLR, linestyle=':', linewidth=0.8)
ax4.axhline(1.6, color=RED, linestyle='--', linewidth=0.8, alpha=0.5, label='BAD_D=1.6')
ax4.legend(fontsize=7)
_style(ax4, 'D. IAS vs BAD_D\n(cor=BAD_Db)')

# Panel E: Correlation Heatmap
ax5 = fig.add_subplot(gs[1, 0:2])
corr_cols = ['FII_IT','FII_Central','FII_IAS','BAD_Df','BAD_Db','BAD_D','K2','Pachy_Min']
corr_data = clean[corr_cols].dropna()
corr_mat = corr_data.corr(method='spearman')
im = ax5.imshow(corr_mat, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
ax5.set_xticks(range(len(corr_cols)))
ax5.set_yticks(range(len(corr_cols)))
ax5.set_xticklabels(corr_cols, rotation=45, ha='right', fontsize=7)
ax5.set_yticklabels(corr_cols, fontsize=7)
for i in range(len(corr_cols)):
    for j in range(len(corr_cols)):
        val = corr_mat.iloc[i, j]
        color = 'white' if abs(val) > 0.5 else TEXT
        ax5.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=6.5, color=color)
plt.colorbar(im, ax=ax5, shrink=0.8, label='Spearman rho')
_style(ax5, 'E. Spearman Correlation Matrix - FII x Pentacam Ant/Post')

# Panel F: ROC Curves
ax6 = fig.add_subplot(gs[1, 2:4])
if roc_results:
    colors = [ACCENT, CYAN, GREEN, ORANGE, RED, PURPLE, PINK]
    for i, (name, res) in enumerate(roc_results.items()):
        ax6.plot(res['fpr'], res['tpr'], color=colors[i % len(colors)],
                 linewidth=1.5, label=f"{name} (AUC={res['auc_cv']:.3f})")
    ax6.plot([0,1],[0,1], '--', color=GRID_CLR, linewidth=0.8)
    ax6.set_xlabel('1 - Especificidade')
    ax6.set_ylabel('Sensibilidade')
    ax6.legend(fontsize=6.5, loc='lower right')
_style(ax6, 'F. ROC: FII + Pentacam Ant/Post vs KC')

# Panel G: Boxplot KC vs Normal
ax7 = fig.add_subplot(gs[2, 0:2])
box_cols = ['FII_IT','FII_Central','BAD_Df','BAD_Db']
positions = []
bdata_nl = []
bdata_kc = []
labels = []
for i, col in enumerate(box_cols):
    nl_v = nl[col].dropna().values
    kc_v = kc[col].dropna().values
    bdata_nl.append(nl_v)
    bdata_kc.append(kc_v)
    labels.append(col)
    positions.append(i)

bp_nl = ax7.boxplot(bdata_nl, positions=[p-0.18 for p in positions], widths=0.3,
                     patch_artist=True, showfliers=False)
bp_kc = ax7.boxplot(bdata_kc, positions=[p+0.18 for p in positions], widths=0.3,
                     patch_artist=True, showfliers=False)
for box in bp_nl['boxes']:
    box.set(facecolor=CYAN, alpha=0.6)
for box in bp_kc['boxes']:
    box.set(facecolor=RED, alpha=0.6)
for element in ['whiskers','caps','medians']:
    for line in bp_nl[element]:
        line.set(color=TEXT, linewidth=0.8)
    for line in bp_kc[element]:
        line.set(color=TEXT, linewidth=0.8)
ax7.set_xticks(positions)
ax7.set_xticklabels(labels, fontsize=8)
ax7.legend([bp_nl['boxes'][0], bp_kc['boxes'][0]], ['Normal','KC'], fontsize=8, loc='upper right')
_style(ax7, 'G. Distribuicao KC vs Normal - FII e BAD Ant/Post')

# Panel H: Scatter FII_IT colored by BAD_Db
ax8 = fig.add_subplot(gs[2, 2:4])
valid_h = clean.dropna(subset=['FII_IT','FII_Central','BAD_Db'])
sc2 = ax8.scatter(valid_h['FII_IT'], valid_h['FII_Central'],
                   c=valid_h['BAD_Db'], cmap='RdYlGn_r', s=15, alpha=0.7,
                   edgecolors='none', vmin=-2, vmax=10)
plt.colorbar(sc2, ax=ax8, label='BAD_Db (post)', shrink=0.8)
ax8.axvline(1.05, color=ORANGE, linestyle='--', linewidth=0.8, alpha=0.6, label='FII_IT=1.05')
ax8.axhline(1.10, color=GREEN, linestyle='--', linewidth=0.8, alpha=0.6, label='FII_C=1.10')
ax8.fill_between([0.5, 1.05], 1.10, 2.0, alpha=0.08, color=RED)
ax8.text(0.78, 1.65, 'KC\nVerdadeiro', ha='center', fontsize=8, color=RED, fontweight='bold')
ax8.set_xlabel('FII_IT (periferia IT)')
ax8.set_ylabel('FII_Central (apice)')
ax8.set_xlim(0.5, 2.0)
ax8.set_ylim(0.5, 2.0)
ax8.legend(fontsize=7, loc='upper right')
_style(ax8, 'H. Mapa 2D FII Central x IT\n(cor = desvio posterior Pentacam)')

# -- SAVE --
out_png = os.path.join(OUT_DIR, 'ponte_fii_curvatura_antpost.png')
fig.savefig(out_png, dpi=180, bbox_inches='tight')
print(f"\n  Dashboard salvo: {out_png}")

out_csv = os.path.join(OUT_DIR, 'correlacoes_fii_antpost.csv')
results_df.to_csv(out_csv, index=False, sep=';')
print(f"  CSV salvo: {out_csv}")

print("\n" + "="*70)
print("  CONCLUSAO")
print("="*70)
if len(results_df) > 0:
    best = results_df.loc[results_df['r'].abs().idxmax()]
    print(f"  Correlacao mais forte: {best['pair']}")
    print(f"    r = {best['r']:.4f}, p = {best['p']:.2e}")
    
    fii_vs_post = results_df[(results_df['x']=='FII_IT') & (results_df['y']=='BAD_Db')]
    fii_vs_ant = results_df[(results_df['x']=='FII_IT') & (results_df['y']=='BAD_Df')]
    if len(fii_vs_post) > 0 and len(fii_vs_ant) > 0:
        r_post = fii_vs_post['r'].values[0]
        r_ant = fii_vs_ant['r'].values[0]
        print(f"\n  ACHADO CHAVE:")
        print(f"    FII_IT vs BAD_Db (posterior): r = {r_post:.4f}")
        print(f"    FII_IT vs BAD_Df (anterior):  r = {r_ant:.4f}")
        ratio = abs(r_post) / max(abs(r_ant), 0.001)
        if abs(r_post) > abs(r_ant):
            print(f"    --> FII correlaciona {ratio:.1f}x MAIS com posterior que anterior")
            print(f"    --> Confirma: FII mede colapso fibrilar que se expressa PRIMEIRO na posterior")
        else:
            print(f"    --> FII correlaciona mais com anterior ({1/ratio:.1f}x)")

if roc_results:
    best_model = max(roc_results.items(), key=lambda x: x[1]['auc_cv'])
    print(f"\n  Melhor modelo preditivo: {best_model[0]}")
    print(f"    AUC_CV = {best_model[1]['auc_cv']:.3f} +/- {best_model[1]['auc_std']:.3f}")

plt.close('all')
print("\n  Analise concluida!")
