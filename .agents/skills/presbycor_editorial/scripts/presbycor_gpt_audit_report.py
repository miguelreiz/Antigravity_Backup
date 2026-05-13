#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT‑style audit report for PresbyCor markdown chapters.
The script scans all chapter *.md files and produces a **suggestion report**
without touching the original files.  It focuses on:
  * Unicode escape literals (e.g. \\u003e, \\u0026)
  * Classic Portuguese orthographic errors (using an expanded typo map)
  * Heading capitalization inconsistencies
  * Excessive blank lines (suggest removal)
  * Residual boilerplate text at the end of chapters
  * Reference numbering jumps or duplicates (reported for manual review)
The output is a markdown file `GPT_Audit_Report.md` placed in the project root.
"""
import re, sys, io
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent

CHAPTERS = [
    "Preface_Methodology.md",
    "Chapter_1_Complete.md", "Chapter_2_Complete.md", "Chapter_3_Complete.md",
    "Chapter_4_Complete.md", "Chapter_5_Complete.md", "Chapter_6_Complete.md",
    "Chapter_7_Complete.md", "Chapter_8_Complete.md", "Chapter_9_Complete.md",
    "Chapter_10_Complete.md", "Chapter_11_Complete.md", "Chapter_12_Complete.md",
    "Chapter_13_Complete.md",
]

# ---------------------------------------------------------------------------
# Expanded typo dictionary (same as used in the fixer, but here we only *suggest*
# ---------------------------------------------------------------------------
TYPO_FIXES = {
    r'\\bextenção\\b': 'extensão', r'\\bExtenção\\b': 'Extensão',
    r'\\baberraturas\\b': 'aberrações', r'\\bAberraturas\\b': 'Aberrações',
    r'\\bmimética a óptica\\b': 'mimetiza a óptica',
    r'\\bconcerteza\\b': 'com certeza', r'\\bConcerteza\\b': 'Com certeza',
    r'\\bexcessão\\b': 'exceção', r'\\bExcessão\\b': 'Exceção',
    r'\\bexcessões\\b': 'exceções', r'\\bExcessões\\b': 'Exceções',
    r'\\bprecizo\\b': 'preciso', r'\\bPrecizo\\b': 'Preciso',
    r'\\bprecizão\\b': 'precisão', r'\\bPrecizão\\b': 'Precisão',
    r'\\bincluíndo\\b': 'incluindo', r'\\bIncluíndo\\b': 'Incluindo',
    r'\\bsubstituíndo\\b': 'substituindo', r'\\bSubstituíndo\\b': 'Substituindo',
    r'\\bdiminuíndo\\b': 'diminuindo', r'\\bDiminuíndo\\b': 'Diminuindo',
    r'\\bdiscuçao\\b': 'discussão', r'\\bDiscuçao\\b': 'Discussão',
    r'\\bdiscuçoes\\b': 'discussões', r'\\bDiscuçoes\\b': 'Discussões',
    r'\\bresção\\b': 'resecção', r'\\bResção\\b': 'Resecção',
    r'\\becessão\\b': 'exceção', r'\\bEcessão\\b': 'Exceção',
    r'\\bcomprensão\\b': 'compreensão', r'\\bComprensão\\b': 'Compreensão',
    r'\\bdesenpenho\\b': 'desempenho', r'\\bDesenpenho\\b': 'Desempenho',
    r'\\bacompainhamento\\b': 'acompanhamento',
    r'\\bbenifício\\b': 'benefício', r'\\bBenifício\\b': 'Benefício',
    r'\\bconseguênc\\b': 'consequênc',
    r'\\bcomprimisso\\b': 'compromisso', r'\\bComprimisso\\b': 'Compromisso',
    r'\\binfluênciar\\b': 'influenciar', r'\\bInfluênciar\\b': 'Influenciar',
    r'\\binfluênciado\\b': 'influenciado',
    r'\\bpofundidade\\b': 'profundidade', r'\\bPofundidade\\b': 'Profundidade',
    r'\\brefracção\\b': 'refração', r'\\bRefracção\\b': 'Refração',
    r'\\bcorrecção\\b': 'correção', r'\\bCorrecção\\b': 'Correção',
    r'\\bprotecção\\b': 'proteção', r'\\bProtecção\\b': 'Proteção',
    r'\\bdirecção\\b': 'direção', r'\\bDirecção\\b': 'Direção',
    r'\\bdisecção\\b': 'dissecção', r'\\bDisecção\\b': 'Dissecção',
    r'\\bacção\\b': 'ação', r'\\bAccção\\b': 'Ação',
    r'\\breacção\\b': 'reação', r'\\bReacção\\b': 'Reação',
    r'\\babstracção\\b': 'abstração',
    r'\\bsobrecorrecção\\b': 'sobrecorreção',
    r'\\bhipocorrecção\\b': 'hipocorreção',
    r'\\bhipercorrecção\\b': 'hipercorreção',
    r'\\btaxa de retratamento\\b': 'Taxa de Retratamento',
    r'\\btaxa de enhancement\\b': 'Taxa de Enhancement',
}

UNICODE_ESCAPES = {
    r'\\u003e': '>', r'\\u003E': '>',
    r'\\u003c': '<', r'\\u003C': '<',
    r'\\u0026': '&',
    r'\\u00e9': 'é', r'\\u00e3': 'ã', r'\\u00f3': 'ó', r'\\u00ed': 'í',
    r'\\u00e7': 'ç', r'\\u00e1': 'á', r'\\u00fa': 'ú', r'\\u00ea': 'ê',
    r'\\u00f4': 'ô', r'\\u00e2': 'â',
}

def find_unicode_issues(text):
    issues = []
    for esc, repl in UNICODE_ESCAPES.items():
        for m in re.finditer(re.escape(esc), text):
            line = text[:m.start()].count('\n') + 1
            snippet = text[m.start():m.start()+30].replace('\n',' ')
            issues.append((line, esc, repl, snippet))
    return issues

def find_typo_issues(text):
    issues = []
    for pattern, replacement in TYPO_FIXES.items():
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            line = text[:m.start()].count('\n') + 1
            original = m.group(0)
            issues.append((line, original, replacement))
    return issues

def find_heading_caps(text):
    issues = []
    for i, line in enumerate(text.split('\n'), start=1):
        m = re.match(r'^(#{1,4}\s+\d+\.\d+[\.\d]*\s+)([a-z])', line)
        if m:
            issues.append((i, line.strip()))
    return issues

def find_excess_blank(text):
    issues = []
    # locate runs of 4+ blank lines
    for m in re.finditer(r'(\n{4,})', text):
        line = text[:m.start()].count('\n') + 1
        issues.append((line, len(m.group(0).split('\n'))-1))
    return issues

def find_trailing_garbage(text):
    issues = []
    patterns = [r'Pronto para copiar para o Google Drive!?', r'\*\*Este Capítulo \d+ está agora COMPLETO\*\*']
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            line = text[:m.start()].count('\n') + 1
            issues.append((line, m.group(0)))
    return issues

def audit_references(text):
    issues = []
    refs = re.findall(r'^(\d+)\.\s', text, re.MULTILINE)
    if not refs:
        return issues
    nums = [int(r) for r in refs]
    for i in range(len(nums)-1):
        if nums[i+1] != nums[i]+1:
            issues.append(f"Salto de numeração: {nums[i]} -> {nums[i+1]}")
    dup = Counter(nums)
    for n,c in dup.items():
        if c>1:
            issues.append(f"Referência {n} duplicada ({c}x)")
    return issues

def process_file(fname):
    path = PROJECT_ROOT / fname
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
    report = []
    u = find_unicode_issues(txt)
    if u:
        report.append('**Unicode escapes**')
        for line, esc, repl, snippet in u:
            report.append(f"- Linha {line}: `{esc}` → `{repl}` (ex.: `{snippet}`)")
    t = find_typo_issues(txt)
    if t:
        report.append('**Ortografia**')
        for line, orig, corr in t:
            report.append(f"- Linha {line}: `{orig}` → `{corr}`")
    h = find_heading_caps(txt)
    if h:
        report.append('**Capítulos – Heading capitalização**')
        for line, content in h:
            report.append(f"- Linha {line}: `{content}` (primeira letra minúscula)")
    b = find_excess_blank(txt)
    if b:
        report.append('**Linhas vazias excessivas**')
        for line, count in b:
            report.append(f"- Linha {line}: {count} linhas vazias consecutivas")
    g = find_trailing_garbage(txt)
    if g:
        report.append('**Texto residual**')
        for line, snippet in g:
            report.append(f"- Linha {line}: `{snippet}`")
    r = audit_references(txt)
    if r:
        report.append('**Referências**')
        for item in r:
            report.append(f"- {item}")
    return report

def main():
    out_path = PROJECT_ROOT / 'GPT_Audit_Report.md'
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write('# GPT‑Based Audit Report – PresbyCor\n\n')
        out.write(f'Projeto: `{PROJECT_ROOT}`\n\n')
        total_issues = 0
        for chap in CHAPTERS:
            rep = process_file(chap)
            out.write(f'## {chap}\n')
            if not rep:
                out.write('*(arquivo não encontrado ou sem problemas detectados)*\n\n')
                continue
            if not rep:
                out.write('Sem sugestões encontradas.\n\n')
            else:
                for line in rep:
                    out.write(line + '\n')
                out.write('\n')
                total_issues += len(rep)
        out.write(f'**Total de sugestões geradas:** {total_issues}\n')
    print(f"[GPT‑Audit] Relatório gerado: {out_path}")

if __name__ == '__main__':
    main()
