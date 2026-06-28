"""
Avaliação INTELIGENTE do YOLOv11-seg:
- Usa a máscara do ESTROMA (AP50=0.925) para extrair features radiômicas GLCM
  regionalizadas (temporal vs. central)
- A segmentação precisa do estroma permite isolar a textura estromal
  sem incluir epitélio/endotélio/fundo — mais limpo que o ROI fixo anterior
- Compara AUC: GLCM-ROI-fixo vs. GLCM-YOLO-estroma vs. fusionado
"""
import numpy as np
import os
import glob
import pandas as pd
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import unicodedata, re
import warnings
warnings.filterwarnings('ignore')

DATASET_DIR = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\yolo_cornea_dataset'
SCRATCH_DIR = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch'

# ============================================================
# 1. CARREGAR MODELO
# ============================================================
from ultralytics import YOLO

best_model = None
for d in sorted(glob.glob(os.path.join(DATASET_DIR, 'runs', 'cornea_seg*'))):
    candidate = os.path.join(d, 'weights', 'best.pt')
    if os.path.exists(candidate):
        best_model = candidate

if best_model is None:
    print("ERRO: Modelo não encontrado!")
    exit(1)

print(f"Modelo: {best_model}")
model = YOLO(best_model)

# ============================================================
# 2. INFERÊNCIA: Extrair features estromais via máscara YOLO
# ============================================================
SPR_DIR = r'D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP'
WIDTH, HEIGHT, OFFSET, PPS = 416, 256, 2048, 416*256

spr_files = sorted(glob.glob(os.path.join(SPR_DIR, '*.SPR')))
print(f"Processando {len(spr_files)} SPR...")

results = []

for fi, fpath in enumerate(spr_files):
    fname = os.path.basename(fpath).replace('.SPR', '')
    
    try:
        with open(fpath, 'rb') as f:
            raw = f.read()
        
        header = raw[:100]
        chunks = [c.decode('ascii', errors='ignore').strip() for c in header.split(b'\x00')]
        valid_chunks = [c for c in chunks if len(c) > 2 and c.replace(' ', '').isalpha()]
        patient_name = " ".join(valid_chunks[:2]) if len(valid_chunks) >= 2 else "UNKNOWN"
        
        arr = np.frombuffer(raw[OFFSET:], dtype=np.uint8)
        nslices = len(arr) // PPS
        
        # Acumular features de todas as fatias
        slice_features = []
        
        for si in range(nslices):
            s = arr[si*PPS:(si+1)*PPS].reshape((HEIGHT, WIDTH))
            if np.mean(s) < 10:
                continue
            
            img_rgb = np.stack([s, s, s], axis=2)
            preds = model.predict(img_rgb, verbose=False, conf=0.25)
            
            if len(preds) == 0 or preds[0].masks is None:
                continue
            
            masks = preds[0].masks.data.cpu().numpy()
            classes = preds[0].boxes.cls.cpu().numpy()
            
            # Encontrar máscara do estroma (classe 1)
            stroma_mask = None
            for mi, cls in enumerate(classes):
                if int(cls) == 1:
                    stroma_mask = masks[mi]
                    break
            
            if stroma_mask is None:
                continue
            
            # Redimensionar máscara
            from skimage.transform import resize
            mask_full = (resize(stroma_mask, (HEIGHT, WIDTH), order=0) > 0.5).astype(np.uint8)
            
            # Extrair ROI estromal TEMPORAL (colunas 100-200)
            temporal_mask = mask_full.copy()
            temporal_mask[:, :100] = 0
            temporal_mask[:, 200:] = 0
            
            # Extrair pixels estromais na região temporal
            stroma_pixels_t = s[temporal_mask > 0]
            
            if len(stroma_pixels_t) < 100:
                continue
            
            # Criar sub-imagem para GLCM (pegar o bounding box da máscara temporal)
            rows = np.any(temporal_mask, axis=1)
            cols = np.any(temporal_mask, axis=0)
            if not np.any(rows) or not np.any(cols):
                continue
            rmin, rmax = np.where(rows)[0][[0, -1]]
            cmin, cmax = np.where(cols)[0][[0, -1]]
            
            roi = s[rmin:rmax+1, cmin:cmax+1]
            roi_mask = temporal_mask[rmin:rmax+1, cmin:cmax+1]
            
            # Aplicar máscara (pixels fora do estroma = 0)
            roi_masked = roi * roi_mask
            
            if roi_masked.shape[0] < 5 or roi_masked.shape[1] < 5:
                continue
            
            # GLCM na ROI mascarada
            try:
                glcm = graycomatrix(roi_masked, distances=[1], 
                                   angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
                                   levels=256, symmetric=True, normed=True)
                
                contrast = np.mean(graycoprops(glcm, 'contrast'))
                correlation = np.mean(graycoprops(glcm, 'correlation'))
                energy = np.mean(graycoprops(glcm, 'energy'))
                homogeneity = np.mean(graycoprops(glcm, 'homogeneity'))
                entropy = shannon_entropy(roi_masked[roi_mask > 0])
                
                # Feature adicional: intensidade média estromal (proxy de densidade)
                mean_intensity = np.mean(stroma_pixels_t)
                std_intensity = np.std(stroma_pixels_t)
                
                slice_features.append({
                    'contrast': contrast,
                    'correlation': correlation,
                    'energy': energy,
                    'homogeneity': homogeneity,
                    'entropy': entropy,
                    'mean_intensity': mean_intensity,
                    'std_intensity': std_intensity
                })
            except:
                continue
        
        if slice_features:
            # Média de todas as fatias
            feat_df = pd.DataFrame(slice_features)
            results.append({
                'File': fname + '.SPR',
                'Patient_Name': patient_name,
                'YOLO_Contrast': feat_df['contrast'].mean(),
                'YOLO_Correlation': feat_df['correlation'].mean(),
                'YOLO_Energy': feat_df['energy'].mean(),
                'YOLO_Homogeneity': feat_df['homogeneity'].mean(),
                'YOLO_Entropy': feat_df['entropy'].mean(),
                'YOLO_MeanIntensity': feat_df['mean_intensity'].mean(),
                'YOLO_StdIntensity': feat_df['std_intensity'].mean(),
                'YOLO_N_Slices': len(slice_features)
            })
    
    except Exception as e:
        pass
    
    if (fi + 1) % 50 == 0:
        print(f"  [{fi+1}/{len(spr_files)}] — {len(results)} com features")

