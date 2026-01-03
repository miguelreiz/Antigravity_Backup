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

10. Artal P, Chen L, Fernández EJ, Singer B, Manzanera S, Williams DR. Neural compensation for the eye's optical aberrations. *Journal of Vision*. 2004;4(4):281-287.

---

## Infográficos Clínicos Sugeridos

### Infográfico 5.1: A Curva de Ablação PresbyCor (Perfil de Profundidade)

**Descrição:**  
Gráfico 2D mostrando o perfil de ablação radial em profundidade comparado a LASIK standard.

**Eixos:**
- **Eixo X:** Distância Radial do Centro (0 a 4 mm)
- **Eixo Y:** Profundidade de Ablação (μm), invertido (0 no topo, -100 na base)

**Duas Curvas Sobrepostas:**

**Curva A (Azul - LASIK Hipermetrópico Standard, Q preservado ~-0.26):**
- Centro: Ablação mínima (~10 μm)
- Perfil: Aumento gradual suave até periferia
- Profundidade máxima a 3.5 mm: ~60 μm
- Label: "Perfil Standard - Asfericidade Preservada"

**Curva B (Vermelho - PresbyCor Custom-Q, Q target -0.85):**
- Centro: Ablação também mínima (~10-15 μm)
- **Diferença Key:** "Ombro" paracentral pronunciado (2.0-3.5 mm)
  - Profundidade a 2.5 mm: ~45 μm
  - Profundidade máxima a 3.5 mm: ~85 μm (**+40% mais profunda**)
- Label: "PresbyCor - Hiper-Prolato (Q = -0.85)"

**Zona Sombreada Verde:** Entre as duas curvas
- Label: "Tecido Extra Removido para Induzir Hiper-Prolatividade"
- Valor numérico: "~25-30 μm adicional na zona 2-3.5 mm"

**Diagrama Inset (Superior Direito):**  
Corte transversal córnea mostrando:
- Estroma pós-ablação Standard: Elevação central moderada
- Estroma pós-ablação PresbyCor: **"Montanha" central** mais pronunciada
- Setas indicando steepening central

**Objetivo:**  
Demonstrar visualmente porque PresbyCor consome mais tecido periférico e cria geometry mais agressiva (justificando cuidado com RSB).

---

### Infográfico 5.2: Fluxograma de Decisão Q-Target (Algoritmo Passo-a-Passo)

**Descrição:**  
Árvore de decisão interativa para cálculo intra-operatório de Q-target.

**Input (Topo do Fluxograma):**

Caixas de dados do paciente:
- Idade: ___ anos
- K Médio: ___ D
- Q Pré-Op: ___
- Pupila Mesópica: ___ mm
- Refração: ___ D
- Olho: ☐ Dominante  ☑ Não-Dominante

**Decisão 1: Selecionar Add Desejada**

Caixas de opção:
- ☐ Ligeira (+1.00 D) - Intermédio
- ☑ Moderada (+1.50 D) - Standard
- ☐ Agressiva (+2.00 D) - Máxima

**Decisão 2: Ajuste por Curvatura**

```
SE K Médio <42 D:
    K_fator = 0.5
    Q_max_seguro = -0.70
SE K Médio 42-45 D:
    K_fator = 0.6
    Q_max_seguro = -0.85
SE K Médio >45 D:
    K_fator = 0.7
    Q_max_seguro = -1.00
```

**Decisão 3: Cálculo Base**

Para Add Moderada (+1.50 D):
```
SA_target = -0.25 μm
ΔQ_necessário = -0.25 / 0.5 = -0.50
Q_base = Q_pré + ΔQ = -0.25 + (-0.50) = -0.75
```

**Decisão 4: Ajuste Etário (Se <50 anos)**

```
SE Idade = 47:
    Redução = (50-47)/20 × 0.1 = 0.015
    Q_ajustado = -0.75 + 0.015 = -0.735
```

**Decisão 5: Ajuste por Tipo Refrativo**

```
SE Hipermetropia: Q_final = Q_ajustado (sem alteração)
SE Miopia >-2.00 D:
    Ajuste_miópe = Miopia × 0.05
    Q_final = Q_ajustado + Ajuste_miópe
```

**Output Final (Base do Fluxograma):**

Caixa verde grande:
```
═══════════════════════════════════
  ✓ Q-TARGET CALCULADO
─────────────────────────────────── 
  Q a programar: -0.75
  OZ recomendada: 6.0 mm
  Compensação esférica: +0.30 D
  
  VALIDAÇÃO:
  ☑ Q < Q_max_seguro? SIM
  ☑ RSB >300 μm? SIM
  
  → PROSSEGUIR CIRURGIA
═══════════════════════════════════
```

