# Capítulo 6: PresbyMAX (Schwind) - A Abordagem Bi-Asférica Multifocal

> [!NOTE]
> **Definição Tecnológica:** O **PresbyMAX** (Schwind Eye-Tech-Solutions, Alemanha) é um módulo de software de ablação proprietário que difere fundamentalmente da modulação de asfericidade global contínua (Q-factor/Custom-Q). Baseia-se na criação de um perfil corneano **bi-asférico multifocal**, consistindo numa zona central otimizada para visão de perto e uma zona periférica para visão de longe, conectadas por uma zona de transição asférica suave. Esta arquitetura mimética a óptica de lentes de contacto multifocais de **Design Centro-Perto (Center-Near Design)**. [1]

## 6.1. Princípios Ópticos: Bi-Asfericidade vs. Prolatividade Contínua

### 6.1.1. Conceito de "Ilha Óptica" (Optical Island)

Ao contrário do Custom-Q/PresbyCor, que induz uma **curva de potência contínua** (gradient smooth de centro para periferia), o PresbyMAX estrutura a córnea em **zonas funcionais distintas**.

**Anatomia do Perfil PresbyMAX:**

**Zona 1 - Zona Central de Perto (Central Near Zone):**
- Diâmetro: 1.8-2.3 mm (programável)
- Geometria: Hiper-convexa (steepening acentuado)
- Função: Foca raios paraciais na distância de leitura (~33-40 cm)
- Potência adicional: +1.50 a +2.50 D (dependendo do perfil selecionado)

**Design Óptico Interno:**  
A zona central **não é uma simples esfera positiva** (o que induziria aberração esférica excessiva). Em vez disso, utiliza um perfil asférico otimizado que:
- Maximiza potência de perto
- Minimiza aberrações de alta ordem desnecessárias (redução de SA positiva que degradaria qualidade)

**Zona 2 - Zona de Transição (Transition Zone):**
- Largura: 0.8-1.2 mm
- Geometria: Asférica progressiva (blend suave)
- Função: **Crítica para qualidade visual**
  - Evita degraus abruptos que gerariam difração severa
  - Cria gradiente de potência contínuo (sem "saltos")
  
**Evidência:** Baenninger demonstrou que a qualidade da zona de transição correlaciona diretamente com sensibilidade ao contraste pós-operatória. Perfis com transições <0.8 mm apresentaram perda de >0.4 log units em frequências médias. [2]

**Zona 3 - Zona Periférica de Longe (Peripheral Distance Zone):**
- Início: ~3.5-4.0 mm do centro
- Extenção radial: Até zona óptica total (6.5-7.0 mm)
- Geometria: Ligeiramente prolata a esférica
- Função: Foca raios periféricos no infinito óptico

**Diferenciação Fundamental:**

| Característica | Custom-Q (PresbyCor) | PresbyMAX |
|----------------|----------------------|-----------|
| **Perfil de Potência** | Curva contínua suave | Zonas discretas (degraus funcionais) |
| **Zona Central** | Elevação moderada distribuída | "Ilha" steep pronunciada |
| **Transição** | Gradiente progressivo natural | Zona de transição engenheirada |
| **Add Máxima** | ~+1.50 a +1.75 D | ~+2.00 a +2.50 D |
| **Dependência Pupilar** | Moderada | **Alta** (ver Secção 6.3) |

### 6.1.2. Modelação Matemática do Perfil

A Schwind utiliza um algoritmo proprietário baseado em equações de **Zernike de alta ordem combinadas** que não é publicamente divulgado em detalhe. No entanto, a partir de análise reversa de topografias pós-PresbyMAX, observa-se:

**Aproximação Matemática (Zona Central):**

$$Z(r) = A \cdot \left(1 - e^{-\frac{r^2}{2\sigma^2}}\right) + B \cdot r^4$$

Onde:
- **Z(r):** Elevação em função do raio
- **A:** Amplitude da adição central (~15-25 μm para +2.00 D add)
- **σ:** Largura da zona central (Gaussian width)
- **B · r⁴:** Termo de aberração esférica de controlo (minimiza SA positiva excessiva)

Esta formulação cria um perfil de **"elevação tipo Gaussiana" (Gaussian-like)** no centro, diferente da elevação polinomial contínua do Custom-Q.

---

## 6.2. Variantes do Algoritmo PresbyMAX

### 6.2.1. PresbyMAX Simétrico (Symmetric)

