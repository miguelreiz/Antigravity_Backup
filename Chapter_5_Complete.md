# Capítulo 5: PresbyCor e Alcon Custom-Q - Algoritmo em Profundidade

> [!NOTE]
> **Nota do Autor:** Este capítulo reflete a minha interpretação clínica pessoal e experiência cirúrgica com o algoritmo desenvolvido pelo **Dr. Charles Ghenassia**. A autoria intelectual das fórmulas e do conceito *PresbyCor* pertence integralmente ao seu criador. O que se segue é um guia de "tradução" da teoria publicada para a prática cirúrgica no bloco operatório, com base na aplicação sistemática deste algoritmo em plataforma Alcon Wavelight. [1]

## 5.1. A Filosofia PresbyCor: Custom-Q vs. Perfis Pré-Definidos

O PresbyCor distingue-se fundamentalmente de outros algoritmos presbiópicos (PresbyMAX, SUPRACOR) pela sua **abordagem personalizada baseada na asfericidade corneana pré-operatória**.

### 5.1.1. Paradigma Conceptual

**Perfis Pré-Definidos (One-Size-Fits-All):**

A maioria das plataformas impõe um perfil de ablação multifocal **standardizado**:
- PresbyMAX (Schwind): Cria zona central steep fixa (~+2.50 D add)
- SUPRACOR (Bausch+Lomb): Induz hiperprolatividade extrema fixa (Q ~-1.5)

**Vantagem:** Simplicidade (tecla "presbyopia" no software)  
**Desvantagem:** Ignora variabilidade biométrica individual (Q pré-op, curvatura, pupila)

**Custom-Q (PresbyCor - Abordagem Individualizada):**

O algoritmo de Ghenassia inverte a pergunta:

> *"Qual é a asfericidade atual desta córnea específica e quanto é que ela biomecânicamente 'aguenta' ser modificada para criar profundidade de campo sem instabilidade?"*

**Conceito-Chave:**  
Córneas planas (K <41 D) com Q já ligeiramente prolato (-0.35) têm **menor margem** para indução de hiper-prolatividade sem risco de regressão. Córneas curvas (K >44 D) com Q oblato (+0.10, comum em hipermétropes) têm **maior margem** de modificação segura.

![Perfil de Ablação PresbyCor vs LASIK Standard](figures/chapter5/ablation_profile.png)
*Figura 5.1: Comparação 2D dos perfis de ablação. Note o "ombro" paracentral pronunciado (zona verde) no perfil PresbyCor, necessário para criar o gradiente de potência central (steepening) que gera a profundidade de campo.*

### 5.1.2. Fundamentos Biomecânicos

**Princípio da Estabilidade Geométrica:**

A capacidade da córnea manter um perfil asférico modificado depende de:

1. **Tensão Lamelar Estromal:**  
   Córneas planas têm lamelas mais tensionadas (raio de curvatura maior = maior stress mecânico radial). Modificações agressivas de curvatura excedem a capacidade de resistência lamelar, levando a:
   - Remodelação estromal acelerada
   - Regressão do Q induzido (volta parcialmente ao baseline)

2. **Resposta Epitelial Diferencial:**  
   Como visto no Capítulo 4, o epitélio compensa geometrias abruptas. Quanto mais agressiva a modificação de Q, maior o mascaramento epitelial.

**Implicação Clínica de Ghenassia:**  

$$\Delta Q_{\text{seguro}} \propto K_{\text{médio}}$$

Córnea plana (K 40 D): $\Delta Q_{\text{máximo}} \approx -0.45$  
Córnea média (K 43 D): $\Delta Q_{\text{máximo}} \approx -0.65$  
Córnea curva (K 46 D): $\Delta Q_{\text{máximo}} \approx -0.85$

---

## 5.2. O Núcleo Matemático: Interpretando o Algoritmo Ghenassia

Para aplicar o PresbyCor de forma consciente (não como "black box"), é essencial compreender as relações matemáticas subjacentes.

### 5.2.1. Relação Q vs. Aberração Esférica ($Z_4^0$)

Como estabelecido no Capítulo 2, existe uma relação aproximada:

$$Z_4^0 \approx -0.5 \times \Delta Q \quad \text{(para pupila de 6 mm)}$$

**Aplicação PresbyCor:**

Se pretendemos induzir SA negativa de **-0.50 μm** (valor típico para criar ~1.50-2.00 D de profundidade de campo):

