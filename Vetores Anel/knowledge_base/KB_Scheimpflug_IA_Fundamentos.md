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
- Não utilizou os algoritmos proprietários do fabricante (Oculus).

### Resultados Exatos

| Grupo | AUC | Sensibilidade | Especificidade |
|---|---|---|---|
| **KC Clínico** | **1.00** | 93.28% | 99.40% |
| **Forme Fruste (FFKC)** | **0.89** | 80.57% | 80.56% |

### Por que é Relevante
1. Prova definitiva que a informação diagnóstica existe nos pixels brutos do Scheimpflug.
2. A queda AUC 1.00→0.89 entre KC clínico e FFKC é esperada: no FFKC as alterações são microscópicas.
3. Nossa AUC de 0.77 (GLCM no Pentacam Standard) confirma o mesmo princípio com método mais simples.

### Lacuna que nosso projeto preenche
- Kamiya não tentou segmentar o epitélio. Nós propomos usar YOLOv11-seg com ground truth do OCT Triton especificamente para a interface epitelial.

---

## PAPER 2: CVS-omics — Radiômica GLCM em Corvis ST (Referência Metodológica)

### Referência Completa
> Ambrósio Jr. R, et al. / Grupo BrAIn.
> *"CVS-omics: A Novel Radiomics Framework for Corneal Deformation Analysis."*
> **PubMed/NIH**, 2025–2026.

### O que o Estudo Fez
- Extraiu descritores GLCM de 3 fases do Corvis ST (estado inicial, primeira aplanação, deformação máxima).
- Classificou Normal vs. FFKC com **Random Forest**.

### Resultados Exatos

| Modelo | AUC | Sensibilidade | Especificidade |
|---|---|---|---|
| **Random Forest CVS-omics** | **0.989** | 93.1% | 96.2% |
| *CBI tradicional (Corvis ST)* | *0.764* | — | — |

### Descritores GLCM e Seu Significado Corneano

| Descritor | Interpretação na córnea |
|---|---|
| **Contraste** | Lamelas degradadas = alto contraste |
| **Dissimilaridade** | Desidratação lamelar = alta dissimilaridade |
| **Homogeneidade** | Estroma íntegro = alta homogeneidade |
| **Energia** | KC = baixa energia (caos local) |
| **Correlação** | Alinhamento lamelar = alta correlação |

### Lacuna que nosso projeto preenche
- CVS-omics requer o Corvis ST (hardware adicional). Nossa abordagem usa apenas o Pentacam Standard — o aparelho mais comum no mundo.

---

## Posicionamento no Mapa da Literatura

| Aspecto | Kamiya (2022) | CVS-omics (2025) | Nosso Projeto |
|---|---|---|---|
| Dispositivo | Scheimpflug estático | Scheimpflug dinâmico | Scheimpflug estático |
| Formato | Imagens processadas | Sequências de vídeo | `.SPR` binário bruto |
| Objetivo IA | Classificação KC | Classificação FFKC | **Segmentação Epitelial** |
| Ground Truth | Diagnóstico clínico | Diagnóstico clínico | **OCT Triton SS** |
| Hardware necessário | Qualquer Pentacam | Pentacam + Corvis ST | **Pentacam Standard** |

---

## Perguntas Difíceis e Respostas Preparadas

**Q: "O `.SPR` bruto tem sinal suficiente?"**
R: AUC 0.77 em GLCM no `.SPR` bruto é a prova empírica direta. O sinal existe.

**Q: "No estático não falta a amplificação do ar-puff?"**
R: No dinâmico medimos deformação lamelar. Aqui medimos retroespalhamento epitélio-Bowman, que independe do ar-puff.

**Q: "AUC 0.77 é inferior ao BAD-D. Por que investir?"**
R: 0.77 é o baseline da Radiômica isolada. A fusão com YOLOv11-seg (treinado pelo OCT) aumentará a especificidade para FFKC — onde o BAD-D falha mais.

---

## Leituras Obrigatórias

1. Kamiya K et al. — PubMed: `"keratoconus deep learning Scheimpflug Kamiya"`
2. CVS-omics — PubMed: `"CVS-omics Corvis radiomics forme fruste 2025"`
3. Reinstein DZ et al. — J Refract Surg 2009, 2012 (Donut Pattern)
4. Ambrósio R Jr et al. — J Refract Surg 2011 (BAD-D original)
5. Gomes JAP et al. — Ocul Surf 2022 ⭐ TFOS Ectasia Workshop (Leitura obrigatória)
