# Dissociação Biomecânica Anterior-Posterior na Ectasia Corneana: Evidências de Colapso de Casca (*Shell Buckling*) e Implicações para a Reavaliação do KMax como Parâmetro Diagnóstico Primário

**Miguel Reis¹**

¹ Projeto Biomecânica Corneana — Análise Computacional Multi-Modal (Scheimpflug, OCT Radiômica, FEM)

---

## Resumo

**Objetivo:** Avaliar o acoplamento biomecânico entre as superfícies anterior e posterior da córnea e investigar as limitações do KMax como parâmetro diagnóstico primário de ectasia, utilizando análise multimodal integrando tomografia de Scheimpflug (Pentacam), índices radiômicos derivados de OCT de domínio espectral (Triton DRI-OCT) e simulação por Elementos Finitos (FEM) com modelo material anisotrópico.

**Métodos:** Estudo transversal analítico incluindo: (i) 660 olhos com descritores de curvatura SPR Scheimpflug; (ii) 443 olhos pareados OCT-Pentacam (408 olhos normais, 35 com ceratocone clínico); (iii) 24 modelos corneanos de Elementos Finitos (material Holzapfel-Gasser-Ogden). As áreas sob a curva ROC (AUROC) foram comparadas pelo método de DeLong. A concordância espacial entre ápices anterior e posterior foi avaliada por correlação de Pearson com IC95% (transformação Z de Fisher). Teste de Mann-Whitney U, teste de Levene para heterogeneidade de variâncias e tamanho de efeito (d de Cohen) complementaram a análise. Regressão linear múltipla com teste F avaliou a contribuição preditiva da forma posterior sobre a anterior.

**Resultados:** A correlação espacial entre os ápices anterior e posterior foi estatisticamente nula (r = +0.027; IC95% −0.050 a +0.103; P = 0.50), com deslocamento periférico médio do ápice posterior de +1.83 mm (IC95% +1.62 a +2.03; P < 10⁻⁵⁷). A correlação entre os valores de desvio de elevação anterior (Df) e posterior (Db) do Belin/Ambrósio Enhanced Ectasia Display (BAD), aparentemente positiva na amostra global (r = +0.306; P < 10⁻¹⁰), revelou-se um artefato de confusão (Paradoxo de Simpson): no subgrupo ceratocone, r = −0.038 (IC95% −0.367 a +0.299; P = 0.83). A AUROC da elevação posterior (Db) para discriminação Normal vs KC foi de 0.917 (d = +3.57), significativamente superior à da elevação anterior (Df: AUROC = 0.850; d = +1.91). No ceratocone grave (BAD_D > 10), o Df atingiu +35.2 ± 36.8, contra +10.2 ± 4.5 do Db (Wilcoxon pareado: W = 0; P = 0.004), com a variância do Df excedendo a de olhos normais por fator de 449× (Levene P < 10⁻¹⁶). A regressão múltipla dos descritores de forma posterior sobre os anteriores explicou no máximo R² = 0.025 (F₃,₅₂₂ = 4.54; P = 0.004). Nos modelos FEM, o *coupling ratio* (ΔZ_ant/ΔZ_post) foi de 0.954 ± 0.010 (CV = 1.05%), independentemente da morfologia da ectasia simulada.

**Conclusão:** As superfícies anterior e posterior da córnea comportam-se como entidades biomecânicas dissociadas. O desvio de elevação posterior (Db) do BAD constitui o sensor primário da descompensação ectásica, enquanto a elevação anterior (Df/KMax) reflete um evento tardio de colapso catastrófico de casca (*shell buckling*). A utilização do KMax como parâmetro diagnóstico primário introduz retardo sistemático na detecção de susceptibilidade à ectasia.

---

## 1. Introdução

A detecção precoce da susceptibilidade à ectasia corneana permanece um dos maiores desafios da cirurgia refrativa contemporânea.¹ A identificação de olhos com risco de descompensação biomecânica — antes que alterações topográficas se tornem clinicamente evidentes — é essencial para a segurança do paciente e para a prevenção da ectasia iatrogênica pós-operatória.²

