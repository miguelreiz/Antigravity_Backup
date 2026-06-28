# -*- coding: utf-8 -*-
"""
CNN Classifier: KC vs Normal from raw Scheimpflug (Pentacam SPR) images
ResNet18 with 5-fold stratified cross-validation
CPU-only training
"""
import warnings
warnings.filterwarnings('ignore')

import sys, os, re, unicodedata, time, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.models as models
import torchvision.transforms as transforms

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_curve, auc, roc_auc_score

# ============================================================
# CONFIG
# ============================================================
SPR_DIR = Path(r"D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP")
CLINICAL_CSV = Path(r"D:\Projetos\Antigravity\Vetores Anel\pentacm\resultados_crossvalidation\matched_pairs_FII_Pentacam.csv")
OUT_DIR = Path(r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch")

IMG_W, IMG_H = 416, 256
PIXELS_PER_SLICE = IMG_W * IMG_H
HEADER_OFFSET = 2048

BATCH_SIZE = 16
EPOCHS = 20
LR = 1e-4
N_FOLDS = 5
N_BOOTSTRAP = 1000
SEED = 42

np.random.seed(SEED)
torch.manual_seed(SEED)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def norm_name(name):
    """Normalize name: remove accents, lowercase, remove prepositions."""
    if not isinstance(name, str):
        return ""
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-z ]', '', s.lower()).strip()
    s = re.sub(r'\s+', ' ', s)
    return s

def name_tokens(name):
    """Get significant tokens (remove common prepositions)."""
    skip = {'de', 'da', 'do', 'dos', 'das', 'e', 'di', 'del'}
    tokens = set(norm_name(name).split()) - skip
    tokens.discard('')
    return frozenset(tokens)

def token_overlap_ratio(t1, t2):
    """Calculate token overlap ratio."""
    if not t1 or not t2:
        return 0.0
    overlap = t1 & t2
    return len(overlap) / min(len(t1), len(t2))

def read_spr_header(filepath):
    """Read patient name from SPR file header."""
    with open(filepath, 'rb') as f:
        hdr = f.read(HEADER_OFFSET)
    # First name at bytes 34-64, Last name at bytes 4-34
    last_name = hdr[4:34].split(b'\x00')[0].decode('latin-1', 'ignore').strip()
    first_name = hdr[34:64].split(b'\x00')[0].decode('latin-1', 'ignore').strip()
    full_name = (first_name + ' ' + last_name).strip()
    return full_name

def read_spr_middle_slice(filepath):
    """Read the middle (temporal) slice from an SPR file."""
    file_size = os.path.getsize(filepath)
    data_size = file_size - HEADER_OFFSET
    n_slices = data_size // PIXELS_PER_SLICE
    if n_slices < 1:
        return None
    mid_slice_idx = n_slices // 2
    offset = HEADER_OFFSET + mid_slice_idx * PIXELS_PER_SLICE
    with open(filepath, 'rb') as f:
        f.seek(offset)
        raw = f.read(PIXELS_PER_SLICE)
    if len(raw) < PIXELS_PER_SLICE:
        return None
    img = np.frombuffer(raw, dtype=np.uint8).reshape(IMG_H, IMG_W)
    return img

# ============================================================
# PHASE 1: Load clinical data
# ============================================================
print("=" * 70)
print("PHASE 1: Loading clinical data")
print("=" * 70)

clinical = pd.read_csv(CLINICAL_CSV, sep=';', encoding='utf-8-sig')
print(f"  Loaded {len(clinical)} matched pairs")
print(f"  Columns: {list(clinical.columns)}")

# Build target: KC=1 if BAD_D >= 1.6 OR Penta_Class != 'Normal'
clinical['BAD_D_num'] = pd.to_numeric(clinical['BAD_D'].astype(str).str.replace(',', '.'), errors='coerce')
clinical['target'] = ((clinical['BAD_D_num'] >= 1.6) | (clinical['Penta_Class'] != 'Normal')).astype(int)

print(f"  Target distribution: {clinical['target'].value_counts().to_dict()}")
print(f"  Penta_Class distribution: {clinical['Penta_Class'].value_counts().to_dict()}")

# Build token index from clinical data (using nome_pentacam)
clinical['tokens_penta'] = clinical['nome_pentacam'].apply(name_tokens)