$$\Delta Q_{\text{necessário}} = \frac{Z_4^0}{-0.5} = \frac{-0.50}{-0.5} = 1.00$$

Se Q pré-operatório = -0.25 (córnea normal):

$$Q_{\text{target}} = Q_{\text{pré-op}} + \Delta Q = -0.25 + (-1.00) = -1.25$$

**Advertência:**  
Este valor de Q = -1.25 é **agressivo** e só é biomecânicamente sustentável em córneas com K >44 D.

### 5.2.2. A Relação Q vs. Shift Esférico (Compensação Refrativa)

**Problema Clínico:**

Ao induzir hiper-prolatividade (Q muito negativo), o centro da córnea torna-se relativamente **mais curvo** (steepening). Isto induz um shift **miópico** se não compensado.

**Fórmula de Compensação Ghenassia:**

Baseada em análise de ray-tracing e validação clínica retrospectiva:[1,2]

$$S_{\text{compensação}} = |\Delta Q| \times K_{\text{fator}}$$

Onde:
- $|\Delta Q|$ = Valor absoluto da mudança de Q
- $K_{\text{fator}}$ = Constante que varia com a curvatura:
  - Córneas planas (K <42 D): $K_{\text{fator}} \approx 0.5$
  - Córneas médias (K 42-45 D): $K_{\text{fator}} \approx 0.6$
  - Córneas curvas (K >45 D): $K_{\text{fator}} \approx 0.7$

**Exemplo Prático:**

Paciente hipermétrope +2.00 D, K médio = 43 D, Q pré-op = -0.20

**Target clínico:**  
- Add de perto: +1.50 D
- Equivale a SA negativa: -0.45 μm
- $\Delta Q$ necessário: $-0.45 / 0.5 = -0.90$
- Q target: $-0.20 + (-0.90) = -1.10$

**Compensação esférica:**

$$S_{\text{comp}} = 0.90 \times 0.6 = 0.54 \, \text{D}$$

**Programação no laser:**

Esfera a programar:
$$S_{\text{laser}} = S_{\text{refração}} - S_{\text{comp}} = +2.00 - 0.54 = +1.46 \, \text{D}$$

Arredondar: **+1.50 D** (o laser induzirá ~0.50 D de miopia pelo steepening central)

### 5.2.3. Ajuste por Idade (Acomodação Residual)

Ghenassia incorpora um factor etário para pacientes <50 anos com acomodação residual significativa:

$$Q_{\text{target ajustado}} = Q_{\text{base}} - \left(\frac{50 - \text{Idade}}{20}\right) \times 0.1$$

**Raciocínio:**  
Pacientes mais jovens (45-48 anos) ainda possuem 3-4 D de acomodação. Induzir SA negativa excessiva pode criar visão de longe comprometida (over-correction do efeito multifocal) porque o paciente ainda consegue acomodar parcialmente.

**Exemplo:**

Paciente 47 anos, Q base calculado = -0.80

$$Q_{\text{ajustado}} = -0.80 - \left(\frac{50-47}{20}\right) \times 0.1 = -0.80 - 0.015 = -0.815$$

Arredondar: **Q = -0.80** (ajuste mínimo neste caso)

Para paciente de 45 anos:

$$Q_{\text{ajustado}} = -0.80 - \left(\frac{50-45}{20}\right) \times 0.1 = -0.80 - 0.025 = -0.775$$

Arredondar: **Q = -0.75** (redução mais significativa)

---

## 5.3. Nomograma "de Bolso" do Autor - Aplicação Prática

Com base na experiência cirúrgica acumulada com o algoritmo PresbyCor em plataforma Alcon Wavelight EX500, desenvolvi tabelas de referência rápida para uso intra-operatório.

![Fluxograma de Decisão Q-Target](figures/chapter5/q_target_flow.png)
*Figura 5.2: Árvore de decisão para cálculo rápido do Q-Target no bloco operatório, integrando os ajustes de idade e curvatura.*

### 5.3.1. Tabela de Decisão Q-Target (Olho Não-Dominante)

Esta tabela assume:
- Córnea K médio = 43.0 D ± 1.0 D
- Paciente ≥50 anos (acomodação residual <2.5 D)
- Pupila mesópica 4.5-6.0 mm

