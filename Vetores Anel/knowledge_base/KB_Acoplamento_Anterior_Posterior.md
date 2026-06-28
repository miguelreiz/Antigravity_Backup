# Acoplamento Anterior × Posterior da Córnea
## Análise Multi-Eixo: Scheimpflug, OCT, FEM

---

## Sumário Executivo

Análise abrangente da relação entre curvatura anterior e posterior da córnea
usando dados de **672 olhos SPR Scheimpflug**, **443 pares matched OCT-Pentacam**,
e **24 modelos FEM (Elementos Finitos)**.

### Conclusão Principal

> **As superfícies anterior e posterior da córnea se movem de forma INDEPENDENTE
> no espaço (r=0.028), com a posterior funcionando como sensor primário do
> ceratocone (AUC=0.917 vs 0.850 da anterior, d=2.1× maior).**

---

## 1. Hipótese Testada

*Existe relação entre curvatura posterior e anterior do Pentacam de forma
anatômica, funcional, óptica, comática, biomecânica e radiométrica?*

### Resultado: 6 Eixos de Análise

| # | Eixo | Fonte | r / Métrica | p-value | Veredicto |
|---|------|-------|-------------|---------|-----------|
| 1 | **Anatômico** | 672 SPR Scheimpflug | r = 0.063 | ns | ❌ Sem correlação geométrica |
| 2 | **Funcional** | 443 pares clínicos | AUC = 0.866 | *** | ✅ Sinergia K2 × Pachy |
| 3 | **Óptico** | 636 olhos SPR | r = 0.250 | 1.7e-10 | ✅ Correlação significativa |
| 4 | **Comático** | 634 olhos SPR | r = -0.086 | 0.031 | ✅ Inversamente correlacionadas |
| 5 | **Biomecânico** | 24 modelos FEM | r = 0.998 | *** | ✅ Acoplamento mecânico perfeito |
| 6 | **Radiométrico (FII)** | 5.228 OCT + 207 CASIA2 | AUC > 0.90 | *** | ✅ Biomarcador validado |

---

## 2. Descentração Espacial: O Achado Principal

### 2.1 Co-localização dos Ápices (672 SPR)

| Métrica | Valor | Interpretação |
|---------|-------|---------------|
| r(Apex_Ant, Apex_Post) | **0.028** (p=0.47) | ZERO correlação espacial |
| Slope regressão | **0.033** (ideal = 1.0) | Ápices não se acompanham |
| R² | **0.0008** | Ant explica 0.08% da posição post |
| Shift médio (Post−Ant) | **+1.79 ± 2.72 mm** | Posterior mais periférico |
| |Shift| absoluto | **2.59 ± 1.97 mm** | ~2.6mm de diferença média |

### 2.2 Correlações Espaciais

| Par | r | p | Sig |
|-----|---|---|-----|
| Shift vs Decentração | **+0.550** | 9.8e-52 | *** |
| Shift vs Assimetria Post | **−0.231** | 3.7e-9 | *** |
| Decentração vs Assimetria Post | **−0.251** | 1.2e-10 | *** |
| Decentração vs Irregularidade Ant | **+0.108** | 0.006 | ** |

---

## 3. Acoplamento BAD_Df × BAD_Db (443 pares Pentacam)

### 3.1 Correlação Estratificada

| Grupo | N | r(BAD_Df, BAD_Db) | Interpretação |
|-------|---|-------------------|---------------|
| **Global** | 443 | **+0.306*** | Artefato de Simpson |
| **Normal** | 309 | +0.058 (ns) | Quasi-independentes |
| **Suspeito** | 91 | −0.043 (ns) | Leve inversão |
| **KC** | 43 | +0.043 (ns) | Desacoplamento |

### 3.2 Poder Diagnóstico

| Índice | AUC | Cohen d | N |
|--------|-----|---------|---|
| BAD_Df (anterior) | 0.850 | 0.70 | 443 |
| **BAD_Db (posterior)** | **0.917** | **1.49** | 443 |
| BAD_D (composto) | 1.000 | — | 443 |
| FII_IT (OCT) | 0.541* | — | 443 |
| Full (FII+Penta) | **0.988** | — | 443 |

*FII_IT baixo nesta coorte por viés de seleção (matched pairs)

### 3.3 Padrões de Desacoplamento

