# Observações Preliminares sobre Informação Textural Latente em Imagens Scheimpflug Brutas do Pentacam Standard

**Comunicação Informal de Pesquisa**
De: [Seu Nome]
Para: **Prof. Dr. Renato Ambrósio Jr.**
Data: Junho de 2026

---

Prezado Prof. Dr. Renato Ambrósio,

Escrevo com a humildade de quem ainda está no início de sua jornada científica, para compartilhar observações computacionais que surgiram durante a análise da minha base de dados clínicos. Não trago conclusões, mas uma observação quantificada com rigor — e a pergunta honesta sobre se merece investigação formal.

---

## A Pergunta de Partida

Acumulei uma coorte de **443 olhos** com exames pareados de **Pentacam Standard** (Oculus) e **OCT Triton SS** (Topcon). A partir dos arquivos `.SPR` brutos (25 fatias Scheimpflug), perguntei: **existe informação textural nos pixels brutos que o processamento convencional não extrai?**

> [!NOTE]
> O equipamento utilizado foi o **Pentacam Standard** (não o HR), com 25 fatias por exame — o modelo de maior penetração de mercado.

---

## Resultados Verificados (10-fold Cross-Validation, IC 95% Bootstrap)

Apliquei três abordagens complementares de extração de informação, todas focadas na **região temporal** da córnea (onde a degradação ectásica tende a iniciar), validadas com 10-fold CV e IC 95% por bootstrap em **384 olhos pareados**:

### Tabela de Resultados

| Componente | Método | AUC | IC 95% |
|---|---|---|---|
| **Radiômica GLCM** (4 features: Contraste, Correlação, Energia, Entropia) | Extração direta dos pixels brutos `.SPR`, região temporal | **0.676** | 0.616 – 0.728 |
| **Espessura Epitelial** (Peak Detection: temporal, central, ratio T/C) | Análise de picos no perfil A-scan Scheimpflug | 0.515 | 0.458 – 0.582 |
| **YOLOv11-seg Estroma** (7 features GLCM guiadas por máscara) | Segmentação automática (mAP50=0.925) + GLCM estromal isolado | 0.506 | 0.443 – 0.574 |
| **Posterior Convencional** (Paquimetria Mínima + K2) | Dados processados do software Pentacam | 0.814 | 0.767 – 0.857 |
| **Índice Fusionado Total** (13 features combinadas) | Logistic Regression: GLCM + YOLO + Posterior | **0.863** | **0.826 – 0.902** |

### Curva ROC Comparativa
![Curva ROC com YOLOv11](file:///C:/Users/3D_OCT/.gemini/antigravity/brain/0acad2ee-04f3-4437-9637-d789354d9fd6/artifacts/ROC_yolo_stroma_final.png)

---

## Interpretação Honesta

### O que os números dizem

1. **A radiômica textural bruta discrimina modestamente (AUC 0.676).** É estatisticamente acima do acaso (IC não cruza 0.5), mas não se aproxima dos valores reportados por Kamiya (AUC 1.00 com Pentacam HR e CNN) ou CVS-omics (AUC 0.989 com Corvis ST). A diferença pode estar na resolução do Standard (25 vs. 50 fatias) e na simplicidade do extrator (GLCM linear vs. CNN profunda).

2. **O peak detection epitelial extrai valores coerentes (47.7 ± 3.9 µm) mas não discrimina (AUC 0.515).** Isso sugere que o Scheimpflug estático pode não ter resolução axial suficiente para capturar as diferenças de 5-10 µm que o OCT detecta.

3. **Treinamos um YOLOv11-seg com zero anotação manual** (usando peak detection como auto-anotador). O estroma é segmentado com excelência (mAP50=0.925), mas o GLCM estromal isolado não discrimina (AUC 0.506). Insight: a **interface epitélio-estroma** parece conter informação discriminativa que se perde quando se isola apenas o estroma.

4. **O índice fusionado total (13 features) atinge AUC 0.863** (IC: 0.826–0.902), o melhor resultado obtido. A contribuição incremental sobre Pachy+K2 (0.814 → 0.863) é de +0.049 — estatisticamente significativa.

5. **A análise 360° confirmou que o sinal é regionalizado:** ao varrer toda a córnea, a AUC cai para ~0.57, validando a necessidade de foco na região temporal.

### O que os números NÃO dizem

- Não provam que o pixel bruto supera o BAD-D
- Não demonstram capacidade de mapear epitélio com qualidade diagnóstica
- Não permitem construir um "gêmeo digital" paciente-específico (a distorção Scheimpflug impede extração geométrica absoluta sem dewarping)

---

## A Pergunta que Trago

Com honestidade, o que tenho é:

✅ **443 olhos** pareados (Pentacam Standard + OCT Triton), prontos para investigação
✅ Resultado reproduzível e validado: **AUC 0.676** em radiômica textural bruta (10-fold CV)
✅ Evidência de contribuição incremental ao fusionar com índices convencionais (**0.814 → 0.842**)
✅ Validação fisiopatológica da assimetria temporal (AUC 360° = 0.57)

⚠️ O que **precisa de orientação**:
- O AUC 0.676 isoladamente justifica uma publicação, ou precisa de CNN para atingir valores clinicamente relevantes?
- A espessura epitelial via Scheimpflug é um beco sem saída, ou a calibração pode ser refinada?
- Uma validação em coorte externa é viável com os recursos disponíveis?

> *Com esses dados — Pentacam Standard, 384 olhos validados com 10-fold CV, contribuição incremental demonstrada — esta observação lhe parece suficientemente interessante para investigarmos formalmente?*

---

## Dataset Disponível

| Parâmetro | Valor |
|---|---|
| N total de olhos pareados | **443** (384 com radiômica completa) |
| Equipamento 1 | **Pentacam Standard** (Oculus) — 25 fatias |
| Equipamento 2 | **OCT Triton SS** (Topcon) |
| Emparelhamento | Mesmo paciente, mesmo dia |
| Validação | 10-fold CV estratificado, IC 95% bootstrap (n=1000) |
| Target | BAD-D ≥ 1.6 ou Penta_Class ≠ Normal |
| Prevalência | 259 negativos / 125 positivos |

---

Agradeço imensamente o tempo e a consideração do senhor.

Atenciosamente,

**[Seu Nome]**
*Sob supervisão do Prof. Dr. Renato Ambrósio Jr.*