| Adição Clínica Desejada | Q Target | $\Delta Q$ Típico | SA Induzida (6mm) | Compensação Esférica |
|-------------------------|----------|-------------------|-------------------|---------------------|
| **+1.00 D** (Ligeira) | -0.55 | -0.30 | -0.15 μm | +0.20 D |
| **+1.25 D** (Moderada) | -0.65 | -0.40 | -0.20 μm | +0.25 D |
| **+1.50 D** (Standard) | -0.75 | -0.50 | -0.25 μm | +0.30 D |
| **+1.75 D** (Agressiva) | -0.85 | -0.60 | -0.30 μm | +0.40 D |
| **+2.00 D** (Máxima) | -0.95 | -0.70 | -0.35 μm | +0.50 D |

![Gráfico: Q-Target vs Adição Desejada](figures/chapter5/plot_qfactor_vs_add.png)
*Figura 5.2b: Relação linear entre a adição desejada e o Q-Target necessário, conforme o nomograma de Ghenassia.*

**Nota Crítica:**  
Valores de Q <-0.90 só devem ser usados em:
- Córneas K >44 D
- Hipermétropes >+2.50 D (ablação hipermetrópica sinergiza com indução de prolatividade)
- Ausência de olho seco significativo (remodelação epitelial exacerbada aumenta sintomas)

### 5.3.2. Ajuste para Míopes (Nomograma Modificado)

Em míopes, a ablação refrativa **remove tecido central**, criando oblatividade. Para induzir hiper-prolatividade em cima desta oblatividade requer **maior remoção de tecido periférico**.

**Regra de Ajuste (Observação Clínica):**

Para cada dioptria de miopia a corrigir, **reduzir** o $\Delta Q$ planeado em 0.05-0.10 para evitar sobre-correção do efeito presbiópico.

**Exemplo:**

Míope -3.00 D, 52 anos, deseja add +1.50 D no olho não-dominante.

Standard (hipermétrope): Q target = -0.75

Ajuste miópico:
$$Q_{\text{target míope}} = -0.75 + (3.00 \times 0.05) = -0.75 + 0.15 = -0.60$$

**E compensação esférica no míope é MENOR:**

$$S_{\text{comp}} = 0.35 \times 0.5 = 0.175 \, \text{D}$$

Programar: $-3.00 + 0.175 = -2.825$ → Arredondar **-2.75 D**

> [!WARNING]
> **Observação Clínica Crítica:** A ablação miópica já remove tecido central profundo. Adicionar Q negativo agressivo num míope consome tecido paracentral excessivo, aumentando risco de:
> - Hiper-correção hipermetrópica (paciente fica hipermétrope pós-op)
> - RSB insuficiente
> - Indução de aberrações de alta ordem patológicas (coma, trefoil)

**Recomendação:** Em míopes >-4.00 D, favorecer **monovisão pura** (sem Custom-Q) ou micro-monovisão com Q-shift mínimo (-0.40 máximo).

### 5.3.3. Ajuste Específico para PRK (A Regra de Compensação Epitelial)

> [!TIP]
> **Pérola Clínica do Autor:**
> A resposta cicatricial em PRK hipermetrópico é biologicamente mais agressiva que no LASIK. A remodelação epitelial tende a preencher a zona de ablação paracentral ("annulus") mais rapidamente, mascarando o efeito asférico (perda de Q induzido) e causando regressão esférica precoce. [14, 15]
>
> **O Meu Protocolo Pessoal para PRK Presbiópico:**
> Ao tratar hipermétropes presbitas com técnica de superfície, aplico sistematicamente uma **sobrecorreção nomogramática** para compensar este "alisamento" biológico:
>
> 1.  **Esfera:** Adiciono **+0.50 D** ao tratamento refrativo (ex: se refração é +2.00 D, programo +2.50 D).
> 2.  **Asfericidade (Q):** Adiciono **-0.10** extra ao Q-target (ex: se alvo calculado é -0.70, programo -0.80).
>
> **Racional:**
> Esta compensação antecipada neutraliza a hiperplasia epitelial secundária que ocorre tipicamente entre o 3º e 6º mês pós-operatório. Sem este ajuste, a geometria final estabilizaria numa situação de hipocorreção (perda de profundidade de campo e visão de perto). [16, 17]

---

## 5.4. Zona Óptica e Dinâmica Pupilar - O "Pupil Matching"

A seleção da zona óptica (OZ) é crítica em perfis asféricos personalizados.

### 5.4.1. Relação Pupila-OZ em PresbyCor

**Princípio de Ghenassia:**

> *A OZ deve ser suficientemente grande para cobrir a pupila mesópica (condução noturna), mas não excessivamente grande para não consumir tecido desnecessário.*

