# Guia BioRender para Diagramas Anatómicos/Ópticos

## 🎨 **SETUP INICIAL - BIORENDER**

**Acesso:** https://biorender.com
- **Plano:** Academic/Pro (necessário para export alta resolução)
- **Custo:** ~$200-300/ano (vale a pena para publicação)
- **Trial:** 14 dias grátis (pode criar alguns diagramas)

---

## 📋 **DIAGRAMAS PRIORITÁRIOS DO LIVRO:**

### **PARTE I - FUNDAMENTOS (Capítulos 1-2)**

#### 1. Anatomia do Aparelho Acomodativo (Cap 1)
**BioRender Elements Needed:**
- Eyeball (cross-section)
- Crystalline lens
- Ciliary muscle
- Zonules of Zinn
- Cornea

**Descrição para BioRender:**
```
Create anatomical cross-section of eye showing accommodation mechanism:
- Cornea (anterior)
- Crystalline lens (center, biconvex)
- Ciliary muscle (circular, around lens equator)
- Zonular fibers connecting ciliary muscle to lens capsule
- Labels: "Relaxed state (Distance vision)" vs "Contracted state (Near vision)"
- Show lens shape change: flattened → more spherical
- Arrows indicating zonular tension changes
- Color scheme: Blue (cornea), Yellow (lens), Red (muscle)
```

**Arquivo Salvar:** `chapter1_accommodation_mechanism.png`

---

#### 2. Q-Factor e Aberração Esférica (Cap 2)
**BioRender Elements Needed:**
- Cornea profile (custom shape)
- Light rays
- Focus points

**Descrição para BioRender:**
```
Create 3 corneal profiles side-by-side comparing Q-factors:

PROFILE 1 - PROLATE (Q = -0.26, Normal):
- Curved line: steeper center, flatter periphery
- 3 light rays: parallel entry, converging to single focal point
- Label: "Prolate (Normal) Q = -0.26"

PROFILE 2 - HYPERPROLATE (Q = -0.80, PresbyCor):
- Curved line: very steep center, very flat periphery
- 3 light rays: peripheral rays focus AFTER central rays
- Show 2 focal points (near and far)
- Label: "Hyperprolate (PresbyCor) Q = -0.80"
- Highlight "EDOF Zone" between focal points

PROFILE 3 - OBLATE (Q = +0.50, Post-LASIK):
- Curved line: flatter center, steeper periphery
- Light rays: peripheral rays focus BEFORE central rays
- Label: "Oblate (Post-Myopic LASIK) Q = +0.50"

Color: Cornea = blue, Light rays = yellow/orange, Focal points = red
```

**Arquivo Salvar:** `chapter2_qfactor_comparison.png`

---

### **PARTE II - TÉCNICAS CIRÚRGICAS (Capítulos 4-8)**

#### 3. LASIK vs PRK - Comparação Anatómica (Cap 4)
**Descrição para BioRender:**
```
Create 2-panel comparison:

PANEL A - LASIK:
- Cornea cross-section (5 layers visible)
- Epithelium (thin, top)
- Bowman's layer
- Stroma (thick middle)
- Show flap creation: hinged flap (100-110 μm thickness)
- Laser ablation in stromal bed
- Flap repositioned
- Labels: "Flap", "Ablation zone", "Untouched endothelium"

PANEL B - PRK:
- Same cornea cross-section
- Epithelium completely removed (shown as removed layer)
- Laser ablation directly on Bowman's/anterior stroma
- No flap
- Label: "Epithelium regenerates 3-5 days"

Add comparison table below:
Recovery | LASIK: 1-2 days | PRK: 5-7 days
Pain | LASIK: Minimal | PRK: Moderate
Biomechanics | LASIK: RSB dependent | PRK: Stronger long-term
```

**Arquivo Salvar:** `chapter4_lasik_vs_prk.png`

---

#### 4. PresbyCor - Perfil de Ablação (Cap 5)
**Descrição para BioRender:**
```
Create corneal ablation profile visualization:

CROSS-SECTION VIEW:
- Pre-op cornea: smooth prolate curve (Q = -0.26)
- Post-op cornea: hyperprolate curve (Q = -0.80)
- Show tissue removed: shaded area between curves
  - Central: minimal removal (preserve add power)
  - Paracentral: moderate removal
  - Peripheral: maximum removal (create steep transition)

TOPOGRAPHIC VIEW (bird's eye):
- Concentric rings showing power distribution
- Center (2mm): +add power (red/warm colors)
- Mid-zone (2-5mm): transition
- Periphery (5-6mm): distance power (blue/cool colors)

Labels:
- "Central Add Zone: +1.50 to +2.00 D effective"
- "Peripheral Distance Zone"
- "Smooth transition = EDOF"
```

**Arquivo Salvar:** `chapter5_presbycor_ablation_profile.png`

---

#### 5. PRESBYOND - Blend Zone Concept (Cap 7)
**Descrição for BioRender:**
```
Create diagram showing binocular blend zone:

TOP VIEW - DEFOCUS CURVES:
Two overlapping bell curves:
- Blue curve: Dominant eye (peak at 0 D, target +0.50 D)
- Red curve: Non-dominant eye (peak at -1.25 D, micro-myopia)
- Green shaded area: OVERLAP zone = "Blend Zone" (60-100 cm)

SIDE VIEW - FUNCTIONAL VISION:
Distance (>3m): Dominant eye primary
Intermediate (60-100cm): BOTH eyes contributing equally (fusion)
Near (<40cm): Non-dominant eye primary

Show patient figure at computer (blend zone distance)
Arrows: Both eyes → Fused image → Clear vision

Label: "Blend Zone = Stereo fusion + Optimal intermediate"
```