# De-duplicate: get unique pentacam patients with their labels
# Group by pentacam name tokens - take the worst label (max target)
patient_labels = {}
for _, row in clinical.iterrows():
    tk = row['tokens_penta']
    if len(tk) < 2:
        continue
    key = tk
    if key not in patient_labels:
        patient_labels[key] = row['target']
    else:
        patient_labels[key] = max(patient_labels[key], row['target'])

print(f"  Unique pentacam patients with labels: {len(patient_labels)}")
print(f"    KC (target=1): {sum(1 for v in patient_labels.values() if v == 1)}")
print(f"    Normal (target=0): {sum(1 for v in patient_labels.values() if v == 0)}")

# ============================================================
# PHASE 2: Read SPR files and match with clinical data
# ============================================================
print("\n" + "=" * 70)
print("PHASE 2: Reading SPR files and matching with clinical data")
print("=" * 70)

spr_files = sorted(glob.glob(str(SPR_DIR / "*.SPR")))
print(f"  Found {len(spr_files)} SPR files")

# Read all SPR headers
spr_data = []
for i, fp in enumerate(spr_files):
    name = read_spr_header(fp)
    tokens = name_tokens(name)
    spr_data.append({
        'filepath': fp,
        'name': name,
        'tokens': tokens,
        'filename': os.path.basename(fp)
    })
    if (i + 1) % 100 == 0:
        print(f"  Read {i + 1}/{len(spr_files)} headers...")

print(f"  Read all {len(spr_data)} headers")

# Match SPR files to clinical labels using token overlap
matched = []
unmatched = 0
for spr in spr_data:
    spr_tokens = spr['tokens']
    if len(spr_tokens) < 2:
        unmatched += 1
        continue
    
    best_match = None
    best_overlap = 0
    for clinical_tokens, label in patient_labels.items():
        overlap = token_overlap_ratio(spr_tokens, clinical_tokens)
        if overlap > best_overlap:
            best_overlap = overlap
            best_match = (clinical_tokens, label)
    
    if best_match and best_overlap >= 0.50:
        matched.append({
            'filepath': spr['filepath'],
            'name': spr['name'],
            'spr_tokens': spr_tokens,
            'clinical_tokens': best_match[0],
            'target': best_match[1],
            'overlap': best_overlap,
            'filename': spr['filename']
        })
    else:
        unmatched += 1

print(f"  Matched: {len(matched)} SPR files")
print(f"  Unmatched: {unmatched} SPR files")

# Group by patient for patient-level splitting
patient_groups = defaultdict(list)
for m in matched:
    patient_groups[m['clinical_tokens']].append(m)

print(f"  Unique patients: {len(patient_groups)}")
target_counts = defaultdict(int)
for tk, items in patient_groups.items():
    target_counts[items[0]['target']] += 1
print(f"  Patients KC=1: {target_counts[1]}, Normal=0: {target_counts[0]}")

# ============================================================
# PHASE 3: Read images
# ============================================================
print("\n" + "=" * 70)
print("PHASE 3: Reading images (middle slices)")
print("=" * 70)

images = []
labels = []
patient_ids = []
valid_count = 0

patient_list = list(patient_groups.keys())
patient_label_list = [patient_groups[pk][0]['target'] for pk in patient_list]

for i, (patient_key, items) in enumerate(patient_groups.items()):
    for item in items:
        img = read_spr_middle_slice(item['filepath'])
        if img is not None:
            images.append(img)
            labels.append(item['target'])
            patient_ids.append(patient_key)
            valid_count += 1
    if (i + 1) % 50 == 0:
        print(f"  Processed {i + 1}/{len(patient_groups)} patients ({valid_count} valid images)...")

images = np.array(images)
labels = np.array(labels)
print(f"  Total valid images: {len(images)}")
print(f"  Image shape: {images[0].shape}")
print(f"  Label distribution: KC={np.sum(labels==1)}, Normal={np.sum(labels==0)}")

# ============================================================
# PHASE 4: Build Dataset and Model
# ============================================================
print("\n" + "=" * 70)
print("PHASE 4: Building dataset and model")
print("=" * 70)