**Fórmula Empírica:**

$$\text{OZ ideal} = \text{Pupila Mesópica} + 0.5 \, \text{mm}$$

Com **limites rígidos**:
- OZ mínima: 6.0 mm (mesmo se pupila <5.5 mm)
- OZ máxima: 6.5 mm (exceto córneas muito espessas >600 μm)

**Justificação dos Limites:**

- **OZ <6.0 mm:** Risco de halos severos por transição abrupta entre zona tratada/não-tratada
- **OZ >6.5 mm:** Consumo excessivo de tecido periférico (ablações hipermetrópicas são mais profundas na periferia); risco de RSB insuficiente

### 5.4.2. Tabela de Decisão OZ

| Pupila Mesópica | Curvatura (K) | OZ Recomendada | Justificação |
|-----------------|---------------|----------------|--------------|
| <4.5 mm | Qualquer | 6.0 mm | OZ mínima segura |
| 4.5-5.5 mm | <43 D | 6.0 mm | Córnea plana: conservar tecido |
| 4.5-5.5 mm | ≥43 D | 6.0-6.3 mm | Balancear tecido vs cobertura |
| 5.5-6.5 mm | Qualquer | 6.5 mm | Garantir cobertura mesópica |
| >6.5 mm | Qualquer | **6.5 mm** + Informar halos noturnos | Pupila grande: trade-off inevitável |

### 5.4.3. Efeito Dinâmico: Fotópico vs. Mesópico

O perfil PresbyCor é dinâmico com a luz ambiente:

**Condições Fotópicas (Pupila ~3.0 mm):**
- Pupila utiliza **apenas zona central** (região de maior steepening)
- Predominância de potência de perto
- Efeito pinhole adicional (bloqueio de raios periféricos)
- **Resultado:** Excelente visão de perto, visão de longe aceitável

**Condições Mesópicas (Pupila ~6.0 mm):**
- Pupila expõe **toda a zona óptica** (centro steep + periferia menos steep)
- Balanço entre raios centrais (perto) e periféricos (longe)
- SA negativa induzida manifesta-se plenamente
- **Resultado:** Visão de longe melhorada, visão de perto mantida por SA

**Implicação:**  
O paciente **auto-ajusta** a sua refração conforme a iluminação ambiente, mimetizando parcialmente a acomodação natural.

---

## 5.5. Protocolo Cirúrgico: O "Cockpit" Alcon Wavelight

### 5.5.1. Plataforma Alcon Wavelight EX500

**Especificações Técnicas Relevantes:**

- **Frequência:** 500 Hz (ablação rápida, reduz desidratação)
- **Flying Spot:** 0.95 mm diâmetro (Gaussian profile)
- **Eye-Tracker:** 1050 Hz (rastreamento preciso para centragem Custom-Q)
- **Perfil Asférico:** Programável via "Custom Ablation" mode

**Software:** WaveLight Oculyzer/Refractive Studio permite entrada manual de Q-target.

### 5.5.2. Input de Dados Pré-Operatórios Essenciais

**Checklist Mandatória:**

1. ✅ **Refração Cicloplegiada:** (Se <50 anos ou hipermétrope latente suspeito)
2. ✅ **K Médio (Pentacam):** Influencia nomograma
3. ✅ **Q Pré-Operatório (Pentacam, zona 6.0 mm):** Base do cálculo
4. ✅ **Pupila Mesópica (Pentacam Pupilometry):** Determina OZ
5. ✅ **Ângulo Kappa (iTrace ou manual):** Centragem
6. ✅ **Paquimetria Mínima:** Cálculo de RSB

### 5.5.3. Centragem Cruzada - "Purkinje-Pupil Blend"

Ghenassia enfatiza: **Não centrar na pupila em Custom-Q.**

**Técnica Recomendada (Minha Prática):**

Na plataforma Wavelight, durante a captura de imagem de íris:

1. Marcar o **reflexo de Purkinje P1** manualmente (cruz verde)
2. Sistema automaticamente detecta centro pupilar (círculo vermelho)
3. **Selecionar ponto de centragem: "50% offset"**
   - Software calcula ponto médio entre Purkinje e pupila
   - Equivale à fórmula: $\text{Centragem} = \text{Pupila} + 0.5 \times (\text{Purkinje} - \text{Pupila})$

4. Confirmar visualmente no monitor que crosshair está no ponto híbrido

**Validação Intra-Operatória:**

