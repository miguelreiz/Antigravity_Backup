# Pentacam Scheimpflug AI Analysis

> Investigacao computacional de imagens Scheimpflug brutas do Pentacam Standard para deteccao de ceratocone usando radiomics, deep learning (YOLOv11-seg, ResNet18) e analise de elementos finitos (FEM).

## Status do Projeto

**Conclusao cientifica (validada com 3 estrategias independentes):**

Os pixels brutos do Pentacam Standard (25 fatias) **nao contem informacao textural suficiente** para discriminar ceratocone. Todos os metodos testados (GLCM, YOLOv11-seg, ResNet18) convergem para AUC ~0.5 com validacao rigorosa. O unico modelo robusto e Paquimetria Minima + K2 (AUC ~0.82).

## Resultados Consolidados

| Metodo | Validacao | AUC | IC 95% | Status |
|---|---|---|---|---|
| GLCM ROI-fixo (4 feat) | Nested 5x5 CV | 0.527 | 0.439-0.662 | Aleatorio |
| GLCM YOLO-Estroma (7 feat) | 10-fold CV | 0.506 | 0.443-0.574 | Aleatorio |
| Espessura Epitelial (Peak Det.) | 10-fold CV | 0.515 | 0.458-0.582 | Aleatorio |
| ResNet18 CNN pixels brutos | 5-fold CV | 0.592 | 0.491-0.683 | Aleatorio |
| **Posterior (Pachy+K2)** | Nested 5x5 CV | **0.822** | 0.766-0.843 | **Robusto** |

## Estrutura do Repositorio

```
├── README.md
├── requirements.txt
│
├── radiomics/                    # Extracao e validacao de features radiomicas
│   ├── batch_peak_detection.py   # Peak detection epitelial (673 SPR)
│   ├── batch_radiomics.py        # GLCM extraction (full 360)
│   ├── batch_radiomics_IT.py     # GLCM infero-temporal
│   ├── compute_fused_index.py    # Indice fusionado com 10-fold CV
│   ├── cross_validate_radiomics.py
│   └── external_validation.py    # 3 estrategias de validacao rigorosa
│
├── segmentation/                 # YOLOv11-seg corneal layer segmentation
│   ├── train_yolo_cpu.py         # Training pipeline (10 epochs)
│   ├── train_yolo_50ep.py        # Extended training (50 epochs)
│   ├── evaluate_yolo_cornea.py   # YOLO-guided GLCM evaluation
│   └── refine_epithelial_annotation.py
│
├── classification/               # CNN classifier
│   └── train_cnn_classifier.py   # ResNet18 on raw pixels
│
├── spr_tools/                    # SPR file parsing utilities
│   ├── decode_spr.py             # Binary format decoder
│   ├── analyze_spr.py            # Exploratory analysis
│   └── explore_spr_header.py     # Header parsing
│
├── fem_engine/                   # Finite Element Method simulation
│   ├── mesh_generator.py         # Cornea mesh generation
│   ├── febio_builder.py          # FEBio model builder
│   ├── runner.py                 # FEBio execution wrapper
│   ├── post_processor.py         # Results post-processing
│   ├── advanced_analysis.py      # HGO material model analysis
│   └── parametric_study.py       # Ring parameter sweep
│
├── digital_twin/                 # Digital twin pipeline
│   ├── digital_twin_extractor.py # SPR -> patient-specific geometry
│   ├── fem_bridge.py             # Geometry -> FEM model
│   └── plot_digital_twin.py      # Visualization
│
├── visualization/                # Plotting and visualization
│   ├── plot_densitometry.py
│   ├── plot_pentacam_epithelium_map.py
│   ├── plot_progression_epithelium_map.py
│   └── scratch_pentacam_layers.py
│
├── results/                      # Output plots and CSV results
│   ├── ROC_yolo_stroma_final.png
│   ├── ROC_indice_fusionado.png
│   ├── ROC_CNN_ResNet18_KC.png
│   ├── external_validation_roc.png
│   ├── external_validation_boxplot.png
│   ├── epithelial_peak_detection.csv
│   ├── yolo_stroma_features.csv
│   ├── external_validation_results.csv
│   ├── delong_test_results.csv
│   └── cnn_classifier_results.csv
│
├── docs/                         # Documentation and reports
│   ├── Sabatina_Auditoria_Critica.md
│   ├── Sabatina_2_Resultados_Reais.md
│   ├── Sabatina_3_Verdade_Final.md
│   ├── Carta_Ambrosio_Humilde.md
│   ├── Artigo_Cientifico_Ambrosio.md
│   └── KB_Scheimpflug_IA_Fundamentos.md
│
└── knowledge_base/               # Reference materials
```

## Como Usar

### Pre-requisitos
```bash
pip install -r requirements.txt
```

### Extracao de features radiomicas
```python
python radiomics/batch_radiomics_IT.py
python radiomics/compute_fused_index.py
```

### Treinamento YOLOv11-seg
```python
# Requer dataset em yolo_cornea_dataset/ (gerado a partir de SPR files)
python segmentation/train_yolo_cpu.py
python segmentation/evaluate_yolo_cornea.py
```

### Simulacao FEM
```python
python fem_engine/mesh_generator.py
python fem_engine/febio_builder.py
python fem_engine/runner.py
python fem_engine/post_processor.py
```

## Coorte

- **443 olhos** pareados Pentacam Standard + OCT Triton
- **384 olhos** com dados clinicos completos
- **25 fatias** Scheimpflug por exame (formato .SPR binario)

## Metodologia de Validacao

Tres estrategias independentes implementadas:
1. **Repeated 5x2 CV** (Dietterich 1998)
2. **Nested 5x5 CV** (outer para AUC, inner para hyperparameters)
3. **Bootstrap .632+** (less biased than standard bootstrap)
4. **Teste DeLong** para comparacao formal entre modelos

## Tecnologias

- Python 3.14
- PyTorch + torchvision (ResNet18)
- Ultralytics YOLOv11 (segmentacao)
- scikit-learn (validacao, metricas)
- scikit-image (GLCM, radiomics)
- FEBio (elementos finitos)
- NumPy, Pandas, Matplotlib

## Licenca

Este projeto e para fins de pesquisa academica.

## Autor

Miguel Reiz (@miguelreiz)