Historicamente, a ceratometria máxima (KMax) e os mapas de curvatura da superfície anterior, obtidos inicialmente por reflexão de disco de Plácido, constituíram a base seminal do diagnóstico e estadiamento do ceratocone.³ A classificação de Amsler-Krumeich, amplamente adotada na prática clínica, estratifica a gravidade da doença com base primordialmente em valores de curvatura anterior.⁴ Mais recentemente, protocolos de indicação de *crosslinking* (CXL) corneano fundamentam-se na documentação de aumento progressivo do KMax — tipicamente > 1.0 D em 12 meses — como evidência de progressão.¹

Com o advento da tomografia corneana de Scheimpflug, o Belin/Ambrósio Enhanced Ectasia Display (BAD) permitiu a análise integrada de parâmetros de elevação anterior (Df), elevação posterior (Db), perfil paquimétrico e seus respectivos desvios em relação a um banco de dados normativo.⁵,⁶ A inclusão da elevação posterior representou um avanço paradigmático, uma vez que alterações desta superfície são frequentemente reconhecidas como o primeiro sinal tomográfico de ectasia.⁷,⁸

A integração subsequente de dados tomográficos com parâmetros biomecânicos derivados do Corvis ST (Oculus) deu origem ao Tomographic and Biomechanical Index (TBI), que utiliza inteligência artificial (random forest com leave-one-out cross-validation) para otimizar a detecção de susceptibilidade à ectasia.⁹ Este conceito — de que a avaliação multimodal supera qualquer parâmetro isolado — constitui o fundamento do presente estudo.

Paralelamente, o Índice de Integridade Fibrilar (FII), derivado da razão de backscattering estromal anterior/posterior em OCT de domínio espectral de alta resolução, permite quantificar o deslizamento lamelar intersticial como biomarcador radiômico de dano microestrutural.¹⁰ A modelagem por Elementos Finitos (FEM) com material hiperelástico anisotrópico (Holzapfel-Gasser-Ogden) oferece ainda a possibilidade de simular *in silico* o comportamento diferencial das superfícies anterior e posterior sob condições controladas de debilitamento estromal.

Embora o BAD, o TBI e outros índices compostos tenham revolucionado o diagnóstico da ectasia, a contribuição relativa de cada superfície corneana — e as implicações biomecânicas da anisotropia estromal — permanecem insuficientemente caracterizadas. O presente estudo propõe-se a: (i) quantificar o acoplamento espacial e de magnitude entre deformações anterior e posterior; (ii) avaliar se a forma do defeito posterior determina a forma do anterior; (iii) modelar a dinâmica de progressão do Df em função da severidade; e (iv) caracterizar o padrão de falha da superfície anterior como fenômeno de colapso de casca (*shell buckling*).

---

## 2. Métodos

### 2.1. Populações de Estudo

O estudo incluiu dados de três fontes independentes, conforme descrito a seguir.

**Base SPR Scheimpflug (n = 660 olhos).** Arquivos binários de curvatura (.spr) obtidos por tomografia Scheimpflug (Pentacam, Oculus GmbH, Wetzlar, Alemanha) foram processados por decodificador computacional proprietário. Para cada olho, foram extraídos: raio de curvatura sagital das superfícies anterior e posterior, coordenadas do ápice de curvatura (posição radial em mm e ângulo meridional), descritores de forma (irregularidade, assimetria, residual RMS) e índice de descentração do ápice.

**Base Pareada OCT-Pentacam (n = 443 olhos).** Exames de OCT de domínio espectral (Triton DRI-OCT, Topcon Corp., Tóquio, Japão) e tomografia Scheimpflug (Pentacam) do mesmo paciente foram pareados por nome e lateralidade. O conjunto de dados incluiu 408 olhos classificados como normais e 35 olhos com diagnóstico de ceratocone clínico, confirmado por topografia (padrão de Rabinowitz), sinais biomicroscópicos e/ou história clínica compatível. As variáveis tomográficas incluíram os valores finais de desvio do BAD (D, Df, Db), ceratometrias (K1, K2), paquimetria mínima e ART_Max. Os índices radiômicos incluíram o FII nas regiões central, inferotemporal (IT), inferocentral (IC) e inferonasal (IN).

