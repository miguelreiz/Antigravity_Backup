"""
hypothesis_ant_post.py — Teste de Hipótese: Relação Curvatura Anterior × Posterior
====================================================================================
Análise em 5 eixos:
  1. ANATÔMICO:    Correlação geométrica r_ant × r_post
  2. FUNCIONAL:    Regressão logística K2 × Pachy_Min para ectasia
  3. ÓPTICO:       Poder refrativo Gullstrand computado
  4. COMÁTICO:     Índices de assimetria e irregularidade
  5. BIOMECÂNICO:  Integração com dados FEM (se disponíveis)

Gera dashboard visual com 5 painéis e relatório estatístico completo.

Author: Antigravity Pipeline
Date: 2025-06
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, roc_curve

# ============================================================
# ESTILO VISUAL (dark theme consistente com o projeto)
# ============================================================

DARK_BG = "#161B22"
DARK_FG = "#0D1117"
GRID_COLOR = "#21262D"
SPINE_COLOR = "#6E7681"
C_ANT = "#00D4AA"     # Verde-turquesa para anterior
C_POST = "#F4C430"    # Dourado para posterior
C_CORR = "#BD93F9"    # Roxo para correlação
C_FUNC = "#FF7B72"    # Vermelho para funcional
C_OPT = "#58A6FF"     # Azul para óptico
C_COMA = "#D2A8FF"    # Lilás para comático
C_FEM = "#FFA657"     # Laranja para FEM

FONT_COLOR = "white"

plt.rcParams.update({
    'figure.facecolor': DARK_BG,
    'axes.facecolor': DARK_FG,
    'axes.edgecolor': SPINE_COLOR,
    'axes.labelcolor': FONT_COLOR,
    'text.color': FONT_COLOR,
    'xtick.color': FONT_COLOR,
    'ytick.color': FONT_COLOR,
    'grid.color': GRID_COLOR,
    'grid.alpha': 0.5,
    'grid.linestyle': '--',
    'legend.facecolor': DARK_BG,
    'legend.edgecolor': SPINE_COLOR,
    'legend.labelcolor': FONT_COLOR,
    'font.family': 'sans-serif',
    'font.size': 10,
})


def _style_axis(ax):
    ax.set_facecolor(DARK_FG)
    ax.tick_params(colors=FONT_COLOR)
    for spine in ax.spines.values():
        spine.set_color(SPINE_COLOR)
    ax.grid(color=GRID_COLOR, linestyle='--', alpha=0.5)


# ============================================================
# PATHS
# ============================================================

RESULTS_DIR = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\results'
CURVATURE_CSV = os.path.join(RESULTS_DIR, 'batch_curvature_metrics.csv')
PAIRS_CSV = r'D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\matched_pairs_FII_Pentacam.csv'
FEM_DIR = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\fem_engine'
OUTPUT_DIR = RESULTS_DIR


# ============================================================
# 1. CARREGAR DADOS
# ============================================================

def load_data():
    """Carrega ambas as fontes de dados."""
    data = {}
    
    # Curvature metrics (do batch extractor)
    if os.path.exists(CURVATURE_CSV):
        df_curv = pd.read_csv(CURVATURE_CSV, sep=';')
        data['curvature'] = df_curv
        print(f"[1] Curvature metrics: {len(df_curv)} olhos")
    else:
        print(f"[AVISO] Arquivo não encontrado: {CURVATURE_CSV}")
        print("         Execute batch_curvature_extractor.py primeiro!")
        data['curvature'] = None
    
    # Clinical pairs
    if os.path.exists(PAIRS_CSV):
        df_clin = pd.read_csv(PAIRS_CSV, sep=';')
        for c in ['BAD_D', 'K1', 'K2', 'Astig', 'ART_Max', 'Pachy_Min']:
            if c in df_clin.columns:
                df_clin[c] = pd.to_numeric(df_clin[c], errors='coerce')
        # Criar target
        if 'BAD_D' in df_clin.columns and 'Penta_Class' in df_clin.columns:
            df_clin['target'] = (
                (df_clin['BAD_D'] >= 1.6) | (df_clin['Penta_Class'] != 'Normal')
            ).astype(int)
        data['clinical'] = df_clin
        print(f"[2] Clinical pairs: {len(df_clin)} registros")
    else:
        print(f"[AVISO] Arquivo não encontrado: {PAIRS_CSV}")
        data['clinical'] = None
    
    return data


# ============================================================
# EIXO 1: ANATÔMICO — Correlação Geométrica r_ant × r_post
# ============================================================

def axis1_anatomical(df, ax1, ax2):
    """Correlação entre raio anterior e posterior."""
    print("\n" + "=" * 60)
    print("  EIXO 1: ANATÔMICO — Correlação r_ant × r_post")
    print("=" * 60)
    
    # Filtrar valores válidos
    valid = df.dropna(subset=['R_Anterior_mm', 'R_Posterior_mm']).copy()
    n_start = len(valid)
    
    # --- QC 1: Filtrar por resíduo do ajuste (qualidade do fit) ---
    # Manter apenas olhos com bom ajuste circular (residual < mediana + 1.5*IQR)
    for col in ['Residual_Ant', 'Residual_Post']:
        if col in valid.columns:
            q1, q3 = valid[col].quantile(0.25), valid[col].quantile(0.75)
            iqr = q3 - q1
            valid = valid[valid[col] <= q3 + 1.5 * iqr]
    
    # --- QC 2: Filtrar raios fisicamente plausíveis ---
    # Mesmo com distorção Scheimpflug, raios > 10000mm = quase planos (sem curvatura)
    # Esses são bordas retas que não representam geometria corneana real
    valid = valid[(valid['R_Anterior_mm'] > 1.0) & (valid['R_Anterior_mm'] < 5000)]
    valid = valid[(valid['R_Posterior_mm'] > 0.5) & (valid['R_Posterior_mm'] < 5000)]
    
    # --- QC 3: IQR-based filtering nos dados remanescentes ---
    for col in ['R_Anterior_mm', 'R_Posterior_mm']:
        q1, q3 = valid[col].quantile(0.25), valid[col].quantile(0.75)
        iqr = q3 - q1
        valid = valid[(valid[col] >= q1 - 2.0*iqr) & (valid[col] <= q3 + 2.0*iqr)]
    
    print(f"  N original: {n_start} → N pós-QC: {len(valid)} ({len(valid)/n_start*100:.1f}%)")
    
    r_ant = valid['R_Anterior_mm'].values
    r_post = valid['R_Posterior_mm'].values
    
    # --- ANÁLISE EM ESCALA LOG (lida com a assimetria da distorção) ---
    log_r_ant = np.log10(r_ant)
    log_r_post = np.log10(r_post)
    
    # Correlação de Pearson (escala original)
    r_pearson, p_pearson = stats.pearsonr(r_ant, r_post)
    print(f"\n  [Escala Original]")
    print(f"  Pearson r = {r_pearson:.4f}, p = {p_pearson:.2e}")
    
    # Correlação de Spearman (não-paramétrica, rank-based - invariante a transformação)
    r_spearman, p_spearman = stats.spearmanr(r_ant, r_post)
    print(f"  Spearman ρ = {r_spearman:.4f}, p = {p_spearman:.2e}")
    
    # Correlação em escala log (cancela parte da distorção multiplicativa)
    r_log, p_log = stats.pearsonr(log_r_ant, log_r_post)
    print(f"\n  [Escala Log10]")
    print(f"  Pearson r(log) = {r_log:.4f}, p = {p_log:.2e}")
    
    # Regressão em log
    slope_log, intercept_log, r_log_val, _, _ = stats.linregress(log_r_ant, log_r_post)
    print(f"  Regressão: log(R_post) = {slope_log:.4f} × log(R_ant) + {intercept_log:.4f}")
    print(f"  R² = {r_log_val**2:.4f}")
    
    # Regressão linear (escala original)
    slope, intercept, r_value, p_value, std_err = stats.linregress(r_ant, r_post)
    print(f"\n  [Regressão Original]")
    print(f"  R_post = {slope:.4f} × R_ant + {intercept:.4f}, R² = {r_value**2:.4f}")
    
    # Ratio r_ant/r_post (usando IQR filter)
    ratio = valid['Ratio_Rant_Rpost'].dropna()
    q1r, q3r = ratio.quantile(0.25), ratio.quantile(0.75)
    iqrr = q3r - q1r
    ratio_clean = ratio[(ratio >= q1r - 2*iqrr) & (ratio <= q3r + 2*iqrr)]
    
    print(f"\n  Ratio R_ant/R_post (IQR-filtered, N={len(ratio_clean)}):")
    print(f"    Mean = {ratio_clean.mean():.4f} ± {ratio_clean.std():.4f}")
    print(f"    Median = {ratio_clean.median():.4f}")
    print(f"    IQR = [{ratio_clean.quantile(0.25):.4f}, {ratio_clean.quantile(0.75):.4f}]")
    
    # --- Plot 1: Scatter r_ant vs r_post (LOG SCALE) ---
    _style_axis(ax1)
    ax1.scatter(log_r_ant, log_r_post, alpha=0.4, s=15, color=C_CORR, edgecolors='none')
    
    # Linha de regressão (log)
    x_line = np.linspace(log_r_ant.min(), log_r_ant.max(), 100)
    y_line = slope_log * x_line + intercept_log
    ax1.plot(x_line, y_line, color=C_ANT, linewidth=2, linestyle='-',
             label=f'r(log)={r_log:.3f}, p={p_log:.1e}')
    
    # IC 95% da regressão
    n = len(log_r_ant)
    y_pred = slope_log * log_r_ant + intercept_log
    se = np.sqrt(np.sum((log_r_post - y_pred)**2) / (n - 2))
    x_mean = np.mean(log_r_ant)
    ci = 1.96 * se * np.sqrt(1/n + (x_line - x_mean)**2 / np.sum((log_r_ant - x_mean)**2))
    ax1.fill_between(x_line, y_line - ci, y_line + ci, alpha=0.15, color=C_ANT)
    
    ax1.set_xlabel('log₁₀(R Anterior)')
    ax1.set_ylabel('log₁₀(R Posterior)')
    ax1.set_title('Eixo 1: Correlação Anatômica (Log)', fontweight='bold')
    ax1.legend(fontsize=8)
    
    # --- Plot 2: Distribuição do Ratio (IQR-filtered) ---
    _style_axis(ax2)
    ax2.hist(ratio_clean, bins=30, color=C_CORR, alpha=0.7, edgecolor=SPINE_COLOR)
    ax2.axvline(ratio_clean.median(), color=C_ANT, linestyle='--', linewidth=2,
                label=f'Median={ratio_clean.median():.2f}')
    ax2.axvline(1.2, color=C_POST, linestyle=':', linewidth=2,
                label='Gullstrand (1.20)')
    ax2.set_xlabel('Ratio R_ant / R_post')
    ax2.set_ylabel('Contagem')
    ax2.set_title('Distribuição do Ratio (IQR)', fontweight='bold')
    ax2.legend(fontsize=8)
    
    return {
        'N': len(valid),
        'pearson_r': r_pearson, 'pearson_p': p_pearson,
        'spearman_rho': r_spearman, 'spearman_p': p_spearman,
        'log_r': r_log, 'log_p': p_log,
        'R2': r_value**2, 'R2_log': r_log_val**2,
        'ratio_median': ratio_clean.median(), 'ratio_iqr': iqrr,
        'slope': slope, 'intercept': intercept,
    }


# ============================================================
# EIXO 2: FUNCIONAL — Regressão Logística e Feature Importance
# ============================================================

def axis2_functional(df_clin, ax1, ax2):
    """Análise funcional: K2 × Pachy_Min na predição de ectasia."""
    print("\n" + "=" * 60)
    print("  EIXO 2: FUNCIONAL — Predição de Ectasia")
    print("=" * 60)
    
    required = ['K2', 'Pachy_Min', 'target']
    valid = df_clin.dropna(subset=required).copy()
    print(f"  N válido: {len(valid)}")
    print(f"  Target: {valid['target'].value_counts().to_dict()}")
    
    X = valid[['K2', 'Pachy_Min']].values
    y = valid['target'].values
    
    # --- Regressão Logística ---
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_scaled, y)
    
    # Odds ratios
    coefs = lr.coef_[0]
    odds_ratios = np.exp(coefs)
    feature_names = ['K2', 'Pachy_Min']
    
    print(f"\n  Regressão Logística (padronizada):")
    for name, coef, OR in zip(feature_names, coefs, odds_ratios):
        print(f"    {name:15s}: β = {coef:+.4f}, OR = {OR:.4f}")
    
    # Cross-validation AUC
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    pipeline = lambda: LogisticRegression(max_iter=1000, random_state=42)
    
    # Modelo completo (K2 + Pachy_Min)
    scores_full = cross_val_score(
        pipeline(), X_scaled, y, cv=cv, scoring='roc_auc'
    )
    
    # Modelo apenas K2
    scores_k2 = cross_val_score(
        pipeline(), X_scaled[:, 0:1], y, cv=cv, scoring='roc_auc'
    )
    
    # Modelo apenas Pachy_Min
    scores_pm = cross_val_score(
        pipeline(), X_scaled[:, 1:2], y, cv=cv, scoring='roc_auc'
    )
    
    print(f"\n  AUC (5-fold CV):")
    print(f"    K2 + Pachy_Min:  {scores_full.mean():.3f} ± {scores_full.std():.3f}")
    print(f"    K2 alone:        {scores_k2.mean():.3f} ± {scores_k2.std():.3f}")
    print(f"    Pachy_Min alone: {scores_pm.mean():.3f} ± {scores_pm.std():.3f}")
    
    # --- Interaction term ---
    X_interact = np.column_stack([X_scaled, X_scaled[:, 0] * X_scaled[:, 1]])
    scores_interact = cross_val_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X_interact, y, cv=cv, scoring='roc_auc'
    )
    print(f"    K2 × Pachy (interação): {scores_interact.mean():.3f} ± {scores_interact.std():.3f}")
    
    # --- Random Forest feature importance ---
    all_cols = ['K2', 'Pachy_Min']
    extra_cols = ['K1', 'Astig', 'BAD_D', 'ART_Max']
    for c in extra_cols:
        if c in valid.columns and valid[c].notna().sum() > 50:
            all_cols.append(c)
    
    X_rf = valid[all_cols].values
    valid_mask = ~np.isnan(X_rf).any(axis=1)
    X_rf = X_rf[valid_mask]
    y_rf = y[valid_mask]
    
    rf = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42)
    rf.fit(X_rf, y_rf)
    importances = rf.feature_importances_
    
    print(f"\n  Random Forest Feature Importance:")
    for name, imp in sorted(zip(all_cols, importances), key=lambda x: -x[1]):
        print(f"    {name:15s}: {imp:.4f}")
    
    # --- Plot 1: ROC Curves comparativas ---
    _style_axis(ax1)
    
    # ROC para cada modelo
    models_roc = {
        'K2 + Pachy': (X_scaled, C_ANT, '-'),
        'K2 only': (X_scaled[:, 0:1], C_POST, '--'),
        'Pachy only': (X_scaled[:, 1:2], C_FUNC, ':'),
    }
    
    for name, (X_m, color, ls) in models_roc.items():
        y_scores = np.zeros(len(y))
        for train_idx, test_idx in cv.split(X_m, y):
            model = LogisticRegression(max_iter=1000, random_state=42)
            model.fit(X_m[train_idx], y[train_idx])
            y_scores[test_idx] = model.predict_proba(X_m[test_idx])[:, 1]
        fpr, tpr, _ = roc_curve(y, y_scores)
        auc = roc_auc_score(y, y_scores)
        ax1.plot(fpr, tpr, color=color, linewidth=2, linestyle=ls,
                label=f'{name} (AUC={auc:.3f})')
    
    ax1.plot([0, 1], [0, 1], '--', color=SPINE_COLOR, alpha=0.5)
    ax1.set_xlabel('False Positive Rate')
    ax1.set_ylabel('True Positive Rate')
    ax1.set_title('Eixo 2: ROC — Anterior vs Posterior', fontweight='bold')
    ax1.legend(fontsize=8)
    
    # --- Plot 2: Feature importance bar chart ---
    _style_axis(ax2)
    sorted_idx = np.argsort(importances)[::-1]
    colors = [C_ANT if 'K' in all_cols[i] else C_POST for i in sorted_idx]
    bars = ax2.barh(
        [all_cols[i] for i in sorted_idx],
        [importances[i] for i in sorted_idx],
        color=colors, edgecolor=SPINE_COLOR, alpha=0.8
    )
    ax2.set_xlabel('Importance')
    ax2.set_title('Eixo 2: Feature Importance (RF)', fontweight='bold')
    ax2.invert_yaxis()
    
    return {
        'AUC_full': scores_full.mean(),
        'AUC_K2': scores_k2.mean(),
        'AUC_Pachy': scores_pm.mean(),
        'AUC_interact': scores_interact.mean(),
        'OR_K2': odds_ratios[0],
        'OR_Pachy': odds_ratios[1],
    }


# ============================================================
# EIXO 3: ÓPTICO — Poder Refrativo Gullstrand
# ============================================================

def axis3_optical(df, ax1, ax2):
    """Análise óptica: poder refrativo anterior vs posterior."""
    print("\n" + "=" * 60)
    print("  EIXO 3: ÓPTICO — Poder Refrativo Computado")
    print("=" * 60)
    
    valid = df.dropna(subset=['R_Anterior_mm', 'R_Posterior_mm', 'CT_mm']).copy()
    
    # Filtrar outliers
    for col in ['R_Anterior_mm', 'R_Posterior_mm', 'CT_mm']:
        mean, std = valid[col].mean(), valid[col].std()
        valid = valid[(valid[col] > mean - 3*std) & (valid[col] < mean + 3*std)]
    
    # Constantes refrativas
    n_air = 1.000
    n_cornea = 1.376
    n_aqueous = 1.336
    
    r_ant = valid['R_Anterior_mm'].values
    r_post = valid['R_Posterior_mm'].values
    ct = valid['CT_mm'].values
    
    # Poder refrativo (proporcional, não absoluto, devido distorção)
    # P = (n2 - n1) / R [em metros]
    P_ant = (n_cornea - n_air) / (r_ant / 1000)  # D
    P_post = (n_aqueous - n_cornea) / (r_post / 1000)  # D (negativo)
    
    # Gullstrand total
    P_total = P_ant + P_post - (ct / 1000) / n_cornea * P_ant * P_post
    
    # Contribuição relativa
    contrib_ant = np.abs(P_ant) / (np.abs(P_ant) + np.abs(P_post)) * 100
    contrib_post = np.abs(P_post) / (np.abs(P_ant) + np.abs(P_post)) * 100
    
    print(f"  N válido: {len(valid)}")
    print(f"\n  Poder Anterior (proporcional):")
    print(f"    Mean = {P_ant.mean():.2f} D, Std = {P_ant.std():.2f} D")
    print(f"  Poder Posterior (proporcional):")
    print(f"    Mean = {P_post.mean():.2f} D, Std = {P_post.std():.2f} D")
    print(f"  Poder Total (Gullstrand):")
    print(f"    Mean = {P_total.mean():.2f} D, Std = {P_total.std():.2f} D")
    print(f"\n  Contribuição relativa:")
    print(f"    Anterior: {contrib_ant.mean():.1f}% ± {contrib_ant.std():.1f}%")
    print(f"    Posterior: {contrib_post.mean():.1f}% ± {contrib_post.std():.1f}%")
    
    # Correlação P_ant vs P_post
    r_corr, p_corr = stats.pearsonr(P_ant, P_post)
    print(f"\n  Correlação P_ant vs P_post: r = {r_corr:.4f}, p = {p_corr:.2e}")
    
    # --- Plot 1: Scatter P_ant vs P_post ---
    _style_axis(ax1)
    ax1.scatter(P_ant, P_post, alpha=0.4, s=15, color=C_OPT, edgecolors='none')
    
    # Regressão
    slope, intercept, r_val, p_val, se = stats.linregress(P_ant, P_post)
    x_line = np.linspace(P_ant.min(), P_ant.max(), 100)
    ax1.plot(x_line, slope * x_line + intercept, color=C_ANT, linewidth=2,
             label=f'r={r_corr:.3f}')
    
    ax1.set_xlabel('Poder Anterior (D, proporcional)')
    ax1.set_ylabel('Poder Posterior (D, proporcional)')
    ax1.set_title('Eixo 3: Acoplamento Óptico', fontweight='bold')
    ax1.legend(fontsize=8)
    
    # --- Plot 2: Contribuição relativa (bar) ---
    _style_axis(ax2)
    categories = ['Anterior', 'Posterior']
    means = [contrib_ant.mean(), contrib_post.mean()]
    stds = [contrib_ant.std(), contrib_post.std()]
    bars = ax2.bar(categories, means, yerr=stds, capsize=5,
                   color=[C_ANT, C_POST], edgecolor=SPINE_COLOR, alpha=0.8)
    ax2.set_ylabel('Contribuição (%)')
    ax2.set_title('Eixo 3: Contribuição Refrativa', fontweight='bold')
    ax2.set_ylim(0, 100)
    
    # Anotar Gullstrand teórico
    ax2.axhline(89.3, color=SPINE_COLOR, linestyle=':', alpha=0.5)
    ax2.text(0.5, 91, 'Gullstrand (89.3%)', ha='center', fontsize=7,
             color=SPINE_COLOR, transform=ax2.get_xaxis_transform())
    
    return {
        'P_ant_mean': P_ant.mean(),
        'P_post_mean': P_post.mean(),
        'P_total_mean': P_total.mean(),
        'contrib_ant': contrib_ant.mean(),
        'contrib_post': contrib_post.mean(),
        'correlation': r_corr,
        'p_value': p_corr,
    }


# ============================================================
# EIXO 4: COMÁTICO — Assimetria e Irregularidade
# ============================================================

def axis4_comatic(df, ax1, ax2):
    """Análise comática: assimetria e irregularidade das superfícies."""
    print("\n" + "=" * 60)
    print("  EIXO 4: COMÁTICO — Assimetria e Irregularidade")
    print("=" * 60)
    
    valid = df.dropna(subset=['Irregularity_Ant', 'Irregularity_Post',
                              'Asymmetry_Ant', 'Asymmetry_Post']).copy()
    
    # Filtrar outliers
    for col in ['Irregularity_Ant', 'Irregularity_Post', 'Asymmetry_Ant', 'Asymmetry_Post']:
        mean, std = valid[col].mean(), valid[col].std()
        valid = valid[(valid[col] > mean - 3*std) & (valid[col] < mean + 3*std)]
    
    print(f"  N válido: {len(valid)}")
    
    irreg_ant = valid['Irregularity_Ant'].values
    irreg_post = valid['Irregularity_Post'].values
    asym_ant = valid['Asymmetry_Ant'].values
    asym_post = valid['Asymmetry_Post'].values
    
    # Correlações
    r_irreg, p_irreg = stats.pearsonr(irreg_ant, irreg_post)
    r_asym, p_asym = stats.pearsonr(asym_ant, asym_post)
    
    print(f"\n  Irregularidade:")
    print(f"    Anterior: {irreg_ant.mean():.6f} ± {irreg_ant.std():.6f}")
    print(f"    Posterior: {irreg_post.mean():.6f} ± {irreg_post.std():.6f}")
    print(f"    Correlação: r = {r_irreg:.4f}, p = {p_irreg:.2e}")
    
    print(f"\n  Assimetria (ratio nasal/temporal):")
    print(f"    Anterior: {asym_ant.mean():.4f} ± {asym_ant.std():.4f}")
    print(f"    Posterior: {asym_post.mean():.4f} ± {asym_post.std():.4f}")
    print(f"    Correlação: r = {r_asym:.4f}, p = {p_asym:.2e}")
    
    # Paired t-test: irregularidade anterior vs posterior
    t_irreg, p_paired_irreg = stats.ttest_rel(irreg_ant, irreg_post)
    print(f"\n  T-test pareado (irregularidade ant vs post):")
    print(f"    t = {t_irreg:.4f}, p = {p_paired_irreg:.2e}")
    
    # Wilcoxon (não-paramétrico)
    w_stat, p_wilcox = stats.wilcoxon(irreg_ant, irreg_post)
    print(f"  Wilcoxon: W = {w_stat:.1f}, p = {p_wilcox:.2e}")
    
    # --- Plot 1: Scatter Irregularidade ant vs post ---
    _style_axis(ax1)
    ax1.scatter(irreg_ant, irreg_post, alpha=0.4, s=15, color=C_COMA, edgecolors='none')
    
    # Linha de identidade
    lim_max = max(irreg_ant.max(), irreg_post.max())
    ax1.plot([0, lim_max], [0, lim_max], '--', color=SPINE_COLOR, alpha=0.5, label='x=y')
    
    # Regressão
    slope, intercept, r_val, _, _ = stats.linregress(irreg_ant, irreg_post)
    x_line = np.linspace(irreg_ant.min(), irreg_ant.max(), 100)
    ax1.plot(x_line, slope * x_line + intercept, color=C_ANT, linewidth=2,
             label=f'r={r_irreg:.3f}')
    
    ax1.set_xlabel('Irregularidade Anterior')
    ax1.set_ylabel('Irregularidade Posterior')
    ax1.set_title('Eixo 4: Acoplamento Comático', fontweight='bold')
    ax1.legend(fontsize=8)
    
    # --- Plot 2: Box-plot comparativo ---
    _style_axis(ax2)
    
    bp_data = [asym_ant, asym_post]
    bp = ax2.boxplot(bp_data, labels=['Anterior', 'Posterior'],
                     patch_artist=True, widths=0.5)
    
    colors_bp = [C_ANT, C_POST]
    for patch, color in zip(bp['boxes'], colors_bp):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    for element in ['whiskers', 'caps', 'medians']:
        for item in bp[element]:
            item.set_color(FONT_COLOR)
    for flier in bp['fliers']:
        flier.set(markerfacecolor=SPINE_COLOR, markeredgecolor=SPINE_COLOR, alpha=0.5)
    
    ax2.axhline(1.0, color=SPINE_COLOR, linestyle=':', alpha=0.5, label='Simétrica (1.0)')
    ax2.set_ylabel('Assimetria (N/T ratio)')
    ax2.set_title('Eixo 4: Assimetria NT', fontweight='bold')
    ax2.legend(fontsize=8)
    
    return {
        'irreg_corr': r_irreg, 'irreg_p': p_irreg,
        'asym_corr': r_asym, 'asym_p': p_asym,
        'paired_t_irreg': t_irreg, 'paired_p_irreg': p_paired_irreg,
    }


# ============================================================
# EIXO 5: BIOMECÂNICO — Dados FEM (placeholder - dados do subagente)
# ============================================================

def axis5_biomechanical(ax1, ax2):
    """Análise biomecânica: integração com dados FEM."""
    print("\n" + "=" * 60)
    print("  EIXO 5: BIOMECÂNICO — Acoplamento FEM")
    print("=" * 60)
    
    # Verificar se o script de análise FEM já gerou resultados
    fem_coupling_csv = os.path.join(FEM_DIR, 'ant_post_coupling_results.csv')
    
    if os.path.exists(fem_coupling_csv):
        df_fem = pd.read_csv(fem_coupling_csv, sep=';')
        print(f"  Dados FEM encontrados: {len(df_fem)} modelos")
        
        if 'coupling_apex' in df_fem.columns and 'dz_ant_apex' in df_fem.columns:
            # Plot 1: dZ_ant vs dZ_post at apex
            _style_axis(ax1)
            ax1.scatter(df_fem['dz_ant_apex'], df_fem['dz_post_apex'],
                       alpha=0.7, s=40, color=C_FEM, edgecolors=SPINE_COLOR)
            
            if len(df_fem) > 2:
                r_fem, p_fem = stats.pearsonr(df_fem['dz_ant_apex'], df_fem['dz_post_apex'])
                slope, intercept, _, _, _ = stats.linregress(
                    df_fem['dz_ant_apex'], df_fem['dz_post_apex'])
                x_line = np.linspace(df_fem['dz_ant_apex'].min(), df_fem['dz_ant_apex'].max(), 100)
                ax1.plot(x_line, slope * x_line + intercept, color=C_ANT, linewidth=2,
                        label=f'r={r_fem:.3f}')
                print(f"  Correlação FEM ΔZ_ant vs ΔZ_post: r = {r_fem:.4f}")
            
            ax1.set_xlabel('ΔZ Anterior (µm)')
            ax1.set_ylabel('ΔZ Posterior (µm)')
            ax1.set_title('Eixo 5: Acoplamento FEM', fontweight='bold')
            ax1.legend(fontsize=8)
            
            # Plot 2: Coupling ratio
            if 'coupling_apex' in df_fem.columns:
                _style_axis(ax2)
                coupling = df_fem['coupling_apex'].dropna()
                ax2.hist(coupling, bins=15, color=C_FEM, alpha=0.7, edgecolor=SPINE_COLOR)
                ax2.axvline(coupling.mean(), color=C_ANT, linestyle='--', linewidth=2,
                           label=f'Mean={coupling.mean():.2f}')
                ax2.set_xlabel('Coupling Ratio (ΔZ_ant / ΔZ_post)')
                ax2.set_ylabel('Contagem')
                ax2.set_title('Eixo 5: Ratio de Acoplamento', fontweight='bold')
                ax2.legend(fontsize=8)
        
        return {'status': 'completed', 'N': len(df_fem)}
    
    else:
        print("  [INFO] Dados FEM de acoplamento não encontrados.")
        print("         Execute analyze_ant_post_coupling.py primeiro.")
        
        # Placeholder visual
        for ax in [ax1, ax2]:
            _style_axis(ax)
            ax.text(0.5, 0.5, 'FEM data\npending...', ha='center', va='center',
                    fontsize=14, color=SPINE_COLOR, transform=ax.transAxes)
            ax.set_title('Eixo 5: Biomecânico', fontweight='bold')
        
        return {'status': 'pending'}


# ============================================================
# MAIN — ORQUESTRADOR
# ============================================================

def main():
    print("=" * 70)
    print("  TESTE DE HIPÓTESE: Relação Curvatura Anterior × Posterior")
    print("  Pentacam Scheimpflug — Análise Multi-Eixo")
    print("=" * 70)
    
    data = load_data()
    results = {}
    
    # Verificar dados mínimos
    has_curvature = data['curvature'] is not None and len(data['curvature']) > 10
    has_clinical = data['clinical'] is not None and len(data['clinical']) > 10
    
    if not has_curvature and not has_clinical:
        print("\n[ERRO] Nenhum dado disponível para análise!")
        return
    
    # ---- CRIAR DASHBOARD 5×2 ----
    fig = plt.figure(figsize=(18, 22), facecolor=DARK_BG)
    gs = GridSpec(5, 2, figure=fig, hspace=0.35, wspace=0.3,
                  left=0.07, right=0.95, top=0.95, bottom=0.03)
    
    # Super título
    fig.suptitle('Hipótese: Relação entre Curvatura Anterior e Posterior\n'
                 'Pentacam Scheimpflug — Análise Multi-Eixo',
                 fontsize=16, fontweight='bold', color=FONT_COLOR, y=0.98)
    
    # ---- EIXO 1: ANATÔMICO ----
    if has_curvature:
        ax1_1 = fig.add_subplot(gs[0, 0])
        ax1_2 = fig.add_subplot(gs[0, 1])
        results['axis1'] = axis1_anatomical(data['curvature'], ax1_1, ax1_2)
    
    # ---- EIXO 2: FUNCIONAL ----
    if has_clinical:
        ax2_1 = fig.add_subplot(gs[1, 0])
        ax2_2 = fig.add_subplot(gs[1, 1])
        results['axis2'] = axis2_functional(data['clinical'], ax2_1, ax2_2)
    
    # ---- EIXO 3: ÓPTICO ----
    if has_curvature:
        ax3_1 = fig.add_subplot(gs[2, 0])
        ax3_2 = fig.add_subplot(gs[2, 1])
        results['axis3'] = axis3_optical(data['curvature'], ax3_1, ax3_2)
    
    # ---- EIXO 4: COMÁTICO ----
    if has_curvature:
        ax4_1 = fig.add_subplot(gs[3, 0])
        ax4_2 = fig.add_subplot(gs[3, 1])
        results['axis4'] = axis4_comatic(data['curvature'], ax4_1, ax4_2)
    
    # ---- EIXO 5: BIOMECÂNICO ----
    ax5_1 = fig.add_subplot(gs[4, 0])
    ax5_2 = fig.add_subplot(gs[4, 1])
    results['axis5'] = axis5_biomechanical(ax5_1, ax5_2)
    
    # ---- SALVAR ----
    output_path = os.path.join(OUTPUT_DIR, 'hypothesis_ant_post_dashboard.png')
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n\nDashboard salvo em: {output_path}")
    
    # ---- RESUMO FINAL ----
    print("\n" + "=" * 70)
    print("  RESUMO DOS RESULTADOS")
    print("=" * 70)
    
    if 'axis1' in results:
        r1 = results['axis1']
        # Use log-scale correlation as primary (handles Scheimpflug distortion)
        sig1_log = "***" if r1['log_p'] < 0.001 else "**" if r1['log_p'] < 0.01 else "*" if r1['log_p'] < 0.05 else "ns"
        sig1_sp = "***" if r1['spearman_p'] < 0.001 else "**" if r1['spearman_p'] < 0.01 else "*" if r1['spearman_p'] < 0.05 else "ns"
        print(f"\n  EIXO 1 — ANATÔMICO:")
        print(f"    Pearson r(original) = {r1['pearson_r']:.4f}")
        print(f"    Pearson r(log)      = {r1['log_r']:.4f} ({sig1_log})")
        print(f"    Spearman ρ          = {r1['spearman_rho']:.4f} ({sig1_sp})")
        print(f"    R²(log) = {r1['R2_log']:.4f}")
        print(f"    Ratio mediano = {r1['ratio_median']:.4f}")
        best_p1 = min(r1['log_p'], r1['spearman_p'])
        if best_p1 < 0.05:
            print(f"    → HIPÓTESE SUPORTADA: correlação anatômica significativa")
        else:
            print(f"    → HIPÓTESE NÃO SUPORTADA neste eixo")
    
    if 'axis2' in results:
        r2 = results['axis2']
        print(f"\n  EIXO 2 — FUNCIONAL:")
        print(f"    AUC combinado = {r2['AUC_full']:.3f}")
        print(f"    AUC K2 = {r2['AUC_K2']:.3f} vs AUC Pachy = {r2['AUC_Pachy']:.3f}")
        delta_auc = abs(r2['AUC_full'] - max(r2['AUC_K2'], r2['AUC_Pachy']))
        if delta_auc > 0.02:
            print(f"    → COMPLEMENTARIDADE: modelo conjunto supera individuais em {delta_auc:.3f}")
        print(f"    → Interação K2×Pachy: AUC = {r2['AUC_interact']:.3f}")
    
    if 'axis3' in results:
        r3 = results['axis3']
        sig3 = "***" if r3['p_value'] < 0.001 else "**" if r3['p_value'] < 0.01 else "*" if r3['p_value'] < 0.05 else "ns"
        print(f"\n  EIXO 3 — ÓPTICO:")
        print(f"    Contribuição: Ant {r3['contrib_ant']:.1f}% / Post {r3['contrib_post']:.1f}%")
        print(f"    Correlação P_ant vs P_post: r = {r3['correlation']:.4f} ({sig3})")
    
    if 'axis4' in results:
        r4 = results['axis4']
        sig4i = "***" if r4['irreg_p'] < 0.001 else "**" if r4['irreg_p'] < 0.01 else "*" if r4['irreg_p'] < 0.05 else "ns"
        sig4a = "***" if r4['asym_p'] < 0.001 else "**" if r4['asym_p'] < 0.01 else "*" if r4['asym_p'] < 0.05 else "ns"
        print(f"\n  EIXO 4 — COMÁTICO:")
        print(f"    Irregularidade: r = {r4['irreg_corr']:.4f} ({sig4i})")
        print(f"    Assimetria:     r = {r4['asym_corr']:.4f} ({sig4a})")
    
    if 'axis5' in results:
        print(f"\n  EIXO 5 — BIOMECÂNICO: {results['axis5'].get('status', 'pending')}")
    
    # Decisão global (usa melhor p-value de cada eixo)
    significant_axes = 0
    if 'axis1' in results:
        best_p1 = min(results['axis1']['log_p'], results['axis1']['spearman_p'])
        if best_p1 < 0.05:
            significant_axes += 1
    if 'axis3' in results and results['axis3']['p_value'] < 0.05:
        significant_axes += 1
    if 'axis4' in results and results['axis4']['irreg_p'] < 0.05:
        significant_axes += 1
    if 'axis4' in results and results['axis4']['asym_p'] < 0.05:
        significant_axes += 1
    
    print(f"\n  {'=' * 50}")
    print(f"  CONCLUSÃO: {significant_axes}/4 testes com p < 0.05")
    if significant_axes >= 3:
        print(f"  → FORTE EVIDÊNCIA de relação anterior-posterior")
    elif significant_axes >= 2:
        print(f"  → EVIDÊNCIA MODERADA de relação anterior-posterior")
    elif significant_axes >= 1:
        print(f"  → EVIDÊNCIA FRACA de relação anterior-posterior")
    else:
        print(f"  → SEM EVIDÊNCIA significativa de relação")
    print(f"  {'=' * 50}")


if __name__ == '__main__':
    main()
