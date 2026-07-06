import pandas as pd
import numpy as np
from pathlib import Path

CSV_PATH = r'C:\Users\3D_OCT\Documents\Antigravity\Presbycor\Presbycor_Database_Completo.csv'
EXCEL_PATH = r'C:\Users\3D_OCT\Desktop\Presbycor_Database_Final_Consolidado.xlsx'
DIR1 = Path(r'D:\Antigravity\Presbycor arquivos de pacientes')
DIR2 = Path(r'D:\Downloads Comet')

print("="*70)
print("  AUDITORIA COMPLETA - BANCO DE DADOS PRESBYCOR")
print("="*70)

# 1. Load CSV
df = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
print(f"\n[1] BANCO DE DADOS PRINCIPAL (CSV)")
print(f"    Total de linhas: {len(df)}")
print(f"    Total de colunas: {len(df.columns)}")

# 2. Duplicate check in CSV
dup_names = df[df.duplicated('Patient Name', keep=False)]
dup_sources = df[df.duplicated('Source File', keep=False)]
print(f"\n[2] VERIFICAÇÃO DE DUPLICATAS (CSV)")
print(f"    Pacientes com nome duplicado: {len(dup_names)}")
if len(dup_names) > 0:
    print(f"      -> Nomes duplicados:")
    for n in dup_names['Patient Name'].unique():
        print(f"         {n}")
print(f"    Arquivos fonte duplicados: {len(dup_sources)}")

# 3. Patient names
has_name = df['Patient Name'].notna() & (df['Patient Name'].str.strip() != '')
print(f"\n[3] NOMES DOS PACIENTES")
print(f"    Com nome preenchido: {has_name.sum()} / {len(df)}")
print(f"    Sem nome: {(~has_name).sum()}")
if (~has_name).sum() > 0:
    print(f"      -> Arquivos sem nome:")
    for src in df[~has_name]['Source File']:
        print(f"         {src}")

# 4. Dominant eye
print(f"\n[4] OLHO DOMINANTE")
od_yes = df['OD Dominant'].str.strip().str.lower() == 'yes' if 'OD Dominant' in df.columns else pd.Series([False]*len(df))
os_yes = df['OS Dominant'].str.strip().str.lower() == 'yes' if 'OS Dominant' in df.columns else pd.Series([False]*len(df))
print(f"    Pacientes com OD Dominant = yes: {od_yes.sum()}")
print(f"    Pacientes com OS Dominant = yes: {os_yes.sum()}")
print(f"    Pacientes sem olho dominante detectado: {((~od_yes) & (~os_yes)).sum()}")

# 5. Key field coverage
print(f"\n[5] COBERTURA DOS CAMPOS PRINCIPAIS (% preenchidos)")
key_cols = {
    'Patient Name': 'Patient Name',
    'OD Pre Sphere': 'OD Pre Sphere (D)',
    'OD Pre Cylinder': 'OD Pre Cylinder (D)',
    'OD Pre Min Add': 'OD Pre Min Add (D)',
    'OS Pre Sphere': 'OS Pre Sphere (D)',
    'OS Pre Cylinder': 'OS Pre Cylinder (D)',
    'OS Pre Min Add': 'OS Pre Min Add (D)',
    'OD Equi Sphere': 'OD Equi Sphere (D)',
    'OD Equi Q Target': 'OD Equi Q Target',
    'OS Equi Sphere': 'OS Equi Sphere (D)',
    'OS Equi Q Target': 'OS Equi Q Target',
}
for label, col in key_cols.items():
    if col in df.columns:
        n_filled = df[col].notna().sum() - (df[col].astype(str).str.strip() == '').sum()
        pct = 100 * n_filled / len(df)
        bar = '#' * int(pct / 5)
        print(f"    {label:<22} [{bar:<20}] {pct:.1f}%")
    else:
        print(f"    {label:<22} [COLUNA NAO ENCONTRADA]")

# 6. Cross-check with file system
import re
def get_base_name(f): return re.sub(r"\s*\(\d+\)\s*$", "", Path(f).stem).strip().lower()
all_pdfs_fs = list(DIR1.glob('**/*.pdf'))
comet_pdfs = list(DIR2.glob('strategy_*.pdf')) if DIR2.exists() else []
all_pdfs = all_pdfs_fs + comet_pdfs
fs_bases = set(get_base_name(p) for p in all_pdfs)
csv_bases = set(get_base_name(s) for s in df['Source File'])
in_csv_not_fs = csv_bases - fs_bases
in_fs_not_csv = fs_bases - csv_bases
print(f"\n[6] CRUZAMENTO COM SISTEMA DE ARQUIVOS")
print(f"    PDFs únicos no disco: {len(fs_bases)}")
print(f"    Registros no CSV: {len(csv_bases)}")
print(f"    No CSV mas sem PDF no disco: {len(in_csv_not_fs)}")
if in_csv_not_fs:
    for b in sorted(in_csv_not_fs)[:10]: print(f"      -> {b}")
print(f"    PDFs no disco sem registro no CSV: {len(in_fs_not_csv)}")
if in_fs_not_csv:
    for b in sorted(in_fs_not_csv)[:10]: print(f"      -> {b}")

# 7. Excel audit
print(f"\n[7] TABELA EXCEL FINAL (Área de Trabalho)")
try:
    xls = pd.read_excel(EXCEL_PATH, header=1)
    print(f"    Total de linhas no Excel: {len(xls)}")
    col_name = [c for c in xls.columns if 'name' in str(c).lower() or 'nome' in str(c).lower()]
    if col_name:
        filled = xls[col_name[0]].notna().sum()
        print(f"    Linhas com nome preenchido: {filled}")
except Exception as e:
    print(f"    Erro ao ler Excel: {e}")

print(f"\n{'='*70}")
print(f"  RESUMO FINAL")
print(f"{'='*70}")
print(f"  Total de pacientes unicos no banco: {len(df)}")
print(f"  Nomes preenchidos: {has_name.sum()}")
print(f"  Duplicatas no CSV: {len(dup_names)}")
print(f"  PDFs sem registro: {len(in_fs_not_csv)}")
print(f"{'='*70}")