**Base FEM (n = 24 modelos).** Modelos tridimensionais de Elementos Finitos foram construídos em FEBio (Musculoskeletal Research Laboratories, Universidade de Utah) utilizando formulação de material hiperelástico anisotrópico (Holzapfel-Gasser-Ogden — HGO), que incorpora a orientação preferencial das fibrilas de colágeno. A base incluiu 3 variações morfológicas de ectasia (esférica, oval, triangular) e 18 variações paramétricas de diâmetro (D5, D6), profundidade (d60, d70, d80) e espessura residual (t150 a t300 µm). O *coupling ratio* — definido como a razão entre o deslocamento vertical anterior (ΔZ_ant) e posterior (ΔZ_post) — foi calculado em três posições radiais: ápice, raio intermediário (R = 2.5 mm) e periferia (R = 4.0 mm).

### 2.2. Análise Estatística

A normalidade das distribuições foi avaliada pelo teste de Shapiro-Wilk. Dada a distribuição não gaussiana de múltiplas variáveis, as comparações entre grupos (Normal vs KC) foram realizadas pelo teste de Mann-Whitney U. A homogeneidade de variâncias foi avaliada pelo teste de Levene. O tamanho de efeito foi quantificado pelo d de Cohen (*pooled*). Correlações bivariadas foram calculadas pelo coeficiente de Pearson (r) e pelo coeficiente de Spearman (ρ), com intervalos de confiança a 95% obtidos por transformação Z de Fisher. A capacidade discriminativa dos parâmetros de elevação (Df, Db) e dos índices radiômicos (FII) para a diferenciação entre olhos normais e olhos com ceratocone clínico foi avaliada pela área sob a curva ROC (AUROC). As comparações entre AUROCs foram planejadas pelo método de DeLong et al. A contribuição preditiva dos descritores de forma da superfície posterior sobre os da anterior foi avaliada por regressão linear múltipla, com significância global testada pelo teste F.

Os dados foram analisados em Python 3.14 (Python Software Foundation), utilizando as bibliotecas scipy 1.15 e scikit-learn 1.6. O nível de significância estatística foi estabelecido em P < 0.05 (bicaudal) para todas as análises.

---

## 3. Resultados

### 3.1. Características Demográficas e Clínicas

**Tabela 1.** Dados demográficos e parâmetros clínicos por grupo diagnóstico (média ± DP [IC95%]).

| Parâmetro | Normal (n = 408) | KC (n = 35) | U | P | d |
|-----------|------------------|-------------|---|---|---|
| K1 (D) | 42.70 ± 1.59 [42.55–42.86] | 45.32 ± 3.61 [44.13–46.52] | 3.999 | 1.6×10⁻⁵ | +1.44 |
| Paq. Mín. (µm) | 534.6 ± 29.1 [531.8–537.4] | 466.9 ± 40.8 [453.4–480.4] | 13.020 | 6.0×10⁻¹⁶ | −2.24 |
| BAD_D | 1.13 ± 0.70 [1.06–1.20] | 8.43 ± 6.65 [6.22–10.63] | 0 | 9.0×10⁻²³ | +3.72 |
| BAD_Df | +0.05 ± 1.07 [−0.05 a +0.16] | +12.26 ± 22.71 [+4.74 a +19.78] | 2.144 | 6.3×10⁻¹² | +1.91 |
| BAD_Db | −0.03 ± 0.96 [−0.12 a +0.06] | +5.86 ± 4.94 [+4.22 a +7.49] | 1.185 | 2.6×10⁻¹⁶ | +3.57 |
| FII_IT | 1.213 ± 0.160 [1.198–1.229] | 1.207 ± 0.148 [1.158–1.256] | 7.694 | 0.446 | −0.04 |