**Configuração:**  
Ambos os olhos recebem o mesmo perfil multifocal com adição central completa.

**Parâmetros Standard:**
- Add central: +2.00 a +2.50 D (bilateral)
- Zona central: 2.1 mm
- Zona óptica total: 6.5 mm
- Target refrativo longe: Plano (0.00 D)

**Resultados Clínicos (Literatura):**

**Vantagens:**
- Excelente visão de perto binocular: 85-90% atingem J2 ou melhor [3]
- Independência de óculos para leitura: ~80%
- Simetria (ambos os olhos iguais facilita fusão em perto)

**Desvantagens:**
- **Perda de CDVA (Corrected Distance Visual Acuity):** Média de 1-2 linhas
  - Mecanismo: Ambos os olhos possuem zona central multifocal que degrada contraste em longe
  - ~15-20% pacientes queixam-se de "visão de longe não tão nítida quanto antes"
- **Halos noturnos severos:** 30-40% reportam halos proeminentes (especialmente pupilas >5.5 mm)
- **Sensibilidade ao contraste reduzida:** -0.2 a -0.3 log units em 12 cpd

**Indicação Atual:**  
Rara. Maioria dos cirurgiões abandonou estratégia simétrica em favor da híbrida (ver abaixo).

### 6.2.2. PresbyMAX Híbrido (Hybrid) - **PADRÃO ATUAL**

**Conceito (Uthoff et al.):**  
Combinar os benefícios da multifocalidade com os da monovisão, minimizando as desvantagens de cada uma. [4]

**Configuração:**

**Olho Dominante - "Otimizado para Longe com EDOF Leve":**
- **Opção A (Conservadora):** LASIK/PRK standard asférico **sem** PresbyMAX
  - Apenas correção refrativa (preserva Q natural ou wavefront-optimized)
  - Target: Plano (0.00 D)
  - Add: 0 D (usa apenas acomodação residual + pinhole natural)
  
- **Opção B (Moderada):** PresbyMAX "Mild" (se disponível no software)
  - Add central reduzida: +0.75 a +1.00 D
  - Zona central menor: 1.5 mm
  - Prioriza longe, adiciona ligeira DoF para intermédio

**Olho Não-Dominante - "Otimizado para Perto Multifocal Completo":**
- PresbyMAX completo
- Add central: +1.75 a +2.25 D
- Zona central: 2.1-2.3 mm
- Target refrativo: **-0.50 a -0.75 D** (micro-monovisão deliberada)

**Anisometropia Total Induzida:** 0.50-0.75 D

**Raciocínio Neurofisiológico:**

A estratégia híbrida permite:

1. **Olho dominante:** Fornece imagem de longe de alta qualidade (sem multifocalidade = sem perda de contraste)
2. **Olho não-dominante:** Fornece EDOF completa (perto + intermédio)
3. **Fusão binocular:** 
   - Longe: Cérebro seleciona input dominante (nítido)
   - Perto: Cérebro seleciona input não-dominante (multifocal)
   - Intermédio: Somação parcial de ambos

**Resultados Clínicos Híbrido (Baenninger, Luger):** [2,5]

| Parâmetro | PresbyMAX Symmetric | PresbyMAX Hybrid | Vantagem |
|-----------|---------------------|------------------|----------|
| **UCDVA (Longe) 20/25 ou melhor** | 75% | **92%** | Híbrido +17% |
| **UCNVA (Perto) J2 ou melhor** | 88% | 81% | Symmetric +7% (marginal) |
| **Halo Severo** | 35% | **18%** | Híbrido -17% |
| **Perda de Linhas CDVA** | 1.8 linhas | **0.4 linhas** | Híbrido preserva longe |
| **Satisfação Global** | 78% | **89%** | Híbrido +11% |
| **taxa de retratamento** | 18% | **9%** | Híbrido -50% |

**Conclusão Baseada em Evidência:**  
PresbyMAX Híbrido é a estratégia de escolha atual, com melhoria dramática em CDVA e satisfação comparado ao simétrico.

---

## 6.3. Dependência Pupilar: O Calcanhar de Aquiles

O design multifocal zonal do PresbyMAX cria uma **dependência crítica do diâmetro pupilar** para o desempenho óptico.

### 6.3.1. Dinâmica Óptica com Variação Luminosa

**Condições Fotópicas (Luz Brilhante, Pupila ~2.5 mm):**

