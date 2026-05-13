import os
import re

filepath = r"c:\Users\3D_OCT\Documents\Antigravity\Presbycor\Chapter_2_Complete.md"
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

ref_start = -1
val_start = -1

for i, line in enumerate(lines):
    if re.match(r"^#+\s+Referências", line, re.IGNORECASE):
        ref_start = i
    if line.startswith("## 2.11."):
        val_start = i

if ref_start != -1 and val_start != -1 and val_start > ref_start:
    print(f"Encontrado: Referências na linha {ref_start+1}, Secao 2.11 na linha {val_start+1}. Corrigindo...")
    
    # Busca a divisória '---' que está logo acima das referências (opcional)
    split_ref = ref_start
    if split_ref > 0 and lines[split_ref-1].strip() == "":
        split_ref -= 1
    if split_ref > 0 and lines[split_ref-1].strip() == "---":
        split_ref -= 1
        
    part_main = lines[:split_ref]
    part_ref = lines[split_ref:val_start]
    
    # Verifica se há divisória '---' antes de val_start que deve pertencer a ele
    split_val = val_start
    if split_val > 0 and lines[split_val-1].strip() == "":
        split_val -= 1
    if split_val > 0 and lines[split_val-1].strip() == "---":
        split_val -= 1
        
    part_val = lines[split_val:]
    
    # Remove as linhas extras de part_ref que foram capturadas em part_val
    part_ref = lines[split_ref:split_val]
    
    # Remonta o arquivo: Main -> Seção 2.11 -> --- -> Referências
    new_lines = part_main + ["\n"] + part_val + ["\n\n"] + part_ref
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Correção aplicada com sucesso no Capítulo 2.")
else:
    print("Estrutura já parece correta ou marcadores não encontrados.")