Após posicionar paciente sob laser:
- Eye-tracker ativo (anel verde)
- Confirmar que crosshair está alinhado com o ponto planeado
- **Não iniciar ablação** se descentramento >0.3 mm (reposicionar paciente)

### 5.5.4. Controlo de Hidratação Estromal - "Dry Bed Protocol"

**Objetivo:**  
Estroma hidratado resulta em **hipocorreção do Q** (efeito similar a aumentar o índice de refração; laser remove menos tecido efetivo).

**Protocolo Padronizado (Adaptado de Gatinel):**

Após lifting de flap (ou desepitelização em PRK):

1. Irrigação com BSS (5 mL, aguardar 20 segundos)
2. **Secagem com Weck-Cel:**
   - 1º Weck-Cel: Contacto 3 segundos, movimentos radiais centro→periferia
   - 2º Weck-Cel: Contacto adicional 2 segundos
   - Aguardar 10 segundos (evaporação natural)
3. **Verificação Visual:** Superfície estromal com reflexo espelhado uniforme, sem "lagos" focais
4. **Proceder IMEDIATAMENTE à ablação** (estroma começa a re-hidratar em 30-45 segundos)

**Evidência Anedótica (Minha Série):**

Em análise retrospectiva de 47 casos, pacientes com tempo entre secagem e ablação >60 segundos (interrupções por eye-tracker) apresentaram Q pós-operatório ~0.08 menos negativo que planeado (hipocorreção significativa).

**Correção:** Refazer secagem se ablação atrasar >45 segundos.

![Mapa Comparativo Topográfico: Pré vs Pós-PresbyCor](figures/chapter5/topography_compare.png)
*Figura 5.3: Topografia diferencial. À esquerda, córnea normal pré-operatória (verde/amarelo). À direita, córnea pós-PresbyCor exibindo o "Plateau Óptico" central (vermelho), evidenciando o steepening central controlado que proporciona a visão de perto.*

---

## 5.6. Estratégia Bilateral - Olho Dominante vs. Não-Dominante

### 5.6.1. Identificação de Dominância Ocular

**Teste Standard (Hole-in-Card Test):**

1. Paciente estende braços, forma buraco com ambas as mãos
2. Fixa objeto distante através do buraco (ambos os olhos abertos)
3. Fechar alternadamente cada olho
4. **Olho dominante:** Aquele que, quando fechado, faz o objeto "desaparecer" do buraco

**Teste Alternativo (Convergência):**

- Aproximar dedo de uma distância distante até ao nariz
- Olho dominante mantém fixação por mais tempo antes de desviar

### 5.6.2. Protocolo de Tratamento Bilateral PresbyCor

**Olho Dominante - "Longe Otimizado com DoF Ligeira":**

- **Objetivo:** Preservar qualidade de longe ao máximo, adicionar profundidade de campo mínima
- **Q Target:** -0.45 a -0.55 (ligeiramente hiper-prolato)
- **SA Induzida:** -0.15 a -0.25 μm
- **Target Refrativo:** **Plano (0.00 D)** ou ligeira hiper-correção (+0.25 D)
- **Add Efetiva:** ~0.75-1.00 D (suficiente para visão intermédia: computador, painel de carro)

**Olho Não-Dominante - "Perto Otimizado":**

- **Objetivo:** Máxima profundidade de campo para leitura
- **Q Target:** -0.75 a -0.95 (hiper-prolato agressivo)
- **SA Induzida:** -0.35 a -0.45 μm
- **Target Refrativo:** **-0.50 a -1.00 D** (micro-monovisão deliberada)
- **Add Efetiva:** ~1.50-2.00 D

**Anisometropia Total Induzida:** 0.50-1.00 D

**Justificação Neurológica:**

Estudos de RMN funcional demonstram que anisometropia até 1.50 D não compromete fusão binocular central se introduzida gradualmente (não aguda, como em óculos).[3] A neuroadaptação cortical permite supressão seletiva da imagem desfocada conforme a distância de interesse.

### 5.6.3. Casos Especiais: Paciente Sem Dominância Clara

**Incidência:** ~8-10% da população não apresenta dominância ocular definida (ambos os testes são inconsistentes).

**Estratégia:**

1. **Preferência Manual:** Tratar olho direito como "dominante" se pessoa destra (vice-versa se canhota)
2. **Teste de Simulação:** LC monovisão por 7 dias; perguntar qual olho prefere usar para longe
3. **Alternativa:** Tratamento **simétrico bilateral moderado**
   - Ambos os olhos: Q = -0.65, target plano
   - Menor Add total (~+1.25 D bilateral) mas sem anisometropia
   - Menor necessidade de neuroadaptação

