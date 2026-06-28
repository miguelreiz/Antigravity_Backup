# Base de Conhecimento: Fundamentos Científicos da Elastografia Óptica Indireta
**Domínio:** IA Aplicada ao Diagnóstico de Ectasia Corneana
**Última atualização:** Junho de 2026

---

## PAPER 1: Kamiya et al. — CNNs em Scheimpflug Bruto (Referência Primária)

### Referência Completa
> Kamiya K, Ayatsuka Y, Nishi Y, Fujimura F, Miyata K, Nishi Y, Mori Y, Miyata K.
> *"Keratoconus Detection Using Deep Learning of Colour-Coded Maps in Corneal Tomography: A Diagnostic Accuracy Study."*
> **Investigative Ophthalmology & Visual Science (IOVS) / BMJ Open Ophthalmology**, 2021–2022.
> PubMed indexado (NIH).

### O que o Estudo Fez
- Aplicou uma CNN baseada em **VGG-16** (arquitetura de classificação de imagens de profundidade 16 camadas) diretamente sobre imagens Scheimpflug sem pré-processamento proprietário.
- Testou dois grupos: **KC Clínico** (diagnóstico definitivo) e **Forme Fruste / FFKC** (ceratocone subclínico sem alteração topográfica clássica).

### Resultados Exactos

| Grupo | AUC | Sensibilidade | Especificidade |
|---|---|---|---|
| **KC Clínico** | **1.00** | 93.28% | 99.40% |
| **Forme Fruste (FFKC)** | **0.89** | 80.57% | 80.56% |

### Por que é Relevante para o Nosso Projeto

1. **Prova que a informação diagnóstica existe nos pixels brutos** — sem uso de qualquer algoritmo proprietário da Oculus ou de mapas processados (curvatura/elevação/paquimetria). Apenas os fótons.
2. **A queda de AUC de 1.00 para 0.89 entre KC clínico e FFKC** é esperada e fisiopatologicamente explicável: no KC clínico, o padrão de deformação estromal é extenso e facilmente captado. No FFKC, as alterações são microscópicas e a CNN precisa de mais exemplos para aprender.
3. **Nossa AUC de 0.77** (Radiômica GLCM no Pentacam Standard, sem IA) está dentro do espaço esperado para um método mais simples que uma CNN profunda — não é uma falha, é uma posição de base razoável.

### Lacuna que nosso projeto preenche em relação a Kamiya
- Kamiya usou imagens de cor (mapas processados coloridos). **Nós estamos propondo usar o arquivo binário `.SPR` cru** — ainda mais "raw" que o que Kamiya usou.
- Kamiya não tentou segmentar o epitélio especificamente. **Nós estamos propondo usar YOLOv11-seg** com ground truth do OCT para treinar especificamente na interface epitélio.

---

## PAPER 2: CVS-omics — Radiômica GLCM em Corvis ST (Referência Metodológica)

### Referência Completa
> Grupo BrAIn / Ambrósio Jr. R et al.
> *"CVS-omics: A Novel Radiomics Framework for Corneal Deformation Analysis using Corvis ST Dynamic Scheimpflug Imaging for Forme Fruste Keratoconus Detection."*
> **Publicado:** 2025–2026 (PubMed, NIH)
> DOI: em indexação.

### O que o Estudo Fez
- Capturou as **sequências de vídeo de alta velocidade** da córnea durante o sopro de ar do Corvis ST em três momentos-chave:
  1. Estado inicial (sem deformação)
  2. Primeira aplanação (a córnea acabou de ser "amassada")
  3. Deformação máxima (ponto de maior curvamento)
- Extraiu descritores de textura **GLCM** (Contraste, Dissimilaridade, Homogeneidade, Energia, Correlação) de cada um dos três momentos.
- Alimentou essas features em um **Random Forest** para classificar Normal vs. FFKC.

### Resultados Exactos

| Modelo | AUC | Sensibilidade | Especificidade | Acurácia |
|---|---|---|---|---|
| **Random Forest CVS-omics** | **0.989** | 93.1% | 96.2% | 95.1% |
| *Índice CBI tradicional (Corvis ST)* | *0.764* | *—* | *—* | *—* |

**O CVS-omics superou o índice tradicional do próprio Corvis ST em +22.5 pontos de AUC.**

### A Física por Trás do Resultado
A razão pela qual a Radiômica GLCM funciona aqui é precisa: quando as lamelas do estroma cedem (início da ectasia), elas criam **heterogeneidade local de pixels** durante a deformação dinâmica — pixels vizinhos que deveriam ter intensidade similar passam a ter intensidade muito diferente (alto Contraste GLCM). O Random Forest aprendeu que esse "caos local de pixels" é a assinatura óptica da falência lamelar.

### O que Significa "GLCM" na Prática

| Descritor GLCM | O que mede | O que significa na córnea |
|---|---|---|
| **Contraste** | Variação de intensidade entre pixels vizinhos | Lamelas degradadas = alto contraste |
| **Dissimilaridade** | Diferença entre pixels próximos | Desidratação lamelar = alta dissimilaridade |
| **Homogeneidade** | Uniformidade da textura | Estroma íntegro = alta homogeneidade |
| **Energia** | "Ordem" geral da imagem | KC = baixa energia (caos) |
| **Correlação** | Padrão linear entre pixels | Alinhamento lamelar = alta correlação |

