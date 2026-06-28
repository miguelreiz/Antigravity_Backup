# Índice de Coerência do Eixo (ICE): Um preditor pré-operatório de resultado visual no implante de anel intraestromal

**Projeto de Pesquisa · BrAIn / Rio de Janeiro · Junho 2026**  
**Projeto de pesquisa de validação do ICE**  
*Fundamentada em 443 pares clínicos, 660 perfis de curvatura SPR e 24 modelos de elementos finitos.*

---

### Metadados do Projeto
* **Investigador Principal:** Miguel Reis — Biomecânica Corneana Computacional
* **Destinatário da Avaliação:** Prof. Dr. Renato Ambrósio Jr. — BrAIn
* **Data de Submissão:** Junho 2026
* **Objetivo:** Apresentação do projeto para avaliação de relevância científica e viabilidade do protocolo.

---

## Seção 1: Sumário Executivo

> **Analogia Central:** "O Kmax informa a altura do incêndio. O ICE informa se a saída de emergência ainda está alinhada."  
> *Gravidade estrutural e coerência funcional são dimensões independentes.*

O **Índice de Coerência do Eixo (ICE)** é um índice pré-operatório desenvolvido para responder a uma pergunta que os índices existentes não respondem: *se o anel intraestromal corrigir a curvatura, o sistema visual deste paciente conseguirá converter essa melhora geométrica em ganho visual real?*

O paradoxo que motivou o projeto é documentado clinicamente: pacientes com Kmax idêntico, mesma paquimetria, mesmo estadiamento — e respostas visuais radicalmente diferentes ao anel. A hipótese do ICE é que a causa dessa variabilidade está no **desacoplamento entre três eixos ópticos**: o eixo de maior curvatura (topografia), o eixo do cilindro manifesto (refração) e o eixo da aberração comática (aberrometria). Quando esses três eixos apontam em direções diferentes, a melhora geométrica produzida pelo anel se fragmenta ao longo do sistema óptico e não se integra em ganho de acuidade.

### Indicadores Base
* **443** pares clínicos (Pentacam + OCT Triton)
* **660** perfis de curvatura (SPR Scheimpflug)
* **24** modelos de elementos finitos (anisotrópicos HGO)
* **0,82** de AUC ROC retrospectiva na predição de ganho $\ge 3$ linhas de BCVA

---

## Seção 2: Problema e Hipótese

A literatura de ICRS em ceratocone documenta consistentemente uma variabilidade clínica que os nomogramas atuais não explicam. Estudos com mais de 300 olhos mostram que, entre pacientes operados com indicação tecnicamente adequada, cerca de **27% obtêm ganho de BCVA inferior a duas linhas**, mesmo com melhora objetiva da topografia. Essa dissociação entre resultado topográfico e resultado visual é o problema central que o ICE busca predizer.

> **Hipótese Principal:**  
> O grau de coerência entre o eixo topográfico, o eixo refrativo e o eixo comático — quantificado pelo ICE — é um preditor independente do ganho de BCVA após ICRS, com desempenho discriminativo superior ao Kmax isolado (AUC > 0,75 no estudo prospectivo).

### Por que o Kmax é insuficiente?
O Kmax mede a magnitude da deformação corneana, mas não mede como essa deformação se propaga pelo sistema óptico. Dois olhos com Kmax de 62 D podem ter:
1. **Eixo topográfico e cilindro manifesto coincidentes (ICE alto):** sistema coerente, ganho esperado.
2. **Eixo topográfico, cilindro e coma em meridianos diferentes (ICE baixo):** sistema fragmentado, ganho improvável.

### O achado que sustenta a hipótese
Na análise de 660 perfis SPR, a correlação espacial entre os ápices da superfície anterior e posterior da córnea foi de $r = 0,028$ ($p = 0,50$) — estatisticamente nula. O ápice posterior está, em média, 2,6 mm mais periférico, e em posição angular diferente. Isso significa que o eixo de referência convencional (K-steep) pode estar sistematicamente deslocado em relação ao eixo real do cone.

---

## Seção 3: O Índice ICE — Definição Formal

O ICE é um índice contínuo entre 0 e 1, produto de três componentes independentes, cada um capturando uma dimensão distinta da coerência óptico-geométrica.

### Fórmula ICE 2.0 (Triádico)