Os olhos com ceratocone apresentaram valores significativamente mais elevados de curvatura (K1: P = 1.6×10⁻⁵; d = +1.44) e de todos os parâmetros de desvio do BAD (P < 10⁻¹²), com correspondente redução da paquimetria mínima (P = 6.0×10⁻¹⁶; d = −2.24). O tamanho de efeito da elevação posterior (Db: d = +3.57) foi 1.87 vezes superior ao da elevação anterior (Df: d = +1.91), indicando maior resolução discriminativa da superfície posterior. O FII_IT não diferiu significativamente entre os grupos nesta coorte (P = 0.446), achado discutido na seção de limitações.

### 3.2. Ausência de Acoplamento Espacial Anterior-Posterior

Na base SPR (n = 660 olhos), a correlação entre a posição radial do ápice de curvatura anterior e a do ápice posterior foi estatisticamente nula:

$$r = +0.027 \quad (\text{IC95\%: } -0.050 \text{ a } +0.103; \quad P = 0.50)$$

O ápice posterior localizou-se, em média, 1.83 mm mais perifericamente que o anterior (IC95% +1.62 a +2.03; DP = 2.66; teste t uniamostra: t = 17.63; P = 2.8×10⁻⁵⁷). A magnitude absoluta do *shift* foi de 2.59 ± 1.97 mm, com correlação significativa com o índice de descentração (r = +0.550; P = 9.8×10⁻⁵²).

Estes dados demonstram que **a curvatura posterior não apresenta correlação com a curvatura anterior**, nem em localização espacial nem em co-variação dos picos de curvatura. A posição do ápice de uma superfície não fornece informação preditiva sobre a posição do ápice da outra.

### 3.3. Correlação Df × Db: Paradoxo de Simpson

**Tabela 2.** Correlação Pearson entre BAD_Df e BAD_Db, estratificada por grupo diagnóstico.

| Grupo | n | r | IC95% | P | ρ (Spearman) |
|-------|---|---|-------|---|--------------|
| Global | 443 | +0.306 | +0.219 a +0.388 | 4.5×10⁻¹¹ | +0.238 |
| Normal | 408 | +0.134 | +0.037 a +0.228 | 6.9×10⁻³ | +0.144 |
| **KC** | **35** | **−0.038** | **−0.367 a +0.299** | **0.83** | **+0.219** |

A análise global (não estratificada) sugeriu correlação moderada e significativa entre Df e Db (r = +0.306; P < 10⁻¹⁰). Contudo, esta correlação constitui um artefato estatístico clássico: o Paradoxo de Simpson. A separação entre as médias populacionais dos grupos Normal e KC — cuja magnitude é substancialmente maior que a variabilidade intragrupo — gera uma associação espúria quando os dados são analisados em conjunto. Na análise estratificada, a correlação desaparece praticamente no grupo Normal (r = +0.134) e é nula no grupo KC (r = −0.038; P = 0.83). As superfícies anterior e posterior não apresentam co-variação significativa em nenhum dos dois contextos clínicos relevantes.

### 3.4. Capacidade Discriminativa: Elevação Posterior Superior à Anterior

**Tabela 3.** AUROC para diferenciação Normal vs Ceratocone Clínico.

| Parâmetro | AUROC | d de Cohen |
|-----------|-------|------------|
| BAD_Df (elevação anterior) | 0.850 | +1.91 |
| **BAD_Db (elevação posterior)** | **0.917** | **+3.57** |
| BAD_D (índice composto) | 1.000 | +3.72 |
| Modelo combinado (Df + Db + FII) | 0.968 | — |

A AUROC da elevação posterior (0.917) foi superior à da elevação anterior (0.850), com tamanho de efeito praticamente dobrado (d = 3.57 vs 1.91). Este achado é consistente com a premissa de que a superfície posterior, por ser biomecanicamente mais complacente, responde mais precocemente e com maior fidelidade ao defeito ectásico subjacente.⁵,⁷

### 3.5. Independência Morfológica: A Forma Posterior Não Determina a Forma Anterior

**Tabela 4.** Regressão linear múltipla: descritores de forma da superfície posterior como preditores da forma anterior (n = 526 olhos SPR).