class CornealDataset(Dataset):
    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img = self.images[idx].astype(np.float32) / 255.0
        # Resize to 224x224 for ResNet18
        # Use simple numpy resize 
        from PIL import Image
        pil_img = Image.fromarray((img * 255).astype(np.uint8), mode='L')
        pil_img = pil_img.resize((224, 224), Image.BILINEAR)
        img = np.array(pil_img).astype(np.float32) / 255.0
        
        # Convert to tensor: [1, H, W]
        img_tensor = torch.from_numpy(img).unsqueeze(0)
        
        if self.transform:
            img_tensor = self.transform(img_tensor)
        
        label = torch.tensor(self.labels[idx], dtype=torch.float32)
        return img_tensor, label

class RandomFlipTransform:
    def __call__(self, x):
        if torch.rand(1) > 0.5:
            x = torch.flip(x, [-1])  # horizontal flip
        if torch.rand(1) > 0.5:
            x = torch.flip(x, [-2])  # vertical flip
        return x

def build_resnet18_1ch():
    """Build ResNet18 for 1-channel grayscale input, binary classification."""
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    
    # Modify first conv layer: average pretrained RGB weights for 1ch
    old_conv = model.conv1
    new_conv = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    with torch.no_grad():
        new_conv.weight[:] = old_conv.weight.mean(dim=1, keepdim=True)
    model.conv1 = new_conv
    
    # Modify final FC for binary classification (1 output logit)
    model.fc = nn.Linear(model.fc.in_features, 1)
    
    return model

# ============================================================
# PHASE 5: 5-Fold Stratified Cross-Validation
# ============================================================
print("\n" + "=" * 70)
print("PHASE 5: 5-Fold Stratified Cross-Validation (Patient-Level)")
print("=" * 70)

# Create patient-level arrays for splitting
patient_keys = list(patient_groups.keys())
patient_targets = np.array([patient_groups[pk][0]['target'] for pk in patient_keys])

# Map each image to its patient index
image_patient_idx = []
for pid in patient_ids:
    idx = patient_keys.index(pid)
    image_patient_idx.append(idx)
image_patient_idx = np.array(image_patient_idx)

skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)

all_fold_aucs = []
all_val_probs = []
all_val_labels = []
fold_results = []

total_start = time.time()