| Padrão | N | % | KC | BAD_D médio |
|--------|---|---|-----|-------------|
| Normal bilateral (|Df|≤1, |Db|≤1) | 193 | 43.6% | — | — |
| **Posterior isolado** (Db>2, Df<1) | **14** | **3.2%** | 4 (29%) | 3.06 |
| **Anterior isolado** (Df>2, Db<1) | **16** | **3.6%** | 4 (25%) | 2.32 |
| Acoplado bilateral (Df>2, Db>2) | 25 | 5.6% | 25 (100%) | 9.56 |

### 3.4 Amplificação no KC

| | Normal | KC | Delta | Interpretação |
|--|--------|----|----|--------|
| BAD_Df | −0.178 | +10.203 | +10.381 | Anterior amplifica tardiamente |
| BAD_Db | −0.181 | +5.007 | +5.188 | Posterior responde primeiro |
| Wilcoxon Db vs Df no KC | — | — | p=0.044 | Significativamente diferentes |

---

## 4. FII (Índice de Integridade Fibrilar)

### 4.1 Definição

$$\text{FII} = \frac{\bar{B}_{ant}}{\bar{B}_{post}} = \frac{\text{média 33\% anterior do A-scan}}{\text{média 33\% posterior do A-scan}}$$

### 4.2 Regra Diagnóstica Bifatorial

$$\text{KC Verdadeiro} \iff \text{FII}_{\text{Central}} > 1.10 \;\text{AND}\; \text{FII}_{IT} < 1.00$$

### 4.3 Validação

| Coorte | N | Resultado |
|--------|---|-----------|
| Base Tese (Triton Plus) | 5.228 exames | Separação em 5 classes |
| CASIA2 + CorneaNet | 207 olhos | 100% Sens / 100% Esp |
| Cross-val FII × Pentacam | 278 pares | AUC > 0.90 vs BAD-D |
| Moptim Raw Data | 2.085 B-scans | r(Den_Ant, Den_Post) = 0.610 |

### 4.4 FII × Geometria Pentacam

| Correlação | r | p | Interpretação |
|------------|---|---|---------------|
| FII_IT vs BAD_Db | **−0.001** | 0.98 | ZERO — dimensões ortogonais |
| FII_IT vs BAD_Df | +0.079 | 0.096 | ns |
| FII_IT vs BAD_D | +0.081 | 0.089 | ns |

> **O FII é completamente independente da geometria Pentacam.**
> São dimensões diagnósticas ortogonais — combiná-las gera AUC=0.988.

---

## 5. Acoplamento Biomecânico (FEM)

### 5.1 Modelos

24 modelos FEM (FEBio, HGO anisotrópico):
- 18 paramétricos (D5/D6 × d60/d70/d80 × t150/t200/t250/t300)
- 3 morfológicos (baseline, triangular, oval)

### 5.2 Resultados

| Métrica | Valor |
|---------|-------|
| r(ΔZ_ant, ΔZ_post) no ápice | **0.998** |
| Posterior deforma | **4-8% mais** que anterior |
| Ratio coupling apex | **0.930** (post/ant) |
| Von Mises anterior | **0.12 MPa** |
| Von Mises posterior | **0.08 MPa** |

---

## 6. Modelo Sequencial do Defeito

### Fase 1: Pré-clínico
- Colapso fibrilar IT (FII_IT < 1.05)
- Geometria normal (BAD_Df ≈ 0, BAD_Db ≈ 0)

### Fase 2: Sub-clínico
- Posterior cede primeiro (BAD_Db > 2, BAD_Df < 1)
- Ápice posterior desloca +1.8mm para periferia
- 3.2% dos olhos nesta fase

### Fase 3: KC Manifesto
- Anterior amplifica (Df = +10.2 vs Db = +5.0)
- Superfícies desacopladas (r = 0.043)
- Posições dos defeitos potencialmente diferentes

### Fase 4: Desacoplamento Persistente
- r(Apex_Ant, Apex_Post) = 0.028
- |Shift| médio = 2.6mm
- Anterior e posterior continuam independentes

---

## 7. Racional Biomecânico

### Por que a posterior está descentrada?

1. **Rigidez diferencial** (Brillouin):
   - Anterior: 3× mais rígida → casca rígida → deforma difusamente
   - Posterior: 1/3 da rigidez → responde LOCALMENTE → defeito puntiforme IT

2. **Anatomia fibrilar**:
   - Anterior (130μm): fibras oblíquas entrelaçadas ("bow springs")
   - Posterior (350μm): lamelas paralelas/ortogonais → menor resistência

3. **Assimetria de carga**:
   - Tração muscular IT (reto inferior + oblíquo inferior)
   - Limbo IT mais fino que nasal

---

## Scripts e Dados