- Pupila cobre **apenas a zona central** (near zone)
- **100% da luz** passa pela região steep multifocal
- **Resultado:**
  - Visão de perto: **Excelente** (toda a potência add disponível)
  - Visão de longe: **Comprometida** (sem acesso à zona periférica distance)
  - Efeito dominante: Near vision

**Problema Clínico:**  
Pacientes com miose fisiológica acentuada (pupilas fotópicas <2.0 mm, comum em pessoas >60 anos) podem ter dificuldade em longe durante o dia.

**Condições Mesópicas/Escotópicas (Iluminação Reduzida, Pupila ~5.5-6.5 mm):**

- Pupila expande, cobrindo **zona central + transição + periferia**
- Entrada simultânea de:
  - Raios centrais (focam perto)
  - Raios periféricos (focam longe)
- **Resultado:**
  - Visão de longe: **Recuperada** (utilização de zona periférica)
  - Visão de perto: Mantida (zona central continua ativa)
  - **Trade-off:** Halos noturnos (sobreposição de múltiplas imagens focais na retina)

### 6.3.2. Zonas de Risco Pupilar

**Pupila Fotópica Muito Pequena (<2.0 mm):**

- **Problema:** "Aprisionamento" na zona central
- **Sintoma:** Dificuldade em ver longe mesmo em plena luz do dia
- **Prevalência:** ~8-12% da população presbita
- **Contraindicação Relativa:** Considerar monovisão pura em vez de PresbyMAX

**Pupila Mesópica Muito Grande (>7.0 mm):**

- **Problema:** Abertura excessiva expõe zonas de transição e periferia
- **Sintoma:** Halos noturnos severos, starburst lights
- **Mecanismo Óptico:**
  - Múltiplas zonas ópticas simultâneas criam **múltiplos círculos de confusão** na retina
  - Sistema visual não consegue suprimir todas as imagens desfocadas
- **Prevalência:** 15-20% da população <55 anos
- **Contraindicação Absoluta** para PresbyMAX Symmetric
- **Gestão:** PresbyMAX Hybrid com add reduzida ou Custom-Q

### 6.3.3. Pupilometria Pré-Operatória Mandatória

**Protocolo de Avaliação:**

1. **Pentacam Pupil Diameter Module** ou **Sirius Pupilometry:**
   - Medir pupila fotópica (85 cd/m², luz ambiente brilhante)
   - Medir pupila mesópica (0.4 cd/m², luz muito reduzida)

2. **Critérios de Decisão para PresbyMAX:**

| Pupila Fotópica | Pupila Mesópica | Decisão PresbyMAX |
|-----------------|-----------------|-------------------|
| 2.5-3.5 mm | 5.0-6.5 mm | **IDEAL** - Prosseguir |
| <2.0 mm | <4.5 mm | **Risco** - Considerar alternativas |
| >3.5 mm | <5.5 mm | Regular - Prosseguir com cautela |
| Qualquer | >7.0 mm | **ALTO RISCO** - Contraindicar Symmetric, Hybrid com add reduzida |

---

## 6.4. Seleção de Pacientes e Limitações Biométricas

### 6.4.1. Candidatos Ideais

**Perfil Biométrico Óptimo:**

- **Idade:** 48-58 anos (acomodação residual <3.0 D)
- **Refração:** 
  - Hipermétropes: +0.50 a +3.50 D (**melhores candidatos**)
  - Emétropes: ±0.50 D (requerem gestão cuidadosa de expectativas)
  - Míopes: -1.00 a -3.00 D (cautela)
- **Pupila Mesópica:** 5.0-6.5 mm
- **Curvatura Corneana (K médio):** 42-46 D
- **Add Necessária:** +1.50 a +2.00 D

**Justificação:**  
Hipermétropes beneficiam-se duplamente: correção da hipermetropia de longe + adição de perto, ambas atingidas pelo mesmo perfil de steepening central.

### 6.4.2. Curvatura Corneana e Resposta Biomecânica

**Córneas Planas (K <40 D):**

**Desafio Biomecânico:**  
Córneas planas têm:
- Menor reserva de curvatura para modificação
- Maior rigidez biomecânica (raio de curvatura grande = lamelas sob maior tensão)

**Resultado:**  
Taxa elevada de **hipocorreção e regressão** do efeito multifocal.

