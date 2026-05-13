#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Injeta infográficos ausentes/órfãos e corrige imagens quebradas nos capítulos Markdown
do projeto PresbyCor.
"""
import re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent.parent.parent

# --- CAPÍTULO 3 ---
cap3 = root / "Chapter_3_Complete.md"
if cap3.exists():
    text3 = cap3.read_text(encoding="utf8")
    
    # 1. Substituir a imagem Quad-Map quebrada pelo Screening Flow Chart (mais útil)
    text3 = text3.replace(
        "![Protocolo Tomográfico Padrão Quad-Map](figures/chapter3/neutral_topography_quad_map_1767558811134.png)",
        "![Fluxograma de Triagem Tomográfica (Screening Flow)](figures/chapter3/screening_flow.png)"
    )
    text3 = text3.replace(
        "*Figura 3.0: Visualização tomográfica padrão (Quad-Map)",
        "*Figura 3.0: Fluxograma de triagem propedêutica e propedêutica armada"
    )

    # 2. Idade -> Inserir opportunity_windows.png
    if "figures/chapter3/opportunity_windows.png" not in text3:
        text3 = text3.replace(
            "**Pacientes >60 anos:**",
            "![Janelas de Oportunidade Refrativa](figures/chapter3/opportunity_windows.png)\n*Figura 3.1b: Infográfico ilustrando as janelas de oportunidade em cirurgia presbiópica.* \n\n**Pacientes >60 anos:**"
        )
        
    # 3. Emétropes -> Inserir holland_filter.png
    if "figures/chapter3/holland_filter.png" not in text3:
        text3 = text3.replace(
            "#### Emétropes (±0.50 D): Grupo de Maior Risco",
            "#### Emétropes (±0.50 D): Grupo de Maior Risco\n\n![O Filtro de Holland para Emétropes](figures/chapter3/holland_filter.png)\n*Figura 3.3b: Algoritmo de decisão restritiva para o alto risco do paciente emétrope.*"
        )

    # 4. LER / RSB -> Inserir biomechanics_pta_rsb_dual_calculator.png
    if "figures/chapter3/biomechanics_pta_rsb_dual_calculator.png" not in text3:
        text3 = text3.replace(
            "#### Espessura Corneana e Leito Estromal Residual (RSB)",
            "#### Espessura Corneana e Leito Estromal Residual (RSB)\n\n![Calculadora Biomecânica Dual: PTA & RSB](figures/chapter3/biomechanics_pta_rsb_dual_calculator.png)\n*Figura 3.7b: Representação dos limites biomecânicos e interação entre espessura, ablação e risco ectásico.*"
        )

    # 5. Contraindicações -> Inserir risk_matrix_v2.png
    if "figures/chapter3/risk_matrix_v2.png" not in text3:
        text3 = text3.replace(
            "### 3.5.1. Contraindicações Absolutas",
            "### 3.5.1. Contraindicações Absolutas\n\n![Matriz Geral de Risco em Cirurgia Presbiópica](figures/chapter3/risk_matrix_v2.png)\n*Figura 3.10: Matriz colorida categorizando riscos e contraindicações.*"
        )

    cap3.write_text(text3, encoding="utf8")
    print("Capítulo 3 atualizado com infográficos.")


# --- CAPÍTULO 4 ---
cap4 = root / "Chapter_4_Complete.md"
if cap4.exists():
    text4 = cap4.read_text(encoding="utf8")
    
    # 1. Corrigir decision_tree_pt.png -> diagram_lasik_vs_prk.png
    text4 = text4.replace(
        "![Árvore de Decisão: PRK vs. LASIK](figures/chapter4/decision_tree_pt.png)",
        "![Árvore de Decisão: PRK vs. LASIK](figures/chapter4/diagram_lasik_vs_prk.png)"
    )

    cap4.write_text(text4, encoding="utf8")
    print("Capítulo 4: Link de decision_tree_pt para diagram_lasik_vs_prk corrigido.")

# --- CAPÍTULO 7 ---
cap7 = root / "Chapter_7_Complete.md"
if cap7.exists():
    text7 = cap7.read_text(encoding="utf8")
    
    # 1. Inserir ai_presbyond_blend_concept.png
    if "figures/chapter7/ai_presbyond_blend_concept.png" not in text7:
        text7 = text7.replace(
            "## 7.1. O Conceito de Blend Zone",
            "## 7.1. O Conceito de Blend Zone\n\n![O Conceito de Blend Zone em PRESBYOND](figures/chapter7/ai_presbyond_blend_concept.png)\n*Figura 7.1b: Infográfico esquematizado do prolongamento da profundidade de foco e intersecção binocular.*"
        )

    cap7.write_text(text7, encoding="utf8")
    print("Capítulo 7: ai_presbyond_blend_concept inserido.")

# --- CAPÍTULO 9 ---
cap9 = root / "Chapter_9_Complete.md"
if cap9.exists():
    text9 = cap9.read_text(encoding="utf8")
    
    if "figures/chapter9/ai_rsb_biomechanics.png" not in text9:
        text9 = text9.replace(
            "## 9.1. Limitações Biomecânicas e de Superfície Ocular",
            "## 9.1. Limitações Biomecânicas e de Superfície Ocular\n\n![Considerações Biomecânicas no Olho Pós-Refrativo](figures/chapter9/ai_rsb_biomechanics.png)\n*Figura 9.1b: Limitações anatómicas no retratamento lamelar e de superfície.*"
        )
    cap9.write_text(text9, encoding="utf8")
    print("Capítulo 9: ai_rsb_biomechanics inserido.")

print("\nConcluída injeção e correção de imagens!")