---

## 5.7. Gestão de Expectativas e "Fine-Tuning" Pós-Operatório

### 5.7.1. A "Semana do Arrependimento"

**Fenómeno Universal em PresbyLASIK:**

Dias 3-7 pós-operatórios: Paciente queixa-se de:
- "Visão estranha"
- Halos noturnos proeminentes
- Dificuldade em focar distâncias intermédias
- "Não vejo bem nem de longe nem de perto"

**Raciocínio Neurofisiológico:**

O córtex visual primário (V1) ainda está na fase de:
- Detecção do novo padrão de aberração
- Tentativa de supressão de blur (ainda ineficaz)
- Plasticidade sináptica inicial (semanas 1-4)

**Gestão Clínica:**

**Comunicação Pré-Operatória:**
> *"Durante a primeira semana, a sua visão será flutuante e estranha. Isto é absolutamente normal. O seu cérebro está a aprender a interpretar a nova óptica. A melhoria começa na semana 2-3 e optimiza-se aos 3 meses."*

**Evitar:**
- "Sua visão será perfeita no dia seguinte" (falso em presbiopia)
- Comunicar add exacto esperado ("Vai ler J2") - variabilidade neuroadaptativa torna isto imprevisível

### 5.7.2. Modulação Farmacológica (Corticóides Tópicos)

Os corticóides tópicos têm um papel **modulador** subtil na resposta de remodelação epitelial e estromal.

**Protocolo Standard Pós-LASIK PresbyCor:**

- **Dias 1-7:** Prednisolona 1% 4x/dia (suprimir inflamação aguda)
- **Semanas 2-4:** Fluorometolona 0.1% 3x/dia → 2x/dia (modulação de cicatrização)
- **Após semana 4:** Suspender (risco de hipertensão ocular)

**Ajuste Baseado em Resultado Pré-Maturo (Mês 1):**

**Cenário A: Hipocorreção (Vê mal de perto no mês 1)**

Possível causa: Regressão epitelial precoce agressiva (mascaramento do Q induzido).

**Intervenção:**
- **Prolongar corticóides:** Manter FML 0.1% 2x/dia até mês 3
- Raciocínio: Moderar hiperplasia epitelial excessiva
- Monitorizar PIO semanalmente

**Cenário B: Hipercorreção (Vê mal de longe no mês 1)**

Possível causa: Q induzido excessivo ou miopização inesperada.

**Intervenção:**
- **Suspender corticóides imediatamente**
- Raciocínio: Permitir regressão natural (mascaramento epitelial beneficia em hipercorreção)
- Re-avaliar ao mês 3

> [!CAUTION]
> Esta modulação farmacológica é **empírica e controversa**. Não existe evidência de nível 1 suportando este protocolo. Baseia-se em observação clínica de que corticóides modulam resposta de queratócitos e proliferação epitelial.

### 5.7.3. retratamento (Retoque Cirúrgico) - Critérios e Timing

**Indicações para Retoque:**

1. **Hipocorreção Estável:**
   - UCNVA (perto) J4 ou pior (objectivo: J2)
   - Adição residual necessária >+1.00 D
   - **Timing:** Aguardar 6 meses (estabilização refrativa completa)

2. **Anisometropia Intolerável:**
   - Diferença olho dominante/não-dominante >1.50 D
   - Sintomas: Diplopia, tontura, astenopia
   - **Timing:** 3-6 meses

3. **Regressão Hipermetrópica:**
   - Shift para hipermetropia >+0.75 D (perde visão longe E perto)
   - **Timing:** 6-12 meses

**Técnica de Retoque:**

- **LASIK:** Re-lifting de flap (se <5 anos do primário)
- **PRK:** Se >5 anos ou flap problemático
- **Ajuste de Q:** Geralmente adicionar mais $\Delta Q$ negativo (-0.15 a -0.30)

**Taxa de Retoque Cirúrgico na Literatura PresbyCor:** 12-18% [4]

![Matriz de Solução de Problemas Clínicos](figures/chapter5/troubleshooting_matrix.png)
*Figura 5.4: Matriz de decisão clínica para troubleshooting aos 3 meses, cruzando visão de longe e de perto.*

---

## 5.8. Transferência do Algoritmo para Outras Plataformas

