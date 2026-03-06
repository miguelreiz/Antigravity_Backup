#!/usr/bin/env python3
"""
Gerador de DOCX Master - PresbyCor Book
Compila todos os capítulos em um documento Word formatado para editora
"""

import os
import glob
import subprocess
from pathlib import Path

def check_pandoc():
    """Verifica se pandoc está instalado ou usa binário local"""
    # Primeiro tenta usar binário local
    local_pandoc = Path.cwd() / 'pandoc_bin'
    if local_pandoc.exists():
        return str(local_pandoc)
    
    # Tenta usar pandoc do sistema
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            return 'pandoc'
    except FileNotFoundError:
        pass
    
    return None

def generate_master_markdown(chapters, output_path):
    """Gera arquivo markdown master combinando todos os capítulos"""
    
    print(f"📝 Gerando arquivo markdown master...")
    
    with open(output_path, 'w', encoding='utf-8') as master:
        # Metadados YAML
        master.write("---\n")
        master.write("title: \"PresbyCor: Estratégias Modernas para Presbiopia e Mecânica do Laser\"\n")
        master.write("author: \"Dr. Miguel Reis\"\n")
        master.write("date: \"2024 - Edição de Pesquisa\"\n")
        master.write("lang: pt-BR\n")
        master.write("---\n\n")
        
        # Adicionar capítulos
        for i, chapter_file in enumerate(chapters, 1):
            print(f"  ✓ Adicionando {chapter_file.name}")
            
            content = chapter_file.read_text(encoding='utf-8')
            
            # Adicionar quebra de página antes de cada capítulo (exceto o primeiro)
            if i > 1:
                master.write("\n\\newpage\n\n")
            
            master.write(content)
            master.write("\n\n")
    
    print(f"✅ Markdown master gerado: {output_path}")

def convert_to_docx(md_file, docx_file, pandoc_path='pandoc'):
    """Converte markdown para DOCX usando pandoc"""
    
    print(f"\n📄 Convertendo para DOCX...")
    
    cmd = [
        pandoc_path,
        str(md_file),
        '-o', str(docx_file),
        '--resource-path=.',  # Para encontrar imagens
        '--toc',              # Índice automático
        '--toc-depth=2',      # Profundidade do índice
        '--standalone',       # Documento completo
    ]
    
    # Adicionar documento de referência se existir
    ref_doc = Path('reference.docx')
    if ref_doc.exists():
        cmd.extend(['--reference-doc', str(ref_doc)])
        print(f"  ℹ️  Usando documento de referência: {ref_doc}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ DOCX gerado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao converter para DOCX:")
        print(f"   {e.stderr}")
        return False

def main():
    """Função principal"""
    
    print("=" * 80)
    print("📚 GERADOR DE LIVRO MASTER - PresbyCor")
    print("=" * 80)
    
    # Diretórios
    base_dir = Path.cwd()
    output_dir = base_dir / "_Export_To_Drive"
    output_dir.mkdir(exist_ok=True)
    
    # Verificar pandoc
    pandoc_path = check_pandoc()
    if not pandoc_path:
        print("\n⚠️  ERRO: Pandoc não encontrado!")
        print("   Por favor, baixe o pandoc ou aguarde a instalação.")
        return False
    
    print(f"\n✓ Pandoc detectado: {pandoc_path}")
    
    # Encontrar capítulos
    chapter_files = sorted(
        base_dir.glob("Chapter_*_Complete.md"),
        key=lambda f: (
            float(f.stem.split('_')[1].replace('Plus', '.5'))
            if 'Plus' in f.stem.split('_')[1]
            else float(f.stem.split('_')[1])
        )
    )
    
    if not chapter_files:
        print("❌ Nenhum capítulo encontrado!")
        return False
    
    print(f"\n📖 Encontrados {len(chapter_files)} capítulos:")
    for ch in chapter_files:
        print(f"   • {ch.name}")
    
    # Gerar markdown master
    master_md = output_dir / "PresbyCor_Master.md"
    generate_master_markdown(chapter_files, master_md)
    
    # Converter para DOCX
    master_docx = output_dir / "PresbyCor_MASTER_BOOK.docx"
    
    if convert_to_docx(master_md, master_docx, pandoc_path):
        print(f"\n{'=' * 80}")
        print(f"✅ SUCESSO!")
        print(f"{'=' * 80}")
        print(f"\n📁 Arquivo gerado:")
        print(f"   {master_docx.absolute()}")
        print(f"\n📊 Estatísticas:")
        print(f"   • Capítulos: {len(chapter_files)}")
        print(f"   • Tamanho: {master_docx.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Remover arquivo temporário
        if master_md.exists():
            master_md.unlink()
            print(f"\n🧹 Arquivo temporário removido")
        
        return True
    else:
        print(f"\n❌ Falha na conversão")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
