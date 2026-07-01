#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRESBYCOR — Extrator de PDFs + Pipeline ML/DL Completo
Extrai dados de 337 PDFs de pacientes e faz engenharia reversa do algoritmo
"""

import sys, os, re, json, glob, warnings
sys.stdout.reconfigure(encoding='utf-8')
warnings.filterwarnings('ignore')

# Pastas com PDFs reais (sem sinteticos)
PDF_DIRS = [
    r"D:\Antigravity\Presbycor arquivos de pacientes",
    r"D:\Downloads Comet",
]
OUT_CSV  = r"C:\Users\3D_OCT\Documents\Antigravity\Presbycor\pacientes_reais.csv"
OUT_JSON = r"C:\Users\3D_OCT\Documents\Antigravity\Presbycor\resultados_ml_real.json"

# ─── INSTALAR DEPENDENCIAS ───────────────────────────────────────────────────
def instalar(pkg):
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", pkg, "-q"], check=False)

print("Verificando dependencias...")
try:
    import pdfplumber
except:
    print("  Instalando pdfplumber...")
    instalar("pdfplumber")
    import pdfplumber

try:
    import pandas as pd
except:
    instalar("pandas")
    import pandas as pd

try:
    import numpy as np
except:
    instalar("numpy")
    import numpy as np

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    from sklearn.neural_network import MLPRegressor
    from sklearn.preprocessing import StandardScaler
except:
    instalar("scikit-learn")
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    from sklearn.neural_network import MLPRegressor
    from sklearn.preprocessing import StandardScaler

print("Dependencias OK\n")

# ─── EXTRATOR DE PDF ─────────────────────────────────────────────────────────
def extrair_valor(texto, patterns):
    """Tenta extrair um valor numerico usando multiplos padroes regex"""
    for pat in patterns:
        m = re.search(pat, texto, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1).replace(',', '.'))
            except:
                pass
    return None

def extrair_texto_pdf(path):
    """Extrai todo o texto de um PDF"""
    try:
        with pdfplumber.open(path) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    except Exception as e:
        return ""

def parse_presbycor_pdf(path):
    """Extrai dados estruturados de um PDF do Presbycor"""
    texto = extrair_texto_pdf(path)
    if not texto or len(texto) < 100:
        return None

    nome = os.path.basename(path).replace('.pdf','')

    # ── INPUTS ──
    idade = extrair_valor(texto, [
        r'Age[:\s]+(\d+)', r'Idade[:\s]+(\d+)', r'(\d+)\s*years?\s*old',
        r'Age\s*/\s*Sex[:\s]+(\d+)', r'(\d{2})\s*Y'
    ])

    esfera_od = extrair_valor(texto, [
        r'OD.*?Sphere[:\s]+([-+]?\d+[.,]\d+)',
        r'Right.*?Sphere[:\s]+([-+]?\d+[.,]\d+)',
        r'Sphere.*?OD[:\s]+([-+]?\d+[.,]\d+)',
        r'SPH.*?OD[:\s]+([-+]?\d+[.,]\d+)',
        r'OD\s+([-+]?\d+[.,]\d+)\s+([-+]?\d+[.,]\d+)',
    ])

    cilindro_od = extrair_valor(texto, [
        r'OD.*?Cylinder[:\s]+([-+]?\d+[.,]\d+)',
        r'OD.*?Cyl[:\s]+([-+]?\d+[.,]\d+)',
        r'CYL.*?OD[:\s]+([-+]?\d+[.,]\d+)',
    ])

    adicao = extrair_valor(texto, [
        r'Add(?:ition)?[:\s]+([\d.,]+)\s*[Dd]',
        r'Near Add[:\s]+([\d.,]+)',
        r'Add\s*=\s*([\d.,]+)',
        r'\+?([\d.,]+)\s*D\s*add',
        r'Addi[cç][aã]o[:\s]+([\d.,]+)',
    ])

    esfera_target_od = extrair_valor(texto, [
        r'Target.*?OD.*?Sphere[:\s]+([-+]?\d+[.,]\d+)',
        r'Target.*?Sph.*?OD[:\s]+([-+]?\d+[.,]\d+)',
        r'Planned.*?OD[:\s]+([-+]?\d+[.,]\d+)',
        r'OD.*?Target[:\s]+([-+]?\d+[.,]\d+)',
        r'Esf.*?Final.*?OD[:\s]+([-+]?\d+[.,]\d+)',
    ])

    q_target = extrair_valor(texto, [
        r'Q.*?target[:\s]+([-+]?\d+[.,]\d+)',
        r'Q.*?alvo[:\s]+([-+]?\d+[.,]\d+)',
        r'Q[:\s]+([-+]?\d+[.,]\d+)',
        r'Asphericity.*?target[:\s]+([-+]?\d+[.,]\d+)',
    ])

    k_mean = extrair_valor(texto, [
        r'K\s*mean[:\s]+([\d.,]+)',
        r'Km[:\s]+([\d.,]+)',
        r'Mean\s*K[:\s]+([\d.,]+)',
        r'K1.*?K2.*?([\d]{2}[.,]\d+)',
    ])

    k1 = extrair_valor(texto, [
        r'K1[:\s]+([\d.,]+)',
        r'Kflat[:\s]+([\d.,]+)',
        r'K\s*flat[:\s]+([\d.,]+)',
    ])

    k2 = extrair_valor(texto, [
        r'K2[:\s]+([\d.,]+)',
        r'Ksteep[:\s]+([\d.,]+)',
        r'K\s*steep[:\s]+([\d.,]+)',
    ])

    paquimetria = extrair_valor(texto, [
        r'Pachy(?:metry)?[:\s]+(\d{3,4})',
        r'CCT[:\s]+(\d{3,4})',
        r'Thickness[:\s]+(\d{3,4})',
        r'(\d{3,4})\s*[μu]m',
    ])

    zona_optica = extrair_valor(texto, [
        r'Optical\s*Zone[:\s]+([\d.,]+)',
        r'OZ[:\s]+([\d.,]+)',
        r'Zona\s*[oO]ptica[:\s]+([\d.,]+)',
        r'Zone[:\s]+([\d.,]+)\s*mm',
    ])

    estrategia = None
    for s in ['EQUI', 'DUAL', 'equi', 'dual', 'equivision', 'dualvision',
              'Equi-Vision', 'Dual-Vision', 'MICRO', 'micro']:
        if s.lower() in texto.lower():
            estrategia = 'EQUI' if 'equi' in s.lower() else 'DUAL'
            break

    olho_dominante = None
    if re.search(r'dominant.*?OD|OD.*?dominant|direito.*?dominante|dominante.*?OD', texto, re.I):
        olho_dominante = 'OD'
    elif re.search(r'dominant.*?OE|OE.*?dominant|esquerdo.*?dominante|dominante.*?OE', texto, re.I):
        olho_dominante = 'OE'

    record = {
        'arquivo': nome,
        'idade': idade,
        'esfera_od': esfera_od,
        'cilindro_od': cilindro_od,
        'adicao_D': adicao,
        'k1': k1,
        'k2': k2,
        'k_mean': k_mean if k_mean else ((k1+k2)/2 if k1 and k2 else None),
        'paquimetria': paquimetria,
        'zona_optica': zona_optica,
        'esfera_target_od': esfera_target_od,
        'q_target': q_target,
        'estrategia': estrategia,
        'olho_dominante': olho_dominante,
        'texto_len': len(texto),
    }

    # Contar campos nao-nulos
    campos_validos = sum(1 for k,v in record.items()
                        if k not in ['arquivo','estrategia','olho_dominante','texto_len'] and v is not None)
    record['campos_validos'] = campos_validos

    return record

# ─── EXTRAÇÃO ────────────────────────────────────────────────────────────────
print("=" * 60)
print("FASE 1 — EXTRACAO DE PDFs")
print("=" * 60)

# Coletar PDFs de todas as pastas
pdfs = []
for d in PDF_DIRS:
    if os.path.exists(d):
        pdfs += glob.glob(os.path.join(d, "**", "*.pdf"), recursive=True)

# Deduplicar por conteudo (hash do nome base sem numero entre parenteses)
def normalizar_nome(path):
    nome = os.path.basename(path)
    nome = re.sub(r'\s*\(\d+\)\.pdf$', '.pdf', nome)  # remove (1), (2)...
    return nome.lower().strip()

vistos = {}
for p in pdfs:
    chave = normalizar_nome(p)
    if chave not in vistos:
        vistos[chave] = p

pdfs = list(vistos.values())
print(f"PDFs unicos encontrados: {len(pdfs)} (duplicatas removidas)")

registros = []
erros = 0
for i, pdf in enumerate(pdfs):
    if i % 20 == 0:
        print(f"  Processando {i+1}/{len(pdfs)}...")
    rec = parse_presbycor_pdf(pdf)
    if rec:
        registros.append(rec)
    else:
        erros += 1

df_raw = pd.DataFrame(registros)
print(f"\nRegistros extraidos: {len(df_raw)}")
print(f"Erros/vazios: {erros}")
print(f"\nCampos por registro (media): {df_raw['campos_validos'].mean():.1f}")
print(f"\nCobertura por coluna:")
for col in df_raw.columns:
    if col not in ['arquivo','estrategia','olho_dominante','texto_len','campos_validos']:
        n = df_raw[col].notna().sum()
        pct = 100*n/len(df_raw)
        bar = '█' * int(pct/5)
        print(f"  {col:20s}: {n:3d}/{len(df_raw)} ({pct:5.1f}%) {bar}")

df_raw.to_csv(OUT_CSV, index=False, encoding='utf-8')
print(f"\nCSV salvo: {OUT_CSV}")

# ─── PREPARAR DADOS PARA ML ──────────────────────────────────────────────────
print("\n" + "=" * 60)
print("FASE 2 — PREPARACAO PARA ML")
print("=" * 60)

# Features e targets
features = ['idade', 'esfera_od', 'cilindro_od', 'k1', 'k2', 'k_mean', 'paquimetria', 'zona_optica']
target_esf = 'esfera_target_od'
target_q = 'q_target'

df_ml = df_raw[features + [target_esf, target_q]].dropna(subset=['idade'])
print(f"Registros com dados suficientes: {len(df_ml)}")

# Dataset para prever esfera target
df_esf = df_ml[features + [target_esf]].dropna()
df_q   = df_ml[features + [target_q]].dropna()
print(f"Casos com esfera_target: {len(df_esf)}")
print(f"Casos com q_target: {len(df_q)}")

resultados = {}

for nome_target, df_target, col_target in [
    ("Esfera Final OD", df_esf, target_esf),
    ("Q Target", df_q, target_q)
]:
    print(f"\n{'='*60}")
    print(f"FASE 3 — ML para: {nome_target}")
    print(f"{'='*60}")

    feats_disp = [f for f in features if f in df_target.columns and df_target[f].notna().sum() > len(df_target)*0.5]
    X = df_target[feats_disp].fillna(df_target[feats_disp].median())
    y = df_target[col_target]

    if len(X) < 10:
        print(f"  Poucos dados ({len(X)} casos). Pulando.")
        continue

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelos = {
        'Regressao Linear': LinearRegression(),
        'Polinomial grau2': Pipeline([('poly', PolynomialFeatures(2)), ('lin', LinearRegression())]),
        'Random Forest': RandomForestRegressor(n_estimators=200, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=200, random_state=42),
        'Rede Neural MLP': Pipeline([
            ('scaler', StandardScaler()),
            ('mlp', MLPRegressor(hidden_layer_sizes=(64,32,16), max_iter=500, random_state=42))
        ]),
    }

    print(f"\nFeatures usadas ({len(feats_disp)}): {feats_disp}")
    print(f"Amostras treino: {len(X_train)} | teste: {len(X_test)}")
    print(f"\n{'Modelo':35s} {'R2':>8} {'RMSE':>8} {'MAE':>8}")
    print("-" * 62)

    res_target = {}
    melhor_r2 = -999
    melhor_nome = None

    for nome_m, modelo in modelos.items():
        try:
            modelo.fit(X_train, y_train)
            y_pred = modelo.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            rmse = mean_squared_error(y_test, y_pred)**0.5
            mae = mean_absolute_error(y_test, y_pred)
            print(f"{nome_m:35s} {r2:8.4f} {rmse:8.4f} {mae:8.4f}")
            res_target[nome_m] = {'r2': round(r2,4), 'rmse': round(rmse,4), 'mae': round(mae,4)}
            if r2 > melhor_r2:
                melhor_r2 = r2
                melhor_nome = nome_m
        except Exception as e:
            print(f"{nome_m:35s} ERRO: {e}")

    print("-" * 62)
    if melhor_nome:
        print(f"Melhor modelo: {melhor_nome} (R2={melhor_r2:.4f})")

        # Importancia das variaveis (Random Forest)
        rf = RandomForestRegressor(n_estimators=200, random_state=42)
        rf.fit(X_train, y_train)
        importancias = sorted(zip(feats_disp, rf.feature_importances_), key=lambda x: -x[1])
        print(f"\nImportancia das variaveis:")
        for feat, imp in importancias:
            bar = '█' * int(imp*40)
            print(f"  {feat:20s}: {imp:.4f} {bar}")

    resultados[nome_target] = res_target

# ─── SALVAR RESULTADOS ───────────────────────────────────────────────────────
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 60)
print("PIPELINE CONCLUIDO!")
print(f"  CSV com dados: {OUT_CSV}")
print(f"  Resultados ML: {OUT_JSON}")
print("=" * 60)

# Mostrar amostra dos dados extraidos
print("\nAMOSTRA DOS DADOS EXTRAIDOS (5 primeiros casos):")
print(df_raw[['arquivo','idade','esfera_od','cilindro_od','adicao_D','k_mean','esfera_target_od','q_target']].head(10).to_string())
