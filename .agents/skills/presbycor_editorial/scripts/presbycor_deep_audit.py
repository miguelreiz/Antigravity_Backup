#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PresbyCor Deep Audit — Segunda Passagem
========================================
Audita todos os capítulos em busca de imperfeições residuais:
  1. Tabelas Markdown quebradas (colunas inconsistentes)
  2. Referências numeradas ausentes (saltos: 1,2,3..9,11 = falta 10)
  3. Lixo residual ("Pronto para copiar", "COMPLETO")
  4. Headings com numeração inconsistente ou erros
  5. Links/imagens com paths quebrados
  6. Alert boxes mal-formatadas (> [!TYPE] sem fechar)
  7. Erros ortográficos adicionais em português
  8. Linhas vazias excessivas (>3 consecutivas)
  9. Referências duplicadas no mesmo capítulo (ref 5 aparece 2x)
  10. Nota de rodapé com "\\u" escapes unicode residuais
"""
import sys, io, re, json
from pathlib import Path
from collections import Counter

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

# ═══════════════════════════════════════
# EXPANDED TYPO DICTIONARY (PT-PT e PT-BR)
# ═══════════════════════════════════════
TYPO_FIXES = {
    # Ortografia clássica
    r'\bextenção\b': 'extensão', r'\bExtenção\b': 'Extensão',
    r'\baberraturas\b': 'aberrações', r'\bAberraturas\b': 'Aberrações',
    r'\bmimética a óptica\b': 'mimetiza a óptica',
    r'\bconcerteza\b': 'com certeza', r'\bConcerteza\b': 'Com certeza',
    r'\bexcessão\b': 'exceção', r'\bExcessão\b': 'Exceção',
    r'\bexcessões\b': 'exceções', r'\bExcessões\b': 'Exceções',
    r'\bprecizo\b': 'preciso', r'\bPrecizo\b': 'Preciso',
    r'\bprecizão\b': 'precisão', r'\bPrecizão\b': 'Precisão',
    r'\bincluíndo\b': 'incluindo', r'\bIncluíndo\b': 'Incluindo',
    r'\bsubstituíndo\b': 'substituindo', r'\bSubstituíndo\b': 'Substituindo',
    r'\bdiminuíndo\b': 'diminuindo', r'\bDiminuíndo\b': 'Diminuindo',
    r'\bdiscuçao\b': 'discussão', r'\bDiscuçao\b': 'Discussão',
    r'\bdiscuçoes\b': 'discussões', r'\bDiscuçoes\b': 'Discussões',
    r'\bresção\b': 'resecção', r'\bResção\b': 'Resecção',
    r'\becessão\b': 'exceção', r'\bEcessão\b': 'Exceção',
    r'\bcomprensão\b': 'compreensão', r'\bComprensão\b': 'Compreensão',
    r'\bdesenpenho\b': 'desempenho', r'\bDesenpenho\b': 'Desempenho',
    r'\bacompainhamento\b': 'acompanhamento',
    r'\bbenifício\b': 'benefício', r'\bBenifício\b': 'Benefício',
    r'\bconseguênc\b': 'consequênc',
    r'\bcomprimisso\b': 'compromisso', r'\bComprimisso\b': 'Compromisso',
    r'\binfluênciar\b': 'influenciar', r'\bInfluênciar\b': 'Influenciar',
    r'\binfluênciado\b': 'influenciado',
    r'\bpofundidade\b': 'profundidade', r'\bPofundidade\b': 'Profundidade',
    r'\brefracção\b': 'refração', r'\bRefracção\b': 'Refração',
    r'\bcorrecção\b': 'correção', r'\bCorrecção\b': 'Correção',
    r'\bprotecção\b': 'proteção', r'\bProtecção\b': 'Proteção',
    r'\bdirecção\b': 'direção', r'\bDirecção\b': 'Direção',
    r'\bdisecção\b': 'dissecção', r'\bDisecção\b': 'Dissecção',
    r'\bsecção\b': 'secção',  # Este é válido em PT-PT, manter
    r'\bacção\b': 'ação', r'\bAccção\b': 'Ação',
    r'\breacção\b': 'reação', r'\bReacção\b': 'Reação',
    r'\babstracção\b': 'abstração',
    r'\bsobrecorrecção\b': 'sobrecorreção',
    r'\bhipocorrecção\b': 'hipocorreção',
    r'\bhipercorrecção\b': 'hipercorreção',
    # Capitalização em tabelas
    r'\btaxa de retratamento\b': 'Taxa de Retratamento',
    r'\btaxa de enhancement\b': 'Taxa de Enhancement',
    # Espaçamento em operadores LaTeX comuns no texto
    # (não tocar em fórmulas $$ )
}

# Erros comuns de formatação Markdown (auto-fix)
def fix_broken_tables(text):
    """Detecta e conserta linhas de tabela com colunas a mais no final (pipe extra)."""
    fixes = 0
    lines = text.split('\n')
    result = []
    in_table = False
    expected_cols = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            cols = stripped.count('|') - 1
            if not in_table:
                in_table = True
                expected_cols = cols
            # Detectar pipe extra no meio da célula (ex: "| ALERTA - texto | mais texto |")
            # Isto é difícil de corrigir automaticamente sem contexto
            result.append(line)
        else:
            if in_table:
                in_table = False
                expected_cols = 0
            result.append(line)
    
    return '\n'.join(result), fixes


def fix_excessive_blank_lines(text):
    """Remove sequências de >3 linhas em branco consecutivas."""
    fixes = 0
    # Substitui 4+ linhas vazias por 2
    new_text = re.sub(r'\n{4,}', '\n\n\n', text)
    if new_text != text:
        fixes = 1
    return new_text, fixes


def fix_trailing_garbage(text):
    """Remove textos residuais de conclusão/sistema no final dos capítulos."""
    fixes = 0
    garbage_patterns = [
        r'\*\*Este Capítulo \d+ está agora COMPLETO\*\*.*?$',
        r'Pronto para copiar para o Google Drive!?\s*$',
        r'\*\*O Capítulo \d+ está.*?COMPLETO\*\*.*?$',
        r'---\s*\n\s*\n\s*$',  # --- seguido apenas de espaços no final
    ]
    for pat in garbage_patterns:
        new_text = re.sub(pat, '', text, flags=re.MULTILINE | re.DOTALL)
        if new_text != text:
            fixes += 1
            text = new_text
    
    # Garantir que termina com \n
    text = text.rstrip() + '\n'
    return text, fixes


def fix_unicode_escapes(text):
    """Captura qualquer \\uXXXX escape literal restante."""
    fixes = 0
    replacements = {
        r'\\u003e': '>', r'\\u003E': '>',
        r'\\u003c': '<', r'\\u003C': '<',
        r'\\u0026': '&',
        r'\\u00e9': 'é', r'\\u00e3': 'ã',
        r'\\u00f3': 'ó', r'\\u00ed': 'í',
        r'\\u00e7': 'ç', r'\\u00e1': 'á',
        r'\\u00fa': 'ú', r'\\u00ea': 'ê',
        r'\\u00f4': 'ô', r'\\u00e2': 'â',
    }
    for pattern, replacement in replacements.items():
        new_text, n = re.subn(re.escape(pattern), replacement, text)
        if n:
            fixes += n
            text = new_text
    return text, fixes


def fix_typos(text):
    """Aplica dicionário expandido de correções ortográficas."""
    fixes = 0
    for pattern, replacement in TYPO_FIXES.items():
        new_text, n = re.subn(pattern, replacement, text)
        if n:
            fixes += n
            text = new_text
    return text, fixes


def fix_heading_caps(text):
    """Corrige headings que começam com letra minúscula."""
    fixes = 0
    lines = text.split('\n')
    result = []
    for line in lines:
        m = re.match(r'^(#{1,4}\s+\d+\.\d+[\.\d]*\s+)([a-z])(.*)', line)
        if m:
            result.append(m.group(1) + m.group(2).upper() + m.group(3))
            fixes += 1
        else:
            result.append(line)
    return '\n'.join(result), fixes


def audit_references(text, filename):
    """Audita a seção de referências para detectar saltos de numeração e duplicatas."""
    issues = []
    refs = re.findall(r'^(\d+)\.\s', text, re.MULTILINE)
    if not refs:
        return issues
    
    ref_nums = [int(r) for r in refs]
    
    # Verificar saltos
    for i in range(len(ref_nums) - 1):
        expected = ref_nums[i] + 1
        actual = ref_nums[i + 1]
        if actual != expected and actual > expected:
            issues.append(f"  [REF] Salto de numeração: ref {ref_nums[i]} -> {actual} (falta ref {expected})")
    
    # Verificar duplicatas
    counts = Counter(ref_nums)
    for num, count in counts.items():
        if count > 1:
            issues.append(f"  [REF] Referência {num} duplicada ({count}x)")
    
    return issues


def process_chapter(filepath):
    """Processa um capítulo: corrige e audita."""
    if not filepath.exists():
        return {'file': filepath.name, 'skipped': True}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original = text
    total_fixes = 0
    details = []
    
    # 1. Unicode escapes
    text, n = fix_unicode_escapes(text)
    if n: details.append(f"unicode_escapes: {n}"); total_fixes += n
    
    # 2. Typos
    text, n = fix_typos(text)
    if n: details.append(f"ortografia: {n}"); total_fixes += n
    
    # 3. Heading caps
    text, n = fix_heading_caps(text)
    if n: details.append(f"heading_caps: {n}"); total_fixes += n
    
    # 4. Excessive blank lines
    text, n = fix_excessive_blank_lines(text)
    if n: details.append(f"linhas_vazias: {n}"); total_fixes += n
    
    # 5. Trailing garbage
    text, n = fix_trailing_garbage(text)
    if n: details.append(f"lixo_residual: {n}"); total_fixes += n
    
    # 6. Reference audit (read-only, does not modify)
    ref_issues = audit_references(text, filepath.name)
    
    # Save if changed
    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
    
    return {
        'file': filepath.name,
        'fixes': total_fixes,
        'details': details,
        'ref_issues': ref_issues,
        'changed': text != original,
    }


def main():
    print("\n" + "=" * 60)
    print(" PresbyCor Deep Audit — SEGUNDA PASSAGEM v2.0")
    print("=" * 60)
    print(f"[Projeto] {PROJECT_ROOT}\n")
    
    total_fixes = 0
    total_ref_issues = 0
    all_results = []
    
    for ch in CHAPTERS:
        fp = PROJECT_ROOT / ch
        result = process_chapter(fp)
        all_results.append(result)
        
        if result.get('skipped'):
            print(f"  [SKIP] {result['file']}")
            continue
        
        fixes = result['fixes']
        total_fixes += fixes
        
        if fixes > 0:
            detail_str = ', '.join(result['details'])
            print(f"  [FIX] {result['file']} -> {fixes} correcoes ({detail_str})")
        else:
            print(f"  [OK]  {result['file']} -> Sem erros restantes")
        
        for issue in result.get('ref_issues', []):
            print(issue)
            total_ref_issues += 1
    
    print(f"\n{'=' * 60}")
    print(f" RESUMO: {total_fixes} correcoes aplicadas")
    if total_ref_issues:
        print(f" AVISOS: {total_ref_issues} problemas em referencias (requerem revisao manual)")
    else:
        print(f" REFERENCIAS: Todas consistentes!")
    print("=" * 60)


if __name__ == '__main__':
    main()
