#!/usr/bin/env python3
"""
Script para atualizar referências de imagens nos capítulos para versões em português
"""

import re
import os
from pathlib import Path

# Diretório base
BASE_DIR = Path(__file__).parent

# Mapeamento de imagens disponíveis em português
PT_IMAGES_MAP = {
    # Chapter 1
    'duane_curve.png': 'duane_curve_pt.png',
    
    # Chapter 4
    'centration_strategy.png': 'centration_strategy_pt.png',
    'epithelial_ingrowth.png': 'epithelial_ingrowth_pt.png',
    'epithelial_masking_effect.png': 'epithelial_masking_effect_pt.png',
    'haze_hazard_map.png': 'haze_hazard_map_pt.png',
    'healing_cascade.png': 'healing_cascade_pt.png',
    'mmc_protocol.png': 'mmc_protocol_pt.png',
    'recovery_timeline.png': 'recovery_timeline_pt.png',
}

def update_chapter_images(chapter_file):
    """Atualiza referências de imagens em um capítulo para versões em português"""
    
    if not chapter_file.exists():
        print(f"⚠️  Arquivo não encontrado: {chapter_file}")
        return False
    
    print(f"\n📖 Processando: {chapter_file.name}")
    
    # Ler conteúdo
    content = chapter_file.read_text(encoding='utf-8')
    original_content = content
    
    # Contadores
    replacements = 0
    
    # Substituir referências de imagens
    for original_img, pt_img in PT_IMAGES_MAP.items():
        # Padrão para encontrar referências markdown de imagens
        pattern = rf'!\[(.*?)\]\((figures/[^)]*{re.escape(original_img)})\)'
        
        def replace_match(match):
            nonlocal replacements
            caption = match.group(1)
            original_path = match.group(2)
            # Substituir apenas o nome do arquivo, mantendo o caminho
            new_path = original_path.replace(original_img, pt_img)
            replacements += 1
            return f'![{caption}]({new_path})'
        
        content = re.sub(pattern, replace_match, content)
    
    # Salvar se houve mudanças
    if content != original_content:
        chapter_file.write_text(content, encoding='utf-8')
        print(f"✅ {replacements} imagem(ns) atualizada(s) para português")
        return True
    else:
        print(f"ℹ️  Nenhuma imagem para atualizar")
        return False

def main():
    """Função principal"""
    print("="*70)
    print("🇧🇷 ATUALIZADOR DE IMAGENS PARA PORTUGUÊS")
    print("="*70)
    
    # Listar todos os capítulos
    chapters = sorted(BASE_DIR.glob("Chapter_*_Complete.md"))
    
    if not chapters:
        print("❌ Nenhum capítulo encontrado!")
        return
    
    print(f"\n📚 Encontrados {len(chapters)} capítulos")
    
    updated_count = 0
    for chapter in chapters:
        if update_chapter_images(chapter):
            updated_count += 1
    
    print("\n" + "="*70)
    print(f"✅ CONCLUÍDO: {updated_count} capítulo(s) atualizado(s)")
    print("="*70)

if __name__ == "__main__":
    main()
