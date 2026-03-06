#!/usr/bin/env python3
"""
Script de Publicação de Versão - Livro PresbyCor
Compila o livro e gera versão numerada automaticamente para Google Drive
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Diretórios
PROJECT_ROOT = Path(__file__).parent
EXPORT_DIR = PROJECT_ROOT / "_Export_To_Drive"
VERSION_FILE = EXPORT_DIR / "version_history.json"
PANDOC_BIN = PROJECT_ROOT / "pandoc_bin"

def load_version_history():
    """Carrega histórico de versões"""
    if VERSION_FILE.exists():
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"versions": [], "current_version": "1.0.0"}

def save_version_history(history):
    """Salva histórico de versões"""
    EXPORT_DIR.mkdir(exist_ok=True)
    with open(VERSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def increment_version(version, bump_type="patch"):
    """Incrementa número de versão"""
    major, minor, patch = map(int, version.split('.'))
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1
    
    return f"{major}.{minor}.{patch}"

def compile_book():
    """Compila livro master"""
    print("📝 Compilando livro...")
    
    # Executar script de compilação
    result = subprocess.run(
        ["python3", "compile_master_book.py"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Erro na compilação:\n{result.stderr}")
        return False
    
    print("✅ Markdown master gerado")
    return True

def clean_yaml_issues(master_file):
    """Remove blocos YAML problemáticos"""
    with open(master_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    cleaned_lines = []
    in_yaml = False
    yaml_count = 0
    
    for line in lines:
        if line.strip() == '---':
            if yaml_count == 0:
                cleaned_lines.append(line)
                yaml_count += 1
            elif not in_yaml:
                in_yaml = True
                continue
            else:
                in_yaml = False
                continue
        elif not in_yaml or yaml_count == 0:
            cleaned_lines.append(line)
    
    clean_file = EXPORT_DIR / "PresbyCor_Master_Clean.md"
    with open(clean_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))
    
    return clean_file

def convert_to_docx(markdown_file, output_file):
    """Converte Markdown para DOCX"""
    print(f"📄 Convertendo para DOCX: {output_file.name}")
    
    cmd = [
        str(PANDOC_BIN),
        str(markdown_file),
        '-o', str(output_file),
        '--toc',
        '--toc-depth=3',
        '-f', 'markdown+emoji'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Erro na conversão:\n{result.stderr}")
        return False
    
    print(f"✅ DOCX gerado: {output_file.name}")
    return True

def create_changelog_entry():
    """Solicita descrição das mudanças"""
    print("\n📝 Descrição das mudanças nesta versão:")
    print("(Digite uma linha de cada vez, linha vazia para finalizar)")
    
    changes = []
    while True:
        line = input("  • ")
        if not line.strip():
            break
        changes.append(line.strip())
    
    return changes if changes else ["Atualização geral"]

def main():
    """Função principal"""
    print("=" * 80)
    print("📚 PUBLICADOR DE VERSÃO - PresbyCor")
    print("=" * 80)
    print()
    
    # Carregar histórico
    history = load_version_history()
    current_version = history["current_version"]
    
    print(f"📌 Versão atual: {current_version}")
    print()
    
    # Perguntar tipo de incremento
    print("Tipo de incremento:")
    print("  1. Patch (bugfix, pequenas correções) - ex: 1.0.0 → 1.0.1")
    print("  2. Minor (novos conteúdos, melhorias) - ex: 1.0.0 → 1.1.0")
    print("  3. Major (reestruturação grande) - ex: 1.0.0 → 2.0.0")
    print()
    
    bump_choice = input("Escolha (1/2/3) [1]: ").strip() or "1"
    bump_types = {"1": "patch", "2": "minor", "3": "major"}
    bump_type = bump_types.get(bump_choice, "patch")
    
    # Nova versão
    new_version = increment_version(current_version, bump_type)
    print(f"\n🆕 Nova versão: {new_version}")
    
    # Solicitar changelog
    changes = create_changelog_entry()
    
    # Compilar livro
    print()
    if not compile_book():
        return
    
    # Limpar YAML
    master_file = EXPORT_DIR / "PresbyCor_Master.md"
    clean_file = clean_yaml_issues(master_file)
    print("✅ YAML limpo")
    
    # Converter para DOCX
    timestamp = datetime.now().strftime("%Y%m%d")
    output_filename = f"PresbyCor_v{new_version}_{timestamp}.docx"
    output_file = EXPORT_DIR / output_filename
    
    if not convert_to_docx(clean_file, output_file):
        return
    
    # Obter tamanho do arquivo
    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    
    # Atualizar histórico
    version_entry = {
        "version": new_version,
        "date": datetime.now().isoformat(),
        "filename": output_filename,
        "size_mb": round(file_size_mb, 2),
        "changes": changes
    }
    
    history["versions"].append(version_entry)
    history["current_version"] = new_version
    save_version_history(history)
    
    # Relatório final
    print()
    print("=" * 80)
    print("✅ PUBLICAÇÃO CONCLUÍDA")
    print("=" * 80)
    print()
    print(f"📦 Arquivo: {output_filename}")
    print(f"📊 Tamanho: {file_size_mb:.2f} MB")
    print(f"🔢 Versão: {new_version}")
    print()
    print("📝 Mudanças:")
    for change in changes:
        print(f"  • {change}")
    print()
    print("📤 Próximo passo:")
    print(f"   Faça upload de '{output_filename}' para o Google Drive")
    print()
    print(f"📍 Localização: {output_file}")
    print()

if __name__ == "__main__":
    main()