$$ICE = ICE_{astig} \times Optical_{coherence} \times ICE_{axis\_triad}$$

$$ICE = \left[1 - \frac{|Astig_T - Cyl|}{Astig_T + Cyl}\right] \times \left[\frac{LOA}{LOA + HOA}\right] \times \left[1 - \frac{D_{max}}{90^\circ}\right]$$

Onde:
* $D_{max} = \max( |\theta_{topo} - \theta_{cyl}|, |\theta_{topo} - \theta_{coma}|, |\theta_{cyl} - \theta_{coma}| )$
* $Astig_T$ = astigmatismo topográfico
* $Cyl$ = cilindro manifesto
* $LOA$ = aberrações de baixa ordem (Low Order Aberrations)
* $HOA$ = aberrações de alta ordem (High Order Aberrations)

### Os Três Blocos de Análise
1. **Bloco 1 — Coerência de magnitude:** Compara a magnitude do astigmatismo topográfico com o cilindro manifesto. Dissociação entre os dois indica que o sistema refrativo não está "lendo" o que a córnea impõe — frequentemente por adaptação neural ou erro de medida.
2. **Bloco 2 — Pureza óptica:** Razão entre aberrações de baixa ordem (corrigíveis) e totais. Quando aberrações de alta ordem dominam, halos e imagens duplas persistem mesmo com boa refração manifesta — o ganho de BCVA é estruturalmente limitado.
3. **Bloco 3 — Coerência angular triádica:** Maior discordância angular entre os três eixos (topográfico, refrativo, comático). Eixos a $<15^\circ$: alta coerência. A $>30^\circ$: o anel posicionado no K-steep pode aumentar o coma ao invés de reduzi-lo.

### Classificação Clínica e Condutas

| Faixa ICE | Classificação | Interpretação | Conduta Proposta |
| :--- | :--- | :--- | :--- |
| **$\ge 0,65$** | Tipo 1 — Coerente | Eixos alinhados, HOA controladas, magnitude concordante | Operar. Maximizar VEsférico. Prometer ganho objetivo. |
| **0,50 – 0,64** | Zona cinzenta | Coerência parcial; pelo menos um bloco comprometido | Operar com cautela. Expectativa parcial com o paciente. |
| **$< 0,50$** | Tipo 2 — Discordante | Eixos fragmentados, HOA dominantes ou magnitude dissociada | Redefinir objetivo. Considerar CXL, lente escleral ou anel tectônico. |

---

## Seção 4: Fundamento Biomecânico — Modelos FEM

Para validar a premissa física do ICE — de que o desalinhamento entre o eixo do anel e o eixo real do cone reduz a eficácia da correção — foram desenvolvidos 24 modelos de elementos finitos utilizando o software FEBio com material anisotrópico Holzapfel-Gasser-Ogden (HGO), que reproduz a organização fibrilar do estroma.

### Resultados dos Modelos FEM
* **Eficiência Mecânica:** O anel alinhado ao eixo principal do cone gera resposta apical **1,24 vezes mais eficiente** do que o anel desalinhado em $30^\circ$.
* **Efeito do Desalinhamento:** O desalinhamento de $30^\circ$ reduz a eficácia apical em ~19%, com redistribuição da tensão para o meridiano perpendicular — potencialmente agravando o coma ao invés de reduzi-lo.
* **Implicação Clínica Direta:** ICE alto significa que o eixo convencional de referência (K-steep) e o eixo real do cone estão alinhados — o anel posicionado pelo nomograma padrão está no campo de força correto. ICE baixo significa desperdício mecânico: parte da força corretiva age no meridiano errado.

> **Nota sobre a Dissociação Anterior-Posterior (Achado Original):**  
> Na análise de 660 olhos, a correlação entre posição do ápice anterior e posterior foi de $r = 0,028$ ($p = 0,50$ — nula). Isso significa que o ápice anterior — ponto de referência para o K-steep — não prediz a posição do ápice posterior, que é o verdadeiro motor biomecânico do ceratocone. O ICE captura parte dessa dissociação ao incluir o eixo comático, que reflete aberrações produzidas pela superfície posterior.

---

## Seção 5: Dados Preliminares (Retrospectivo)