yolo_csv = os.path.join(SCRATCH_DIR, 'yolo_stroma_features.csv')
yolo_df = pd.DataFrame(results)
yolo_df.to_csv(yolo_csv, sep=';', index=False)
print(f"\nYOLO estroma features: {len(yolo_df)} pacientes")

# ============================================================
# 3. PAREAR E CALCULAR AUC
# ============================================================
def norm(name):
    if not isinstance(name, str): return ""
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-z ]', '', s.lower()).strip()
    return s

def get_tokens(name):
    skip = {'de','da','do','dos','das','e','di','del'}
    return frozenset(set(norm(name).split()) - skip - {''})

matched = pd.read_csv(r'D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\matched_pairs_FII_Pentacam.csv', sep=';')
radiomics_old = pd.read_csv(r'D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\pentacam_mass_radiomics.csv', sep=';')

# Merge by File
merged = radiomics_old.merge(yolo_df, on='File', how='left', suffixes=('_old', '_yolo'))

matched['tokens'] = matched['nome_pentacam'].apply(get_tokens)
merged['tokens'] = merged['Patient_Name_old'].apply(get_tokens)

paired = []
for _, m in matched.iterrows():
    m_tok = m['tokens']
    if len(m_tok) < 1: continue
    best, best_s = None, 0
    for _, r in merged.iterrows():
        r_tok = r['tokens']
        ov = m_tok & r_tok
        sc = len(ov) / max(1, min(len(m_tok), len(r_tok)))
        if sc > best_s and sc >= 0.5:
            best_s = sc; best = r
    if best is not None:
        paired.append({
            'BAD_D': m['BAD_D'], 'Pachy_Min': m['Pachy_Min'], 'K2': m['K2'],
            'Penta_Class': m['Penta_Class'],
            # Old radiomics (ROI fixo)
            'Old_Entropy': best['Entropy'], 'Old_Contrast': best['Contrast'],
            'Old_Correlation': best['Correlation'], 'Old_Energy': best['Energy'],
            # YOLO-guided radiomics
            'YOLO_Contrast': best.get('YOLO_Contrast', np.nan),
            'YOLO_Correlation': best.get('YOLO_Correlation', np.nan),
            'YOLO_Energy': best.get('YOLO_Energy', np.nan),
            'YOLO_Homogeneity': best.get('YOLO_Homogeneity', np.nan),
            'YOLO_Entropy': best.get('YOLO_Entropy', np.nan),
            'YOLO_MeanIntensity': best.get('YOLO_MeanIntensity', np.nan),
            'YOLO_StdIntensity': best.get('YOLO_StdIntensity', np.nan),
        })

df = pd.DataFrame(paired)
df['target'] = ((df['BAD_D'] >= 1.6) | (df['Penta_Class'] != 'Normal')).astype(int)

print(f"\nPareados: {len(df)}")
print(f"  Com YOLO features: {df['YOLO_Entropy'].notna().sum()}")
print(f"  Target: {df['target'].value_counts().to_dict()}")

