# Infográfico: Fluxograma de Triagem Pré-Operatória com Aberrometria

## Objetivo
Fornecer algoritmo visual claro e prático para decisão cirúrgica baseada em valores aberrométricos, permitindo identificar candidatos ideais vs contraindicações.

## Descrição Visual

### Estrutura: Fluxograma Vertical com Decisões Binárias

**Estilo:**
- Caixas retangulares para perguntas/decisões
- Losangos para pontos de bifurcação
- Setas coloridas por resultado (verde = prosseguir, vermelho = parar, amarelo = cautela)
- Ícones de sinais de trânsito (✅ ⚠️ ❌)

---

### NÍVEL 1: Entrada

**Caixa Inicial (Azul escuro):**
```
┌──────────────────────────────────────┐
│  PACIENTE PRESBIÓPICO CANDIDATO      │
│  Queixa: Dificuldade de perto        │
│  Exame: Córnea transparente          │
│                                      │
│  ▼ AVALIAÇÃO ABERROMÉTRICA ▼        │
└──────────────────────────────────────┘
```

Equipamento indicado: **iTrace / OPD-Scan III**
Pupila de medição: **6.0 mm (padronizado)**

---

### NÍVEL 2: Primeira Triagem - RMS HOA

**Losango de Decisão:**
```
          ╱────────────────╲
         ╱  RMS HOA Total   ╲
        ╱   (6 mm pupila)    ╲
       ╱   < 0.50 μm?         ╲
       ╲_____________________ ╱
```

**RAMO ESQUERDO (NÃO - RMS ≥ 0.50 μm):**
```
┌────────────────────────────────┐
│  ❌ IRREGULARIDADE SIGNIFICATIVA│
│                                │
│  RMS HOA ≥ 0.50 μm             │
│  Qualidade óptica comprometida │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│  OPÇÕES:                       │
│  1. T-CAT Regularização        │
│  2. Descontinuar presbiopia    │
│  3. Considerar RLE             │
└────────────────────────────────┘
```

**RAMO DIREITO (SIM - RMS < 0.50 μm):**
Prosseguir para Nível 3 ↓

---

### NÍVEL 3: Avaliação de Coma

**Losango de Decisão:**
```
          ╱────────────────╲
         ╱  Coma Vertical ou ╲
        ╱   Horizontal         ╲
       ╱   (Z₃⁺¹ ou Z₃⁻¹)      ╲
       ╲  > 0.30 μm?           ╱
        ╲___________________  ╱
```

**RAMO ESQUERDO (SIM - Coma > 0.30 μm):**
```
┌────────────────────────────────┐
│  ⚠️ ALTO RISCO MULTIFOCAL       │
│                                │
│  Coma > 0.30 μm                │
│  Sintoma: Diplopia monocular   │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│  ALTERNATIVAS SEGURAS:         │
│                                │
│  1️⃣ Monovisão Simples           │
│    (sem indução de SA neg.)    │
│    Alvo: -0.75 a -1.50 D       │
│                                │
│  2️⃣ RLE Bilateral               │
│    (evitar córnea)             │
│    IOL: EDOF ou multifocal     │
│                                │
│  ❌ NÃO: PresbyLASIK multifocal │
└────────────────────────────────┘
```

**RAMO DIREITO (NÃO - Coma ≤ 0.30 μm):**
Prosseguir para Nível 4 ↓

---

### NÍVEL 4: Avaliação de SA Pré-Existente

**Losango de Decisão:**
```
          ╱────────────────╲
         ╱  SA Total (Z₄⁰)   ╲
        ╱   > +0.30 μm?       ╲
       ╱   (SA positiva alta) ╲
       ╲_____________________ ╱
```

**RAMO ESQUERDO (SIM - SA > +0.30 μm):**
```
┌────────────────────────────────┐
│  ⚠️ SA POSITIVA ELEVADA         │
│                                │
│  Indício: Opacidade lenticular │
│  ou córnea oblata severa       │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│  AVALIAÇÃO ADICIONAL:          │
│                                │
│  • Pentacam Densitometry       │
│  • OSI (Objective Scatter)     │
│  • Classificação DLS           │
│                                │
│  Se DLS Stage 2:               │
│  → Favorecer RLE               │
│                                │
│  Razão: Induzir Q hiper-prolato│
│  pode NÃO compensar SA interna │
└────────────────────────────────┘
```

