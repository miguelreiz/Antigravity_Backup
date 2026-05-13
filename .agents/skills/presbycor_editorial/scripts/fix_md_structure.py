#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
PresbyCor — Structural Markdown Fix Script
==========================================
Corrige erros estruturais em todos os capitulos:
  1. Escapes unicode literais: \\u003e -> >  \\u003c -> <  \\u0026 -> &
  2. Headings com primeira letra minuscula (ex: 'retratamento')
  3. Remove secoes de Referencias Bibliograficas duplicadas
  4. Corrige \\u003e [!NOTE] etc. (alert boxes quebradas)
"""

import re
import os
from pathlib import Path

# scripts/ -> presbycor_editorial/ -> skills/ -> .agents/ -> Presbycor/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

# Capitulos a processar
CHAPTERS = [
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
]

def fix_unicode_escapes(text: str) -> tuple[str, int]:
    """Substitui escapes unicode literais por caracteres reais."""
    fixes = 0
    replacements = [
        (r'\\u003e', '>'),
        (r'\\u003c', '<'),
        (r'\\u0026', '&'),
        (r'\\u003E', '>'),
        (r'\\u003C', '<'),
    ]
    for pattern, replacement in replacements:
        new_text, n = re.subn(pattern, replacement, text)
        fixes += n
        text = new_text
    return text, fixes


def fix_heading_capitalization(text: str) -> tuple[str, int]:
    """Corrige headings que comecam com letra minuscula apos ###."""
    fixes = 0
    lines = text.split('\n')
    result = []
    for line in lines:
        m = re.match(r'^(#{1,4}\s+)([a-z])(.*)', line)
        if m:
            corrected = m.group(1) + m.group(2).upper() + m.group(3)
            result.append(corrected)
            fixes += 1
        else:
            result.append(line)
    return '\n'.join(result), fixes


def remove_duplicate_references(text: str) -> tuple[str, int]:
    """
    Remove secoes de Referencias Bibliograficas duplicadas.
    Mantem apenas a PRIMEIRA ocorrencia.
    """
    marker = '## Referências Bibliográficas'
    marker_alt = '## Referencias Bibliograficas'
    
    # Verificar quantas ocorrencias existem
    count = text.count(marker) + text.count(marker_alt)
    if count <= 1:
        return text, 0
    
    # Encontrar a posicao da primeira e segunda ocorrencia
    first_pos = text.find(marker)
    if first_pos == -1:
        first_pos = text.find(marker_alt)
    
    second_pos = text.find(marker, first_pos + 1)
    if second_pos == -1:
        second_pos = text.find(marker_alt, first_pos + 1)
    
    if second_pos == -1:
        return text, 0
    
    # Remover tudo a partir da segunda ocorrencia ate o final
    # (ou ate o proximo separador --- se existir antes do fim)
    text_before = text[:second_pos].rstrip()
    
    # Verificar se ha conteudo apos a secao duplicada (alem de --- e espacos)
    text_after_dup = text[second_pos:]
    # Procurar por proximo heading de nivel 2 apos a secao duplicada
    next_section = re.search(r'\n## (?!Referências|Referencias)', text_after_dup)
    
    if next_section:
        # Ha mais conteudo apos as refs duplicadas — manter esse conteudo
        remaining = text_after_dup[next_section.start():]
        text = text_before + '\n\n' + remaining.lstrip()
    else:
        # A secao duplicada e o fim do arquivo — apenas remover
        text = text_before + '\n'
    
    return text, count - 1


def fix_file(filepath: Path) -> dict:
    """Aplica todas as correcoes em um arquivo."""
    if not filepath.exists():
        return {'file': filepath.name, 'skipped': True, 'reason': 'nao encontrado'}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()
    
    text = original
    total_fixes = 0
    report = {'file': filepath.name, 'fixes': {}}
    
    # 1. Escapes unicode
    text, n = fix_unicode_escapes(text)
    if n:
        report['fixes']['unicode_escapes'] = n
        total_fixes += n
    
    # 2. Capitalizacao de headings
    text, n = fix_heading_capitalization(text)
    if n:
        report['fixes']['heading_caps'] = n
        total_fixes += n
    
    # 3. Referencias duplicadas
    text, n = remove_duplicate_references(text)
    if n:
        report['fixes']['duplicate_refs'] = n
        total_fixes += n
    
    report['total_fixes'] = total_fixes
    
    if total_fixes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        report['saved'] = True
    else:
        report['saved'] = False
    
    return report


def main():
    print("\n[PresbyCor] Structural Markdown Fix — Todos os Capitulos")
    print(f"[Projeto] {PROJECT_ROOT}\n")
    
    total_files_fixed = 0
    total_corrections = 0
    
    for chapter_file in CHAPTERS:
        filepath = PROJECT_ROOT / chapter_file
        report = fix_file(filepath)
        
        if report.get('skipped'):
            print(f"  [SKIP] {report['file']} — {report.get('reason', '')}")
            continue
        
        if report['total_fixes'] > 0:
            fixes_detail = ', '.join(f"{k}: {v}" for k, v in report['fixes'].items())
            print(f"  [OK] {report['file']} — {report['total_fixes']} correccoes ({fixes_detail})")
            total_files_fixed += 1
            total_corrections += report['total_fixes']
        else:
            print(f"  [--] {report['file']} — sem erros estruturais")
    
    print(f"\n{'='*50}")
    print(f"[Resumo] {total_files_fixed} arquivos corrigidos, {total_corrections} correccoes totais")
    
    return total_files_fixed, total_corrections


if __name__ == '__main__':
    main()