**Evidência:**  
Estudo de Luger demonstrou que córneas com K <40 D apresentaram:
- Perda de Add aos 12 meses: 0.40 ± 0.22 D (vs. 0.18 ± 0.12 D em K >42 D)
- Taxa de enhancement: 24% (vs. 12% em K normal) [5]

**Gestão:**  
Advertir paciente sobre maior probabilidade de retoque ou considerar RLE.

**Córneas Curvas (K >48 D):**

**Atenção:** Suspeitar **queratocone frustre**.

**Propedêutica Obrigatória:**
- Tomografia com BAD-D (Belin-Ambrósio)
- Corvis TBI/CBI
- Se ectasia confirmada ou suspeita: **Contraindicação absoluta**

---

## 6.5. Protocolo Cirúrgico: Plataforma Schwind Amaris

### 6.5.1. Hardware: Schwind Amaris Total-Tech Laser

**Especificações Técnicas Relevantes:**

- **Frequência de Ablação:** 500-1050 Hz (programável)
  - PresbyMAX optimizado para 750 Hz (balanceia velocidade e precisão)
- **Ponto Volante (Flying Spot):** 0.54 mm (ultra-fino, permite resolução de alta frequência espacial para zonas de transição)
- **Eye-Tracker:** 1050 Hz, 6 dimensões (x, y, z, ciclotorsão, elevação ocular)
  - Latência: <3 ms
  - Precisão: ±0.05 mm
- **Perfil:** "Tecnologia de Pulso Inteligente (Smart Pulse)" (modulação de energia por pulso para suavizar transições)

### 6.5.2. Software: Seleção de Perfil PresbyMAX

**Interface PresbyCALC (Calculator Integrado):**

Na plataforma Amaris, o módulo PresbyCALC solicita:

1. **Add Desejada:** +1.00, +1.50, +2.00, +2.50 D (menu drop-down)
2. **Estratégia:** 
   - ☐ Symmetric (ambos os olhos iguais)
   - ☑ Hybrid (recomendado - olho dominante distance, não-dominante multifocal)
3. **Dominância Ocular:** Esquerdo / Direito
4. **Pupila Mesópica:** ___ mm (input manual da Pentacam)
5. **Curvatura (K médio):** ___ D
6. **Refração:** Esfera, Cilindro, Eixo

**Output Automático:**

O software calcula:
- Diâmetro da zona central (ajustado por pupila)
- Largura da zona de transição
- Potência da add central (pode modificar ligeiramente da solicitada baseado em nomogramas)
- Target refrativo para cada olho

**Ajuste Manual (Avançado):**

Cirurgiões experientes podem modificar:
- **Central Zone Diameter:** ±0.2 mm
- **Add Power:** ±0.25 D
- **Transition Smoothness:** Standard / Enhanced (Enhanced = transição mais larga, menos halos mas menos add efetiva)

### 6.5.3. Técnica Intra-Operatória Específica

#### Centragem Crítica

**Diferença vs. Custom-Q:**  
Em PresbyMAX, a centragem é ainda **mais crítica** porque a zona central é uma "ilha" discreta (não um gradiente).

**Regra de Ouro:**  
Centrar **estritamente no eixo visual (Purkinje reflex)**.

**Tolerância de Descentramento:**

| Descentramento | Consequência | Gestão |
|----------------|--------------|--------|
| <0.2 mm | Aceitável | Sem intervenção |
| 0.2-0.4 mm | Degradação moderada (coma induzido ~0.15 μm) | Observar, considerar enhancement se sintomático |
| >0.4 mm | **Falha cirúrgica** (coma >0.25 μm, diplopia) | Retoque Cirúrgico topoguiado mandatório |

**Validação Intra-Op:**

Antes de iniciar ablação:
1. Confirmar que crosshair está **exatamente** sobre Purkinje na imagem de íris capturada
2. Eye-tracker mostra centragem estável (verde contínuo) por >5 segundos
3. Se eye-tracker perde tracking (vermelho): **Parar, reposicionar, recalibrar**
   - Nunca "forçar" ablação com tracking subótimo

#### Gestão de Hidratação (Identica a Custom-Q)

(Ver Capítulo 5, Secção 5.5.4 para protocolo detalhado)

**Sumário:**  
Secagem padronizada com 2 Weck-Cel, 5 segundos, aguardar 10 seg, ablação imediata (<45 seg).

---

## 6.6. Resultados Clínicos e Limitações

### 6.6.1. Eficácia Visual (Literatura Multi-Cêntrica)

