import pandas as pd
import numpy as np
import unicodedata
import re
import matplotlib.pyplot as plt
import seaborn as sns
import os

out_img = r"D:\radiomics_gap_diagnostico.png"

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

# Load datasets
matched_df = pd.read_csv(r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\matched_pairs_FII_Pentacam.csv", sep=';')
rad_df = pd.read_csv(r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\pentacam_mass_radiomics.csv", sep=';')

rad_df['tokens'] = rad_df['Patient_Name'].apply(get_tokens)
matched_df['tokens'] = matched_df['nome_pentacam'].apply(get_tokens)

# Merge based on token overlap
merged_rows = []
for idx, m_row in matched_df.iterrows():
    m_tok = m_row['tokens']
    if len(m_tok) < 1: continue
    
    # Find matching SPR files
    matches = []
    for _, r_row in rad_df.iterrows():
        r_tok = r_row['tokens']
        overlap = m_tok & r_tok
        if len(overlap) >= 1 and len(overlap) >= 0.5 * min(len(m_tok), len(r_tok)):
            matches.append(r_row)
            
    if matches:
        # If multiple SPRs, just take the one with highest entropy for now (worst case scenario)
        best_match = max(matches, key=lambda x: x['Entropy'])
        
        row_data = m_row.to_dict()
        row_data['SPR_File'] = best_match['File']
        row_data['Entropy'] = best_match['Entropy']
        row_data['Contrast'] = best_match['Contrast']
        row_data['Correlation'] = best_match['Correlation']
        
        # Determine group
        # fii_pos = FII_Class in ['KC Verdadeiro', 'Forme Fruste'] OR FII_IT < 1.05
        fii_pos = (row_data.get('FII_Class') in ['KC Verdadeiro', 'Forme Fruste']) or (row_data.get('FII_IT', 1.1) < 1.05)
        # penta_pos = BAD_D >= 2.6
        penta_pos = row_data.get('BAD_D', 0) >= 2.6
        
        if fii_pos and penta_pos:
            group = 'KC Confirmado (Concordante)'
        elif not fii_pos and not penta_pos:
            group = 'Normal (Concordante)'
        elif fii_pos and not penta_pos:
            group = 'Gap Diagnóstico (FII+ / Penta-)'
        else:
            group = 'Falso Positivo Penta (FII- / Penta+)'
            
        row_data['Group'] = group
        merged_rows.append(row_data)

final_df = pd.DataFrame(merged_rows)
print(f"Pareados {len(final_df)} exames (Triton + Pentacam + SPR Radiomics)")

if len(final_df) > 0:
    # Print stats by group
    stats = final_df.groupby('Group')['Entropy'].agg(['count', 'mean', 'std'])
    print("\n--- Entropia Estromal por Grupo Clínico ---")
    print(stats)
    
    # Print the Gap Diagnostico cases
    gap_cases = final_df[final_df['Group'] == 'Gap Diagnóstico (FII+ / Penta-)']
    print(f"\nEncontrados {len(gap_cases)} pacientes no Gap Diagnóstico.")
    if len(gap_cases) > 0:
        print(gap_cases[['nome_triton', 'FII_IT', 'BAD_D', 'Entropy']].head(10).to_string())
        
    # Plotting
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=final_df, x='Group', y='Entropy', inner="point", palette='Set2')
    plt.title('Validação da Radiômica Scheimpflug: Detecção do Gap Diagnóstico\n(Entropia vs. Diagnóstico Multimodal)', fontsize=14, fontweight='bold')
    plt.ylabel('Entropia Estromal (Caos Fibrilar)', fontsize=12)
    plt.xlabel('Grupo Clínico (OCT Triton vs. Pentacam Clássico)', fontsize=12)
    plt.xticks(rotation=15)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add significance lines if applicable visually
    norm_mean = final_df[final_df['Group'] == 'Normal (Concordante)']['Entropy'].mean()
    if not np.isnan(norm_mean):
        plt.axhline(norm_mean, color='green', linestyle='--', alpha=0.5, label='Média Normal')
    
    plt.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(out_img), exist_ok=True)
    plt.savefig(out_img, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nGráfico salvo em: {out_img}")
else:
    print("Não foi possível parear os arquivos.")