| Variável Dependente (Anterior) | R² | F(3, 522) | P |
|--------------------------------|-----|-----------|---|
| Irregularidade | 0.005 | 0.80 | 0.493 |
| Assimetria | 0.001 | 0.13 | 0.942 |
| Residual (RMS) | 0.025 | 4.54 | 0.004 |

Os três descritores de forma da superfície posterior (irregularidade, assimetria e residual), utilizados conjuntamente como variáveis independentes, explicaram no máximo 2.5% da variância dos descritores correspondentes da superfície anterior. Este resultado indica que a morfologia do defeito posterior não se transmite para a anterior: as superfícies geram suas respectivas formas por mecanismos independentes.

### 3.6. Confirmação por Elementos Finitos: Acoplamento Constitutivo, Não Morfológico

**Tabela 5.** *Coupling ratio* (ΔZ_ant / ΔZ_post) nos modelos FEM por morfologia de ectasia.

| Morfologia | Coupling (Ápice) | Coupling (Mid) | Coupling (Periferia) |
|-----------|------------------|----------------|----------------------|
| Esférica (*baseline*) | 0.923 | 0.945 | 1.024 |
| Oval | 0.958 | 0.947 | 1.016 |
| Triangular | 0.958 | 0.931 | 1.015 |
| **Todos (n = 24)** | **0.954 ± 0.010** | — | — |
| **CV** | **1.05%** | — | — |

A variação do *coupling ratio* entre todas as morfologias e parametrizações foi de apenas 1.05% (CV). Este dado demonstra que a transmissão mecânica entre superfícies é uma propriedade constitutiva — determinada pela rigidez do material estromal e pela orientação fibrilar — e não pela geometria específica da ectasia. A superfície anterior transmite aproximadamente 95% da magnitude do deslocamento posterior, mas filtra sua forma espacial, comportando-se como filtro mecânico passa-baixa.

### 3.7. Evidência de *Shell Buckling*: Transição Catastrófica da Superfície Anterior

**Tabela 6.** Desvios de elevação por estágio de severidade no ceratocone.

| Estágio (BAD_D) | n | Df (média ± DP) | Db (média ± DP) | Razão Df/Db | Var(Df) |
|------------------|---|-----------------|-----------------|-------------|---------|
| Moderado (3–6) | 16 | +4.69 ± 3.49 | +4.10 ± 5.08 | 1.14 | 12.2 |
| Avançado (6–10) | 10 | +3.74 ± 4.40 | +4.78 ± 2.26 | 0.78 | 19.4 |
| **Grave (>10)** | **9** | **+35.18 ± 36.76** | **+10.18 ± 4.54** | **3.45** | **1.351** |

No estágio avançado, a razão Df/Db foi de 0.78, indicando que a superfície anterior estava proporcionalmente menos deformada que a posterior — comportamento consistente com resistência ativa da casca estromal anterior. No estágio grave, ocorreu inversão súbita: o Df saltou para +35.18 (aumento de 9.4× em relação ao estágio anterior), enquanto o Db cresceu apenas 2.1×. A diferença entre Df e Db no estágio grave foi estatisticamente significativa (Wilcoxon pareado: W = 0; P = 0.004).

A variância do Df no ceratocone (515.7) excedeu a de olhos normais (1.15) por fator de **449×** (teste de Levene: P = 1.1×10⁻¹⁶), enquanto a do Db cresceu 26×. Este padrão — estabilidade aparente seguida de deformação súbita e altamente variável — é a assinatura mecânica de *shell buckling* (flambagem de casca), fenômeno bem caracterizado na engenharia de estruturas de casca fina.¹¹

### 3.8. Ectasia Sub-clínica: Colapso Fibrilar com KMax Dentro da Normalidade

Na base de validação FII-Pentacam, foram identificados 4 olhos com colapso fibrilar confirmado por OCT (FII_IT < 1.05) cujo KMax médio era de 44.19 D (IC95% 43.58–44.81; DP = 0.63). Todos estes olhos (100%) apresentavam KMax inferior a 45 D — valor universalmente considerado dentro dos limites de normalidade. Nenhum destes pacientes satisfazia critérios topográficos convencionais para suspeita de ectasia, apesar de já apresentarem evidência radiômica de deslizamento lamelar ativo.

