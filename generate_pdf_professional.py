#!/usr/bin/env python3
"""
Gerador automático de PDF profissional do livro PresbyCor
Converte todos os Markdown para PDF com imagens embutidas
"""

import markdown
from weasyprint import HTML, CSS
import os
from pathlib import Path

print("📚 Gerando PDF Profissional do PresbyCor...")
print("=" * 60)

# Base directory
base_dir = Path("/Users/miguelreis/Downloads/Takeout/NotebookLM/PresbyCor_ Modern Strategies for Presbyopia and La")
os.chdir(base_dir)

# Ordem dos capítulos
chapters = [
    "Preface_Methodology.md",
    "Chapter_1_Complete.md",
    "Chapter_2_Complete.md",
    "Chapter_3_Complete.md",
    "Chapter_4_Complete.md",
    "Chapter_5_Complete.md",
    "Chapter_6_Complete.md",
    "Chapter_7_Complete.md",
    "Chapter_8_Complete.md",
    "Chapter_9_Complete.md",
    "Chapter_10_Complete.md",
    "Chapter_11_Complete.md",
    "Chapter_12_Complete.md",
    "Chapter_13_Complete.md",
    "Bibliography_Consolidated.md",
    "Glossary_Abbreviations.md",
    "Appendices_Technical.md",
    "About_Author.md"
]

# Ler e consolidar todo o conteúdo
full_markdown = ""
for chapter in chapters:
    print(f"✓ Processando: {chapter}")
    if os.path.exists(chapter):
        with open(chapter, 'r', encoding='utf-8') as f:
            content = f.read()
            full_markdown += f"\n\n---\n\n{content}\n\n"
    else:
        print(f"  ⚠️ Arquivo não encontrado: {chapter}")

# Converter Markdown para HTML
print("\n🔧 Convertendo Markdown → HTML...")
md = markdown.Markdown(extensions=['extra', 'toc', 'tables', 'fenced_code'])
html_content = md.convert(full_markdown)

# Template HTML com CSS profissional
html_template = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>PresbyCor: Modern Strategies for Presbyopia and Laser Mechanics</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm;
            @top-center {{
                content: "PresbyCor - Dr. Miguel Reis";
                font-size: 9pt;
                color: #666;
            }}
            @bottom-center {{
                content: "Página " counter(page);
                font-size: 9pt;
                color: #666;
            }}
        }}
        
        body {{
            font-family: 'Georgia', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }}
        
        h1 {{
            font-size: 24pt;
            color: #1565c0;
            page-break-before: always;
            margin-top: 2cm;
            border-bottom: 3px solid #1565c0;
            padding-bottom: 0.5cm;
        }}
        
        h2 {{
            font-size: 18pt;
            color: #2e7d32;
            margin-top: 1cm;
            border-left: 5px solid #2e7d32;
            padding-left: 0.5cm;
        }}
        
        h3 {{
            font-size: 14pt;
            color: #e65100;
            margin-top: 0.8cm;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1cm auto;
            page-break-inside: avoid;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0.5cm 0;
            font-size: 10pt;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        
        th {{
            background-color: #1565c0;
            color: white;
            font-weight: bold;
        }}
        
        code {{
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }}
        
        pre {{
            background-color: #f5f5f5;
            padding: 1cm;
            border-left: 4px solid #1565c0;
            overflow-x: auto;
            page-break-inside: avoid;
        }}
        
        blockquote {{
            border-left: 5px solid #ff9800;
            padding-left: 1cm;
            margin-left: 0;
            font-style: italic;
            background-color: #fff3e0;
            padding: 0.5cm 0.5cm 0.5cm 1cm;
        }}
        
        .title-page {{
            text-align: center;
            padding-top: 5cm;
            page-break-after: always;
        }}
        
        .title-page h1 {{
            font-size: 36pt;
            color: #1565c0;
            border: none;
            page-break-before: avoid;
            margin-top: 0;
        }}
        
        .title-page .author {{
            font-size: 18pt;
            margin-top: 2cm;
            color: #666;
        }}
        
        .title-page .date {{
            font-size: 14pt;
            margin-top: 1cm;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <h1>PresbyCor</h1>
        <h2 style="border:none; color:#666;">Modern Strategies for Presbyopia<br/>and Laser Mechanics</h2>
        <p class="author">Dr. Miguel Reis<br/>Médico Oftalmologista<br/>Especialista em Cirurgia Refrativa e Córnea</p>
        <p class="date">Janeiro 2026</p>
    </div>
    
    {html_content}
</body>
</html>
"""

# Salvar HTML temporário
html_file = "/tmp/presbycor_temp.html"
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✓ HTML gerado")

# Gerar PDF
print("\n📄 Gerando PDF...")
output_pdf = os.path.expanduser("~/Desktop/PresbyCor_Professional_Complete_20260103.pdf")

HTML(html_file, base_url=str(base_dir)).write_pdf(
    output_pdf,
    stylesheets=[],
    presentational_hints=True
)

print(f"\n✅ PDF criado com sucesso!")
print(f"📍 Localização: {output_pdf}")
print(f"\n📊 Estatísticas:")
print(f"   - Capítulos processados: {len([c for c in chapters if os.path.exists(c)])}")
print(f"   - Tamanho estimado: {os.path.getsize(output_pdf) / (1024*1024):.1f} MB")
print("\n" + "=" * 60)