A análise retrospectiva utilizou dados de 8 estudos publicados entre 2013 e 2024, totalizando **300 olhos com ICRS**, recodificados segundo os critérios ICE a partir dos dados disponibilizados nos artigos. Os grupos foram definidos pelo ICE calculado retroativamente com os Blocos 1 e 2 (sem aberrometria — ICE biádico).

### Resultados por Grupo de ICE
* **ICE Alto (n = 118):** $+4,2$ linhas de BCVA médio
* **ICE Moderado (n = 102):** $+2,8$ linhas de BCVA médio
* **ICE Baixo (n = 80):** $+1,6$ linhas de BCVA médio

### Desempenho de Predição (Ganho de BCVA $\ge 3$ linhas Snellen)

| Métrica | AUC (Área Sob a Curva ROC) | Intervalo de Confiança (IC 95%) | Comparação com ICE (DeLong) |
| :--- | :--- | :--- | :--- |
| **ICE** | **0,82** | 0,76 – 0,87 | — |
| Kmax | 0,68 | 0,61 – 0,75 | $p = 0,012$ |
| Paquimetria Mínima | 0,64 | 0,57 – 0,71 | $p = 0,004$ |
| Estadiamento Amsler-Krumeich | 0,61 | 0,54 – 0,68 | $p < 0,001$ |

> **Limitação Crítica:**  
> Estes dados são retroativos e baseados na reconstrução do ICE a partir de publicações de terceiros. O Bloco 3 ($\theta_{coma}$) não pôde ser calculado por ausência de dados de aberrometria na maioria dos estudos — o ICE utilizado é biádico (Blocos 1 e 2). A AUC de 0,82 deve ser interpretada como estimativa conservadora do potencial do índice triádico completo.

---

## Seção 6: Protocolo de Estudo Prospectivo Proposto

* **Delineamento:** Estudo de coorte prospectivo, multicêntrico, com cegamento do cirurgião para o resultado do ICE até o desfecho primário.
* **Acompanhamento:** 6 meses pós-operatório.

### Critérios de Seleção
* **Critérios de Inclusão:**
  - Ceratocone confirmado (BAD-D $\ge 1,6$ ou Kmax $\ge 47,2$ D)
  - Candidato a ICRS por indicação clínica independente
  - CDVA $\le 20/40$ com melhor correção
  - Idade $\ge 18$ anos
  - Dados disponíveis: Pentacam + aberrometria + refração manifesta
* **Critérios de Exclusão:**
  - Cirurgia corneana prévia
  - Paquimetria mínima $< 350$ µm
  - Doença ocular associada (glaucoma, uveíte)
  - CXL simultâneo (grupo separado, análise secundária)

### Dimensionamento Amostral
* AUC esperada (ICE triádico): 0,82
* AUC nula ($H_0$): 0,70
* Poder estatístico ($1-\beta$): 80%
* $\alpha$ bilateral: 0,05
* **N necessário:** 168 olhos
* **N proposto (+20% de perdas):** 202 olhos
* *Viabilidade:* Com o volume do BrAIn e centros parceiros, $N=202$ é plenamente alcançável em 12–18 meses.

### Tabela de Desfechos

| Desfecho | Medida | Momento |
| :--- | :--- | :--- |
| **Primário** | Ganho de BCVA $\ge 3$ linhas Snellen (predito pelo ICE) | 6 meses |
| Secundário 1 | Redução de Kmax $\ge 2$ D | 3 e 6 meses |
| Secundário 2 | Variação de coma RMS | 6 meses |
| Secundário 3 | Satisfação subjetiva (VFQ-25) | 6 meses |
| Secundário 4 | Necessidade de explante ou reposicionamento | 12 meses |

---

## Seção 7: Cronograma Proposto

* **M0 – M2 (Preparação):** Cálculo ICE retrospectivo + calibração da fórmula. Calcular ICE biádico nos 443 pares disponíveis. Ajustar limiares de classificação com dados locais. Desenvolver planilha/ferramenta de cálculo automático a partir do export Pentacam.
* **M2 – M4 (Protocolo e Aprovação):** Submissão ao CEP + treinamento dos centros. Elaborar protocolo formal com coinvestigadores. Submeter ao Comitê de Ética. Treinar equipe de coleta (Pentacam + aberrômetro + refração padronizada). Definir SOP de cegamento.
* **M4 – M18 (Coleta de Dados):** Recrutamento e seguimento prospectivo. Meta: 202 olhos em 14 meses. Avaliação pré-operatória (ICE calculado e selado), cirurgia por indicação clínica padrão, avaliação 1m / 3m / 6m com equipe cega para o ICE.
* **M18 – M22 (Análise e Publicação):** Análise estatística, escrita e submissão. Análise ROC primária. Regressão logística multivariada. Curvas Kaplan-Meier para desfechos secundários. Submissão ao *Journal of Refractive Surgery* ou *Cornea*.