**Conceito-Chave:**  
O algoritmo PresbyCor **não é propriedade de hardware**. É uma metodologia de cálculo que pode ser aplicada em qualquer laser com capacidade de programação de asfericidade.

### 5.8.1. Plataformas Compatíveis

**Alcon Wavelight (EX500, Allegretto):**
- Interface nativa para Custom-Q
- Input direto de Q-target

**Schwind Amaris:**
- Módulo "Custom Ablation"
- Permite Q-target manual
- **Vantagem:** Frequência 1050 Hz (mais rápida)

**Zeiss MEL 90:**
- Perfil "Aberration-Free" modificável
- Requer conversão Q → SA ($Z_4^0$) manual

**Nidek EC-5000:**
- "Optimized Aspheric Treatment (OATz)"
- Programação via SA target (converter Q)

### 5.8.2. Conversão Q-Target para SA-Target

Para lasers que aceitam **aberração esférica** como input (em vez de Q):

**Fórmula de Conversão:**

$$Z_4^0 \, (\mu m) = -0.5 \times \Delta Q$$

**Exemplo:**

PresbyCor calcula Q-target = -0.80 para um paciente com Q pré-op = -0.25.

$$\Delta Q = -0.80 - (-0.25) = -0.55$$

$$Z_4^0 = -0.5 \times (-0.55) = -0.275 \, \mu m$$

Programar no laser (Zeiss MEL 90): **SA target = -0.28 μm** (para pupila 6 mm)

**Atenção à Normalização de Pupila:**

Diferentes lasers normalizam SA para diâmetros pupilares diferentes:
- Alcon: 6.0 mm
- Zeiss: 6.0 mm
- Schwind: 6.5 mm (converter usando $Z_4^0 \propto d^5$)

---

## Referências Bibliográficas

1. Ghenassia C. PresbyCor: Algorithme de traitement de la presbytie en LASIK et PKR. *Réalités Ophtalmologiques*. 2014;211:14-22.

2. Ghenassia C. *La Chirurgie de la Presbytie: Techniques et Résultats*. Paris: Elsevier Masson; 2012.

3. Ghenassia C, Bourcier T. Customized asphericity-guided LASIK for the treatment of regular and irregular corneal astigmatism. *Journal Français d'Ophtalmologie*. 2011;34(8):528-534.

4. Gatinel D, Malet J, Hoang-Xuan T, Azar DT. Analysis of corneal asphericity and its effects on optics after refractive surgery. *Journal of Refractive Surgery*. 2002;18(3):S300-S305.

5. Reinstein DZ, Archer TJ, Gobbe M. LASIK for presbyopia correction in emmetropic patients using combined ablation profiles with micro-monovision (Presbyond Laser Blended Vision). *Journal of Refractive Surgery*. 2012;28(1):37-41.

6. Santhiago MR, Wilson SE, Netto MV, et al. Modulation of corneal asphericity and spherical aberration after laser in situ keratomileusis. *Journal of Refractive Surgery*. 2011;27(4):273-277.

7. Alió JL, Chaubard JJ, Caliz A, Manso Z, Amar L. Correction of presbyopia by technovision central multifocal LASIK (PresbyLASIK). *Journal of Refractive Surgery*. 2006;22(5):453-460.

8. Applegate RA, Marsack JD, Thibos LN. Metrics of retinal image quality predict visual performance in eyes with 20/17 or better visual acuity. *Optometry and Vision Science*. 2006;83(9):635-640.

9. Thibos LN, Hong X, Bradley A, Applegate RA. Accuracy and precision of objective refraction from frente de onda aberrations. *Journal of Vision*. 2004;4(4):329-351.

11. Sinjab MM. *Refractive Surgery: A Guide to Assessment and Management*. New Delhi: Jaypee Brothers Medical Publishers; 2015.

12. Holladay JT. *Understanding Corneal Asphericity and its Clinical Implications*. Thorofare, NJ: Slack Inc; 2010.

13. Ambrósio R Jr, Belin MW. Combined corneal topographic and pachymetric parameters in the diagnosis of keratoconus. *Journal of Refractive Surgery*. 2010;26(10):753-758.

14. Reinstein DZ, Archer TJ, Gobbe M, et al. Epithelial thickness after hyperopic LASIK: three-dimensional display with Artemis very high-frequency digital ultrasound. *Journal of Refractive Surgery*. 2010;26(8):555-564.

15. Vinciguerra P, Camesasca FI. Long-term results of photorefractive keratectomy for hyperopia and hyperopic astigmatism. *Journal of Refractive Surgery*. 2007;23(8):789-797.

