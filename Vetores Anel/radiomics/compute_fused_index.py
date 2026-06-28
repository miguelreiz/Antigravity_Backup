"""
Índice Fusionado: Radiômica IT + Espessura Epitelial + Elevação Posterior
Pareia todos os dados disponíveis e calcula AUC por componente e combinado.
Com 10-fold cross-validation e IC 95% por bootstrap.
"""
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings('ignore')
import unicodedata, re

out_dir = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch'

# ===== 1. CARREGAR TODOS OS DATASETS =====

# 1a. Matched Pairs (443 olhos com ground truth FII + BAD-D)
matched = pd.read_csv(r'D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\matched_pairs_FII_Pentacam.csv', sep=';')

# 1b. Radiômica Mass (665 SPR com Entropy, Contrast, Correlation, Energy)
radiomics = pd.read_csv(r'D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\pentacam_mass_radiomics.csv', sep=';')

# 1c. Radiômica IT específica (673 SPR com Entropy_Central e Entropy_IT)
radiomics_it = pd.read_csv(r'D:\pentacam_mass_radiomics_IT.csv', sep=';')

# 1d. Peak Detection Epitelial (673 SPR)
epi = pd.read_csv(r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch\epithelial_peak_detection.csv', sep=';')

print(f"Matched pairs: {len(matched)}")
print(f"Radiomics mass: {len(radiomics)}")
print(f"Radiomics IT: {len(radiomics_it)}")
print(f"Epithelial PD: {len(epi)}")

# ===== 2. PAREAMENTO POR NOME =====
def norm(name):
    if not isinstance(name, str): return ""
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-z ]', '', s.lower()).strip()
    return s

def get_tokens(name):
    skip = {'de','da','do','dos','das','e','di','del'}
    tokens = set(norm(name).split()) - skip
    tokens.discard('')
    return frozenset(tokens)

# Merge radiomics com IT e epi (por File)
rad_merged = radiomics.merge(radiomics_it[['File','Entropy_IT']], on='File', how='left')
rad_merged = rad_merged.merge(epi[['File','Epi_Temporal_um','Epi_Central_um','Epi_Ratio_TC']], on='File', how='left')

# Agora parear com matched_pairs por nome
matched['tokens'] = matched['nome_pentacam'].apply(get_tokens)
rad_merged['tokens'] = rad_merged['Patient_Name'].apply(get_tokens)

paired_rows = []
for _, m_row in matched.iterrows():
    m_tok = m_row['tokens']
    if len(m_tok) < 1: continue
    
    best = None
    best_score = 0
    for _, r_row in rad_merged.iterrows():
        r_tok = r_row['tokens']
        overlap = m_tok & r_tok
        score = len(overlap) / max(1, min(len(m_tok), len(r_tok)))
        if score > best_score and score >= 0.5:
            best_score = score
            best = r_row
    
    if best is not None:
        row = {
            'BAD_D': m_row['BAD_D'],
            'Pachy_Min': m_row['Pachy_Min'],
            'K1': m_row['K1'],
            'K2': m_row['K2'],
            'FII_IT': m_row['FII_IT'],
            'FII_Class': m_row['FII_Class'],
            'Penta_Class': m_row['Penta_Class'],
            'penta_pos': m_row['penta_pos'],
            'fii_pos': m_row['fii_pos'],
            # Radiomics
            'Entropy': best['Entropy'],
            'Contrast': best['Contrast'],
            'Correlation': best['Correlation'],
            'Energy': best['Energy'],
            'Entropy_IT': best.get('Entropy_IT', np.nan),
            # Epithelial
            'Epi_Temporal_um': best.get('Epi_Temporal_um', np.nan),
            'Epi_Central_um': best.get('Epi_Central_um', np.nan),
            'Epi_Ratio_TC': best.get('Epi_Ratio_TC', np.nan),
        }
        paired_rows.append(row)

df = pd.DataFrame(paired_rows)
print(f"\nPareados com sucesso: {len(df)} olhos")
print(f"  Com Entropy_IT: {df['Entropy_IT'].notna().sum()}")
print(f"  Com Epi_Temporal: {df['Epi_Temporal_um'].notna().sum()}")

# ===== 3. DEFINIR TARGET =====
# Target binário: BAD_D >= 1.6 (suspect+) OU Penta_Class != 'Normal'
df['target'] = ((df['BAD_D'] >= 1.6) | (df['Penta_Class'] != 'Normal')).astype(int)
print(f"\nTarget: {df['target'].value_counts().to_dict()}")

# ===== 4. CALCULAR AUC POR COMPONENTE (10-fold CV) =====