for fold, (train_pat_idx, val_pat_idx) in enumerate(skf.split(patient_keys, patient_targets)):
    print(f"\n--- FOLD {fold + 1}/{N_FOLDS} ---")
    fold_start = time.time()
    
    # Get image indices for train and val patients
    train_mask = np.isin(image_patient_idx, train_pat_idx)
    val_mask = np.isin(image_patient_idx, val_pat_idx)
    
    train_images = images[train_mask]
    train_labels = labels[train_mask]
    val_images = images[val_mask]
    val_labels = labels[val_mask]
    
    print(f"  Train: {len(train_images)} images (KC={np.sum(train_labels==1)}, N={np.sum(train_labels==0)})")
    print(f"  Val:   {len(val_images)} images (KC={np.sum(val_labels==1)}, N={np.sum(val_labels==0)})")
    
    # Handle class imbalance with pos_weight
    n_pos = np.sum(train_labels == 1)
    n_neg = np.sum(train_labels == 0)
    pos_weight = torch.tensor([n_neg / max(n_pos, 1)], dtype=torch.float32)
    print(f"  Pos weight: {pos_weight.item():.2f}")
    
    # Create datasets
    train_ds = CornealDataset(train_images, train_labels, transform=RandomFlipTransform())
    val_ds = CornealDataset(val_images, val_labels, transform=None)
    
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, 
                              num_workers=0, pin_memory=False)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False,
                            num_workers=0, pin_memory=False)
    
    # Build model
    model = build_resnet18_1ch()
    model.train()
    
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)
    
    # Training loop
    best_val_auc = 0.0
    best_model_state = None
    
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0
        n_batches = 0
        
        for batch_imgs, batch_labels in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_imgs).squeeze(-1)
            loss = criterion(outputs, batch_labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            n_batches += 1
        
        scheduler.step()
        
        # Validation
        model.eval()
        val_probs = []
        val_true = []
        val_loss = 0
        n_val_batches = 0
        
        with torch.no_grad():
            for batch_imgs, batch_labels in val_loader:
                outputs = model(batch_imgs).squeeze(-1)
                loss = criterion(outputs, batch_labels)
                val_loss += loss.item()
                n_val_batches += 1
                probs = torch.sigmoid(outputs).numpy()
                val_probs.extend(probs)
                val_true.extend(batch_labels.numpy())
        
        val_probs_arr = np.array(val_probs)
        val_true_arr = np.array(val_true)
        
        # Calculate AUC
        if len(np.unique(val_true_arr)) > 1:
            val_auc = roc_auc_score(val_true_arr, val_probs_arr)
        else:
            val_auc = 0.5
        
        if val_auc > best_val_auc:
            best_val_auc = val_auc
            best_model_state = {k: v.clone() for k, v in model.state_dict().items()}
        
        avg_train_loss = train_loss / max(n_batches, 1)
        avg_val_loss = val_loss / max(n_val_batches, 1)
        
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  Epoch {epoch+1:2d}/{EPOCHS}: "
                  f"TrainLoss={avg_train_loss:.4f} "
                  f"ValLoss={avg_val_loss:.4f} "
                  f"ValAUC={val_auc:.4f} "
                  f"BestAUC={best_val_auc:.4f}")
    
    # Final evaluation with best model
    model.load_state_dict(best_model_state)
    model.eval()
    
    final_probs = []
    final_true = []
    with torch.no_grad():
        for batch_imgs, batch_labels in val_loader:
            outputs = model(batch_imgs).squeeze(-1)
            probs = torch.sigmoid(outputs).numpy()
            final_probs.extend(probs)
            final_true.extend(batch_labels.numpy())
    
    final_probs = np.array(final_probs)
    final_true = np.array(final_true)
    
    if len(np.unique(final_true)) > 1:
        fold_auc = roc_auc_score(final_true, final_probs)
    else:
        fold_auc = 0.5
    
    fold_time = time.time() - fold_start
    print(f"  FOLD {fold + 1} RESULT: AUC = {fold_auc:.4f} (time: {fold_time:.0f}s)")
    
    all_fold_aucs.append(fold_auc)
    all_val_probs.extend(final_probs)
    all_val_labels.extend(final_true)
    fold_results.append({
        'fold': fold + 1,
        'auc': fold_auc,
        'n_train': len(train_images),
        'n_val': len(val_images),
        'time_sec': fold_time
    })

total_time = time.time() - total_start

# ============================================================
# PHASE 6: Results and Bootstrap CI
# ============================================================
print("\n" + "=" * 70)
print("PHASE 6: Results and Bootstrap CI")
print("=" * 70)

all_val_probs = np.array(all_val_probs)
all_val_labels = np.array(all_val_labels)

# Overall AUC from pooled predictions
if len(np.unique(all_val_labels)) > 1:
    overall_auc = roc_auc_score(all_val_labels, all_val_probs)
else:
    overall_auc = 0.5

mean_fold_auc = np.mean(all_fold_aucs)
std_fold_auc = np.std(all_fold_aucs)

print(f"\n  Per-fold AUCs: {[f'{a:.4f}' for a in all_fold_aucs]}")
print(f"  Mean Fold AUC: {mean_fold_auc:.4f} +/- {std_fold_auc:.4f}")
print(f"  Pooled AUC:    {overall_auc:.4f}")

# Bootstrap 95% CI
bootstrap_aucs = []
rng = np.random.RandomState(SEED)
for _ in range(N_BOOTSTRAP):
    idx = rng.randint(0, len(all_val_labels), size=len(all_val_labels))
    if len(np.unique(all_val_labels[idx])) > 1:
        b_auc = roc_auc_score(all_val_labels[idx], all_val_probs[idx])
        bootstrap_aucs.append(b_auc)

bootstrap_aucs = np.array(bootstrap_aucs)
ci_lower = np.percentile(bootstrap_aucs, 2.5)
ci_upper = np.percentile(bootstrap_aucs, 97.5)

