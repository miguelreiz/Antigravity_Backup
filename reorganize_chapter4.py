import re

file_path = '/Users/miguelreis/Downloads/Takeout/NotebookLM/PresbyCor_ Modern Strategies for Presbyopia and La/Chapter_4_Complete.md'

with open(file_path, 'r') as f:
    content = f.read()

# Split into Body and Infographics Appendix
split_marker = "## Infográficos Clínicos Sugeridos"
if split_marker not in content:
    print("Error: Could not find split marker")
    exit(1)

body, appendix = content.split(split_marker)

# Extract Infographics from Appendix
# We need to manually identify start/end of each infographic based on the known structure in the file
# Or just hardcode the extractions if we have the content.
# Since I have the content from the view_file, I will define the infographic blocks explicitly in the script to be safe.

info_4_1_block = """
### Infográfico 4.1: O Efeito de Mascaramento Epitelial (Corte Transversal Dinâmico)

![O Efeito de Mascaramento Epitelial: O Inimigo Oculto](figures/chapter4/epithelial_masking_effect_pt.png)
*Figura 4.1: Sequência temporal do efeito de mascaramento epitelial em ablação presbiópica. Painel 1 (Dia 0): Perfil hiper-prolato planeado (Q=-0.80) com geometria abrupta mostrando "bossa" central íngreme e "fosso" periférico profundo. Painel 2 (Semanas 2-12): Remodelamento compensatório ativo - o epitélio adelgaça sobre o pico central (42μm) e espessa no fosso periférico (62μm), preenchendo irregularidades. Painel 3 (Ano 1): Resultado final estabilizado mostrando superfície anterior lisa que mascara o perfil estromal subjacente, reduzindo a asfericidade efetiva de Q=-0.80 para Q=-0.40 (perda de 50% do efeito presbiópico planeado). Demonstra porque a sobrecorreção nomogramática é necessária.*
"""

info_4_2_block = """
### Infográfico 4.2: Centragem – Pupila vs. Purkinje vs. Ponto Médio

![A Trindade da Centragem: Pupila vs. Purkinje vs. Ponto Médio](figures/chapter4/centration_strategy_pt.png)
*Figura 4.2: Estratégia de centragem em cirurgia presbiópica mostrando os três alvos possíveis. Centro Pupilar (ponto vermelho): risco de coma se Kappa alto. Reflexo de Purkinje/Eixo Visual (cruz verde): risco de cobertura pupilar inadequada. Ponto Médio/Halfway Point (estrela dourada): estratégia de compromisso ótimo posicionada a 50% entre pupila e Purkinje. Zona de ablação (círculo azul 6.5mm) centrada no Ponto Médio demonstra cobertura pupilar adequada mantendo proximidade ao eixo visual. Tabela de decisão: Kappa <0.3mm → centrar na pupila; Kappa 0.3-0.6mm → centrar no Ponto Médio (⭐ gold standard); Kappa >0.6mm → centrar no Purkinje ou contraindicar. Ilustra o balanço crítico entre qualidade óptica e funcionalidade anatómica.*
"""

info_4_3_block = """
### Infográfico 4.3: Linha Temporal de Recuperação Visual (PRK vs. LASIK)

![A Corrida da Recuperação: PRK vs. LASIK](figures/chapter4/recovery_timeline_pt.png)
*Figura 4.3: Comparação temporal de recuperação visual entre PRK e LASIK em cirurgia presbiópica. Curva LASIK ("A Lebre", azul): início alto aos 80% (Dia 1), rápida ascensão a 95% (Semana 1), platô de 100% (Mês 1) com "Efeito Wow" e capacidade de condução no Dia 2-3. Curva PRK ("A Tartaruga", laranja): início baixo aos 20% (Dia 1), queda para "Poço do Desespero" aos 10% (Dia 3 - pico inflamatório com dor/fotofobia), recuperação lenta a 50% (Dia 5-7 com remoção de lente terapêutica), zona de flutuação 60-70% (Semanas 2-4 com ghosting/haze transiente), cruzamento das curvas aos 95% (Mês 3 - convergência), platô final 100% (Mês 6). Gap de Reabilitação sombreado demonstra período de resiliência necessária. Painéis laterais mostram jornadas do paciente: LASIK ("já lendo telefone Dia 1") vs PRK ("Semana Cega" e "maraton completa Mês 3").*
"""