def compute_auc_cv(X, y, name, n_splits=10):
    """Calcula AUC com k-fold CV e bootstrap IC 95%"""
    valid = X.notna().all(axis=1)
    X_clean = X[valid].values
    y_clean = y[valid].values
    
    if len(np.unique(y_clean)) < 2 or len(y_clean) < 20:
        print(f"  {name}: Dados insuficientes ({len(y_clean)} amostras)")
        return None, None, None
    
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=1000, C=1.0))
    ])
    
    cv = StratifiedKFold(n_splits=min(n_splits, min(np.bincount(y_clean))), shuffle=True, random_state=42)
    
    try:
        y_prob = cross_val_predict(pipe, X_clean, y_clean, cv=cv, method='predict_proba')[:, 1]
        auc = roc_auc_score(y_clean, y_prob)
        
        # Bootstrap IC 95%
        n_boot = 1000
        aucs_boot = []
        rng = np.random.RandomState(42)
        for _ in range(n_boot):
            idx = rng.choice(len(y_clean), len(y_clean), replace=True)
            if len(np.unique(y_clean[idx])) < 2: continue
            aucs_boot.append(roc_auc_score(y_clean[idx], y_prob[idx]))
        
        ci_low = np.percentile(aucs_boot, 2.5)
        ci_high = np.percentile(aucs_boot, 97.5)
        
        print(f"  {name}: AUC = {auc:.3f} (IC 95%: {ci_low:.3f} - {ci_high:.3f}) [n={len(y_clean)}]")
        return auc, (ci_low, ci_high), (y_clean, y_prob)
    except Exception as e:
        print(f"  {name}: ERRO - {e}")
        return None, None, None

print("\n=== AUC POR COMPONENTE (10-fold CV, IC 95% Bootstrap) ===\n")

# Componente 1: Radiômica GLCM (região temporal)
auc_rad, ci_rad, data_rad = compute_auc_cv(
    df[['Entropy', 'Contrast', 'Correlation', 'Energy']], 
    df['target'], 
    "Radiômica GLCM (4 features)"
)

# Componente 1b: Entropy IT só
auc_eit, ci_eit, data_eit = compute_auc_cv(
    df[['Entropy_IT']], 
    df['target'], 
    "Entropy IT (univariada)"
)

# Componente 2: Espessura Epitelial (temporal)
auc_epi, ci_epi, data_epi = compute_auc_cv(
    df[['Epi_Temporal_um', 'Epi_Central_um', 'Epi_Ratio_TC']], 
    df['target'], 
    "Espessura Epitelial (T+C+Ratio)"
)

# Componente 3: Elevação Posterior (via Pachy_Min como proxy)
auc_post, ci_post, data_post = compute_auc_cv(
    df[['Pachy_Min', 'K2']], 
    df['target'], 
    "Posterior (Pachy_Min + K2)"
)

# ===== 5. ÍNDICE FUSIONADO =====
# Combinar TODOS os componentes disponíveis
fusion_cols = ['Entropy', 'Contrast', 'Correlation', 'Energy', 
               'Entropy_IT', 
               'Epi_Temporal_um', 'Epi_Central_um', 'Epi_Ratio_TC',
               'Pachy_Min', 'K2']

auc_fusion, ci_fusion, data_fusion = compute_auc_cv(
    df[fusion_cols], 
    df['target'], 
    "ÍNDICE FUSIONADO (10 features)"
)

# ===== 6. PLOT ROC COMPARATIVO =====
fig, ax = plt.subplots(figsize=(8, 7))

colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f39c12']
labels_data = [
    (data_rad, f'Radiômica GLCM (AUC={auc_rad:.3f})', colors[0]),
    (data_epi, f'Espessura Epitelial (AUC={auc_epi:.3f})', colors[1]),
    (data_post, f'Posterior (AUC={auc_post:.3f})', colors[2]),
    (data_fusion, f'ÍNDICE FUSIONADO (AUC={auc_fusion:.3f})', colors[4]),
]

for data, label, color in labels_data:
    if data is not None:
        y_true, y_prob = data
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        lw = 3 if 'FUSIONADO' in label else 1.5
        ax.plot(fpr, tpr, color=color, linewidth=lw, label=label)

ax.plot([0,1], [0,1], 'k--', alpha=0.3, linewidth=1)
ax.set_xlabel('1 - Especificidade', fontsize=13)
ax.set_ylabel('Sensibilidade', fontsize=13)
ax.set_title('Curva ROC: Componentes Individuais vs. Índice Fusionado\n(10-fold CV, Pentacam Standard — Região Temporal)', fontsize=13, fontweight='bold')
ax.legend(loc='lower right', fontsize=10)
ax.set_xlim([0, 1])
ax.set_ylim([0, 1.02])
ax.grid(True, alpha=0.3)

roc_path = os.path.join(out_dir, 'ROC_indice_fusionado.png')
plt.tight_layout()
plt.savefig(roc_path, dpi=300, bbox_inches='tight')
print(f"\nROC salvo em: {roc_path}")

# ===== 7. RESUMO TABULAR =====
print("\n" + "="*70)
print("  RESUMO FINAL — ÍNDICES COM VALIDAÇÃO CRUZADA")
print("="*70)
print(f"{'Componente':<35} {'AUC':>6} {'IC 95%':>20} {'N':>5}")
print("-"*70)
for name, auc, ci in [
    ("Radiômica GLCM (4 features)", auc_rad, ci_rad),
    ("Entropy IT (univariada)", auc_eit, ci_eit),
    ("Espessura Epitelial (3 features)", auc_epi, ci_epi),
    ("Posterior (Pachy+K2)", auc_post, ci_post),
    ("ÍNDICE FUSIONADO (10 features)", auc_fusion, ci_fusion),
]:
    if auc is not None:
        print(f"  {name:<33} {auc:>6.3f} ({ci[0]:.3f} - {ci[1]:.3f})")
    else:
        print(f"  {name:<33}   N/A")
print("="*70)