print(f"\n  Bootstrap 95% CI ({N_BOOTSTRAP} iters): [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"  GLCM Baseline AUC: 0.676")
print(f"  CNN vs GLCM: {'BETTER' if overall_auc > 0.676 else 'WORSE'} "
      f"(Delta = {overall_auc - 0.676:+.4f})")

# ============================================================
# PHASE 7: ROC Curve Plot
# ============================================================
print("\n" + "=" * 70)
print("PHASE 7: Generating ROC curve")
print("=" * 70)

fpr, tpr, thresholds = roc_curve(all_val_labels, all_val_probs)

fig, ax = plt.subplots(1, 1, figsize=(8, 7))

# Plot CNN ROC
ax.plot(fpr, tpr, 'b-', lw=2.5, 
        label=f'ResNet18 CNN (AUC={overall_auc:.3f}, CI=[{ci_lower:.3f},{ci_upper:.3f}])')

# Plot GLCM reference
ax.axhline(y=0, color='gray', alpha=0)  # dummy for spacing
ax.plot([0, 0.324, 1], [0, 0.676, 1], 'r--', lw=1.5, alpha=0.7,
        label=f'GLCM Radiomics Baseline (AUC=0.676)')

# Diagonal
ax.plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5, label='Random (AUC=0.500)')

# Styling
ax.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=13)
ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=13)
ax.set_title('ROC: CNN (ResNet18) vs GLCM Radiomics\n'
             'Keratoconus Detection from Scheimpflug Images\n'
             f'5-Fold CV, N={len(all_val_labels)} images', fontsize=14, fontweight='bold')
ax.legend(loc='lower right', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_xlim([-0.02, 1.02])
ax.set_ylim([-0.02, 1.02])

# Add text box with summary
textstr = (f'Mean Fold AUC: {mean_fold_auc:.3f} ± {std_fold_auc:.3f}\n'
           f'Pooled AUC: {overall_auc:.3f}\n'
           f'Bootstrap 95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]\n'
           f'Training: {EPOCHS} epochs, CPU\n'
           f'Total time: {total_time:.0f}s')
ax.text(0.55, 0.25, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
roc_path = OUT_DIR / 'ROC_CNN_ResNet18_KC.png'
plt.savefig(roc_path, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f"  ROC curve saved: {roc_path}")

# ============================================================
# PHASE 8: Save results CSV
# ============================================================
results_df = pd.DataFrame(fold_results)
results_df.loc[len(results_df)] = {
    'fold': 'MEAN',
    'auc': mean_fold_auc,
    'n_train': '-',
    'n_val': '-',
    'time_sec': total_time
}
results_df.loc[len(results_df)] = {
    'fold': 'POOLED',
    'auc': overall_auc,
    'n_train': '-',
    'n_val': len(all_val_labels),
    'time_sec': '-'
}
results_df.loc[len(results_df)] = {
    'fold': 'CI_LOWER',
    'auc': ci_lower,
    'n_train': '-',
    'n_val': '-',
    'time_sec': '-'
}
results_df.loc[len(results_df)] = {
    'fold': 'CI_UPPER',
    'auc': ci_upper,
    'n_train': '-',
    'n_val': '-',
    'time_sec': '-'
}
results_df.loc[len(results_df)] = {
    'fold': 'GLCM_BASELINE',
    'auc': 0.676,
    'n_train': '-',
    'n_val': '-',
    'time_sec': '-'
}

csv_path = OUT_DIR / 'cnn_classifier_results.csv'
results_df.to_csv(csv_path, index=False, sep=';')
print(f"  Results CSV saved: {csv_path}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print(f"  Model: ResNet18 (pretrained, 1ch grayscale)")
print(f"  Task: KC vs Normal binary classification")
print(f"  Data: {len(images)} images from {len(patient_groups)} patients")
print(f"  Cross-validation: {N_FOLDS}-fold stratified (patient-level)")
print(f"  Training: {EPOCHS} epochs, batch_size={BATCH_SIZE}, lr={LR}")
print(f"  Total time: {total_time:.0f}s ({total_time/60:.1f} min)")
print()
print(f"  >>> CNN AUC (Pooled):     {overall_auc:.4f}")
print(f"  >>> CNN AUC (Mean±Std):   {mean_fold_auc:.4f} ± {std_fold_auc:.4f}")
print(f"  >>> Bootstrap 95% CI:     [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"  >>> GLCM Baseline AUC:    0.6760")
print(f"  >>> Delta (CNN - GLCM):   {overall_auc - 0.676:+.4f}")
print(f"  >>> CNN {'OUTPERFORMS' if overall_auc > 0.676 else 'UNDERPERFORMS'} GLCM")
print("=" * 70)
print("DONE!")
