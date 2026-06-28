"""
batch_curvature_extractor.py — Extração em Batch de Métricas Geométricas
=========================================================================
Processa TODOS os arquivos .SPR (Pentacam Scheimpflug) e extrai:
  - r_ant (raio de curvatura anterior)
  - r_post (raio de curvatura posterior)
  - ct (espessura central, mm)
  - decentração do apex (anterior vs posterior)
  - assimetria de curvatura (nasal vs temporal)
  - índice de irregularidade (desvio da circularidade)

Nota: Valores absolutos carregam distorção Scheimpflug, mas razões
e correlações inter-pacientes permanecem válidas.

Author: Antigravity Pipeline
Date: 2025-06
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import glob
import json
import numpy as np
import pandas as pd
from scipy import optimize
from skimage import filters
import warnings
import traceback

warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURAÇÃO
# ============================================================

SPR_DIR = r'D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP'
OUT_DIR = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\results'
os.makedirs(OUT_DIR, exist_ok=True)

# Geometria de imagem SPR
WIDTH = 416
SLICE_HEIGHT = 256
PIXELS_PER_SLICE = WIDTH * SLICE_HEIGHT
HEADER_OFFSET = 2048

# Escala: ~14mm campo de visão em 416 pixels
FOV_MM = 14.0
MM_PER_PIXEL = FOV_MM / float(WIDTH)

# Parâmetros de QC
MIN_EDGE_POINTS = 20      # Mínimo de pontos válidos para ajuste
MAX_RADIUS_PIX = 500       # Raio máximo aceitável em pixels (filtro outlier)
MIN_THICKNESS_PIX = 3      # Espessura mínima para considerar córnea válida


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def fit_circle(x, y):
    """Ajuste de círculo por mínimos quadrados. Retorna (xc, yc, R)."""
    def calc_R(xc, yc):
        return np.sqrt((x - xc)**2 + (y - yc)**2)
    def f_2(c):
        Ri = calc_R(*c)
        return Ri - Ri.mean()
    center_estimate = np.mean(x), np.mean(y)
    try:
        center, ier = optimize.leastsq(f_2, center_estimate, maxfev=5000)
        if ier not in [1, 2, 3, 4]:
            return None, None, None
    except Exception:
        return None, None, None
    xc, yc = center
    Ri = calc_R(xc, yc)
    R = Ri.mean()
    residual = np.std(Ri)
    return xc, yc, R, residual


def compute_irregularity(x, y, xc, yc, R):
    """
    Índice de irregularidade: RMS do desvio dos pontos da borda
    em relação ao círculo ajustado, normalizado pelo raio.
    """
    Ri = np.sqrt((x - xc)**2 + (y - yc)**2)
    rms = np.sqrt(np.mean((Ri - R)**2))
    return rms / R if R > 0 else np.nan


def compute_asymmetry(x, y, center_x):
    """
    Assimetria nasal-temporal: diferença de curvatura entre as
    metades esquerda (nasal) e direita (temporal) da córnea.
    Retorna o ratio R_nasal / R_temporal.
    """
    # Dividir em nasal (esquerda) e temporal (direita)
    mask_left = x < center_x
    mask_right = x >= center_x
    
    if np.sum(mask_left) < 10 or np.sum(mask_right) < 10:
        return np.nan, np.nan, np.nan
    
    result_left = fit_circle(x[mask_left], y[mask_left])
    result_right = fit_circle(x[mask_right], y[mask_right])
    
    if result_left[2] is None or result_right[2] is None:
        return np.nan, np.nan, np.nan
    
    r_nasal = result_left[2]
    r_temporal = result_right[2]
    ratio = r_nasal / r_temporal if r_temporal > 0 else np.nan
    
    return r_nasal, r_temporal, ratio


def extract_edges(img):
    """
    Extrai bordas anterior e posterior da imagem Scheimpflug.
    Retorna arrays de pontos (x, y) para cada borda.
    """
    img_blur = filters.gaussian(img, sigma=2.0)
    thresh = filters.threshold_otsu(img_blur)
    binary = img_blur > thresh
    
    ant_points = []
    post_points = []
    
    # Scan em todas as colunas dentro da ROI central
    center_x = WIDTH // 2
    roi_width = 200  # Ampliado para capturar mais da córnea
    start_col = max(0, center_x - roi_width // 2)
    end_col = min(WIDTH, center_x + roi_width // 2)
    
    for x in range(start_col, end_col):
        col_data = binary[:, x]
        bright_indices = np.where(col_data)[0]
        if len(bright_indices) > MIN_THICKNESS_PIX:
            y_ant = bright_indices[0]   # Primeiro pixel brilhante (anterior)
            y_post = bright_indices[-1]  # Último pixel brilhante (posterior)
            ant_points.append([x, y_ant])
            post_points.append([x, y_post])
    
    return np.array(ant_points), np.array(post_points)


def process_single_spr(spr_path):
    """
    Processa um arquivo .SPR e retorna dicionário de métricas.
    Usa a fatia central para extração de geometria.
    """
    patient_id = os.path.basename(spr_path).replace('.SPR', '')
    
    # Ler dados brutos
    with open(spr_path, 'rb') as f:
        raw_data = f.read()
    
    img_data = raw_data[HEADER_OFFSET:]
    arr = np.frombuffer(img_data, dtype=np.uint8)
    num_slices = len(arr) // PIXELS_PER_SLICE
    
    if num_slices < 1:
        return None, "Sem slices válidos"
    
    # Coletar fatias válidas
    valid_slices = []
    for i in range(num_slices):
        s = arr[i * PIXELS_PER_SLICE : (i + 1) * PIXELS_PER_SLICE]
        if len(s) == PIXELS_PER_SLICE:
            s = s.reshape((SLICE_HEIGHT, WIDTH))
            if np.mean(s) > 10:  # Filtro de fatia vazia
                valid_slices.append(s)
    
    if len(valid_slices) < 3:
        return None, f"Apenas {len(valid_slices)} fatias válidas"
    
    # Usar fatia central (melhor qualidade)
    center_idx = len(valid_slices) // 2
    img = valid_slices[center_idx]
    
    # Extrair bordas
    ant_points, post_points = extract_edges(img)
    
    if len(ant_points) < MIN_EDGE_POINTS or len(post_points) < MIN_EDGE_POINTS:
        return None, f"Pontos insuficientes: ant={len(ant_points)}, post={len(post_points)}"
    
    # Converter para mm
    x_ant_mm = ant_points[:, 0] * MM_PER_PIXEL
    y_ant_mm = -ant_points[:, 1] * MM_PER_PIXEL  # Y invertido (imagem)
    x_post_mm = post_points[:, 0] * MM_PER_PIXEL
    y_post_mm = -post_points[:, 1] * MM_PER_PIXEL
    
    # ---- AJUSTE DE CÍRCULO (ANTERIOR) ----
    result_ant = fit_circle(x_ant_mm, y_ant_mm)
    if result_ant[2] is None:
        return None, "Falha no ajuste anterior"
    xc_ant, yc_ant, r_ant, resid_ant = result_ant
    
    # ---- AJUSTE DE CÍRCULO (POSTERIOR) ----
    result_post = fit_circle(x_post_mm, y_post_mm)
    if result_post[2] is None:
        return None, "Falha no ajuste posterior"
    xc_post, yc_post, r_post, resid_post = result_post
    
    # ---- ESPESSURA CENTRAL ----
    apex_idx_ant = np.argmax(y_ant_mm)
    apex_x_ant = x_ant_mm[apex_idx_ant]
    apex_y_ant = y_ant_mm[apex_idx_ant]
    
    # Ponto posterior correspondente no mesmo X
    y_post_at_apex = np.interp(apex_x_ant, x_post_mm, y_post_mm)
    ct_mm = abs(apex_y_ant - y_post_at_apex)
    
    # ---- DECENTRAÇÃO DO APEX ----
    apex_idx_post = np.argmin(y_post_mm)  # Ponto mais posterior (menor Y = mais profundo)
    # Correção: usar argmax para posterior também (menos negativo = mais próximo do anterior)
    apex_idx_post = np.argmax(y_post_mm)
    apex_x_post = x_post_mm[apex_idx_post]
    
    # Decentração em mm (diferença de posição X dos ápices)
    decentration_mm = abs(apex_x_ant - apex_x_post)
    
    # ---- RAZÃO DE CURVATURA ----
    ratio_ant_post = r_ant / r_post if r_post > 0 else np.nan
    
    # ---- IRREGULARIDADE ----
    irreg_ant = compute_irregularity(x_ant_mm, y_ant_mm, xc_ant, yc_ant, r_ant)
    irreg_post = compute_irregularity(x_post_mm, y_post_mm, xc_post, yc_post, r_post)
    
    # ---- ASSIMETRIA ----
    center_x_mm = (WIDTH // 2) * MM_PER_PIXEL
    _, _, asym_ant = compute_asymmetry(x_ant_mm, y_ant_mm, center_x_mm)
    _, _, asym_post = compute_asymmetry(x_post_mm, y_post_mm, center_x_mm)
    
    # ---- NÚMERO DE FATIAS VÁLIDAS ----
    n_valid = len(valid_slices)
    
    # ---- MÉTRICAS DE PODER REFRATIVO (GULLSTRAND) ----
    # Nota: valores proporcionais devido à distorção Scheimpflug
    n_cornea = 1.376
    n_air = 1.000
    n_aqueous = 1.336
    
    # Poder em escala relativa (mm -> precisa converter para metros para D)
    # P = (n2 - n1) / R [em metros] = (n2-n1) / (R/1000) * 1000 D
    # Com distorção, usamos a razão P_ant/P_post que cancela o fator de escala
    P_ant_rel = (n_cornea - n_air) / r_ant if r_ant > 0 else np.nan
    P_post_rel = (n_aqueous - n_cornea) / r_post if r_post > 0 else np.nan
    P_ratio = abs(P_ant_rel / P_post_rel) if P_post_rel != 0 else np.nan
    
    # Compilar resultados
    metrics = {
        'Patient_ID': patient_id,
        'N_Valid_Slices': n_valid,
        'R_Anterior_mm': round(r_ant, 4),
        'R_Posterior_mm': round(r_post, 4),
        'Ratio_Rant_Rpost': round(ratio_ant_post, 4),
        'CT_mm': round(ct_mm, 4),
        'Decentration_mm': round(decentration_mm, 4),
        'Irregularity_Ant': round(irreg_ant, 6),
        'Irregularity_Post': round(irreg_post, 6),
        'Asymmetry_Ant': round(asym_ant, 4) if not np.isnan(asym_ant) else np.nan,
        'Asymmetry_Post': round(asym_post, 4) if not np.isnan(asym_post) else np.nan,
        'P_Ratio_AntPost': round(P_ratio, 4) if not np.isnan(P_ratio) else np.nan,
        'Residual_Ant': round(resid_ant, 6),
        'Residual_Post': round(resid_post, 6),
        'Apex_X_Ant_mm': round(apex_x_ant, 4),
        'Apex_X_Post_mm': round(apex_x_post, 4),
    }
    
    return metrics, None


# ============================================================
# MAIN — PROCESSAMENTO EM BATCH
# ============================================================

def main():
    print("=" * 70)
    print("  BATCH CURVATURE EXTRACTOR — Análise Geométrica Ant/Post")
    print("=" * 70)
    
    spr_files = sorted(glob.glob(os.path.join(SPR_DIR, "*.SPR")))
    print(f"\nTotal de arquivos SPR encontrados: {len(spr_files)}")
    
    if not spr_files:
        print("[ERRO] Nenhum arquivo .SPR encontrado!")
        return
    
    results = []
    errors = []
    
    for i, spr_path in enumerate(spr_files):
        patient_id = os.path.basename(spr_path).replace('.SPR', '')
        
        try:
            metrics, error = process_single_spr(spr_path)
            if metrics is not None:
                results.append(metrics)
                if (i + 1) % 50 == 0:
                    print(f"  [{i+1}/{len(spr_files)}] Processado: {patient_id} ✓")
            else:
                errors.append((patient_id, error))
                if (i + 1) % 50 == 0:
                    print(f"  [{i+1}/{len(spr_files)}] Erro: {patient_id} — {error}")
        except Exception as e:
            errors.append((patient_id, str(e)))
            if (i + 1) % 50 == 0:
                print(f"  [{i+1}/{len(spr_files)}] Exceção: {patient_id} — {e}")
    
    # Criar DataFrame
    df = pd.DataFrame(results)
    
    # Salvar
    out_path = os.path.join(OUT_DIR, "batch_curvature_metrics.csv")
    df.to_csv(out_path, index=False, sep=';')
    
    # ---- RELATÓRIO ----
    print(f"\n{'=' * 70}")
    print(f"  RELATÓRIO DE EXTRAÇÃO")
    print(f"{'=' * 70}")
    print(f"  Total processado: {len(spr_files)}")
    print(f"  Sucesso:          {len(results)} ({100*len(results)/len(spr_files):.1f}%)")
    print(f"  Erros:            {len(errors)} ({100*len(errors)/len(spr_files):.1f}%)")
    print(f"\n  Salvo em: {out_path}")
    
    if len(results) > 0:
        print(f"\n--- Estatísticas Descritivas ---")
        for col in ['R_Anterior_mm', 'R_Posterior_mm', 'Ratio_Rant_Rpost', 'CT_mm',
                     'Decentration_mm', 'Irregularity_Ant', 'Irregularity_Post',
                     'Asymmetry_Ant', 'Asymmetry_Post', 'P_Ratio_AntPost']:
            if col in df.columns:
                vals = df[col].dropna()
                if len(vals) > 0:
                    print(f"  {col:25s}: mean={vals.mean():.4f}  std={vals.std():.4f}  "
                          f"min={vals.min():.4f}  max={vals.max():.4f}  N={len(vals)}")
    
    if errors:
        print(f"\n--- Primeiros 10 Erros ---")
        for pid, err in errors[:10]:
            print(f"  {pid}: {err}")
    
    print(f"\n{'=' * 70}")
    print(f"  Extração concluída.")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
