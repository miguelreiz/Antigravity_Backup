"""
Treinamento YOLOv11-seg otimizado para CPU.
Reutiliza o dataset já exportado na rodada anterior.
- 10 epochs (com early stopping patience=5)
- imgsz=256 (mais rápido)
- fraction=0.3 (usa 30% das imagens por epoch — suficiente para convergência)
"""
import os
from ultralytics import YOLO

DATASET_DIR = r'C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\yolo_cornea_dataset'
yaml_path = os.path.join(DATASET_DIR, 'dataset.yaml')

print("=" * 60)
print("  YOLOv11-seg — Treinamento Otimizado (CPU)")
print("=" * 60)

# Verificar que o dataset existe
train_dir = os.path.join(DATASET_DIR, 'images', 'train')
n_train = len([f for f in os.listdir(train_dir) if f.endswith('.png')])
print(f"Imagens de treino disponíveis: {n_train}")

model = YOLO('yolo11n-seg.pt')

results = model.train(
    data=yaml_path,
    epochs=10,
    imgsz=256,          # Menor que 416 = 2.6x mais rápido
    batch=32,           # Batch maior em CPU é mais eficiente
    task='segment',
    name='cornea_seg_cpu',
    project=os.path.join(DATASET_DIR, 'runs'),
    patience=5,         # Early stopping agressivo
    fraction=0.3,       # Usa 30% do dataset por epoch (~3600 imgs)
    mosaic=0.0,
    flipud=0.5,
    fliplr=0.5,
    scale=0.2,
    degrees=0.0,
    workers=0,
    verbose=True,
    exist_ok=True
)

print("\n" + "=" * 60)
print("  TREINAMENTO CONCLUÍDO!")
print("=" * 60)

# Métricas finais
best_model = os.path.join(DATASET_DIR, 'runs', 'cornea_seg_cpu', 'weights', 'best.pt')
print(f"Melhor modelo: {best_model}")

if os.path.exists(best_model):
    # Validação final
    model_best = YOLO(best_model)
    metrics = model_best.val(data=yaml_path, imgsz=256, batch=32)
    
    print(f"\n--- Métricas de Segmentação (Val Set) ---")
    print(f"  mAP50 (seg):  {metrics.seg.map50:.4f}")
    print(f"  mAP50-95 (seg): {metrics.seg.map:.4f}")
    print(f"  mAP50 (box):  {metrics.box.map50:.4f}")
    
    # Per-class
    if hasattr(metrics.seg, 'ap_class_index'):
        names = {0: 'epithelium', 1: 'stroma', 2: 'endothelium'}
        for i, idx in enumerate(metrics.seg.ap_class_index):
            print(f"  AP50 {names.get(int(idx), idx)}: {metrics.seg.ap50[i]:.4f}")
