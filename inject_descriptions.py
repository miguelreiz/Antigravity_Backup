import os, glob, re
from pathlib import Path

def get_description_from_md(md_path):
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        # Ignore first line if it's the title
        if lines and lines[0].startswith('# Infográfico'):
            lines = lines[1:]
        return '\n'.join(lines).strip()
    except Exception as e:
        print(f"Erro lendo {md_path}: {e}")
        return ""

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping {file_path} due to read error: {e}")
        return False

    original_content = content
    
    # 1. DELETE 'Infográficos Clínicos Sugeridos' section
    # Matches '## Infográficos Clínicos Sugeridos' until the end of document or next '## '
    pattern_delete = r'\n?## Infográficos Clínicos Sugeridos.*?(\Z|\n# |\n---)'
    
    match = re.search(pattern_delete, content, flags=re.DOTALL)
    if match:
        # Keep the group 1 (which is the boundary like \n--- or \n# )
        end_boundary = match.group(1) if match.group(1) else ""
        content = content[:match.start()] + end_boundary + content[match.end():]
        print(f"DELETADO bloco residual em: {file_path}")

    # For safety, let's also delete just the title if it's lingering
    content = content.replace("## Infográficos Clínicos Sugeridos\n", "")

    # 2. Inject descriptions from md files
    for md_path in glob.glob('figures/**/*.md', recursive=True):
        p = Path(md_path)
        desc = get_description_from_md(md_path)
        if not desc or len(desc) < 50:
            continue
            
        # Infer png name
        png_name = None
        md_text = open(md_path, 'r', encoding='utf-8').read()
        png_match = re.search(r'\((figures/[^)]+\.png)\)', md_text)
        if png_match:
            png_name = Path(png_match.group(1)).name
        else:
            parts = p.stem.split('_')
            if len(parts) >= 4:
                png_name = '_'.join(parts[3:]) + '.png'
            else:
                png_name = p.stem + '.png'
                
        # Find where this PNG is used in `content`
        escaped_png = re.escape(png_name)
        # Look for ![...](.../png_name.png)
        # Followed optionally by caption line starting with *
        # We want to capture the whole block to append to it
        img_pattern = re.compile(r'(!\[.*?\]\([^)]*' + escaped_png + r'\)(?:\n\*[^*]+\*)?)')
        
        matches = img_pattern.findall(content)
        if matches:
            for match in matches:
                # Check if we already injected it
                snippet = desc[:30].strip()
                if snippet not in content:
                    injection = match + "\n\n**Detalhes da Imagem:**\n\n" + desc + "\n"
                    content = content.replace(match, injection)
                    print(f"INJETADO texto de {p.name} em {file_path}")

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files_to_check = glob.glob('Chapter_*_Complete.md')
    files_to_check += ['PresbyCor_FULL_BOOK.md', 'PresbyCor_Livro_Final_Com_Imagens.md']
    
    export_clean = os.path.join('_Export_To_Drive', 'PresbyCor_Master_Clean.md')
    if os.path.exists(export_clean):
        files_to_check.append(export_clean)

    for f in files_to_check:
        if os.path.exists(f):
            process_file(f)

if __name__ == "__main__":
    main()
    print("Processamento concluído.")
