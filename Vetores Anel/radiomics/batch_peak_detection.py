"""
Peak Detection Epithelial Thickness Extractor
Extrai espessura epitelial de TODOS os .SPR usando análise de picos no perfil A-scan.
Sem deep learning. Sem caixa preta.
"""
import numpy as np
import os
import glob
import csv
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

spr_dir = r'D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP'
out_csv = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch\epithelial_peak_detection.csv'

WIDTH = 416
HEIGHT = 256
OFFSET = 2048
PPS = WIDTH * HEIGHT

# Escala pixel-mm (estimativa baseada em anatomia)
# Eixo vertical: a córnea central tem ~550um de espessura e ocupa ~48 pixels
# Portanto: ~550/48 = ~11.5 um/pixel vertical
UM_PER_PIXEL_V = 11.5

def extract_epithelial_thickness(img, col_start, col_end):
    """
    Para cada coluna no range, encontra os picos de brilho.
    O primeiro pico = superfície anterior do epitélio.
    O primeiro vale APÓS o pico = base do epitélio (Bowman).
    Distância = espessura epitelial em pixels.
    """
    thicknesses = []
    
    for col in range(col_start, col_end):
        profile = img[:, col].astype(float)
        
        # Suavizar levemente para remover ruído de alta frequência
        smoothed = gaussian_filter1d(profile, sigma=1.0)
        
        # Encontrar picos com prominence mínima (para ignorar ruído)
        peaks, props = find_peaks(smoothed, prominence=15, distance=8)
        
        if len(peaks) < 1:
            continue
        
        first_peak = peaks[0]
        peak_val = smoothed[first_peak]
        
        # Encontrar o vale após o primeiro pico
        # Procurar o ponto onde o brilho cai abaixo de 40% do pico
        threshold = peak_val * 0.40
        valley_pos = None
        for row in range(first_peak + 1, min(first_peak + 30, HEIGHT)):
            if smoothed[row] < threshold:
                valley_pos = row
                break
        
        if valley_pos is None:
            continue
        
        thickness_px = valley_pos - first_peak
        thickness_um = thickness_px * UM_PER_PIXEL_V
        
        # Sanity check: epitélio humano = 40-70um (3-7 pixels)
        if 2 <= thickness_px <= 12:
            thicknesses.append({
                'col': col,
                'peak_row': first_peak,
                'valley_row': valley_pos,
                'thickness_px': thickness_px,
                'thickness_um': thickness_um
            })
    
    return thicknesses

# Processar todos os SPR
spr_files = sorted(glob.glob(os.path.join(spr_dir, '*.SPR')))
print(f"Processando {len(spr_files)} arquivos .SPR...")

results = []
errors = 0

for fi, fpath in enumerate(spr_files):
    fname = os.path.basename(fpath)
    try:
        with open(fpath, 'rb') as f:
            raw = f.read()
        
        arr = np.frombuffer(raw[OFFSET:], dtype=np.uint8)
        nslices = len(arr) // PPS
        
        # Coletar de todas as fatias válidas
        patient_thicknesses = []
        
        for si in range(nslices):
            s = arr[si*PPS:(si+1)*PPS].reshape((HEIGHT, WIDTH))
            if np.mean(s) < 10:
                continue
            
            # Região temporal: colunas 130-210 (lado esquerdo da córnea)
            # Região central: colunas 190-230
            # Região nasal: colunas 220-300
            
            # FOCO TEMPORAL (como o usuário pediu)
            temporal = extract_epithelial_thickness(s, 130, 200)
            central = extract_epithelial_thickness(s, 195, 225)
            
            if temporal:
                avg_t = np.mean([t['thickness_um'] for t in temporal])
                patient_thicknesses.append({
                    'slice': si,
                    'region': 'temporal',
                    'mean_thickness_um': avg_t,
                    'n_points': len(temporal)
                })
            
            if central:
                avg_c = np.mean([t['thickness_um'] for t in central])
                patient_thicknesses.append({
                    'slice': si,
                    'region': 'central',
                    'mean_thickness_um': avg_c,
                    'n_points': len(central)
                })
        
        # Resumo do paciente
        temporal_vals = [p['mean_thickness_um'] for p in patient_thicknesses if p['region'] == 'temporal']
        central_vals = [p['mean_thickness_um'] for p in patient_thicknesses if p['region'] == 'central']
        
        results.append({
            'File': fname,
            'Epi_Temporal_um': np.mean(temporal_vals) if temporal_vals else np.nan,
            'Epi_Central_um': np.mean(central_vals) if central_vals else np.nan,
            'Epi_Ratio_TC': (np.mean(temporal_vals) / np.mean(central_vals)) if (temporal_vals and central_vals and np.mean(central_vals) > 0) else np.nan,
            'N_Slices_Valid': len(set(p['slice'] for p in patient_thicknesses)),
        })
        
    except Exception as e:
        errors += 1
        results.append({
            'File': fname,
            'Epi_Temporal_um': np.nan,
            'Epi_Central_um': np.nan,
            'Epi_Ratio_TC': np.nan,
            'N_Slices_Valid': 0,
        })
    
    if (fi + 1) % 100 == 0:
        print(f"  [{fi+1}/{len(spr_files)}] processados...")

# Salvar CSV
with open(out_csv, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['File', 'Epi_Temporal_um', 'Epi_Central_um', 'Epi_Ratio_TC', 'N_Slices_Valid'], delimiter=';')
    writer.writeheader()
    writer.writerows(results)

# Estatísticas
import pandas as pd
df = pd.DataFrame(results)
valid = df.dropna(subset=['Epi_Temporal_um'])
print(f"\n=== RESULTADOS PEAK DETECTION ===")
print(f"Total processados: {len(spr_files)}")
print(f"Extrações válidas: {len(valid)} ({100*len(valid)/len(spr_files):.1f}%)")
print(f"Erros: {errors}")
print(f"\nEspessura Epitelial Temporal:")
print(f"  Média: {valid['Epi_Temporal_um'].mean():.1f} um")
print(f"  Desvio: {valid['Epi_Temporal_um'].std():.1f} um")
print(f"  Range: {valid['Epi_Temporal_um'].min():.1f} - {valid['Epi_Temporal_um'].max():.1f} um")
print(f"\nEspessura Epitelial Central:")
print(f"  Média: {valid['Epi_Central_um'].mean():.1f} um")
print(f"  Desvio: {valid['Epi_Central_um'].std():.1f} um")
print(f"\nRatio Temporal/Central:")
print(f"  Média: {valid['Epi_Ratio_TC'].mean():.3f}")
print(f"  Desvio: {valid['Epi_Ratio_TC'].std():.3f}")
print(f"\nCSV salvo em: {out_csv}")
