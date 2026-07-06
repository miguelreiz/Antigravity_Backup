import fitz, easyocr, numpy as np, re, time, csv, os, sys
from pathlib import Path

# Unbuffer output
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

PRESBYCOR_DIR = Path(r"D:\Antigravity\Presbycor arquivos de pacientes")
OUTPUT_DIR = Path(r"C:\Users\3D_OCT\Documents\Antigravity\Presbycor")
CSV_PATH = OUTPUT_DIR / "Presbycor_Database_Completo.csv"
DPI = 200

print("Initializing EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)
print("Ready.")

def get_base_name(f): return re.sub(r"\s*\(\d+\)\s*$", "", Path(f).stem).strip().lower()

all_pdfs = list(PRESBYCOR_DIR.glob("**/*.pdf"))
if Path(r"D:\Downloads Comet").exists():
    all_pdfs.extend(Path(r"D:\Downloads Comet").glob("strategy_*.pdf"))
pdf_map = {get_base_name(p): p for p in all_pdfs}

print("Reading CSV...")
with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
    records = list(csv.DictReader(f))

updated = 0
t0 = time.time()

for i, rec in enumerate(records):
    source = rec.get("Source File")
    if not source: continue
    
    bname = get_base_name(source)
    if bname not in pdf_map:
        continue
        
    pdf_path = pdf_map[bname]
    
    try:
        doc = fitz.open(str(pdf_path))
        page = doc[0]
        mat = fitz.Matrix(DPI/72, DPI/72)
        # Crop exactly the thin strip where Dominant Eye is located (y=410 to y=440)
        # 1653 is width of A4 at 200 DPI, height doesn't matter we just take a Rect
        rect = fitz.Rect(0, 410, 1654, 450)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB, clip=rect)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
        doc.close()
        
        # OCR the thin strip
        res = reader.readtext(img, detail=1, paragraph=False)
        tokens = []
        for bbox, text, conf in res:
            xc = (bbox[0][0]+bbox[2][0])/2
            tokens.append((xc, str(text).strip().lower()))
        
        tokens.sort(key=lambda t: t[0])
        
        od_dominant = ""
        os_dominant = ""
        
        # First "yes/no" is OD, second is OS (usually around x=776 and x=1566)
        for xc, t in tokens:
            if t in ["yes", "no"]:
                if xc < 1000:
                    od_dominant = t
                else:
                    os_dominant = t
                    
        rec["OD Dominant"] = od_dominant
        rec["OS Dominant"] = os_dominant
        updated += 1
        
        if (i+1) % 50 == 0:
            print(f"[{i+1}/{len(records)}] Processed...")
            
    except Exception as e:
        print(f"[{i+1}/{len(records)}] Error {source}: {e}")

with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

print(f"Finished updating {updated} records for Dominant Eye in {(time.time()-t0):.1f}s!")