### Scripts de Análise

| Script | Função |
|--------|--------|
| `radiomics/hypothesis_ant_post.py` | Teste 5 eixos: anatômico/funcional/óptico/comático/biomecânico |
| `radiomics/ponte_fii_curvatura.py` | Ponte FII × Curvatura Ant/Post (443 pares) |
| `radiomics/batch_curvature_extractor.py` | Extração de curvaturas dos SPR |
| `fem_engine/analyze_ant_post_coupling.py` | Acoplamento FEM anterior-posterior |
| `fem_engine/post_processor.py` | Processador FEM com perfil posterior |

### Resultados

| Arquivo | Conteúdo |
|---------|----------|
| `results/batch_curvature_metrics.csv` | 672 olhos × 16 métricas curvatura |
| `results/correlacoes_fii_antpost.csv` | 12 pares de correlação FII × Pentacam |
| `results/hypothesis_ant_post_dashboard.png` | Dashboard 5 eixos |
| `results/ponte_fii_curvatura_antpost.png` | Dashboard FII × Curvatura (8 painéis) |
| `results/descentracao_antpost_espacial.png` | Dashboard descentração espacial |
| `fem_engine/fem_antpost_*.png` | 4 figuras FEM |

### Capítulos do Livro Relevantes

| Capítulo | Conteúdo |
|----------|----------|
| CH-021 | SII/FII — definição e diretrizes clínicas |
| CH-026 | Paradigma Diagnóstico FII — validação massiva |
| CH-028 | Incisões na perspectiva fibrilar |

---

## 8. A Forma da Posterior Gera a Forma da Anterior?

### 8.1 Descritores de Forma (526 olhos SPR)

| Par | Pearson r | p | Interpretação |
|-----|-----------|---|---------------|
| Irregularidade Post → Ant | **+0.028** | 0.52 (ns) | ZERO |
| Assimetria Post → Ant | **+0.015** | 0.74 (ns) | ZERO |
| Residual Post → Ant | **−0.145** | 8.7e-4 | Fraco, INVERSO |

### 8.2 Regressão Múltipla: Post(Irr, Asym, Res) → Anterior

| Target Anterior | R² | Variância Explicada |
|-----------------|-----|---------------------|
| Irregularidade Ant | **0.005** | **0.5%** |
| Assimetria Ant | **0.001** | **0.1%** |
| Residual Ant | **0.025** | **2.5%** |

> **Conclusão: A forma da posterior explica no máximo 2.5% da forma da anterior.**
> São formas geradas por mecanismos INDEPENDENTES.

### 8.3 FEM: Morfologia vs Coupling (24 modelos)

| Modelo | Coupling Apex | Coupling Mid | Coupling Periph | ΔZ Post (%) |
|--------|---------------|--------------|-----------------|-------------|
| Baseline (round) | 0.9228 | 0.9452 | 1.0245 | +8.4% |
| Oval | 0.9579 | 0.9472 | 1.0162 | +4.4% |
| Triangular | 0.9576 | 0.9309 | 1.0152 | +4.4% |

- **CV do coupling ratio = 1.03%** — praticamente constante
- D5 vs D6: coupling = 0.959 vs 0.952 (p < 1e-12, mas delta < 1%)
- **Conclusão FEM**: o acoplamento é propriedade CONSTITUTIVA (material),
  não morfológica (forma)

### 8.4 Achado Inesperado: Astigmatismo × Desacoplamento

| Correlação | r | p |
|------------|---|---|
| Astig vs Desac (Db−Df) | **+0.919** | 1.1e-180 |

Em altos astigmatismos, o acoplamento BAD_Df-BAD_Db AUMENTA (r=0.881),
enquanto em baixos astigmatismos permanece fraco (r=0.118).

### 8.5 Modelo Integrado

**Por que a posterior não gera a anterior?**

1. Estroma anterior (130μm, fibras oblíquas) = casca rígida
   → redistribui stress DIFUSAMENTE → perde a "assinatura" da forma posterior
2. Estroma posterior (350μm, lamelas paralelas) = resposta LOCAL
   → forma puntiforme fiel ao defeito fibrilar
3. O coupling ratio é ~0.95 → a anterior acompanha ~95% da MAGNITUDE
   mas a FORMA é filtrada pela rigidez da casca anterior

> **A anterior acompanha a MAGNITUDE mas NÃO a FORMA da posterior.**
> São como um alto-falante (posterior = fonte) passando por um filtro
> passa-baixa (anterior = casca rígida): amplitude transmitida, forma borrada.