**RAMO DIREITO (NÃO - SA ≤ +0.30 μm):**
Prosseguir para Nível 5 ↓

---

### NÍVEL 5: Candidato Aprovado - Planejamento

**Caixa Final (Verde):**
```
┌═══════════════════════════════════┐
║  ✅ CANDIDATO IDEAL PRESBYLASIK   ║
║                                   ║
║  RMS HOA < 0.50 μm  ✓             ║
║  Coma < 0.30 μm     ✓             ║
║  SA normal          ✓             ║
╞═══════════════════════════════════╡
║  PLANEJAMENTO CIRÚRGICO:          ║
║                                   ║
║  📊 Estratégia:                   ║
║     Custom-Q / PresbyCor          ║
║                                   ║
║  🎯 Alvo de SA:                   ║
║     -0.40 a -0.60 μm              ║
║     (Zona terapêutica segura)     ║
║                                   ║
║  🔧 Q-target:                     ║
║     -0.80 a -1.20                 ║
║     (Hiper-prolato controlado)    ║
║                                   ║
║  👁️ Dominância:                   ║
║     OD: Plano (visão longe)       ║
║     OE: -0.75 D (micro-monov.)    ║
║                                   ║
║  ⭕ Zona Óptica:                  ║
║     Pupila mesópica + 0.5-1.0 mm  ║
║     Tipicamente: 6.0-6.5 mm       ║
╞═══════════════════════════════════╡
║  ⚠️ CENTRAGEM CRÍTICA:            ║
║     No Purkinje reflex (eixo vis.)║
║     NÃO no centro pupilar         ║
║     Tolerância máxima: 0.3 mm     ║
└───────────────────────────────────┘
```

---

### Rodapé: Legenda de Cutoffs

```
┌──────────────────────────────────────────────────────────┐
│  📏 VALORES DE CUTOFF CRÍTICOS (Pupila 6 mm)             │
├──────────────────────────────────────────────────────────┤
│  RMS HOA:                                                │
│    ✅ < 0.35 μm = Ideal                                  │
│    ⚠️ 0.35-0.50 μm = Aceitável (avaliar Coma)           │
│    ❌ > 0.50 μm = Alto risco                             │
│                                                          │
│  Coma (Z₃⁺¹ ou Z₃⁻¹):                                    │
│    ✅ < 0.20 μm = Excelente                              │
│    ⚠️ 0.20-0.30 μm = Moderado (sintomas noturnos)        │
│    ❌ > 0.30 μm = Contraindicação multifocal             │
│                                                          │
│  SA (Z₄⁰):                                               │
│    Pré-op normal: +0.05 a +0.15 μm                       │
│    Pré-op problemático: > +0.30 μm                       │
│    Pós-op alvo: -0.40 a -0.60 μm                         │
└──────────────────────────────────────────────────────────┘
```

---

### Paleta de Cores por Caminho

- **Verde (✅):** Caminho aprovado, prosseguir
- **Amarelo (⚠️):** Cautela, alternativas seguras
- **Vermelho (❌):** Contraindicado, parar/redireccionar

**Cores HEX:**
- Verde: #10B981
- Amarelo: #F59E0B
- Vermelho: #EF4444
- Azul (neutro): #3B82F6
- Cinza claro (fundo): #F3F4F6

---

## Tamanho Sugerido
- **Orientação:** Vertical (portrait)
- **Resolução:** 1000×1400 px
- **DPI:** 300
- **Formato:** PNG

---

## Uso no Capítulo

Inserir na seção 2.3.5 após o texto introdutório "Fluxograma de Triagem Pré-Operatória", com legenda:

*Figura 2.X: Algoritmo de decisão aberrométrica para cirurgia de presbiopia. Siga o fluxo baseado em valores de RMS HOA, Coma e SA para identificar candidatos ideais vs contraindicações absolutas.*