**Objetivo:**  
Servir como checklist interativo visual para cálculo rápido e sem erros no bloco operatório.

---

### Infográfico 5.3: Mapa Comparativo - Córnea Pré vs. Pós PresbyCor

**Descrição:**  
Dois mapas axiais (topografia) lado a lado com escala de cores.

**Painel Esquerdo: Pré-Operatório**

Mapa axial topográfico (Pentacam):
- Centro (2 mm): Cor amarela-laranja (43.5 D)
- Paracentro (2-4 mm): Laranja (43.0 D)
- Mid-periferia (4-6 mm): Verde-azul (42.0 D)
- Periferia (>6 mm): Azul (40.5 D)
- **Q exibido:** -0.24 (ligeiramente prolato, normal)
- Label: "Córnea Normal Pré-Op (Q = -0.24)"

**Painel Direito: 3 Meses Pós-PresbyCor**

Mapa axial topográfico:
- **Centro (0-1.5 mm): Vermelho intenso (46.0 D)** ← Steepening central
- Paracentro (1.5-3 mm): Laranja-amarelo (44.5 D) ← Transição
- Mid-periferia (3-5 mm): Verde (42.5 D) ← Relativamente flat
- Periferia (>5 mm): Azul (40.0 D) ← Muito flat
- **Q exibido:** -0.82 (hiper-prolato)
- Label: "Pós-PresbyCor (Q = -0.82, Add +1.50 D)"

**Elementos Visuais Adicionais:**

**Seta Anotada:** Do centro pré-op ao pós-op
- "ΔK central = +2.5 D"

**Linha de Perfil:** Corte horizontal mostrando potência dióptrica vs. distância
- Gráfico linear sobreposto mostrando declínio acentuado pré→pós

**Caixa de Texto:**  
"**Optical Plateau Central:** A zona central cria pseudo-adição para perto enquanto periferia mantém longe. Este gradiente controlado = EDOF."

**Objetivo:**  
Permitir visualização direta do efeito topográfico do PresbyCor (útil para explicar ao paciente e para ensino).

---

### Infográfico 5.4: Troubleshooting Matrix (Mês 3 Pós-Op)

**Descrição:**  
Matriz 2×2 baseada em queixas do paciente com condutas.

**Eixo Vertical:** Visão de Longe (UCDVA)
- Topo: Boa (20/25 ou melhor)
- Base: Má (20/40 ou pior)

**Eixo Horizontal:** Visão de Perto (UCNVA)
- Esquerda: Má (J4 ou pior)
- Direita: Boa (J2 ou melhor)

**4 Quadrantes:**

---

**Quadrante Superior Esquerdo (VERDE - Sucesso Parcial):**
- **Visão Longe:** Boa ✓
- **Visão Perto:** Má ✗

**Diagnóstico Provável:**
- Hipocorreção do efeito presbiópico
- Q real pós-op <Q planeado (mascaramento epitelial excessivo)

**Aberrometria Esperada:**
- SA negativa <-0.20 μm (deveria ser -0.30 a -0.40 μm)

**Conduta:**
1. **Confirmar estabilização:** Aguardar até mês 6
2. **Retoque Cirúrgico:**
   - Re-lift flap (ou PRK)
   - Adicionar Q: -0.15 a -0.25
   - Target miópico adicional: -0.25 a -0.50 D (olho não-dominante)

**Taxa de Sucesso Retoque Cirúrgico:** 85-90%

---

**Quadrante Superior Direito (VERDE INTENSO - Sucesso Total):**
- **Visão Longe:** Boa ✓
- **Visão Perto:** Boa ✓

**Achado:**
- Q pós-op conforme planeado
- Neuroadaptação completa

**Conduta:**
- **ALTA** (follow-up anual standard)
- Reforçar: Óculos ocasionais (condução noturna prolongada, leitura prolongada <30 cm) são normais

---

**Quadrante Inferior Esquerdo (VERMELHO - Falha Total):**
- **Visão Longe:** Má ✗
- **Visão Perto:** Má ✗

**Diagnóstico Provável:**
- Complicação: Descentramento, epithelial ingrowth, striae
- Regressão hipermetrópica inesperada
- Aberrações de alta ordem patológicas (coma, trefoil)

**Propedêutica Urgente:**
1. Topografia (identificar descentramento)
2. Aberrometria (quantificar coma)
3. OCT anterior (procurar ingrowth, striae)

**Conduta:**
- **Se Coma >0.40 μm:** Topography-Guided Retoque Cirúrgico
- **Se Ingrowth Grau 3:** Re-lift + debridamento
- **Se Striae:** Lifting + stretching + sutura temporária

