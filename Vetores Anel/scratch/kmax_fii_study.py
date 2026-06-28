import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Configuracao de plot
BG = '#0d1117'; TEXT = '#c9d1d9'
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': '#161b22',
                     'axes.edgecolor': '#21262d', 'axes.labelcolor': TEXT,
                     'text.color': TEXT, 'xtick.color': TEXT, 'ytick.color': TEXT})

print('='*70)
print('  ESTUDO: KMAX vs FII NA BASE DE VALIDACAO')
print('='*70)

df = pd.read_csv(r'D:\Projetos\Antigravity\Vetores Anel\exports\Validacao_FII_Pentacam.csv', sep=';')

# Extrair KMax de acordo com o olho validado
kmax_list = []
fii_it_list = []
fii_c_list = []
diag_list = []

for _, row in df.iterrows():
    olho = str(row.get('olho_fii', '')).strip().upper()
    if pd.isna(row.get('fii_it')): continue
    
    # Kmax
    kmax = np.nan
    if 'OD' in olho:
        kmax = str(row.get('kmax_od', '')).replace(',','.')
    elif 'OS' in olho:
        kmax = str(row.get('kmax_os', '')).replace(',','.')
        
    try:
        kmax = float(kmax)
        if kmax > 30 and kmax < 100: # limites fisiologicos
            kmax_list.append(kmax)
            fii_it_list.append(float(str(row['fii_it']).replace(',','.')))
            fii_c_list.append(float(str(row['fii_c']).replace(',','.')))
            diag_list.append(str(row.get('diag_topo', 'Desc')))
    except:
        pass

vdf = pd.DataFrame({'KMax': kmax_list, 'FII_IT': fii_it_list, 'FII_C': fii_c_list, 'Diag': diag_list})
vdf['is_kc'] = vdf['Diag'].str.contains('KC|Ceratocone|Keratoconus', case=False).astype(int)

# 1. KMax quando FII está alterado
# Regra: FII_IT < 1.05 (Alerta Fibrilar IT)
fii_alt = vdf[vdf['FII_IT'] < 1.05]
fii_norm = vdf[vdf['FII_IT'] >= 1.05]

print(f'\n1. MEDIA DO KMAX POR STATUS DO FII_IT (< 1.05):')
print(f"  FII Normal   (N={len(fii_norm):>3}): KMax medio = {fii_norm['KMax'].mean():.2f} D (min={fii_norm['KMax'].min():.2f}, max={fii_norm['KMax'].max():.2f})")
print(f"  FII Alterado (N={len(fii_alt):>3}): KMax medio = {fii_alt['KMax'].mean():.2f} D (min={fii_alt['KMax'].min():.2f}, max={fii_alt['KMax'].max():.2f})")

print(f'\n2. MEDIA DO KMAX POR STATUS DO FII CENTRAL (> 1.10):')
fc_alt = vdf[vdf['FII_C'] > 1.10]
fc_norm = vdf[vdf['FII_C'] <= 1.10]
print(f"  FII_C Normal   (N={len(fc_norm):>3}): KMax medio = {fc_norm['KMax'].mean():.2f} D")
print(f"  FII_C Alterado (N={len(fc_alt):>3}): KMax medio = {fc_alt['KMax'].mean():.2f} D")

# Vamos ver os piores casos de FII_IT (< 0.90)
fii_severe = vdf[vdf['FII_IT'] < 0.90]
print(f"\n  Casos FII_IT Severo (<0.90) (N={len(fii_severe)}): KMax medio = {fii_severe['KMax'].mean():.2f} D")

# 2. O KMax de 49 já é ceratocone?
print(f'\n3. ANALISE DO KMAX ~ 49 D:')
k49 = vdf[(vdf['KMax'] >= 48.0) & (vdf['KMax'] <= 50.0)]
print(f"  Encontrados {len(k49)} olhos com KMax entre 48.0 e 50.0 D.")

if len(k49) > 0:
    kc = k49['is_kc'].sum()
    print(f"  Desses, {kc} ({kc/len(k49)*100:.1f}%) tem ceratocone clinico.")
    print(f"  FII_IT Medio nesse grupo: {k49['FII_IT'].mean():.3f}")
    
    print("\n  Detalhes dos casos com KMax ~49:")
    for _, row in k49.iterrows():
        status = 'KC' if row['is_kc'] else 'Norm/S'
        alerta = 'FII ALTERADO!' if row['FII_IT'] < 1.05 else 'Fii OK'
        print(f"  - KMax: {row['KMax']:.1f} D | Diag: {status:<6} | FII_IT: {row['FII_IT']:.3f} ({alerta})")

# 4. Encontrar FII_IT alterados com KMax PERFEITAMENTE NORMAL (<45D)
print(f'\n4. O INVISIVEL (KMax Normal < 45 D, FII Alterado < 1.0):')
inv = vdf[(vdf['KMax'] < 45.0) & (vdf['FII_IT'] < 1.0)]
print(f"  Encontrados {len(inv)} olhos com FII colapsado mas KMax perfeito.")
for _, row in inv.iterrows():
    print(f"  - KMax: {row['KMax']:.1f} D | Diag: {row['Diag']:<15} | FII_IT: {row['FII_IT']:.2f}")

# Grafico Rápido
plt.figure(figsize=(8,6))
sc = plt.scatter(vdf['KMax'], vdf['FII_IT'], c=vdf['is_kc'], cmap='coolwarm', alpha=0.7)
plt.axhline(1.05, color='orange', linestyle='--', label='Corte FII_IT (1.05)')
plt.axvline(47.2, color='red', linestyle=':', label='KMax Suspeito (47.2)')
plt.axvline(49.0, color='red', linestyle='--', label='KMax KC (49.0)')
plt.xlabel('KMax (Dioptrias)')
plt.ylabel('FII Inferotemporal')
plt.title('KMax vs Integridade Fibrilar (FII_IT)')
plt.legend()
plt.savefig(r'c:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\results\kmax_vs_fii.png', dpi=150)
print("\nDashboard salvo em: results/kmax_vs_fii.png")