**Arquivo Salvar:** `chapter7_presbyond_blend_zone.png`

---

### **PARTE III - APLICAÇÕES AVANÇADAS (Capítulos 9-11)**

#### 6. RSB (Residual Stromal Bed) - Biomecânica (Cap 9)
**Descrição para BioRender:**
```
Create corneal cross-section with measurements:

NORMAL CORNEA (Pre-op):
- Total thickness: 550 μm
- Layers labeled

POST-LASIK CORNEA:
- Flap: 110 μm (hinged, top)
- Ablation depth: 80 μm (removed tissue, shown as gap)
- RSB: 360 μm (remaining stroma)
- Endothelium: intact

COLOR CODING:
- RSB >350 μm: GREEN (safe)
- RSB 300-350 μm: YELLOW (caution)
- RSB <300 μm: RED (danger - ectasia risk)

Add calculation formula:
RSB = Pachymetry - Flap thickness - Ablation depth
Target: ≥300 μm (presbyopia: ≥320 μm recommended)

Show ectasia risk arrow: Low → High as RSB decreases
```

**Arquivo Salvar:** `chapter9_rsb_biomechanics.png`

---

#### 7. DLK Grading Visual (Cap 11)
**Descrição para BioRender:**
```
Create 4-panel progression of DLK severity:

Each panel: LASIK interface (magnified view, looking down through flap)

GRADE 1:
- Few white dots scattered in periphery
- Interface mostly clear
- Label: "Peripheral dots only"

GRADE 2:
- More dense white infiltrates
- Extending toward center
- Label: "Paracentral involvement"

GRADE 3:
- Diffuse white infiltrates ("sand")
- Covering entire interface
- Label: "Diffuse 'Sahara' - EMERGENCY"

GRADE 4:
- Dense white opacity
- Visible striae (wrinkles) in flap
- Label: "Critical - Risk permanent vision loss"

Color: White infiltrates on gray background
Add management below each: Pred dosing + urgency level
```

**Arquivo Salvar:** `chapter11_dlk_grading.png`

---

### **DIAGRAMAS ÓPTICOS AVANÇADOS**

#### 8. Ray Tracing - Multifocal Effect (Cap 2)
**Descrição para BioRender:**
```
Create optical ray tracing diagram:

SETUP:
- Hyperprolate cornea on left (Q = -0.80)
- 5 parallel light rays entering from left
- Retina on right

RAY PATHS:
- Ray 1 (central, 0mm): Focuses at Point A (near focus, +2.00 D)
- Ray 2-3 (paracentral, 2mm): Focus between A and B
- Ray 4-5 (peripheral, 4mm): Focus at Point B (distance focus, 0 D)

RESULT:
- Extended focal zone A→B shaded
- Label: "EDOF = Extended Depth of Focus"
- Show object distances: 6m (Point B) to 40cm (Point A)

Add MTF curve below showing:
- Standard cornea: Sharp peak, narrow base
- Hyperprolate: Lower peak, WIDER base (trade-off)
```

**Arquivo Salvar:** `chapter2_ray_tracing_edof.png`

---

## 🎯 **WORKFLOW BIORENDER:**

### **Passo-a-Passo:**

1. **Login BioRender** → Create New
2. **Search Icons:** Use biblioteca médica
   - "eye anatomy"
   - "cornea cross section"
   - "light rays"
   - "lens"
3. **Drag & Drop** elementos
4. **Customize:**
   - Colors (usar esquema consistente)
   - Labels (fonte: Arial/Helvetica, 12-14pt)
   - Arrows (usar estilo consistente)
5. **Export:**
   - Format: PNG
   - Resolution: **300 DPI** (publicação)
   - Size: 2000-3000px width
6. **Salvar em:** `figures/chapter[X]/biorender_[name].png`

---

## 📊 **PRIORIDADES (Ordem Recomendada):**

**Alta Prioridade:**
1. ✅ Q-Factor comparison (Cap 2) - Fundamental
2. ✅ LASIK vs PRK (Cap 4) - Didático
3. ✅ PresbyCor ablation profile (Cap 5) - Core técnico
4. ✅ PRESBYOND blend zone (Cap 7) - Conceito único
5. ✅ RSB biomechanics (Cap 9) - Segurança

**Média Prioridade:**
6. DLK grading (Cap 11)
7. Accommodation mechanism (Cap 1)
8. Ray tracing EDOF (Cap 2)

**Baixa Prioridade (opcional):**
- Diagramas complementares
- Variações técnicas

---

## 💡 **DICAS BIORENDER:**

1. **Use Templates:** BioRendertem templates "Eye Anatomy" prontos
2. **Consistência:** Mesmo esquema de cores em todos
3. **Simplicidade:** Menos é mais (não sobrecarregar)
4. **Labels Claros:** Font size ≥12pt, contraste alto
5. **Export Batch:** Exportar todos de uma vez (mesmo DPI)

---

## 📁 **ORGANIZAÇÃO FINAL:**

```
/figures
  /biorender_source  (arquivos .bio - fonte editável)
  /chapter1
    - biorender_accommodation.png
  /chapter2
    - biorender_qfactor_comparison.png
    - biorender_ray_tracing.png
  /chapter4
    - biorender_lasik_vs_prk.png
  /chapter5
    - biorender_presbycor_profile.png
  /chapter7
    - biorender_presbyond_blend.png
  /chapter9
    - biorender_rsb_biomechanics.png
  /chapter11
    - biorender_dlk_grading.png
```

---

**Total Estimado:** ~8-12 diagramas BioRender (3-4 horas trabalho)

**Quando completar, commitar:**
```bash
git add figures/
git commit -m "Add BioRender anatomical/optical diagrams"
git push
```
