"""
YOLOv11-seg cornea segmentation — 50-epoch CPU retraining
Resumes from previous best weights and trains 50 more epochs.
"""
import warnings
warnings.filterwarnings('ignore')

import os, sys, time, datetime

# ── paths ──────────────────────────────────────────────────────────────
WEIGHTS  = r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\yolo_cornea_dataset\runs\cornea_seg_cpu\weights\best.pt"
DATA     = r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\yolo_cornea_dataset\dataset.yaml"
PROJECT  = r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\yolo_cornea_dataset\runs"
RUN_NAME = "cornea_seg_50ep"

# ── sanity checks ─────────────────────────────────────────────────────
for p in (WEIGHTS, DATA):
    if not os.path.exists(p):
        sys.exit(f"ERROR: not found → {p}")

print(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] Starting training")
print(f"  Weights : {WEIGHTS}")
print(f"  Dataset : {DATA}")
print(f"  Project : {PROJECT}/{RUN_NAME}")
print(f"  Device  : cpu")
print()

# ── train ──────────────────────────────────────────────────────────────
from ultralytics import YOLO

model = YOLO(WEIGHTS, task="segment")

t0 = time.time()

results = model.train(
    data=DATA,
    epochs=50,
    imgsz=256,
    batch=32,
    fraction=0.3,
    patience=15,
    device="cpu",
    workers=0,
    project=PROJECT,
    name=RUN_NAME,
    exist_ok=True,
    # augmentation
    mosaic=0.0,
    flipud=0.5,
    fliplr=0.5,
    degrees=0.0,
    # misc
    verbose=True,
    plots=True,
    save=True,
    save_period=10,          # checkpoint every 10 epochs
)

elapsed = time.time() - t0
print(f"\n{'='*60}")
print(f"Training finished in {datetime.timedelta(seconds=int(elapsed))}")
print(f"{'='*60}\n")

# ── validation ─────────────────────────────────────────────────────────
best_wt = os.path.join(PROJECT, RUN_NAME, "weights", "best.pt")
if not os.path.exists(best_wt):
    best_wt = WEIGHTS  # fallback

print(f"Running validation with: {best_wt}")
val_model = YOLO(best_wt, task="segment")
metrics = val_model.val(
    data=DATA,
    imgsz=256,
    batch=32,
    device="cpu",
    workers=0,
    plots=True,
    project=PROJECT,
    name=f"{RUN_NAME}_val",
    exist_ok=True,
)

# ── per-class metrics ─────────────────────────────────────────────────
class_names = {0: "epithelium", 1: "stroma", 2: "endothelium"}

print(f"\n{'='*60}")
print("Per-class segmentation metrics (mask)")
print(f"{'='*60}")
print(f"{'Class':<15} {'mAP50':>8} {'mAP50-95':>10} {'Precision':>10} {'Recall':>8}")
print("-" * 55)

# Box metrics
box = metrics.box
# Mask metrics
seg = metrics.seg

for i, name in class_names.items():
    try:
        mp  = seg.class_result(i)[0]  # precision
        mr  = seg.class_result(i)[1]  # recall
        m50 = seg.class_result(i)[2]  # mAP50
        m95 = seg.class_result(i)[3]  # mAP50-95
        print(f"{name:<15} {m50:>8.4f} {m95:>10.4f} {mp:>10.4f} {mr:>8.4f}")
    except Exception as e:
        print(f"{name:<15}  -- error: {e}")

print("-" * 55)
print(f"{'ALL (mask)':<15} {seg.map50:>8.4f} {seg.map:>10.4f}")
print()

print(f"\n{'='*60}")
print("Per-class detection metrics (box)")
print(f"{'='*60}")
print(f"{'Class':<15} {'mAP50':>8} {'mAP50-95':>10} {'Precision':>10} {'Recall':>8}")
print("-" * 55)
for i, name in class_names.items():
    try:
        bp  = box.class_result(i)[0]
        br  = box.class_result(i)[1]
        b50 = box.class_result(i)[2]
        b95 = box.class_result(i)[3]
        print(f"{name:<15} {b50:>8.4f} {b95:>10.4f} {bp:>10.4f} {br:>8.4f}")
    except Exception as e:
        print(f"{name:<15}  -- error: {e}")

print("-" * 55)
print(f"{'ALL (box)':<15} {box.map50:>8.4f} {box.map:>10.4f}")
print()

print(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] Done.")
