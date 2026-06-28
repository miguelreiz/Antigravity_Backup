import os
import glob
import numpy as np
import pandas as pd
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy
from sklearn.metrics import roc_auc_score, roc_curve
import unicodedata
import re
import warnings

warnings.filterwarnings('ignore')

spr_dir = r'D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP'
matched_csv = r"D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\matched_pairs_FII_Pentacam.csv"

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

print("1. Processando arquivos SPR em massa (Análise 360º de todas as fatias)...")
spr_files = glob.glob(os.path.join(spr_dir, "*.SPR"))

width = 416
slice_height = 256
pixels_per_slice = width * slice_height
offset = 2048

results = []

count = 0
for file_path in spr_files:
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            
        header = raw_data[:100]
        chunks = [c.decode('ascii', errors='ignore').strip() for c in header.split(b'\x00')]
        valid_chunks = [c for c in chunks if len(c) > 2 and c.replace(' ', '').isalpha()]
        patient_name = " ".join(valid_chunks[:2]) if len(valid_chunks) >= 2 else "UNKNOWN"
        
        img_data = raw_data[offset:]
        arr = np.frombuffer(img_data, dtype=np.uint8)
        num_slices = len(arr) // pixels_per_slice
        if num_slices < 10:
            continue
            
        valid_slices = []
        for i in range(num_slices):
            s = arr[i*pixels_per_slice : (i+1)*pixels_per_slice].reshape((slice_height, width))
            if np.mean(s) > 10:
                valid_slices.append(s)
                
        if len(valid_slices) > 0:
            # Process ALL slices for this patient
            slice_entropies = []
            slice_contrasts = []
            
            for slice_img in valid_slices:
                center_cols = slice_img[:, 180:230]
                row_means = np.mean(center_cols, axis=1)
                apex_row = np.argmax(row_means)
                
                roi_top = apex_row + 15
                roi_bottom = roi_top + 40
                roi_left = 180
                roi_right = 230
                
                roi_img = slice_img[roi_top:roi_bottom, roi_left:roi_right]
                
                if roi_img.size == (40 * 50):
                    glcm = graycomatrix(roi_img, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
                    contrast = np.mean(graycoprops(glcm, 'contrast'))
                    entropy_val = shannon_entropy(roi_img)
                    
                    slice_entropies.append(entropy_val)
                    slice_contrasts.append(contrast)
            
            if len(slice_entropies) > 0:
                results.append({
                    'File': os.path.basename(file_path),
                    'Patient_Name': patient_name,
                    'Entropy_Mean': np.mean(slice_entropies),
                    'Entropy_Max': np.max(slice_entropies),
                    'Entropy_Std': np.std(slice_entropies), # Asymmetry
                    'Contrast_Mean': np.mean(slice_contrasts),
                    'Contrast_Max': np.max(slice_contrasts),
                    'Contrast_Std': np.std(slice_contrasts) # Asymmetry
                })
        
        count += 1
        if count % 100 == 0:
            print(f"  {count}/{len(spr_files)}...")
            
    except Exception as e:
        continue

rad_df = pd.DataFrame(results)
print(f"Radiômica 360º extraída para {len(rad_df)} pacientes.")

print("\n2. Pareando com os dados clínicos (OCT Triton Ground Truth)...")
matched_df = pd.read_csv(matched_csv, sep=';')
rad_df['tokens'] = rad_df['Patient_Name'].apply(get_tokens)
matched_df['tokens'] = matched_df['nome_pentacam'].apply(get_tokens)

merged_rows = []
for idx, m_row in matched_df.iterrows():
    m_tok = m_row['tokens']
    if len(m_tok) < 1: continue
    
    matches = []
    for _, r_row in rad_df.iterrows():
        r_tok = r_row['tokens']
        overlap = m_tok & r_tok
        if len(overlap) >= 1 and len(overlap) >= 0.5 * min(len(m_tok), len(r_tok)):
            matches.append(r_row)
            
    if matches:
        best_match = max(matches, key=lambda x: x['Entropy_Max'])
        row_data = m_row.to_dict()
        row_data.update(best_match.to_dict())
        
        # Determine Ground Truth (FII from Triton)
        is_ectasia = 1 if (row_data.get('FII_Class') in ['KC Verdadeiro', 'Forme Fruste'] or row_data.get('FII_IT', 1.1) < 1.05) else 0
        row_data['y_true'] = is_ectasia
        merged_rows.append(row_data)

final_df = pd.DataFrame(merged_rows)
print(f"Pareamento concluído: {len(final_df)} pares perfeitos.")

if len(final_df) > 0:
    print("\n3. Calculando AUCs das novas métricas 360º (Ground Truth: Ectasia/Suscetibilidade no OCT)")
    
    y_true = final_df['y_true']
    
    features = ['Entropy_Mean', 'Entropy_Max', 'Entropy_Std', 'Contrast_Mean', 'Contrast_Max', 'Contrast_Std']
    
    for f in features:
        auc = roc_auc_score(y_true, final_df[f])
        # se auc < 0.5, a relação é inversa, então invertemos para comparar o poder preditivo
        if auc < 0.5:
            auc = 1 - auc
        print(f"  AUC ({f}): {auc:.4f}")
    
    # Calcular um score combinado simples (ex: Max Entropia + Assimetria)
    # Normalizando:
    e_max_norm = (final_df['Entropy_Max'] - final_df['Entropy_Max'].min()) / (final_df['Entropy_Max'].max() - final_df['Entropy_Max'].min())
    e_std_norm = (final_df['Entropy_Std'] - final_df['Entropy_Std'].min()) / (final_df['Entropy_Std'].max() - final_df['Entropy_Std'].min())
    
    combined_score = e_max_norm + e_std_norm
    auc_combined = roc_auc_score(y_true, combined_score)
    if auc_combined < 0.5: auc_combined = 1 - auc_combined
    
    print(f"\n  AUC (Score Combinado: Máximo + Assimetria 360º): {auc_combined:.4f}")
    
    # Mostrar os falsos negativos do BAD-D que foram pegos pela radiômica (O gap diagnóstico)
    penta_pos = final_df['BAD_D'] >= 2.6
    gap_df = final_df[(final_df['y_true'] == 1) & (~penta_pos)]
    print(f"\nPacientes no Gap Diagnóstico (Doentes no OCT, Pentacam BAD-D Normal): {len(gap_df)}")
    print(f"Média do Score Combinado Radiômico nesses pacientes: {combined_score[gap_df.index].mean():.4f}")
    print(f"Média do Score Combinado Radiômico em pacientes Normais: {combined_score[final_df['y_true'] == 0].mean():.4f}")