# AUC
def compute_auc(X_cols, y, name):
    valid = df[X_cols].notna().all(axis=1)
    X = df.loc[valid, X_cols].values
    yc = y[valid].values
    if len(np.unique(yc)) < 2 or len(yc) < 20:
        print(f"  {name}: Insuficiente"); return None, None
    pipe = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(max_iter=1000))])
    cv = StratifiedKFold(n_splits=min(10, min(np.bincount(yc))), shuffle=True, random_state=42)
    yp = cross_val_predict(pipe, X, yc, cv=cv, method='predict_proba')[:,1]
    auc = roc_auc_score(yc, yp)
    bs = []
    rng = np.random.RandomState(42)
    for _ in range(1000):
        idx = rng.choice(len(yc), len(yc), replace=True)
        if len(np.unique(yc[idx])) < 2: continue
        bs.append(roc_auc_score(yc[idx], yp[idx]))
    ci = (np.percentile(bs, 2.5), np.percentile(bs, 97.5))
    print(f"  {name}: AUC = {auc:.3f} (IC: {ci[0]:.3f}-{ci[1]:.3f}) [n={len(yc)}]")
    return auc, (yc, yp)

print("\n" + "="*60)
print("  AUC COMPARATIVO (10-fold CV)")
print("="*60 + "\n")

auc_old, d_old = compute_auc(['Old_Entropy','Old_Contrast','Old_Correlation','Old_Energy'], df['target'], "GLCM ROI-Fixo (método antigo)")
auc_yolo, d_yolo = compute_auc(['YOLO_Contrast','YOLO_Correlation','YOLO_Energy','YOLO_Homogeneity','YOLO_Entropy','YOLO_MeanIntensity','YOLO_StdIntensity'], df['target'], "GLCM YOLO-Estroma (7 feat)")
auc_post, d_post = compute_auc(['Pachy_Min','K2'], df['target'], "Posterior (Pachy+K2)")

# Fusionado YOLO + Posterior
fusion_yolo = ['YOLO_Contrast','YOLO_Correlation','YOLO_Energy','YOLO_Homogeneity','YOLO_Entropy','YOLO_MeanIntensity','YOLO_StdIntensity','Pachy_Min','K2']
auc_fy, d_fy = compute_auc(fusion_yolo, df['target'], "FUSIONADO YOLO+Posterior (9 feat)")

# Fusionado ALL
all_cols = ['Old_Entropy','Old_Contrast','Old_Correlation','Old_Energy','YOLO_Contrast','YOLO_Correlation','YOLO_Energy','YOLO_Homogeneity','YOLO_Entropy','YOLO_MeanIntensity','YOLO_StdIntensity','Pachy_Min','K2']
auc_all, d_all = compute_auc(all_cols, df['target'], "FUSIONADO TOTAL (13 feat)")

# ============================================================
# 4. ROC PLOT
# ============================================================
fig, ax = plt.subplots(figsize=(9, 7))
for data, label, color, lw in [
    (d_old, f'GLCM ROI-Fixo (AUC={auc_old:.3f})' if auc_old else None, '#e74c3c', 1.5),
    (d_yolo, f'GLCM YOLO-Estroma (AUC={auc_yolo:.3f})' if auc_yolo else None, '#3498db', 2),
    (d_post, f'Posterior Pachy+K2 (AUC={auc_post:.3f})' if auc_post else None, '#2ecc71', 1.5),
    (d_fy, f'Fusionado YOLO+Post (AUC={auc_fy:.3f})' if auc_fy else None, '#f39c12', 3),
    (d_all, f'Fusionado TOTAL (AUC={auc_all:.3f})' if auc_all else None, '#9b59b6', 2),
]:
    if data and label:
        fpr, tpr, _ = roc_curve(data[0], data[1])
        ax.plot(fpr, tpr, color=color, linewidth=lw, label=label)

ax.plot([0,1],[0,1],'k--',alpha=0.3)
ax.set_xlabel('1 - Especificidade', fontsize=13)
ax.set_ylabel('Sensibilidade', fontsize=13)
ax.set_title('ROC: GLCM ROI-Fixo vs. GLCM YOLO-Guiado vs. Fusionado\n(10-fold CV, Pentacam Standard — Região Temporal)', fontsize=12, fontweight='bold')
ax.legend(loc='lower right', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 1]); ax.set_ylim([0, 1.02])
roc_path = os.path.join(SCRATCH_DIR, 'ROC_yolo_stroma_final.png')
plt.tight_layout()
plt.savefig(roc_path, dpi=300, bbox_inches='tight')
print(f"\nROC salvo: {roc_path}")
print("\nConcluído!")
