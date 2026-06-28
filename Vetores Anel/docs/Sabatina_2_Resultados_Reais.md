# 🔍 Sabatina #2 — Resultados Reais da Validação Cruzada

## Os números mudaram. Aqui está a verdade.

> [!CAUTION]
> **O AUC 0.77 que estávamos citando na carta ao Dr. Ambrósio caiu para 0.676 com validação cruzada 10-fold.** O resultado original provavelmente veio de um único split treino/teste com overfitting.

---

## Resultados com 10-fold CV + Bootstrap IC 95% (n=384 olhos pareados)

| Componente | AUC | IC 95% | Veredicto |
|---|---|---|---|
| **Radiômica GLCM (4 features)** | **0.676** | 0.616 – 0.728 | ⚠️ Modesto, mas acima do acaso |
| Entropy IT (univariada) | 0.478 | 0.422 – 0.541 | ❌ Pior que aleatório |
| Espessura Epitelial (Peak Det.) | 0.515 | 0.458 – 0.582 | ❌ Aleatório |
| Posterior (Pachy_Min + K2) | **0.814** | 0.767 – 0.857 | ✅ Forte |
| **ÍNDICE FUSIONADO (10 feat.)** | **0.842** | 0.800 – 0.880 | ✅ Forte |

---

## Análise Honesta de Cada Componente

### 1. Radiômica GLCM: AUC 0.676 (era "0.77")

O AUC caiu de 0.77 para **0.676** com validação cruzada rigorosa. Isso significa que:
- O resultado original de 0.77 era **inflado por overfitting** (provavelmente um único split sortudo)
- 0.676 é estatisticamente acima do acaso (IC não cruza 0.5), mas é **modesto**
- Ainda assim, extrair AUC 0.676 de pixels brutos não-processados do Pentacam Standard continua sendo uma observação válida

**O que dizer ao Dr. Renato:** "AUC 0.676 (IC 95%: 0.616–0.728) com 10-fold CV" — e não "0.77".

### 2. Entropy IT: AUC 0.478 — MORTO

A entropia ínfero-temporal como feature univariada é **pior que jogar moeda**. O IC inclui 0.5. Isso é ruído, não sinal. Remover de qualquer claim.

### 3. Espessura Epitelial (Peak Detection): AUC 0.515 — MORTO

Os valores extraídos por peak detection (47.7 ± 3.9 µm) são fisiologicamente coerentes, mas **não discriminam** entre córneas saudáveis e doentes. Possíveis razões:
- A escala pixel→µm é uma estimativa grosseira (11.5 µm/pixel) — pode estar achatando diferenças reais
- O peak detection pode não estar capturando o afinamento real do epitélio no KC
- O Scheimpflug pode não ter resolução axial suficiente para medir diferenças de 5-10 µm

> [!WARNING]
> **Isso enfraquece severamente a tese do "Mapa Epitelial via Pentacam".** Se nem a espessura grosseira discrimina, um mapa refinado por YOLOv11 provavelmente também não vai discriminar — porque o problema pode ser de resolução física do sensor, não de algoritmo.

### 4. Posterior (Pachy_Min + K2): AUC 0.814

Este é o componente mais forte, MAS há um problema: **Pachy_Min e K2 são dados PROCESSADOS pelo software do Pentacam**, não dados brutos. O Pentacam já calcula isso. Então não estamos "extraindo informação nova" — estamos usando dados que o médico já tem.

### 5. Índice Fusionado: AUC 0.842

O índice combinado atinge 0.842, que é forte. Mas a análise honesta mostra que **~90% desse AUC vem de Pachy_Min e K2**, que já estão disponíveis no software. A contribuição incremental da radiômica bruta (0.676 → 0.842) é real, mas modesta.

---

## O Que Isso Significa Para a Carta ao Dr. Ambrósio

### O que PODE ser dito ✅

1. "A radiômica GLCM em pixels brutos do Pentacam Standard atinge AUC 0.676 (10-fold CV, IC 95%: 0.616–0.728)" — **verdadeiro e validado**
2. "Quando combinada com paquimetria mínima e ceratometria, a fusão atinge AUC 0.842" — **verdadeiro**
3. "A análise 360° dilui o sinal (AUC 0.57 → confirma foco temporal)" — **verdadeiro**
4. "O peak detection extrai espessura epitelial com valores fisiologicamente coerentes (47.7 µm)" — **verdadeiro, mas não discrimina**

### O que NÃO pode ser dito ❌

1. ~~"AUC 0.77"~~ → É 0.676 com validação rigorosa
2. ~~"Mapa epitelial discrimina KC"~~ → AUC 0.515, não discrimina
3. ~~"O pixel bruto supera o software"~~ → Pachy_Min sozinho (0.814) bate radiômica bruta (0.676)
4. ~~"Ponto de partida mais democratizante"~~ → 0.676 é exploratório, não revolucionário

### Como reformular a narrativa

A narrativa honesta é: **"A radiômica bruta do Pentacam Standard contribui informação incremental (AUC 0.676) que, quando combinada com índices convencionais, eleva o poder discriminativo de 0.814 para 0.842. A contribuição é estatisticamente significativa mas modesta. O valor não está em substituir o BAD-D, mas em adicionar uma dimensão textural que o processamento convencional ignora."**

---

## Decisão: Ainda vale apresentar ao Dr. Renato?

**Sim, mas com expectativa recalibrada.** O que você tem é:
- Uma observação genuína de que pixels brutos contêm informação textural (AUC 0.676)
- 443 olhos pareados organizados prontos para investigação
- Infraestrutura computacional funcional
- Honestidade científica sobre os limites

O Dr. Renato vai respeitar mais a honestidade dos números reais do que uma apresentação inflada que ele desmontaria em 5 minutos.
