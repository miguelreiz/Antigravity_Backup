import os
import shutil
import glob
import csv
from datetime import datetime

def package_images():
    source_root = "figures"
    dest_root = "_Export_To_Drive/ENTREGA_IMAGENS_FINAL"
    
    # 1. Setup Destination
    if os.path.exists(dest_root):
        shutil.rmtree(dest_root)
    os.makedirs(dest_root, exist_ok=True)
    
    print(f"📦 Iniciando pacote de imagens: {source_root} -> {dest_root}")
    
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.tiff']
    manifest_data = []
    
    # 2. Walk and Copy
    total_copied = 0
    
    # Get all subdirectories in figures
    chapters = [d for d in os.listdir(source_root) if os.path.isdir(os.path.join(source_root, d))]
    
    for chapter in sorted(chapters):
        chapter_source = os.path.join(source_root, chapter)
        chapter_dest = os.path.join(dest_root, chapter)
        
        # Check for images in this chapter
        images = []
        for ext in image_extensions:
            images.extend(glob.glob(os.path.join(chapter_source, ext)))
            
        if images:
            os.makedirs(chapter_dest, exist_ok=True)
            print(f"  📂 Processando {chapter} ({len(images)} imagens)...")
            
            for img_path in sorted(images):
                img_name = os.path.basename(img_path)
                dest_path = os.path.join(chapter_dest, img_name)
                
                shutil.copy2(img_path, dest_path)
                total_copied += 1
                
                # Add to manifest
                file_size_kb = os.path.getsize(img_path) / 1024
                manifest_data.append([chapter, img_name, f"{file_size_kb:.1f} KB", "OK"])

    # 3. Create Manifest
    manifest_path = os.path.join(dest_root, "MANIFESTO_IMAGENS.csv")
    with open(manifest_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Capitulo', 'Nome do Arquivo', 'Tamanho', 'Status'])
        writer.writerows(manifest_data)
        
    print(f"\n✅ SUCESSO! {total_copied} imagens copiadas.")
    print(f"📄 Manifesto criado em: {manifest_path}")

if __name__ == "__main__":
    package_images()
