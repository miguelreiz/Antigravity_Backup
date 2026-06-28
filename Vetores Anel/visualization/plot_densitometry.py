import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

dens_file = r"D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.AutoCSV\CorneaDens-LOAD.CSV"
bad_file = r"D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.AutoCSV\BADisplay-LOAD.CSV"
out_img = r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\images\CH-037_Elastografia_Optica_Indireta\densitometria_vs_bad_d_poc.png"

def load_csv(path):
    for enc in ['utf-8', 'latin-1', 'cp1252']:
        try:
            df = pd.read_csv(path, sep=';', encoding=enc, on_bad_lines='skip')
            return df
        except:
            pass
    return None

df_dens = load_csv(dens_file)
df_bad = load_csv(bad_file)

if df_dens is not None and df_bad is not None:
    # Key should be Pat-ID or First Name + Last Name + Eye
    df_dens['merge_key'] = df_dens['First Name:'].astype(str) + '_' + df_dens['Last Name:'].astype(str) + '_' + df_dens['Exam Eye:'].astype(str).str.strip()
    df_bad['merge_key'] = df_bad['First Name:'].astype(str) + '_' + df_bad['Last Name:'].astype(str) + '_' + df_bad['Exam Eye:'].astype(str).str.strip()
    
    # Drop duplicates for safety
    df_dens = df_dens.drop_duplicates(subset=['merge_key'])
    df_bad = df_bad.drop_duplicates(subset=['merge_key'])
    
    bad_d_col = [c for c in df_bad.columns if 'BAD D:' in c][0]
    
    merged = pd.merge(df_dens, df_bad[['merge_key', bad_d_col]], on='merge_key', how='inner')
    
    dens_col = 'Dens Avg, Tot.Th., Tot.Dia. [%]:'
    
    # Convert strings like '16,2' to float 16.2
    merged[dens_col] = merged[dens_col].astype(str).str.replace(',', '.').astype(float)
    merged[bad_d_col] = merged[bad_d_col].astype(str).str.replace(',', '.').astype(float)
    
    print("Merged shape:", merged.shape)
    print(merged[['merge_key', dens_col, bad_d_col]])
    
    # Plot if we have points
    if len(merged) > 0:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=merged, x=dens_col, y=bad_d_col, s=100, color='red')
        
        # Add labels
        for i in range(len(merged)):
            plt.text(merged[dens_col].iloc[i] + 0.5, merged[bad_d_col].iloc[i], 
                     merged['merge_key'].iloc[i].split('_')[0], fontsize=9)
        
        plt.title('Proof of Concept: Pentacam Densitometry vs BAD-D\n(Equivalência SII / Integridade Fibrilar)', fontsize=12)
        plt.xlabel('Densitometria Média (Total Thickness/Dia) [%]', fontsize=10)
        plt.ylabel('BAD-D (Deformação Estrutural)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        os.makedirs(os.path.dirname(out_img), exist_ok=True)
        plt.savefig(out_img, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {out_img}")