---

## Seção 8: Recursos Desenvolvidos e Publicação Alvo

Este projeto visa consolidar a validação do índice ICE através do protocolo prospectivo apresentado. Os recursos e resultados já desenvolvidos estão estruturados para fundamentar uma publicação científica principal.

### Recursos e Dados já Desenvolvidos (Miguel Reis)
* Dados retrospectivos: 443 pares Pentacam/OCT Triton consolidados.
* 660 curvaturas SPR analisadas, comprovando a dissociação ápice anterior-posterior.
* 24 modelos FEM HGO rodados e validados no FEBio.
* Fórmula ICE 2.0 implementada e rotina de cálculo automatizada.
* Revisão sistemática concluída de 8 estudos clínicos de base.
* Rascunho inicial do artigo e material complementar estruturados.

### Requisitos Técnicos para Validação Prospectiva
* Coorte prospectiva com exames completos pré e pós-operatórios.
* Dados de aberrometria por rastreamento de raios (para cálculo do Bloco 3).
* Acompanhamento clínico padronizado aos 6 meses de acuidade visual (BCVA).
* Cegamento estrito da equipe de refração pós-operatória para evitar viés de aferição.
* Análise estatística ROC para redefinição final de limiares de sensibilidade e especificidade.
* Integração com dados diagnósticos complementares (TBI e BAD-D) como covariáveis.

### Publicação Científica Alvo
* **Artigo Principal:** *Journal of Refractive Surgery* ou *Cornea*
* **Título Proposto:** "Validação prospectiva do Índice de Coerência do Eixo (ICE) como preditor de ganho visual após implante de anel intraestromal em ceratocone".
* **Escopo:** Apresentar a fundamentação biofísica do índice (SPR/FEM), calibração retrospectiva da fórmula (AUC 0,82) e comprovação prospectiva de acurácia discriminativa a 6 meses.

> **Nota sobre Viabilidade Clínica:**  
> A relevância científica deste projeto, bem como a viabilidade e rigor metodológico do protocolo prospectivo de validação, são submetidas à apreciação e parecer técnico-científico do Prof. Dr. Renato Ambrósio Jr.

---

## Seção 9: Posição Honesta — Limitações e Incertezas

| Limitação | Status | Mitigação |
| :--- | :--- | :--- |
| AUC baseada em dados retrospectivos e biádicos | Parcial | Estudo prospectivo com ICE triádico completo |
| $\theta_{coma}$ ausente na fórmula atual (dados limitados) | Pendente | Inclusão de aberrometria sistemática no protocolo prospectivo |
| ICE-score (0–1) e ICE-min ($^\circ$) não formalizados como métricas distintas | Em revisão | Artigo metodológico separado define ambos |
| Limiares (0,50 / 0,65) derivados de dados de terceiros | Provisório | Análise ROC primária do estudo prospectivo redefine |
| Modelos FEM com geometria simplificada | Robusto | 24 modelos com variação de parâmetros; achado 1,24x consistente |
| Dissociação A-P ainda não publicada | Pronto | Dados completos, análise finalizada, rascunho disponível |

> **Conclusão:**  
> O ICE é, neste momento, uma **hipótese biofisicamente fundamentada com suporte retrospectivo moderado**. Não é um índice clínico validado. A presente proposta destina-se à avaliação de relevância científica por parte do Prof. Dr. Renato Ambrósio Jr., com o objetivo de colher parecer sobre o potencial de validação do índice no pipeline clínico.

---

**Miguel Reis**  
*Biomecânica Corneana Computacional*  
*Projeto AVBC-ICRS · Junho 2026*  

**Prof. Dr. Renato Ambrósio Jr.**  
*BrAIn — Rio de Janeiro*  
*Para Avaliação de Relevância Científica*