---

**Quadrante Inferior Direito (AMARELO - Hipercorreção):**
- **Visão Longe:** Má ✗
- **Visão Perto:** Boa ✓

**Diagnóstico Provável:**
- Miopização excessiva (olho não-dominante)
- Q induzido excessivo (>-1.00)
- Anisometropia >1.50 D

**Sintomas Associados:**
- Tontura
- Diplopia transitória
- "Visão estranha binocular"

**Conduta:**
1. **Teste de Oclusão:** Ocluir olho não-dominante melhora sintomas? → Confirma anisometropia excessiva
2. **Refração:** Quantificar miopia residual
3. **Opções:**
   - **Conservadora (Preferível):** Lente contacto temporária positiva no olho miopizado (simular correção); se tolera, enhancement
   - **Retoque Cirúrgico:** PRK/LASIK hipermetrópico ligeiro (+0.50 a +1.00 D) para reduzir anisometropia

---

**Objetivo:**  
Fornecer algoritmo visual rápido para gestão de resultados sub-ótimos aos 3 meses.

---

### Infográfico 5.5: Estratégia Bilateral (Visão Esquemática Olhos)

**Descrição:**  
Diagrama esquemático de ambos os olhos com raios de luz mostrando focos diferentes.

**Painel Esquerdo: Olho Dominante (Direito)**

**Córnea:**
- Perfil ligeiramente prolato (Q = -0.50)
- Cor: Azul claro (steepening mínimo)

**Raios de Luz:**
- Raios paralelos (longe): Focalizam **na retina** (foco perfeito)
- Raios divergentes (perto, 40 cm): Focalizam **ligeiramente atrás da retina** (blur ligeiro)

**Retina:**
- Imagem nítida de carro distante
- Imagem ligeiramente turva de livro

**SA Induzida:** -0.15 μm

**Label:** "Olho Dominante - LONGE Otimizado"  
**Target:** Plano (0.00 D)  
**Add Efetiva:** ~0.75 D

---

**Painel Direito: Olho Não-Dominante (Esquerdo)**

**Córnea:**
- Perfil hiper-prolato agressivo (Q = -0.85)
- Cor: Vermelho-laranja (steepening central pronunciado)

**Raios de Luz:**
- Raios paralelos (longe): Focalizam **ligeiramente antes da retina** (miopia ligeira)
- Raios divergentes (perto, 33 cm): Focalizam **na retina ou próximo** (foco bom)

**Retina:**
- Imagem ligeiramente turva de carro (tolerável)
- Imagem nítida de livro (texto claro)

**SA Induzida:** -0.40 μm

**Label:** "Olho Não-Dominante - PERTO Otimizado"  
**Target:** -0.75 D (micro-monovisão)  
**Add Efetiva:** ~1.75 D

---

**Painel Central: Fusão Binocular (Cérebro)**

**Ícone Cerebral (V1):**
- Inputs de ambos os olhos convergindo

**Para Longe (Infinito):**
- Cerebro seleciona: **Input Olho Dominante** (nítido)
- Suprime: Input olho não-dominante (ligeiro blur)
- **Resultado Perceptual:** Imagem clara de longe

**Para Perto (33 cm):**
- Cerebro seleciona: **Input Olho Não-Dominante** (nítido)
- Utiliza parcialmente: Input olho dominante (EDOF ligeira ajuda)
- **Resultado Perceptual:** Imagem clara de perto

**Para Intermédio (60-80 cm - Computador):**
- Cerebro **soma** inputs de ambos os olhos (Blend Zone)
- Ambos contribuem parcialmente
- **Resultado Perceptual:** Visão funcional intermediária

**Flechas bidirecionais:** Entre cérebro e cenas visuais (longe/perto/intermédio)

**Caixa de Texto:**  
"**Neuroadaptação:** Supressão seletiva + Somação binocular = Seamless vision em todas as distâncias (após 3-6 meses)"

**Objetivo:**  
Ilustrar de forma intuitiva o mecanismo de monovisão balanceada e o papel crítico da neuroadaptação.

---

**Este Capítulo 5 está agora COMPLETO**, com:
- ✅ Algoritmo matemático de Ghenassia completo
- ✅ Nomogramas práticos (hipermetropia, miopia, idade)
- ✅ Protocolo cirúrgico Wavelight detalhado
- ✅ Estratégia bilateral (dominante vs. não-dominante)
- ✅ Gestão pós-operatória e troubleshooting
- ✅ Transferência para outras plataformas
- ✅ 10 Referências bibliográficas
- ✅ 5 Infográficos clínicos detalhados

Pronto para copiar para o Google Drive!
