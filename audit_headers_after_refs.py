import os
import glob
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*50)
print("AUDITORIA ESTRUTURAL: PROCURANDO ORFAOS APOS REFERENCIAS")
print("="*50)

chapters = glob.glob(r"c:\Users\3D_OCT\Documents\Antigravity\Presbycor\Chapter_*_Complete.md")
chapters.append(r"c:\Users\3D_OCT\Documents\Antigravity\Presbycor\Preface_Methodology.md")

count = 0
for filepath in sorted(chapters):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    ref_idx = -1
    for i, line in enumerate(lines):
        if re.match(r"^#+\s+Referências", line, re.IGNORECASE):
            ref_idx = i
            break
            
    if ref_idx == -1:
        print(f"[{filename}] ERRO: Secao de Referencias NAO ENCONTRADA!")
        continue
        
    orphans = []
    # Loop from ref_idx+1 to end of file
    for i in range(ref_idx + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith("#"):
            orphans.append(f"Linha {i+1}: {line}")
            
    if orphans:
        print(f"\n! [{filename}] ALERTA: Encontrados {len(orphans)} cabecalhos APOS as Referencias!")
        for orphan in orphans:
            print(f"   -> {orphan}")
        count += 1
            
if count == 0:
    print("\n[OK] Nenhum cabecalho orfao detectado! A estrutura esta limpa.")

print("\nAUDITORIA CONCLUIDA.")
