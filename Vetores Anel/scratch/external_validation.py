import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
External Validation for Keratoconus Detection Models
=====================================================
Implements three rigorous validation strategies:
  a) Repeated 5x2 CV (Dietterich 1998)
  b) Nested CV (5-outer x 5-inner)
  c) Leave-One-Out Bootstrap (.632+ estimator)

Plus DeLong test for AUC comparison.

Author: ML Training Specialist
Date: 2025-06-05
"""

import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import unicodedata
import re
from collections import defaultdict
from itertools import combinations

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import (
    RepeatedStratifiedKFold, StratifiedKFold, cross_val_predict
)
from sklearn.metrics import roc_auc_score, roc_curve
from scipy import stats

# ============================================================
# 0. UTILITY FUNCTIONS
# ============================================================

PREPOSITIONS = {'de', 'da', 'do', 'dos', 'das', 'e', 'di', 'del'}

def normalize_name(name):
    """Normalize name: remove accents, lowercase, strip."""
    if pd.isna(name):
        return ''
    name = str(name).strip()
    # Unicode normalize
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    return name.lower().strip()

def get_tokens(name):
    """Get significant tokens from a name (exclude prepositions)."""
    name = normalize_name(name)
    tokens = set(re.split(r'\s+', name))
    tokens = tokens - PREPOSITIONS - {'', 'unknown'}
    return tokens

def token_overlap(tokens1, tokens2):
    """Compute fraction of overlapping tokens."""
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1 & tokens2
    min_len = min(len(tokens1), len(tokens2))
    return len(intersection) / min_len if min_len > 0 else 0.0


# ============================================================
# 1. LOAD ALL DATA SOURCES
# ============================================================
print("=" * 70)
print("EXTERNAL VALIDATION: Rigorous Model Assessment")
print("=" * 70)

# --- 1a. Matched clinical pairs ---
pairs_path = r'D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\matched_pairs_FII_Pentacam.csv'
df_pairs = pd.read_csv(pairs_path, sep=';')
print(f"\n[1] Matched pairs: {len(df_pairs)} rows, columns: {list(df_pairs.columns)}")

# --- 1b. Radiomics (GLCM ROI-fixo) ---
radiomics_path = r'D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\pentacam_mass_radiomics.csv'
df_radiomics = pd.read_csv(radiomics_path, sep=';')
print(f"[2] Radiomics: {len(df_radiomics)} rows")

# --- 1c. Epithelial peak detection ---
epi_path = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch\epithelial_peak_detection.csv'
df_epi = pd.read_csv(epi_path, sep=';')
print(f"[3] Epithelial peaks: {len(df_epi)} rows")

# --- 1d. YOLO stroma features ---
yolo_path = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch\yolo_stroma_features.csv'
df_yolo = pd.read_csv(yolo_path, sep=';')
print(f"[4] YOLO stroma: {len(df_yolo)} rows")


# ============================================================
# 2. AGGREGATE PER-FILE FEATURES TO PATIENT-LEVEL (MEDIAN)
# ============================================================

# Radiomics: aggregate by Patient_Name
glcm_cols = ['Entropy', 'Contrast', 'Correlation', 'Energy']
df_radiomics['tokens'] = df_radiomics['Patient_Name'].apply(get_tokens)
# Remove UNKNOWN patients
df_radiomics = df_radiomics[df_radiomics['Patient_Name'].str.upper() != 'UNKNOWN'].copy()
rad_agg = df_radiomics.groupby('Patient_Name')[glcm_cols].median().reset_index()
rad_agg['tokens'] = rad_agg['Patient_Name'].apply(get_tokens)
print(f"\n[Aggregated] Radiomics patients: {len(rad_agg)}")

# YOLO: aggregate by Patient_Name
yolo_feat_cols = ['YOLO_Contrast', 'YOLO_Correlation', 'YOLO_Energy', 
                  'YOLO_Homogeneity', 'YOLO_Entropy', 'YOLO_MeanIntensity', 'YOLO_StdIntensity']
df_yolo = df_yolo[df_yolo['Patient_Name'].str.upper() != 'UNKNOWN'].copy()
df_yolo['tokens'] = df_yolo['Patient_Name'].apply(get_tokens)
yolo_agg = df_yolo.groupby('Patient_Name')[yolo_feat_cols].median().reset_index()
yolo_agg['tokens'] = yolo_agg['Patient_Name'].apply(get_tokens)
print(f"[Aggregated] YOLO patients: {len(yolo_agg)}")


# ============================================================
# 3. BUILD PATIENT-LEVEL CLINICAL DATA FROM PAIRS
# ============================================================

# Each row in pairs has Pentacam clinical data; aggregate by nome_pentacam
clinical_cols = ['BAD_D', 'K1', 'K2', 'Astig', 'ART_Max', 'Pachy_Min', 'Penta_Class']
# Convert numeric columns
for c in ['BAD_D', 'K1', 'K2', 'Astig', 'ART_Max', 'Pachy_Min']:
    df_pairs[c] = pd.to_numeric(df_pairs[c], errors='coerce')

# Create target: BAD_D >= 1.6 OR Penta_Class != 'Normal'
df_pairs['target'] = ((df_pairs['BAD_D'] >= 1.6) | (df_pairs['Penta_Class'] != 'Normal')).astype(int)

# Get unique patients by nome_pentacam
clinical = df_pairs.groupby('nome_pentacam').agg({
    'BAD_D': 'first',
    'K2': 'first',
    'Pachy_Min': 'first',
    'Penta_Class': 'first',
    'target': 'first'
}).reset_index()
clinical['tokens'] = clinical['nome_pentacam'].apply(get_tokens)
print(f"[Clinical] Unique Pentacam patients: {len(clinical)}")
print(f"  Target distribution: {clinical['target'].value_counts().to_dict()}")


# ============================================================
# 4. MATCH DATASETS BY TOKEN OVERLAP (>= 50%)
# ============================================================

def match_to_clinical(df_feat, feat_name, clinical_df, threshold=0.5):
    """Match feature dataframe to clinical by token overlap."""
    matched = []
    used_clinical = set()
    
    for idx, row in df_feat.iterrows():
        best_score = 0
        best_clin_idx = None
        for cidx, crow in clinical_df.iterrows():
            if cidx in used_clinical:
                continue
            score = token_overlap(row['tokens'], crow['tokens'])
            if score > best_score:
                best_score = score
                best_clin_idx = cidx
        if best_score >= threshold and best_clin_idx is not None:
            matched.append((idx, best_clin_idx, best_score))
            used_clinical.add(best_clin_idx)
    
    print(f"  {feat_name}: matched {len(matched)} / {len(df_feat)} patients (threshold={threshold})")
    return matched

print("\n--- Matching datasets ---")
rad_matches = match_to_clinical(rad_agg, "Radiomics", clinical)
yolo_matches = match_to_clinical(yolo_agg, "YOLO", clinical)

# Build merged dataframe
# Start from clinical, merge radiomics and YOLO

# Create lookup: clinical index -> radiomics features
rad_lookup = {}
for ridx, cidx, score in rad_matches:
    rad_lookup[cidx] = ridx

yolo_lookup = {}
for yidx, cidx, score in yolo_matches:
    yolo_lookup[cidx] = yidx

# Build final merged dataset: patients that have ALL sources
rows = []
for cidx, crow in clinical.iterrows():
    row_data = {
        'patient': crow['nome_pentacam'],
        'target': crow['target'],
        'Pachy_Min': crow['Pachy_Min'],
        'K2': crow['K2'],
        'BAD_D': crow['BAD_D'],
        'Penta_Class': crow['Penta_Class'],
    }
    
    # Add radiomics if available
    if cidx in rad_lookup:
        rrow = rad_agg.loc[rad_lookup[cidx]]
        for c in glcm_cols:
            row_data[c] = rrow[c]
        row_data['has_radiomics'] = True
    else:
        row_data['has_radiomics'] = False
    
    # Add YOLO if available
    if cidx in yolo_lookup:
        yrow = yolo_agg.loc[yolo_lookup[cidx]]
        for c in yolo_feat_cols:
            row_data[c] = yrow[c]
        row_data['has_yolo'] = True
    else:
        row_data['has_yolo'] = False
    
    rows.append(row_data)

df_all = pd.DataFrame(rows)
print(f"\n[Merged] Total patients: {len(df_all)}")
print(f"  With radiomics: {df_all['has_radiomics'].sum()}")
print(f"  With YOLO: {df_all['has_yolo'].sum()}")
print(f"  With BOTH: {(df_all['has_radiomics'] & df_all['has_yolo']).sum()}")


# ============================================================
# 5. DEFINE MODELS
# ============================================================

# Model A: GLCM ROI-fixo (4 features)
glcm_features = ['Entropy', 'Contrast', 'Correlation', 'Energy']

# Model B: Posterior (2 features)
posterior_features = ['Pachy_Min', 'K2']

# Model C: Fusionado (13 features: 4 GLCM + 7 YOLO + 2 clinical)
fusionado_features = glcm_features + yolo_feat_cols + ['Pachy_Min', 'K2']

# Datasets for each model
df_glcm = df_all[df_all['has_radiomics']].dropna(subset=glcm_features + ['target']).copy()
df_post = df_all.dropna(subset=posterior_features + ['target']).copy()
df_fusion = df_all[df_all['has_radiomics'] & df_all['has_yolo']].dropna(
    subset=fusionado_features + ['target']).copy()

print(f"\n--- Dataset sizes per model ---")
print(f"  GLCM ROI-fixo:  N={len(df_glcm)}, pos={df_glcm['target'].sum()}")
print(f"  Posterior:       N={len(df_post)}, pos={df_post['target'].sum()}")
print(f"  Fusionado:      N={len(df_fusion)}, pos={df_fusion['target'].sum()}")


# ============================================================
# 6. VALIDATION STRATEGIES
# ============================================================

def make_pipeline():
    """Create LogisticRegression pipeline with StandardScaler."""
    return Pipeline([
        ('scaler', StandardScaler()),
        ('lr', LogisticRegression(max_iter=2000, solver='lbfgs', random_state=42))
    ])

# --- 6a. Repeated 5x2 CV (Dietterich 1998) ---
def repeated_5x2_cv(X, y, n_repeats=5):
    """5 repetitions of 2-fold stratified CV."""
    rskf = RepeatedStratifiedKFold(n_splits=2, n_repeats=n_repeats, random_state=42)
    aucs = []
    fold_predictions = np.zeros(len(y))
    fold_counts = np.zeros(len(y))
    
    for train_idx, test_idx in rskf.split(X, y):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        pipe = make_pipeline()
        pipe.fit(X_train, y_train)
        y_prob = pipe.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_prob)
        aucs.append(auc)
        
        fold_predictions[test_idx] += y_prob
        fold_counts[test_idx] += 1
    
    # Average predictions for ROC
    mask = fold_counts > 0
    fold_predictions[mask] /= fold_counts[mask]
    
    return {
        'mean_auc': np.mean(aucs),
        'std_auc': np.std(aucs),
        'ci_low': np.percentile(aucs, 2.5),
        'ci_high': np.percentile(aucs, 97.5),
        'all_aucs': aucs,
        'avg_proba': fold_predictions,
        'n_folds': len(aucs)
    }


# --- 6b. Nested CV (5-outer x 5-inner) ---
def nested_cv(X, y, n_outer=5, n_inner=5):
    """Nested cross-validation with inner loop for hyperparameter tuning."""
    outer_cv = StratifiedKFold(n_splits=n_outer, shuffle=True, random_state=42)
    
    aucs = []
    all_proba = np.zeros(len(y))
    all_counts = np.zeros(len(y))
    
    C_values = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
    
    for train_idx, test_idx in outer_cv.split(X, y):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        # Inner CV for C selection
        inner_cv = StratifiedKFold(n_splits=n_inner, shuffle=True, random_state=42)
        best_C = 1.0
        best_inner_auc = 0
        
        for C in C_values:
            inner_aucs = []
            for itrain, ival in inner_cv.split(X_train, y_train):
                pipe = Pipeline([
                    ('scaler', StandardScaler()),
                    ('lr', LogisticRegression(C=C, max_iter=2000, solver='lbfgs', random_state=42))
                ])
                pipe.fit(X_train[itrain], y_train[itrain])
                y_val_prob = pipe.predict_proba(X_train[ival])[:, 1]
                try:
                    inner_aucs.append(roc_auc_score(y_train[ival], y_val_prob))
                except ValueError:
                    inner_aucs.append(0.5)
            
            mean_inner = np.mean(inner_aucs)
            if mean_inner > best_inner_auc:
                best_inner_auc = mean_inner
                best_C = C
        
        # Refit with best C on full training fold
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('lr', LogisticRegression(C=best_C, max_iter=2000, solver='lbfgs', random_state=42))
        ])
        pipe.fit(X_train, y_train)
        y_prob = pipe.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_prob)
        aucs.append(auc)
        
        all_proba[test_idx] = y_prob
        all_counts[test_idx] = 1
    
    return {
        'mean_auc': np.mean(aucs),
        'std_auc': np.std(aucs),
        'ci_low': np.percentile(aucs, 2.5),
        'ci_high': np.percentile(aucs, 97.5),
        'all_aucs': aucs,
        'avg_proba': all_proba,
        'n_folds': len(aucs)
    }


# --- 6c. Leave-One-Out Bootstrap (.632+ estimator) ---
def loo_bootstrap_632plus(X, y, n_bootstrap=200):
    """
    .632+ bootstrap estimator (Efron & Tibshirani 1997).
    Less biased than standard bootstrap.
    """
    n = len(y)
    rng = np.random.RandomState(42)
    
    # Training error (apparent / resubstitution)
    pipe = make_pipeline()
    pipe.fit(X, y)
    y_prob_train = pipe.predict_proba(X)[:, 1]
    try:
        err_apparent = 1 - roc_auc_score(y, y_prob_train)
    except ValueError:
        err_apparent = 0.5
    
    # No-information rate
    p1 = np.mean(y)
    p0 = 1 - p1
    gamma = p0 * p1 + p1 * p0  # no-information error rate for AUC ≈ 0.5 equivalence
    # Actually for AUC, no-information rate is 0.5 (random classifier)
    gamma = 0.5  # AUC of random classifier
    
    boot_aucs = []
    oob_predictions = np.zeros(n)
    oob_counts = np.zeros(n)
    
    for b in range(n_bootstrap):
        # Bootstrap sample
        boot_idx = rng.choice(n, size=n, replace=True)
        oob_idx = np.array(list(set(range(n)) - set(boot_idx)))
        
        if len(oob_idx) < 2 or len(np.unique(y[oob_idx])) < 2:
            continue
        
        pipe = make_pipeline()
        pipe.fit(X[boot_idx], y[boot_idx])
        y_oob_prob = pipe.predict_proba(X[oob_idx])[:, 1]
        
        try:
            oob_auc = roc_auc_score(y[oob_idx], y_oob_prob)
            boot_aucs.append(oob_auc)
        except ValueError:
            continue
        
        oob_predictions[oob_idx] += y_oob_prob
        oob_counts[oob_idx] += 1
    
    # .632 estimator
    auc_apparent = 1 - err_apparent
    auc_boot = np.mean(boot_aucs)
    auc_632 = 0.368 * auc_apparent + 0.632 * auc_boot
    
    # .632+ adjustment
    # R = relative overfitting rate
    err_boot = 1 - auc_boot
    err_632 = 1 - auc_632
    no_info_err = 1 - gamma  # = 0.5
    
    if err_boot > err_apparent and no_info_err > err_apparent:
        R = (err_boot - err_apparent) / (no_info_err - err_apparent)
        R = min(R, 1.0)
    else:
        R = 0.0
    
    w = 0.632 / (1 - 0.368 * R)
    w = min(w, 1.0)
    
    auc_632plus = (1 - w) * auc_apparent + w * auc_boot
    
    # Average OOB predictions
    mask = oob_counts > 0
    oob_predictions[mask] /= oob_counts[mask]
    
    return {
        'mean_auc': auc_632plus,
        'std_auc': np.std(boot_aucs),
        'ci_low': np.percentile(boot_aucs, 2.5),
        'ci_high': np.percentile(boot_aucs, 97.5),
        'auc_apparent': auc_apparent,
        'auc_boot_mean': auc_boot,
        'auc_632': auc_632,
        'auc_632plus': auc_632plus,
        'all_aucs': boot_aucs,
        'avg_proba': oob_predictions,
        'n_folds': len(boot_aucs)
    }


# ============================================================
# 7. DeLong Test for comparing AUCs
# ============================================================

def compute_midrank(x):
    """Compute midranks."""
    J = np.argsort(x)
    Z = x[J]
    N = len(x)
    T = np.zeros(N, dtype=float)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        for k in range(i, j):
            T[k] = 0.5 * (i + 1 + j)
        i = j
    T2 = np.empty(N, dtype=float)
    T2[J] = T
    return T2

def delong_roc_variance(ground_truth, predictions):
    """Compute DeLong variance for a single AUC."""
    order = np.argsort(-predictions)
    label_ordered = ground_truth[order]
    pred_ordered = predictions[order]
    
    m = np.sum(label_ordered == 1)
    n = np.sum(label_ordered == 0)
    
    positive_examples = pred_ordered[label_ordered == 1]
    negative_examples = pred_ordered[label_ordered == 0]
    
    # Structural components
    k = len(positive_examples)
    l = len(negative_examples)
    
    # Placements
    tx = np.zeros(k)
    ty = np.zeros(l)
    
    for i in range(k):
        tx[i] = np.sum(negative_examples < positive_examples[i]) + \
                0.5 * np.sum(negative_examples == positive_examples[i])
    
    for j in range(l):
        ty[j] = np.sum(positive_examples > negative_examples[j]) + \
                0.5 * np.sum(positive_examples == negative_examples[j])
    
    tx /= l
    ty /= k
    
    auc = np.mean(tx)
    
    sx = np.var(tx, ddof=1) if k > 1 else 0
    sy = np.var(ty, ddof=1) if l > 1 else 0
    
    var_auc = sx / k + sy / l
    
    return auc, var_auc

def delong_test(y_true, y_pred1, y_pred2):
    """
    DeLong test comparing two AUCs from correlated samples.
    Returns z-statistic and p-value.
    """
    y_true = np.asarray(y_true, dtype=int)
    y_pred1 = np.asarray(y_pred1, dtype=float)
    y_pred2 = np.asarray(y_pred2, dtype=float)
    
    auc1, var1 = delong_roc_variance(y_true, y_pred1)
    auc2, var2 = delong_roc_variance(y_true, y_pred2)
    
    # Covariance estimation
    m = np.sum(y_true == 1)
    n = np.sum(y_true == 0)
    
    pos_idx = y_true == 1
    neg_idx = y_true == 0
    
    pred1_pos = y_pred1[pos_idx]
    pred1_neg = y_pred1[neg_idx]
    pred2_pos = y_pred2[pos_idx]
    pred2_neg = y_pred2[neg_idx]
    
    # Placements for model 1
    v10 = np.zeros(m)
    v01_1 = np.zeros(n)
    for i in range(m):
        v10[i] = np.mean(pred1_neg < pred1_pos[i]) + 0.5 * np.mean(pred1_neg == pred1_pos[i])
    for j in range(n):
        v01_1[j] = np.mean(pred1_pos > pred1_neg[j]) + 0.5 * np.mean(pred1_pos == pred1_neg[j])
    
    # Placements for model 2
    v20 = np.zeros(m)
    v01_2 = np.zeros(n)
    for i in range(m):
        v20[i] = np.mean(pred2_neg < pred2_pos[i]) + 0.5 * np.mean(pred2_neg == pred2_pos[i])
    for j in range(n):
        v01_2[j] = np.mean(pred2_pos > pred2_neg[j]) + 0.5 * np.mean(pred2_pos == pred2_neg[j])
    
    # Covariance
    cov_10 = np.cov(v10, v20)[0, 1] if m > 1 else 0
    cov_01 = np.cov(v01_1, v01_2)[0, 1] if n > 1 else 0
    
    cov_auc = cov_10 / m + cov_01 / n
    
    var_diff = var1 + var2 - 2 * cov_auc
    
    if var_diff <= 0:
        return auc1, auc2, 0, 1.0
    
    z = (auc1 - auc2) / np.sqrt(var_diff)
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    return auc1, auc2, z, p_value


# ============================================================
# 8. RUN ALL VALIDATIONS
# ============================================================

models = {
    'GLCM_ROI_fixo': (df_glcm, glcm_features),
    'Posterior': (df_post, posterior_features),
    'Fusionado': (df_fusion, fusionado_features),
}

strategies = {
    'Repeated_5x2_CV': repeated_5x2_cv,
    'Nested_5x5_CV': nested_cv,
    'Bootstrap_632plus': loo_bootstrap_632plus,
}

results = {}
all_probas = {}  # Store predictions for DeLong test

print("\n" + "=" * 70)
print("RUNNING VALIDATION STRATEGIES")
print("=" * 70)

for model_name, (df_model, features) in models.items():
    print(f"\n{'-' * 50}")
    print(f"Model: {model_name} ({len(features)} features, N={len(df_model)})")
    print(f"  Features: {features}")
    print(f"  Prevalence: {df_model['target'].mean():.1%}")
    print(f"{'-' * 50}")
    
    X = df_model[features].values.astype(float)
    y = df_model['target'].values.astype(int)
    
    for strat_name, strat_func in strategies.items():
        print(f"  Running {strat_name}...", end=' ', flush=True)
        
        try:
            res = strat_func(X, y)
            results[(model_name, strat_name)] = res
            
            key = f"{model_name}_{strat_name}"
            all_probas[key] = {
                'y_true': y.copy(),
                'y_proba': res['avg_proba'].copy(),
                'indices': df_model.index.values.copy()
            }
            
            if strat_name == 'Bootstrap_632plus':
                print(f"AUC={res['auc_632plus']:.4f} "
                      f"(apparent={res['auc_apparent']:.4f}, "
                      f"boot={res['auc_boot_mean']:.4f}, "
                      f".632={res['auc_632']:.4f})")
            else:
                print(f"AUC={res['mean_auc']:.4f} +/- {res['std_auc']:.4f} "
                      f"[{res['ci_low']:.4f}, {res['ci_high']:.4f}]")
        except Exception as e:
            print(f"FAILED: {e}")
            results[(model_name, strat_name)] = None


# ============================================================
# 9. DELONG TESTS
# ============================================================

print("\n" + "=" * 70)
print("DeLong TESTS: Pairwise AUC Comparisons")
print("=" * 70)

# For DeLong, we need predictions on the same patients
# Use Nested CV predictions (most rigorous) on the intersection of patients

# We'll compute DeLong on the Nested CV strategy
delong_results = []
strat_for_delong = 'Nested_5x5_CV'

model_names = list(models.keys())
for i in range(len(model_names)):
    for j in range(i+1, len(model_names)):
        m1, m2 = model_names[i], model_names[j]
        key1 = f"{m1}_{strat_for_delong}"
        key2 = f"{m2}_{strat_for_delong}"
        
        if key1 not in all_probas or key2 not in all_probas:
            continue
        
        # Find common patients by index
        idx1 = set(all_probas[key1]['indices'])
        idx2 = set(all_probas[key2]['indices'])
        common = sorted(idx1 & idx2)
        
        if len(common) < 10:
            print(f"  {m1} vs {m2}: Not enough common patients ({len(common)})")
            continue
        
        # Map to positions
        pos1 = [np.where(all_probas[key1]['indices'] == c)[0][0] for c in common]
        pos2 = [np.where(all_probas[key2]['indices'] == c)[0][0] for c in common]
        
        y_true = all_probas[key1]['y_true'][pos1]
        y_pred1 = all_probas[key1]['y_proba'][pos1]
        y_pred2 = all_probas[key2]['y_proba'][pos2]
        
        # Check y_true consistency
        y_true2 = all_probas[key2]['y_true'][pos2]
        assert np.array_equal(y_true, y_true2), "Target mismatch!"
        
        auc1, auc2, z, p = delong_test(y_true, y_pred1, y_pred2)
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
        
        delong_results.append({
            'Model_1': m1, 'Model_2': m2,
            'AUC_1': auc1, 'AUC_2': auc2,
            'Z_stat': z, 'P_value': p,
            'Significant': sig,
            'N_common': len(common)
        })
        
        print(f"  {m1} (AUC={auc1:.4f}) vs {m2} (AUC={auc2:.4f}): "
              f"z={z:.3f}, p={p:.4f} {sig}")


# ============================================================
# 10. COMPREHENSIVE RESULTS TABLE
# ============================================================

print("\n" + "=" * 70)
print("COMPREHENSIVE RESULTS TABLE")
print("=" * 70)

result_rows = []
for model_name in model_names:
    for strat_name in strategies.keys():
        res = results.get((model_name, strat_name))
        if res is None:
            continue
        
        n_feat = len(models[model_name][1])
        n_samples = len(models[model_name][0])
        
        row = {
            'Model': model_name,
            'N_Features': n_feat,
            'N_Samples': n_samples,
            'Strategy': strat_name,
            'AUC_Mean': res['mean_auc'],
            'AUC_Std': res['std_auc'],
            'AUC_CI_Low': res['ci_low'],
            'AUC_CI_High': res['ci_high'],
            'N_Folds': res['n_folds'],
        }
        
        if strat_name == 'Bootstrap_632plus':
            row['AUC_Apparent'] = res['auc_apparent']
            row['AUC_Boot'] = res['auc_boot_mean']
            row['AUC_632'] = res['auc_632']
            row['AUC_632plus'] = res['auc_632plus']
        
        result_rows.append(row)

df_results = pd.DataFrame(result_rows)

# Print formatted table
print(f"\n{'Model':<18} {'Strategy':<22} {'N':>5} {'Feat':>5} {'AUC':>7} {'+/-Std':>7} {'95% CI':>17}")
print("-" * 85)
for _, r in df_results.iterrows():
    ci_str = f"[{r['AUC_CI_Low']:.3f}, {r['AUC_CI_High']:.3f}]"
    print(f"{r['Model']:<18} {r['Strategy']:<22} {r['N_Samples']:>5} {r['N_Features']:>5} "
          f"{r['AUC_Mean']:>7.4f} {r['AUC_Std']:>7.4f} {ci_str:>17}")

# ============================================================
# 11. COMPARISON WITH ORIGINAL 0.863
# ============================================================

print("\n" + "=" * 70)
print("COMPARISON WITH PREVIOUSLY REPORTED AUC = 0.863")
print("=" * 70)

for model_name in model_names:
    print(f"\n  {model_name}:")
    for strat_name in strategies.keys():
        res = results.get((model_name, strat_name))
        if res is None:
            continue
        auc = res['mean_auc']
        diff = auc - 0.863
        direction = "UP" if diff > 0 else "DOWN"
        print(f"    {strat_name:<22}: AUC={auc:.4f}  ({direction} {abs(diff):.4f} vs 0.863)")

# ============================================================
# 12. SAVE RESULTS
# ============================================================

out_dir = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch'

# Save main results
df_results.to_csv(f'{out_dir}\\external_validation_results.csv', index=False, sep=';')
print(f"\n[Saved] Results -> {out_dir}\\external_validation_results.csv")

# Save DeLong results
if delong_results:
    df_delong = pd.DataFrame(delong_results)
    df_delong.to_csv(f'{out_dir}\\delong_test_results.csv', index=False, sep=';')
    print(f"[Saved] DeLong  -> {out_dir}\\delong_test_results.csv")

# ============================================================
# 13. PLOT ROC CURVES
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for ax_idx, strat_name in enumerate(strategies.keys()):
    ax = axes[ax_idx]
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='Random (AUC=0.5)')
    
    for model_name, color in zip(model_names, ['#2196F3', '#FF9800', '#4CAF50']):
        key = f"{model_name}_{strat_name}"
        if key not in all_probas:
            continue
        
        res = results.get((model_name, strat_name))
        if res is None:
            continue
        
        y_true = all_probas[key]['y_true']
        y_proba = all_probas[key]['y_proba']
        
        # Only plot where we have predictions
        mask = y_proba > 0
        if mask.sum() < 10:
            continue
            
        fpr, tpr, _ = roc_curve(y_true[mask], y_proba[mask])
        auc_val = res['mean_auc']
        
        label = f"{model_name} (AUC={auc_val:.3f})"
        ax.plot(fpr, tpr, color=color, linewidth=2, label=label)
    
    ax.set_xlabel('False Positive Rate', fontsize=11)
    ax.set_ylabel('True Positive Rate', fontsize=11)
    ax.set_title(strat_name.replace('_', ' '), fontsize=13, fontweight='bold')
    ax.legend(loc='lower right', fontsize=9)
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylim([-0.02, 1.02])
    ax.grid(True, alpha=0.3)

plt.suptitle('ROC Curves: Three Validation Strategies', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{out_dir}\\external_validation_roc.png', dpi=150, bbox_inches='tight')
print(f"[Saved] ROC plot -> {out_dir}\\external_validation_roc.png")

# ============================================================
# 14. SUMMARY BOX PLOT
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

positions = []
labels = []
data_to_plot = []
colors_list = []
pos_counter = 0

strategy_colors = {'Repeated_5x2_CV': '#2196F3', 'Nested_5x5_CV': '#FF9800', 'Bootstrap_632plus': '#4CAF50'}

for model_name in model_names:
    for strat_name in strategies.keys():
        res = results.get((model_name, strat_name))
        if res is None:
            continue
        data_to_plot.append(res['all_aucs'])
        positions.append(pos_counter)
        labels.append(f"{model_name}\n{strat_name.replace('_', ' ')}")
        colors_list.append(strategy_colors[strat_name])
        pos_counter += 1
    pos_counter += 0.5  # gap between models

bp = ax.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)

for patch, color in zip(bp['boxes'], colors_list):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

ax.axhline(y=0.863, color='red', linestyle='--', linewidth=1.5, label='Previous: AUC=0.863')
ax.axhline(y=0.5, color='gray', linestyle=':', linewidth=1, alpha=0.5)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=7, rotation=45, ha='right')
ax.set_ylabel('AUC', fontsize=12)
ax.set_title('AUC Distribution Across Validation Strategies', fontsize=14, fontweight='bold')
ax.legend(loc='lower left')
ax.grid(True, axis='y', alpha=0.3)
ax.set_ylim([0.3, 1.05])

plt.tight_layout()
plt.savefig(f'{out_dir}\\external_validation_boxplot.png', dpi=150, bbox_inches='tight')
print(f"[Saved] Boxplot -> {out_dir}\\external_validation_boxplot.png")


# ============================================================
# 15. FINAL VERDICT
# ============================================================

print("\n" + "=" * 70)
print("FINAL VERDICT")
print("=" * 70)

# Get best rigorous AUC (from nested CV)
for model_name in model_names:
    res_nested = results.get((model_name, 'Nested_5x5_CV'))
    if res_nested:
        auc = res_nested['mean_auc']
        holds = "YES" if auc >= 0.85 else "NO"
        print(f"  {model_name:<18}: Nested CV AUC = {auc:.4f}  |  Holds up to 0.863? {holds}")

print("\n[INTERPRETATION]")
print("  - If Nested CV AUC approx 0.863: the estimate was unbiased, publishable")
print("  - If Nested CV AUC < 0.85: some optimistic bias in original 10-fold CV")
print("  - If .632+ AUC matches Nested CV: both estimators agree (strong evidence)")
print("  - DeLong p < 0.05: statistically significant difference between models")

print("\n" + "=" * 70)
print("DONE. All results saved to scratch directory.")
print("=" * 70)
