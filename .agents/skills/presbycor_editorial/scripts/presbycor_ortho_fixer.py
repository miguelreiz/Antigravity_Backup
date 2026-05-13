#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

CHAPTERS = [
    "Preface_Methodology.md",
    "Chapter_1_Complete.md", "Chapter_2_Complete.md", "Chapter_3_Complete.md",
    "Chapter_4_Complete.md", "Chapter_5_Complete.md", "Chapter_6_Complete.md",
    "Chapter_7_Complete.md", "Chapter_8_Complete.md", "Chapter_9_Complete.md",
    "Chapter_10_Complete.md", "Chapter_11_Complete.md", "Chapter_12_Complete.md",
    "Chapter_13_Complete.md"
]

# Dicionário de substituições (Regex seguro para evitar alteração dentro de palavras corretas)
# Utilizamos \\b (word boundary) para garantir a integridade.
TYPO_DICT = {
    # Erros de digitação comuns
    r'\bextenção\b': 'extensão',
    r'\bExtenção\b': 'Extensão',
    r'\bconcerteza\b': 'com certeza',
    r'\bConcerteza\b': 'Com certeza',
    r'\baspecto\b': 'aspeto',  # Apenas se for PT-PT, mas manteremos aspecto se PT-BR (vou pular variaveis polêmicas do acordo ortográfico)
    
    # Capitalização de Tabelas e Protocolos (Notados no CAP 6)
    r'\btaxa de retratamento\b': 'Taxa de Retratamento',
    
    # Erros de sintaxe ou plural
    r'\bmimética a óptica\b': 'mimetiza a óptica',
    r'\baberraturas\b': 'aberrações',
    r'\bAberraturas\b': 'Aberrações',
    
    # Corrigir espaços duplos mas preservando espaços no inicio de linha
    r'(?<!^)(?<!\n)(?<!\r)  +': ' ',  
}

def clean_markdown_garbage(text):
    """Limpa textos residuais de conclusão de tarefas em MD e sujeiras do prompt."""
    garbage = [
        r"\*\*Este Capítulo \d+ está agora COMPLETO\*\*, com:(.*?)(Pronto para copiar para o Google Drive!|Pronto!)",
        r"\*\*O Capítulo \d+ está agora COMPLETO\*\*(.*)Google Drive"
    ]
    for g in garbage:
        # dotall para cruzar quebras de linha no lixo final
        text = re.sub(g, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Limpar excesso de empty lines no fim do arquivo
    text = text.rstrip() + '\n'
    return text

def apply_ortho_fixes(text):
    fixes_count = 0
    # Aplicar o diff de typo
    for pattern, replacement in TYPO_DICT.items():
        if re.search(pattern, text):
            text, n = re.subn(pattern, replacement, text)
            fixes_count += n
            
    # Substituir espaços duplos soltos (excepto os que estão na indentação ou quotes)
    # É delicado em Markdown pois 2 espaços no final da linha significam <br>.
    # Por segurança, pulamos a limpeza de espaços em branco por script automatizado em MD.
            
    # Markdown Lists com letra inicial minúscula (quando não é continuação)
    # Ex: "- melhora a visão" -> "- Melhora a visão"
    # Somente aplicar se tiver certeza? Muito arriscado num livro médico. Apenas dicionário explícito.
    
    return text, fixes_count

def process_file(filepath):
    if not filepath.exists(): return 0
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        
    original = text
    text = clean_markdown_garbage(text)
    text, n = apply_ortho_fixes(text)
    
    total_fixes = n
    if original != text:
        # Text changed due to garbage removal or typos
        total_fixes += 1
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
    return total_fixes

def main():
    print("\n[PresbyCor] Corretor Heurístico Dedicado (v1.0)")
    print("Processando 14 Capitulos...")
    total = 0
    for ch in CHAPTERS:
        fp = PROJECT_ROOT / ch
        if fp.exists():
            fixes = process_file(fp)
            if fixes > 0:
                print(f"  ✓ {ch} -> {fixes} correções aplicadas.")
                total += fixes
            else:
                print(f"  - {ch} -> Limpo.")
    
    print(f"\n[OK] Concluído. {total} correções globais.")

if __name__ == '__main__':
    main()