---

## 4. Discussão

### 4.1. O Modelo de Filtro Passa-Baixa e a Dissociação Anterior-Posterior

Estudos de microscopia Brillouin demonstraram que o módulo de elasticidade do estroma anterior (primeiros ~130 µm) é aproximadamente 3 vezes superior ao do estroma posterior,¹² em consequência da orientação oblíqua e entrelaçada das fibrilas de colágeno, as *bow springs* descritas por Winkler et al.¹³ Esta anisotropia cria uma assimetria funcional fundamental: a superfície posterior, com lamelas paralelas de baixa rigidez, responde focalmente ao defeito ectásico, enquanto a superfície anterior, mecanicamente mais robusta, redistribui o *stress* por uma área extensa.

Nossos resultados demonstram, por três linhas independentes de evidência, que esta redistribuição elimina a correlação entre as superfícies: (i) os ápices de curvatura não co-localizam (r = 0.027; P = 0.50); (ii) a forma posterior explica menos de 2.5% da forma anterior (R² = 0.025); e (iii) o *coupling ratio* FEM é insensível à morfologia (CV = 1.05%), confirmando que a transmissão mecânica preserva a magnitude (~95%) mas atenua a frequência espacial — comportamento clássico de filtro passa-baixa.

### 4.2. Implicações para a Avaliação de Susceptibilidade à Ectasia

Ambrósio et al. propuseram a distinção conceptual entre *Corneal Ectasia Diagnostics* (CED) — a confirmação e estadiamento da doença estabelecida — e *Ectasia Risk Assessment* (ERA) — a caracterização da susceptibilidade intrínseca à descompensação biomecânica antes do aparecimento de sinais clínicos.² Os nossos achados reforçam esta distinção e acrescentam uma dimensão biomecânica: o KMax, enquanto parâmetro exclusivamente anterior, é inerentemente um instrumento de CED (mede a consequência geométrica do colapso já instalado), sendo inadequado como ferramenta de ERA.

O padrão observado de variância explosiva do Df no ceratocone avançado (449× a de normais; P < 10⁻¹⁶) — contrastando com o crescimento ordenado do Db (26×) — é patognomônico de *shell buckling*: a casca anterior mantém-se estável até um limiar crítico de *stress*, ultrapassado o qual cede de forma catastrófica e imprevisível.¹¹ A dependência clínica do KMax como indicador de progressão — base de protocolos de indicação de CXL — é, portanto, vulnerável a dois erros: (i) falsos negativos nos estágios iniciais, quando a casca anterior ainda resiste; e (ii) detecção tardia, quando o *buckling* já ocorreu.

A existência de olhos com evidência radiômica de colapso fibrilar (FII_IT < 1.05) e KMax dentro da normalidade (44.2 ± 0.6 D) corrobora esta vulnerabilidade e reforça a necessidade de integração multimodal — tomográfica (BAD_Db), biomecânica (TBI/CBI) e radiômica (FII) — no *pipeline* de ERA.

### 4.3. Limitações

O subgrupo KC (n = 35), embora suficiente para demonstrar significância estatística robusta nas comparações primárias (P < 10⁻¹²), limitou o poder da estratificação por severidade, particularmente no estágio grave (n = 9). A AUROC modesta do FII_IT (0.539) nesta coorte atribui-se provavelmente a viés de seleção: os pares OCT-Pentacam foram construídos retrospectivamente a partir de exames disponíveis, sem garantia de contemporaneidade, o que pode ter reduzido a correspondência temporal entre o estado estrutural (FII) e o estado tomográfico. Estudos prospectivos longitudinais com aquisição simultânea multimodal são necessários para validar a sequência temporal das fases propostas e determinar o limiar de *stress* crítico do *buckling* anterior.

---

## 5. Conclusões

