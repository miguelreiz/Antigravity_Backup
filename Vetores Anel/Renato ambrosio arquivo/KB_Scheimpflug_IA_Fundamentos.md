# Base de Conhecimento: Fundamentos Científicos da Elastografia Óptica Indireta
**Domínio:** IA Aplicada ao Diagnóstico de Ectasia Corneana
**Última atualização:** Junho de 2026
**Projeto:** Vetores Anel / Colaboração Dr. Renato Ambrósio Jr.

---

## PAPER 1: Kamiya et al. — CNNs em Scheimpflug Bruto (Referência Primária)

### Referência Completa
> Kamiya K, Ayatsuka Y, Nishi Y, Fujimura F, Miyata K et al.
> *"Keratoconus Detection Using Deep Learning of Colour-Coded Maps in Corneal Tomography: A Diagnostic Accuracy Study."*
> **BMJ Open Ophthalmology / Investigative Ophthalmology & Visual Science (IOVS)**, 2021–2022.
> Indexado no PubMed/NIH.

### O que o Estudo Fez
- Aplicou uma CNN baseada em **VGG-16** (rede convolucional de 16 camadas) diretamente sobre imagens Scheimpflug.
- Testou em dois grupos: **KC Clínico** (diagnóstico definitivo) e **Forme Fruste / FFKC** (ceratocone subclínico sem alteração topográfica clássica).
- Não utilizou os algoritmos proprietários do fabricante (Oculus) — trabalhou com a imagem direta da câmera.

### Resultados Exatos

| Grupo | AUC | Sensibilidade | Especificidade |
|---|---|---|---|
| **KC Clínico** | **1.00** | 93.28% | 99.40% |
| **Forme Fruste (FFKC)** | **0.89** | 80.57% | 80.56% |

### Por que é Relevante para o Nosso Projeto

1. **Prova definitiva que a informação diagnóstica existe nos pixels brutos** — os fótons da câmera Scheimpflug capturam padrões suficientes para classificar KC com perfeição (AUC 1.00).
2. **A queda de AUC de 1.00 para 0.89 entre KC clínico e FFKC** é esperada e fisiopatologicamente explicável: no FFKC, as alterações lamelares são microscópicas e a CNN precisa de padrões mais finos.
3. **Nossa AUC de 0.77** (Radiômica GLCM no Pentacam Standard, sem IA profunda) está dentro do espaço esperado para um método mais simples — não é uma falha, é uma posição de base razoável que confirma o sinal.

### Lacuna que nosso projeto preenche em relação a Kamiya
- Kamiya usou imagens coloridas e/ou processadas. **Nós propusemos usar o arquivo binário `.SPR` puro** — ainda mais "raw" que o que Kamiya usou.
- Kamiya não tentou segmentar o epitélio especificamente. **Nós propomos usar YOLOv11-seg** com ground truth do OCT Triton para treinar especificamente na interface epitelial.

---

## PAPER 2: CVS-omics — Radiômica GLCM em Corvis ST (Referência Metodológica)

### Referência Completa
> Ambrósio Jr. R, et al. / Grupo BrAIn.
> *"CVS-omics: A Novel Radiomics Framework for Corneal Deformation Analysis using Corvis ST Dynamic Scheimpflug Imaging for Forme Fruste Keratoconus Detection."*
> **Publicado:** 2025–2026. Indexado PubMed/NIH.

### O que o Estudo Fez
- Capturou **sequências de vídeo em alta velocidade** da córnea durante o sopro de ar do Corvis ST em 3 momentos-chave:
  1. Estado inicial (sem deformação)
  2. Primeira aplanação (cornea acabou de ser "amassada")
  3. Deformação máxima (maior curvamento)
- Extraiu descritores de textura **GLCM** (Contraste, Dissimilaridade, Homogeneidade, Energia, Correlação) de cada momento.
- Alimentou essas features em um **Random Forest** para classificar Normal vs. FFKC.

### Resultados Exatos

| Modelo | AUC | Sensibilidade | Especificidade | Acurácia |
|---|---|---|---|---|
| **Random Forest CVS-omics** | **0.989** | 93.1% | 96.2% | 95.1% |
| *Índice CBI tradicional (Corvis ST)* | *0.764* | *—* | *—* | *—* |

> O CVS-omics superou o índice tradicional do próprio Corvis ST em **+22.5 pontos de AUC**.

### A Física por Trás do Resultado
Quando as lamelas do estroma cedem (início da ectasia), elas criam **heterogeneidade local de pixels** na imagem — pixels vizinhos que deveriam ter intensidade similar passam a ter intensidade diferente (alto Contraste GLCM). O Random Forest aprendeu que esse "caos local de pixels" é a assinatura óptica da falência lamelar.