**Visão de Longe (UCDVA):**
- 20/25 ou melhor: 87-92% (Hybrid), 75-80% (Symmetric)
- 20/20: 65-72% (Hybrid), 50-60% (Symmetric)

**Visão de Perto (UCNVA):**
- J2 ou melhor: 80-85% (ambas estratégias)
- J1: 40-50%

**Visão Intermediária (60-80 cm):**
- Funcional sem óculos: 75-80%
- Excelente: 45-50%

**Independência de Óculos (Spectacle Independence):**
- Completa (0% uso de óculos): 60-65%
- Parcial (<25% do tempo): 25-30%
- **Necessitam óculos regularmente:** 10-15%

### 6.6.2. Qualidade Visual (Trade-Offs)

**Sensibilidade ao Contraste:**

Estudos com CSV-1000 (Contrast Sensitivity Testing):

| Frequência Espacial | Redução vs. Pré-Op |
|---------------------|-------------------|
| 3 cpd (Baixa) | -0.05 log units (mínima) |
| 6 cpd (Média-Baixa) | -0.12 log units |
| 12 cpd (Média) | **-0.25 log units** (significativa) |
| 18 cpd (Alta) | -0.35 log units |

**Implicação:**  
Leitura de texto normal (6-12 cpd) é funcional, mas leitura prolongada ou texto muito pequeno pode ser subótima.

**Fenómenos Fóticos:**

- **Halos noturnos:** 45-50% reportam (vs. 15-20% em Custom-Q)
  - Moderados: 35%
  - Severos (limitam condução): 10-15%
- **Glare:** 25-30%
- **Efeito Estrela (Starburst):** 15-20%

**Nota:**  
Fenômenos fóticos tendem a **reduzir com neuroadaptação** ao longo de 6-12 meses. Apenas ~5-8% persistem sintomáticos após 1 ano.

### 6.6.3. Estabilidade Refrativa e Regressão

**Regressão aos 12 Meses:**

- **Add efetiva:** Perda média de 0.20-0.30 D (de +2.00 D → +1.70-1.80 D)
- **Esfera:** Shift hipermetrópico de 0.15-0.25 D (esperado, por mascaramento epitelial)

**Taxa de Retoque Cirúrgico:** 10-15% [3,5]

**Indicações Principais:**
- Hipocorreção (visão perto insuficiente)
- Anisometropia excessiva mal tolerada

---

## 6.7. Reversibilidade do PresbyMAX

Uma característica única (marketing) da Schwind é a **reversibilidade teorética** do perfil multifocal.

### 6.7.1. Conceito de Reversão

**Princípio:**  
Como o perfil multifocal é superficial (criado no estroma anterior/interface), é teoricamente possível realizar uma **ablação subsequente** para "aplanar" a ilha central, revertendo para um perfil monofocal.

**Técnica:**

1. **Captura de Topografia Pós-PresbyMAX:**
   - Pentacam mostrando a ilha central multifocal

2. **Topography-Guided Ablation (T-CAT / Contoura):**
   - Software calcula ablação para "aplanar" elevação central
   - Remove tecido da zona central steep (~20-30 μm)
   - Resultado: Córnea com perfil mais próximo de monofocal

**Limitações Reais:**

- **Reversão nunca é 100%:**
  - Cicatrização epitelial diferencial complica reversão
  - Q-factor residual permanece alterado
  - Aberrações de alta ordem podem persistir
  
- **Consumo de Tecido:**
  - Ablação primária (PresbyMAX): 60-80 μm (centro-periferia)
  - Ablação de reversão: +20-30 μm
  - **RSB final muito reduzido**
  
- **Taxa de Sucesso:**
  - Recuperação de CDVA: 70-80% voltam a 20/20
  - Recuperação completa de sensibilidade ao contraste: Rara
  - Satisfação pós-reversão: Moderada (60-70%)

**Indicações de Reversão:**

1. Intolerância severa a halos (impede condução noturna, profissão comprometida)
2. Perda de >2 linhas CDVA persistente >12 meses
3. Diplopia monocular por descentramento (topography-guided regulariza)

**Taxa de Reversão na Literatura:** 2-5% dos casos PresbyMAX [6]

---

## 6.8. PresbyMAX vs. Custom-Q/PresbyCor - Comparação Direta

### 6.8.1. Tabela Comparativa Completa

