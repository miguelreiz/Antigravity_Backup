import re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent.parent.parent
md_files = list(root.glob("Chapter_*.md")) + [root / "Preface_Methodology.md"]

# Encontrar todas as imagens mencionadas nos MDs
linked_images = set()
for md in md_files:
    if not md.exists(): continue
    text = md.read_text(encoding="utf8")
    for match in re.finditer(r'!\[.*?\]\((.*?)\)', text):
        path_str = match.group(1).split('/')[-1] # just filename
        linked_images.add(path_str.lower())

# Encontrar todas as imagens reais na pasta figures
fig_dir = root / "figures"
actual_images = set()
if fig_dir.exists():
    for f in fig_dir.rglob("*.*"):
        if f.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            actual_images.add(f.name.lower())

print(f"Total linked in MDs: {len(linked_images)}")
print(f"Total actual in figures/: {len(actual_images)}")

missing_in_md = actual_images - linked_images
missing_on_disk = linked_images - actual_images

print("\n--- IMAGENS NA PASTA MAS NÃO USADAS NOS MDs (INFOGRÁFICOS ESQUECIDOS?) ---")
for m in sorted(missing_in_md):
    path = list(fig_dir.rglob(m))[0] if list(fig_dir.rglob(m)) else m
    print(f"Orphan: {path}")

print("\n--- IMAGENS USADAS NOS MDs MAS NÃO ENCONTRADAS NA PASTA ---")
for m in sorted(missing_on_disk):
    print(f"Missing file: {m}")