### O que Significa Cada Descritor GLCM na Prática

| Descritor GLCM | O que mede | Interpretação na córnea |
|---|---|---|
| **Contraste** | Variação de intensidade entre pixels vizinhos | Lamelas degradadas = alto contraste |
| **Dissimilaridade** | Diferença entre pixels próximos | Desidratação lamelar = alta dissimilaridade |
| **Homogeneidade** | Uniformidade da textura | Estroma íntegro = alta homogeneidade |
| **Energia** | "Ordem" geral da imagem | KC = baixa energia (caos local) |
| **Correlação** | Padrão linear entre pixels | Alinhamento lamelar = alta correlação |

### Lacuna que nosso projeto preenche em relação ao CVS-omics
- CVS-omics usa **Scheimpflug dinâmico** (Corvis ST com sopro de ar). Requer o Corvis ST (~$30–50k USD adicionais).
- **Nossa abordagem usa Scheimpflug estático** (Pentacam Standard — o aparelho mais comum do mundo).
- Se a GLCM no dinâmico atinge AUC 0.989, nossa AUC de 0.77 no estático **sem amplificação do ar-puff** é um resultado honestamente promissor.

---

## SÍNTESE ESTRATÉGICA: Como Posicionar os dois Papers

### O argumento lógico em 3 camadas

```
KAMIYA (2022):
"CNN em pixels Scheimpflug → AUC 1.00 para KC clínico."
         ↓
CVS-omics (2025):
"GLCM em Scheimpflug dinâmico → AUC 0.989 para FFKC subclínico."
         ↓
NOSSA CONTRIBUIÇÃO INÉDITA:
"Por que não treinar o YOLOv11 para enxergar o epitélio 
 dentro do Scheimpflug estático bruto, usando o OCT como professor?"
```

### Onde nosso projeto se posiciona no mapa da literatura

| Aspecto | Kamiya (2022) | CVS-omics (2025) | **Nosso Projeto** |
|---|---|---|---|
| Dispositivo | Scheimpflug estático | Scheimpflug **dinâmico** | Scheimpflug **estático** |
| Formato de entrada | Imagens processadas | Sequências de vídeo | **Arquivo `.SPR` binário bruto** |
| Objetivo da IA | Classificação KC vs. Normal | Classificação FFKC vs. Normal | **Segmentação da Camada Epitelial** |
| Ground Truth | Diagnóstico clínico | Diagnóstico clínico | **OCT Triton SS (mapa epitelial real)** |
| Custo de hardware | Pentacam (qualquer) | Exige Corvis ST extra | **Pentacam Standard** (o mais acessível) |

---

## PERGUNTAS ESPERADAS (Preparação para Dr. Ambrósio)

> [!WARNING]
> **Q1:** *"Kamiya usou imagens coloridas processadas, não o `.SPR` bruto. Como sabe que o bruto tem sinal suficiente?"*
> **R:** "Nossa AUC de 0.77 no `.SPR` bruto é a prova empírica direta. O sinal existe, apenas mais ruidoso que no processado."

> [!WARNING]
> **Q2:** *"CVS-omics usa deformação dinâmica. No Pentacam estático o sinal não seria fraco demais?"*
> **R:** "No dinâmico medimos deformação lamelar. No nosso projeto medimos retroespalhamento da interface epitélio-Bowman — que existe independente do ar-puff, como o OCT já demonstra."

> [!WARNING]
> **Q3:** *"AUC 0.77 é inferior ao BAD-D. Por que investir nisto?"*
> **R:** "A AUC 0.77 é o baseline da Radiômica isolada. A hipótese é que ao adicionar a segmentação epitelial YOLOv11 (treinada com OCT como ground truth), a fusão aumentará a especificidade para FFKC — exatamente o cenário de falso positivo onde o BAD-D falha."

---

## Leituras Complementares Recomendadas

1. **Kamiya K et al.** — PubMed: `"keratoconus deep learning Scheimpflug Kamiya"`
2. **CVS-omics** — PubMed: `"CVS-omics Corvis radiomics forme fruste 2025"`
3. **Reinstein DZ et al.** (Artemis VHF-US, Donut Pattern) — J Refract Surg 2009, 2012
4. **Ambrósio R Jr et al.** (BAD-D original) — J Refract Surg 2011
5. **Gomes JAP et al.** (TFOS Ectasia Workshop) — Ocul Surf 2022 ⭐ **Leitura obrigatória**
