# Infográfico: Comparação Zernike vs Fourier - Diagrama de Venn

## Objetivo
Visualizar graficamente as diferenças e overlaps entre análise de Zernike (wavefront) e Fourier (topografia), facilitando decisão clínica sobre qual método usar.

## Descrição Visual

### Estrutura: Diagrama de Venn com 3 Zonas

**Layout:**
- Dois círculos sobrepostos criando 3 zonas distintas
- Círculo esquerdo (AZUL): "Análise de Zernike"
- Círculo direito (VERDE): "Análise de Fourier"
- Área de overlap (AMARELO): Aplicações onde ambos são úteis

---

### ZONA 1 (Azul - Somente Zernike)

**Título:** "Análise de Frente de Onda - Sistema Óptico Total"

**Ícones/Elementos:**
- 👁️ Olho completo (córnea + cristalino + meios)
- 🌊 Ondas de luz atravessando todo o olho
- 📊 Gráfico de aberrações de alta ordem

**Aplicações Exclusivas:**
- ✅ Cirurgia de presbiopia (Custom-Q, PresbyCor)
- ✅ Wavefront-guided LASIK
- ✅ Predição de qualidade visual (MTF, Strehl)
- ✅ Análise de compensação interna (córnea vs cristalino)
- ✅ PRESBYOND, micro-monovisão optimizada

**Equipamentos:**
- iTrace (Ray-Tracing)
- OPD-Scan III
- COAS-HD, WASCA

**Vantagem Chave:**
"Mede o resultado FINAL que o paciente vê (sistema completo)"

---

### ZONA 2 (Verde - Somente Fourier)

**Título:** "Análise Topográfica - Superfície Corneana"

**Ícones/Elementos:**
- 🔍 Lupa sobre córnea isolada
- 📐 Mapa de elevação/curvatura
- 🌀 Padrão de irregularidade (ondulações)

**Aplicações Exclusivas:**
- ✅ Queratocone (detecção e tratamento)
- ✅ Topography-guided ablation (T-CAT, Contoura)
- ✅ Cicatrizes corneanas (regularização)
- ✅ Avaliação de ectasia pós-LASIK
- ✅ Pós-trauma/cirurgia com irregularidade

**Equipamentos:**
- Pentacam (Scheimpflug)
- Topolyzer
- Galilei Dual Scheimpflug
- Atlas (Placido)

**Vantagem Chave:**
"Detecta irregularidades CORNEANAS puras, mesmo se compensadas internamente"

---

### ZONA 3 (Amarelo - Overlap: Ambos Úteis)

**Título:** "Quando Usar os Dois (Complementares)"

**Cenários:**
1. **Avaliação pré-op completa**
   - Pentacam (topografia) + iTrace (wavefront)
   - Decisão: Wavefront ou topography-guided?

2. **Discordância diagnóstica**
   - Wavefront "limpo" mas topografia irregular → Compensação interna
   - Decisão: Tratar córnea ANTES de presbiopia

3. **Pós-op problemático**
   - Ambos para identificar causa (ablação vs cicatrização)
   - Planejamento de enhancement

4. **Queratoplastia**
   - Fourier: Irregularidade de implante
   - Zernike: Qualidade visual resultante

**Regra de Ouro (Caixa Destacada):**
"Se Fourier e Zernike concordam: ✅ CANDIDATO PERFEITO"
"Se divergem: ⚠️ INVESTIGAR causa antes de operar"

---

### Rodapé: Tabela Decisional Rápida

| Objetivo Cirúrgico | Análise Primária | Análise Secundária |
|--------------------|------------------|--------------------|
| **PresbyLASIK** | Zernike | (Opcional: Fourier p/ screening) |
| **Queratocone/Ectasia** | Fourier | Zernike (qualidade visual) |
| **LASIK miópico/hipermetrópico** | Zernike | - |
| **Pós-trauma** | Fourier | Zernike (pós-regularização) |
| **Enhancement problemático** | Ambos | - |

---

### Paleta de Cores

- **Azul Zernike:** #3B82F6 (azul royal)
- **Verde Fourier:** #10B981 (verde moderno)
- **Amarelo Overlap:** #FCD34D (amarelo ouro)
- **Fundo:** Branco ou cinza muito claro (#F9FAFB)

---

### Anotações Laterais (Call-outs)

**Esquerda (Zernike):**
→ "Normalização: Círculo unitário (ρ = 0-1)"
→ "Padrão OSA/ANSI Z80.28"

**Direita (Fourier):**
→ "Normalização: Domínio de frequência espacial"
→ "Harmônicos: Baixa vs Alta ordem"

**Centro (Overlap):**
→ "Integração: Casos complexos"
→ "Validação cruzada"

---

## Tamanho Sugerido
- **Resolução:** 1200×800 px mínimo
- **DPI:** 300 (print-ready)
- **Formato:** PNG com fundo transparente

---

## Uso no Capítulo

Inserir após a seção 2.3.4 (Tabela Comparativa Definitiva), com legenda:

*Figura 2.X: Diagrama de Venn comparando análises de Zernike vs Fourier. A zona de overlap (amarelo) indica cenários onde ambas são complementares. Use Zernike como padrão para presbiopia e Fourier para irregularidades corneanas.*