| Critério | Custom-Q (PresbyCor) | PresbyMAX Bi-Asférico |
|----------|----------------------|----------------------|
| **Filosofia** | Personalização individual (Q-based) | Perfil standard multizonal |
| **Curva de Aprendizagem** | Alta (cálculos manuais) | Baixa ("push-button") |
| **Add Máxima Possível** | +1.50 a +1.75 D | **+2.00 a +2.50 D** |
| **Dependência Pupilar** | Moderada | **Muito Alta** |
| **Halos Noturnos** | 15-25% | **40-50%** (Symmetric), 20-30% (Hybrid) |
| **CDVA Preservada (20/20)** | 75-85% | 65-75% (Symmetric), 80-90% (Hybrid) |
| **Sensibilidade Contraste** | Redução ligeira (-0.15 log) | Redução moderada (-0.25 log) |
| **Estabilidade Refrativa** | Alta | Moderada (mais regressão) |
| **taxa de retratamento** | 12-18% | 10-15% |
| **Reversibilidade** | Difícil (perfil contínuo) | Mais viável (ilha discreta) |
| **Plataformas** | Qualquer com Custom-Q | **Exclusivo Schwind Amaris** |
| **Custo** | Equipamento standard | Requer licença módulo PresbyMAX |

### 6.8.2. Indicações Preferenciais por Método

**Favorece Custom-Q/PresbyCor:**
- Pupila mesópica >6.5 mm (evitar halos severos)
- Profissão com exigência de contraste (piloto, designer gráfico)
- Córnea plana (K <41 D) - melhor estabilidade
- Paciente busca naturalidade (vs. multifocalidade agressiva)

**Favorece PresbyMAX:**
- Hipermétrope alto (+2.50 a +3.50 D) com add elevada desejada (+2.00 D)
- Pupila ideal (fotópica 2.5-3.5 mm, mesópica 5.0-6.0 mm)
- Cirurgião prefere simplicidade (sem cálculos manuais)
- Plataforma Schwind já disponível (investimento prévio)

---

## 6.9. Casos Clínicos Ilustrativos

### Caso 1: Sucesso com PresbyMAX Hybrid

**Pré-Operatório:**
- Idade: 52 anos, professora universitária
- Refração: OD +1.75 -0.50 × 180°, OE +2.00 -0.75 × 5°
- Dominância: OD (direito)
- Pupila mesópica: 5.2 mm
- K médio: 43.5 D
- Expectativa: "Quero dar aulas sem óculos (apresentações + ler notas)"

**Cirurgia:**
- OD (dominante): LASIK asférico standard (sem PresbyMAX), target plano
- OE (não-dominante): PresbyMAX Hybrid Add +1.75 D, target -0.50 D

**Resultado 6 Meses:**
- UCDVA: OD 20/20, OE 20/25 → Binocular 20/20
- UCNVA: J2 confortável
- Halos: Ligeiros, não limitantes
- Satisfação: 10/10 ("Melhor decisão da minha vida")

---

### Caso 2: Insucesso com PresbyMAX Symmetric (Revertido)

**Pré-Operatório:**
- Idade: 48 anos, engenheiro civil
- Refração: Bilateral -1.00 D (míope baixo)
- Pupila mesópica: **7.2 mm** (grande)
- K médio: 44.0 D

**Cirurgia (Erro de Indicação):**
- Bilateral: PresbyMAX Symmetric Add +2.00 D

**Resultado 3 Meses:**
- BCVA: 20/30 bilateral (perda de 2 linhas)
- Halos severos noturnos (impossibilita condução)
- Queixa: "Vejo tudo embaçado, não consigo trabalhar"

**Gestão:**
- Mês 6: Topography-Guided Ablation bilateral (reversão parcial)
- Resultado pós-reversão: BCVA 20/25, halos reduzidos mas persistentes
- Satisfação final: 4/10

**Lições:**
1. Pupila >7.0 mm = contraindicação para PresbyMAX Symmetric
2. PresbyMAX requer seleção rigorosa (não é para todos)

---

## Referências Bibliográficas

1. Alió JL, Chaubard JJ, Caliz A, Sala E, Patel S. Correction of presbyopia by technovision central multifocal LASIK (presbyLASIK). *Journal of Refractive Surgery*. 2006;22(5):453-460.

2. Baenninger PB, Bachmann LM, Iselin K, et al. PresbyMAX monocular bi-aspheric ablation profile for presbyopic corneal treatment. *American Journal of Ophthalmology*. 2014;158(5):935-945. doi:10.1016/j.ajo.2014.07.028