info_4_4_block = """
### Infográfico 4.4: Protocolo MMC Step-by-Step

![Protocolo de Segurança Mitomicina C: Guia Passo-a-Passo](figures/chapter4/mmc_protocol_pt.png)
*Figura 4.4: Protocolo de segurança MMC em 4 etapas para PRK presbiópico. Etapa 1 (Preparação, azul): Concentração crítica 0.02% em esponja Merocel 6-8mm, NUNCA gotas líquidas diretas. Etapa 2 (Aplicação, amarelo): Cronómetro digital mostrando tempos baseados em profundidade de ablação (<50μm: 15-20seg; 50-80μm: 30-45seg; >80μm: 60seg MÁXIMO). Etapa 3 (Lavagem, azul): Irrigação vigorosa MÍNIMO 30ml BSS sobre leito estromal E fundos de saco conjuntivais (diluição mandatória). Etapa 4 (Proteção, verde): Lente de contacto terapêutica High-DK (Dk/t >100) cobrindo todo o limbo. Legenda inferior enfatiza: sucesso não é evitar MMC, mas garantir concentração correta e lavagem exaustiva para prevenir toxicidade endotelial e scleral melt.*
"""

# Extracting 4.5 and 4.6 dynamically is safer to ensure we get the full text description from the appendix
# But to be precise, let's look for the start and end in the 'appendix' string.

def extract_block(text, start_marker, end_marker=None):
    start_idx = text.find(start_marker)
    if start_idx == -1: return None
    if end_marker:
        end_idx = text.find(end_marker, start_idx)
        if end_idx == -1: return text[start_idx:]
        return text[start_idx:end_idx]
    else:
        return text[start_idx:]

info_4_5_block = extract_block(appendix, "### Infográfico 4.5:", "### Infográfico 4.6:")
info_4_6_block = extract_block(appendix, "### Infográfico 4.6:", None) # Last one

# Insertion Logic using Replace (safer than index math if anchors are unique)

# 4.1 -> After "15-25% do valor planeado [3]"
body = body.replace("15-25% do valor planeado [3]", "15-25% do valor planeado [3]\n\n" + info_4_1_block)

# 4.4 -> After "Córnea <400 μm de espessura residual (risco teórico de toxicidade endotelial)"
body = body.replace("Córnea <400 μm de espessura residual (risco teórico de toxicidade endotelial)", "Córnea <400 μm de espessura residual (risco teórico de toxicidade endotelial)\n\n" + info_4_4_block)

# 4.2 -> After "Balanceia ambos os objetivos"
body = body.replace("Balanceia ambos os objetivos", "Balanceia ambos os objetivos\n\n" + info_4_2_block)

# 4.3 -> After "PRK presbiópico requer 5-6 meses em média. [6]"
body = body.replace("PRK presbiópico requer 5-6 meses em média. [6]", "PRK presbiópico requer 5-6 meses em média. [6]\n\n" + info_4_3_block)

# 4.6 -> After "**Decisão Final**" (inside flowchart) - Be careful with markdown code block
# The flowchart ends with ```. Let's insert AFTER the code block.
body = re.sub(r'(\*\*Decisão Final\*\*\n```)', r'\1\n\n' + info_4_6_block, body)

# 4.5 -> After "Sutura do flap (10-0 Nylon, 3-4 pontos interrompidos) se recorrente"
body = body.replace("Sutura do flap (10-0 Nylon, 3-4 pontos interrompidos) se recorrente", "Sutura do flap (10-0 Nylon, 3-4 pontos interrompidos) se recorrente\n\n" + info_4_5_block)

# Remove the trailing separator line if it exists (usually "---" before the appendix)
body = body.rstrip()
if body.endswith("---"):
    body = body[:-3].rstrip()

# Write back
with open(file_path, 'w') as f:
    f.write(body)

print("Reorganization complete.")
