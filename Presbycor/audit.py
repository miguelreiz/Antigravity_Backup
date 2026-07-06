import pandas as pd
csv_df = pd.read_csv(r'C:\Users\3D_OCT\Documents\Antigravity\Presbycor\Presbycor_Database_Completo.csv')
print(f"Total records in CSV: {len(csv_df)}")
print(f"Records with Patient Name: {csv_df['Patient Name'].notna().sum()}")
print(f"Records with OD Dominant: {csv_df['OD Dominant'].notna().sum()}")
print(f"Records with OS Dominant: {csv_df['OS Dominant'].notna().sum()}")

xls_df = pd.read_excel(r'C:\Users\3D_OCT\Desktop\Presbycor_Database_Final_Consolidado.xlsx', header=1)
print(f"Total records in Final Excel: {len(xls_df)}")