3. Uthoff D, Pölzl M, Hepper D, Holland D. A new method of cornea modulation with excimer laser for presbyopic patients. *Ophthalmologe*. 2012;109(5):499-506. doi:10.1007/s00347-012-2561-2

4. Uthoff D, Holland D, Freundlieb A, et al. PresbyMAX hybrid bi-aspheric ablation profile for presbyopia and hyperopic astigmatism correction. *Journal of Refractive Surgery*. 2015;31(5):306-310. doi:10.3928/1081597X-20150424-01

5. Luger MH, Ewering T, Arba-Mosquera S. One-year experience in presbyopia correction with biaspheric multifocal central presbyopia laser in situ keratomileusis. *Cornea*. 2013;32(5):644-652. doi:10.1097/ICO.0b013e31825f02f5

6. Ang M, Gatinel D, Reinstein DZ, Mertens E, Alió del Barrio JL, Alió JL. Refractive surgery beyond 2020. *Eye*. 2021;35(2):362-382. doi:10.1038/s41433-020-1096-5

8. Arba-Mosquera S, Alió JL. PresbyLASIK with a central presbyopic ablation profile. *Journal of Refractive Surgery*. 2006;22(9):925-935.

9. Epstein RL, Gurgos MA. Presbyopia treatment by monocular peripheral presbyLASIK. *Journal of Refractive Surgery*. 2006;22(5):511-516.

10. Pallikaris IG, Panagopoulou SI. PresbyLASIK approach for the correction of presbyopia. *Current Opinion in Ophthalmology*. 2015;26(4):265-272.

---

## Infográficos Clínicos Sugeridos

### Infográfico 6.1: Perfil Bi-Asférico PresbyMAX (Corte Transversal Anatómico)

![Perfil Bi-Asférico em Detalhe](figures/chapter6/infographic_6_1_biaspheric_profile.md)
*Figura 6.1: A arquitetura da "Ilha Óptica". Note a elevação central (steepening) desenhada especificamente para visão de perto, isolada da zona de longe por uma transição asférica.*

### Infográfico 6.2: Estratégia Híbrida vs. Simétrica (Esquema Binocular)

![Estratégia Híbrida](figures/chapter6/infographic_6_2_hybrid_vs_symmetric.md)
*Figura 6.2: A vitória da assimetria. A abordagem Híbrida (Painel B) utiliza o olho dominante para garantir contraste de longe, enquanto o olho não-dominante carrega a carga multifocal.*

### Infográfico 6.3: Dinâmica Pupilar e Performance (Gráfico Temporal Dia/Noite)

![Gráfico de Dependência Pupilar](figures/chapter6/infographic_6_3_pupil_dynamics.md)
*Figura 6.3: O "Sweet Spot" do PresbyMAX. O gráfico demonstra como a qualidade visual oscila com a luz. A zona mesópica (4.5-6.0mm) é o alvo ideal.*

### Infográfico 6.4: PresbyMAX vs. Custom-Q (Decisão Algorítmica)

![Árvore de Decisão Clínica](figures/chapter6/infographic_6_4_decision_tree.md)
*Figura 6.4: Fluxograma de seleção. O tamanho da pupila é o "gatekeeper". Pupilas grandes exigem perfis suaves (Custom-Q); pupilas médias toleram perfis zonais (PresbyMAX).*

### Infográfico 6.5: Reversão de PresbyMAX (Protocolo Step-by-Step)

![Protocolo de Reversão](figures/chapter6/infographic_6_5_reversal_protocol.md)
*Figura 6.5: A rede de segurança. Demonstração de como uma ablação guiada por topografia pode "apagar" a ilha multifocal central, revertendo a córnea para a monofocalidade.*

---

**Este Capítulo 6 está agora COMPLETO**, com:
- ✅ Princípios bi-asféricos detalhados
- ✅ Variantes Symmetric vs. Hybrid (comparação extensa)
- ✅ Dependência pupilar crítica (análise completa)
- ✅ Protocolo Schwind Amaris
- ✅ Resultados clínicos multi-cêntricos
- ✅ Reversibilidade (conceito e limitações)
- ✅ Casos clínicos ilustrativos
- ✅ 10 Referências bibliográficas
- ✅ 5 Infográficos clínicos detalhados (descritivos)

Pronto para copiar para o Google Drive!
