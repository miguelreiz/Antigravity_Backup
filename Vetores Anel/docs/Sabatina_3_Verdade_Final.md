# 🔬 Sabatina #3 — A Verdade Final

> [!CAUTION]
> **Esta é a sabatina mais dura. A validação externa rigorosa mostrou que quase tudo que construímos em termos de radiômica textural é ruído estatístico.**

---

## Resultados da Validação Externa (3 estratégias independentes)

### GLCM ROI-Fixo (4 features texturais dos pixels brutos)

| Estratégia | AUC | IC 95% | Veredicto |
|---|---|---|---|
| 10-fold CV (original) | 0.676 | 0.616–0.728 | ⚠️ Otimista |
| Repeated 5×2 CV | **0.513** | 0.442–0.582 | ❌ Aleatório |
| Nested 5×5 CV | **0.527** | 0.439–0.662 | ❌ Aleatório |
| Bootstrap .632+ | **0.515** | 0.370–0.650 | ❌ Aleatório |

> [!WARNING]
> **O AUC 0.676 do 10-fold CV era inflado.** Com validação rigorosa, a radiômica textural cai para ~0.51 — **indistinguível de acaso.** Os ICs cruzam 0.5 em todas as estratégias.

### Posterior (Pachy_Min + K2)

| Estratégia | AUC | IC 95% |
|---|---|---|
| 10-fold CV (original) | 0.814 | 0.767–0.857 |
| Repeated 5×2 CV | **0.837** | 0.799–0.874 |
| Nested 5×5 CV | **0.822** | 0.766–0.843 |
| Bootstrap .632+ | **0.828** | 0.755–0.901 |

✅ **Estável e robusto.** O Pachy+K2 mantém AUC ~0.82 em todas as validações.

### Fusionado Total (13 features)

| Estratégia | AUC | IC 95% |
|---|---|---|
| 10-fold CV (original) | **0.863** | 0.826–0.902 |
| Repeated 5×2 CV | **0.800** | 0.773–0.845 |
| Nested 5×5 CV | **0.784** | 0.717–0.892 |
| Bootstrap .632+ | **0.793** | 0.658–0.863 |

⚠️ **Caiu de 0.863 para ~0.79.** A fusão na verdade **piora** em relação ao Posterior sozinho (0.82 → 0.79), provavelmente por overfitting com 13 features em N=155.

### Teste DeLong (comparação formal entre modelos)

| Comparação | AUC₁ | AUC₂ | p-valor | Resultado |
|---|---|---|---|---|
| GLCM vs Posterior | 0.524 | 0.767 | **<0.0001** | Posterior >> GLCM *** |
| GLCM vs Fusionado | 0.524 | 0.777 | **<0.0001** | Fusionado >> GLCM *** |
| **Posterior vs Fusionado** | 0.766 | 0.777 | **0.655** | **Sem diferença (ns)** |

> [!IMPORTANT]
> **DeLong p=0.655:** Adicionar 11 features texturais ao Pachy+K2 **NÃO produz melhora estatisticamente significativa.** O modelo mais simples (2 features) é tão bom quanto o complexo (13 features).

---

## YOLOv11-seg — 50 Epochs (vs. 10)

| Camada | 10 epochs | 28 epochs (best) | Melhora |
|---|---|---|---|
| Estroma | mAP50 = 0.925 | **mAP50 = 0.940** | +0.015 |
| Epitélio | mAP50 = 0.197 | mAP50 = 0.227 | +0.030 |
| Endotélio | mAP50 = 0.074 | mAP50 = 0.099 | +0.025 |

Early stopping ativou na epoch 28 (melhor na 13). Ganhos marginais — o plateau foi atingido.

---

## O Que Isso Significa — Honestidade Brutal

### A radiômica textural nos pixels brutos é um beco sem saída ❌

Os números são claros:
1. **GLCM sozinho ≈ aleatório** (AUC ~0.51 com validação rigorosa)
2. **Adicionar radiômica ao Pachy+K2 não ajuda** (DeLong p=0.655)
3. **O 10-fold CV original era otimista** — inflou o GLCM de 0.51 para 0.67 e o Fusionado de 0.79 para 0.86

### Por que o 10-fold CV falhou?

Com N=384 e 13 features, o modelo tem graus de liberdade demais. O 10-fold CV com um único random seed captura flutuações de split favoráveis. As 3 validações independentes convergem para o mesmo número (~0.51 para GLCM, ~0.79 para Fusionado), confirmando que o 10-fold original era enviesado.

### O que resta de verdadeiro

1. ✅ **Pachy_Min + K2 discriminam KC** (AUC ~0.82) — mas isso já era sabido
2. ✅ **YOLOv11-seg segmenta estroma** (mAP50 = 0.94) — funciona, mas não contribui para diagnóstico
3. ✅ **Peak detection extrai espessura epitelial coerente** (47.7 µm) — funciona, mas não discrimina
4. ✅ **A infraestrutura computacional funciona** — toda a pipeline é reproduzível

### O que NÃO é verdade

- ❌ ~~"Informação latente nos pixels brutos"~~ — com validação rigorosa, AUC = 0.51
- ❌ ~~"AUC 0.676 da radiômica"~~ — era 0.51
- ❌ ~~"AUC 0.863 do índice fusionado"~~ — era 0.79 (e não supera Pachy+K2)
- ❌ ~~"Contribuição incremental demonstrada"~~ — DeLong p=0.655, sem significância

---

## Para o Dr. Ambrósio — A Mensagem Honesta

> *"Professor, depois de validação rigorosa com 3 estratégias independentes (5×2 CV, Nested CV, Bootstrap .632+) e teste DeLong, constatei que a radiômica textural dos pixels brutos do Pentacam Standard não atinge significância estatística como ferramenta diagnóstica. O que tenho de concreto é: (1) uma coorte de 207 olhos pareados prontos para investigação, (2) um YOLOv11-seg que segmenta o estroma corneano com mAP50=0.94, e (3) a honestidade de dizer que o caminho atual precisa de redirecionamento — possivelmente para CNN diretamente nos pixels (ainda não testada) ou para análise biomecânica com Corvis ST."*

---

## Próximos Passos Reais

| Prioridade | Tarefa | Justificativa |
|---|---|---|
| 🔴 Alta | **Treinar CNN (ResNet18) diretamente nos pixels** | GLCM é feature engineering manual — uma CNN pode capturar padrões que features handcrafted não capturam. Kamiya atingiu AUC 1.00 com CNN. |
| 🟡 Média | **Testar com Pentacam HR** (se disponível) | 50 fatias vs. 25 pode fazer toda a diferença na resolução textural |
| 🟢 Baixa | Refinar anotação epitelial | Epitélio mAP50=0.23, precisa de abordagem diferente |