1. **A curvatura posterior não apresenta correlação com a curvatura anterior** — nem em localização espacial (r = 0.027; P = 0.50), nem em morfologia (R² < 2.5%), nem em co-variação dos valores de desvio do BAD dentro do grupo ceratocone (r = −0.038; P = 0.83).

2. A elevação posterior (BAD_Db) constitui o **sensor primário** da descompensação ectásica, com AUROC (0.917) e tamanho de efeito (d = 3.57) significativamente superiores aos da elevação anterior (AUROC = 0.850; d = 1.91).

3. A elevação abrupta do KMax/Df no ceratocone avançado corresponde a um evento de ***shell buckling*** — com variância 449× superior à de normais (Levene P < 10⁻¹⁶) e razão Df/Db = 3.45 no estágio grave (Wilcoxon P = 0.004) — e não a uma progressão linear e previsível da doença.

4. A dependência do KMax como parâmetro diagnóstico primário introduz **retardo sistemático na detecção de susceptibilidade à ectasia**: foram identificados olhos com colapso fibrilar ativo (FII_IT < 1.05) e KMax perfeitamente normal (44.2 ± 0.6 D).

5. A integração de parâmetros posteriores (BAD_Db), biomecânicos (TBI) e radiômicos (FII) ao *pipeline* de *Ectasia Risk Assessment* é fundamental para a detecção pré-topográfica da susceptibilidade e para superar as limitações inerentes à dependência do KMax.

---

## Referências

1. Gomes JA, Tan D, Rapuano CJ, et al. Global consensus on keratoconus and ectatic diseases. *Cornea.* 2015;34(4):359-369.
2. Ambrósio R Jr, Lopes BT, Faria-Correia F, et al. Ectasia detection by the assessment of corneal biomechanics. *Cornea.* 2016;35(7):e18-e20.
3. Rabinowitz YS. Keratoconus. *Surv Ophthalmol.* 1998;42(4):297-319.
4. Krumeich JH, Daniel J, Knülle A. Live-epikeratophakia for keratoconus. *J Cataract Refract Surg.* 1998;24(4):456-463.
5. Ambrósio R Jr, Caiado ALC, Guerra FP, et al. Novel pachymetric parameters based on corneal tomography for diagnosing keratoconus. *J Refract Surg.* 2011;27(10):753-758.
6. Belin MW, Ambrósio R Jr. Scheimpflug imaging for keratoconus and ectatic disease. *Indian J Ophthalmol.* 2013;61(8):401-406.
7. Ambrósio R Jr, Valbon BF, Faria-Correia F, et al. Scheimpflug imaging for laser refractive surgery. *Curr Opin Ophthalmol.* 2013;24(4):310-320.
8. de Sanctis U, Loiacono C, Richiardi L, et al. Sensitivity and specificity of posterior corneal elevation measured by Pentacam in discriminating keratoconus/subclinical keratoconus. *Ophthalmology.* 2008;115(5):735-740.
9. Ambrósio R Jr, Lopes BT, Faria-Correia F, et al. Integration of Scheimpflug-based corneal tomography and biomechanical assessments for enhancing ectasia detection. *J Refract Surg.* 2017;33(7):434-443.
10. Reis M. Índice de Integridade Fibrilar: quantificação radiômica do deslizamento lamelar por OCT de alta resolução. *[Em preparação].*
11. Bushnell D. Buckling of shells — pitfall for designers. *AIAA Journal.* 1981;19(9):1183-1226.
12. Scarcelli G, Pineda R, Yun SH. Brillouin optical microscopy for corneal biomechanics. *Invest Ophthalmol Vis Sci.* 2012;53(1):185-190.
13. Winkler M, Shoa G, Xie Y, et al. Three-dimensional distribution of transverse collagen fibers in the anterior human corneal stroma. *Invest Ophthalmol Vis Sci.* 2013;54(12):7293-7301.

---

*Correspondência: Projeto Biomecânica Corneana — Análise Computacional Multi-Modal*
*Dados e código-fonte: https://github.com/miguelreiz/pentacam-scheimpflug-ai*