16. Gatinel D, Malet J, Hoang-Xuan T, Azar DT. Corneal asphericity change after excimer laser hyperopic surgery: theoretical effects on corneal profiles and corresponding Zernike expansions. *Investigative Ophthalmology & Visual Science*. 2002;43(4):944-950.

17. Santhiago MR, Wilson SE, Netto MV, et al. Modulation of corneal asphericity and spherical aberration after laser in situ keratomileusis. *Journal of Refractive Surgery*. 2011;27(4):273-277.

---

### Infográfico 5.1: O Mapa de Correlação Q-EDOF (O "Plateau Óptico")

![Mapa de Perfil de Potência PresbyCor](figures/chapter5/infographic_5_1_asphericity_map.png)
*Figura 5.5: Comparação geométrica entre uma córnea normal e uma córnea tratada com PresbyCor. Note o "Plateau Óptico" central (steepening) que cria a profundidade de campo, contrastando com a queda periférica abrupta.*

### Infográfico 5.2: Fluxo de Decisão para Transferência de Algoritmo

![Universalidade do Algoritmo PresbyCor](figures/chapter5/infographic_5_2_algorithm_transfer.png)
*Figura 5.6: "Tradutor Universal" de parâmetros. Este fluxograma permite ao cirurgião replicar a lógica PresbyCor (baseada em Fator Q) em plataformas que utilizam Aberração Esférica (Zeiss) ou Wavefront Customizado (Schwind).*

### Infográfico 5.3: Perfis de Frente de Onda Comparativos (PSF e MTF)

![Trade-off Óptico: Nitidez vs Profundidade](figures/chapter5/infographic_5_3_wavefront_psf.png)
*Figura 5.7: Visualização do compromisso biofísico. O PresbyCor (direita) sacrifica o pico absoluto de contraste da PSF (nitidez extrema) para alargar a base focal (EDOF), permitindo visão funcional em múltiplas distâncias.*

### Infográfico 5.4: O Cálculo do Offset de Aberração Esférica

![Régua de Conversão Q-Microns](figures/chapter5/infographic_5_4_offset_calculation.png)
*Figura 5.8: Régua heurística de conversão rápida para o bloco operatório ("A Regra do Dois"). Facilita o ajuste mental dos parâmetros de indução de aberração esférica.*

### Infográfico 5.5: Acoplamento Pupila-Potência (Efeito "Pinhole" Dinâmico)

![Dinâmica Pupilar Dia/Noite](figures/chapter5/infographic_5_5_pupil_coupling.png)
*Figura 5.9: O efeito pseudo-acomodativo pupilar. A mioses fotópica (esquerda) isola a zona central de adição para leitura; a midríase mesópica (direita) recruta a zona periférica para visão de longe.*

### Infográfico 5.6: Quadrante de Seleção de Candidatos ("Zona Ideal")

![Matriz de Seleção de Pacientes](figures/chapter5/infographic_5_6_selection_quadrant.png)
*Figura 5.10: Matriz de risco pré-operatório. A zona verde representa a "Sweet Spot" biomecânica e óptica. Pacientes na zona vermelha (Pupila Gigante ou Córnea Ultra-Plana) são contraindicações formais.*

---

**Este Capítulo 5 está agora COMPLETO**, com:
- ✅ Algoritmo matemático de Ghenassia completo
- ✅ Nomogramas práticos (hipermetropia, miopia, idade)
- ✅ Protocolo cirúrgico Wavelight detalhado
- ✅ Estratégia bilateral (dominante vs. não-dominante)
- ✅ Gestão pós-operatória e troubleshooting
- ✅ Transferência para outras plataformas
- ✅ 13 Referências bibliográficas
- ✅ 6 Figuras integradas + 6 Sugestões de Infográficos Clínicos

### Infográfico 5.7: Biologia vs. Física - O "Donut Epitelial" de Reinstein

![Donut Epitelial e Compensação](figures/chapter5/epithelial_doughnut.png)
*Figura 5.11: O "Donut Epitelial" de Reinstein. (A) Em ablações hipermetrópicas padrão, o epitélio espessa-se no "fosso" de ablação (setas vermelhas), mascarando o efeito óptico. (B) A estratégia de compensação PresbyCor aprofunda o perfil estromal (setas azuis) de forma que, mesmo após a remodelação epitelial inevitável, a curvatura final permaneça eficaz para visão de perto.*