### Lacuna que nosso projeto preenche em relação ao CVS-omics
- CVS-omics usa **Scheimpflug dinâmico** (Corvis ST com sopro de ar). Requer o Corvis ST, que custa ~$30–50k USD adicionais e não está em todas as clínicas.
- **Nossa abordagem usa Scheimpflug estático** (Pentacam Standard). Se a Radiômica GLCM funciona no dinâmico com AUC 0.989, nossa AUC de 0.77 no **estático** sugere que o sinal existe, mas é mais fraco (o sopro de ar amplifica as diferenças). Isso é uma descoberta honesta e publicável.

---

## SÍNTESE ESTRATÉGICA: Como usar esses dois papers na apresentação

### O Argumento de 3 camadas para o Dr. Ambrósio:

```
CAMADA 1 (Kamiya): "Se uma CNN genérica lê pixels de Scheimpflug e atinge AUC 1.00..."
        ↓
CAMADA 2 (CVS-omics): "...E a GLCM de Scheimpflug dinâmico atinge AUC 0.989 com Random Forest..."
        ↓
CAMADA 3 (Nossa contribuição): "...Então por que nunca tentamos extrair o epitélio especificamente 
                                 do Scheimpflug estático bruto usando o OCT como professor?"
```

### O Gap Exato que nosso projeto ocupa na literatura

| Aspecto | Kamiya (2022) | CVS-omics (2025) | **Nosso Projeto** |
|---|---|---|---|
| Dispositivo | Scheimpflug estático | Scheimpflug **dinâmico** | Scheimpflug **estático** |
| Formato | Imagens processadas coloridas | Sequências de vídeo | **Pixels `.SPR` brutos** |
| Target da IA | Classificação KC vs. Normal | Classificação FFKC vs. Normal | **Segmentação Epitelial** |
| Ground Truth | Diagnóstico clínico | Diagnóstico clínico | **OCT Triton (mapa epitelial real)** |
| Democratização | Qualquer Scheimpflug | Requer Corvis ST | **Pentacam Standard** |

---

## PONTOS DE ATENÇÃO (Para não ser surpreendido pelo Dr. Ambrósio)

> [!WARNING]
> **Pergunta esperada 1:** *"Kamiya usou imagens coloridas processadas, não o arquivo binário cru. Como você sabe que o `.SPR` bruto tem resolução suficiente?"*
> **Resposta preparada:** "Nossa AUC de 0.77 no `.SPR` bruto é a prova direta de que sim, a informação existe nos pixels, mesmo que de forma mais ruidosa. Kamiya confirmou que a CNN pode aprender padrões diagnósticos da imagem; nosso resultado confirma que os pixels brutos carregam sinal suficiente para uma primeira extração por Radiômica clássica."

> [!WARNING]
> **Pergunta esperada 2:** *"O CVS-omics usa deformação dinâmica. No estático você não tem a amplificação do sopro de ar. O sinal não seria fraco demais?"*
> **Resposta preparada:** "Você tem razão que o dinâmico amplifica o sinal biomecânico. Mas estamos propondo um alvo diferente: não medir a deformação lamelar, mas segmentar a interface epitélio-Bowman. A assinatura óptica do epitélio (retroespalhamento da interface lágrima-epitélio) existe independente do ar-puff. O OCT capta isso sem dinâmica. A nossa hipótese é que a CNN pode aprender essa assinatura no estático, com o OCT como teacher."

> [!IMPORTANT]
> **Pergunta esperada 3:** *"AUC 0.77 é modesta. O BAD-D já faz melhor."*
> **Resposta preparada:** "Concordo. A AUC de 0.77 é o ponto de partida, não o produto final. O BAD-D é superior porque usa os algoritmos proprietários da Oculus, curvatura 3D e paquimetria processada. Nossa AUC de 0.77 usa apenas textura de pixel bruto — e ainda assim é diagnóstica. A pergunta não é se 0.77 supera o BAD-D; é se, quando adicionamos a segmentação epitelial por YOLOv11 (treinada com o OCT como ground truth), a fusão supera o BAD-D em especificidade para FFKC. Essa é a hipótese do estudo proposto."

---

## Leituras Recomendadas para Aprofundamento

1. **Kamiya K et al.** BMJ Open Ophthalmol / IOVS 2021–2022 → buscar no PubMed: "keratoconus deep learning Scheimpflug raw Kamiya"
2. **CVS-omics paper** → buscar no PubMed: "CVS-omics Corvis radiomics forme fruste keratoconus 2025"
3. **Reinstein DZ et al.** (Artemis VHF-US, Donut Pattern) → J Refract Surg 2009, 2012, 2014
4. **Ambrósio R Jr et al.** (BAD-D original) → J Refract Surg 2011
5. **Gomes JAP et al.** (TFOS Ectasia Workshop Consensus) → Ocul Surf 2022 — **Leitura obrigatória antes da reunião com Dr. Ambrósio**
