import fitz, easyocr, numpy as np, re, time, csv
from pathlib import Path
import traceback
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
import os
os.environ['PYTHONUNBUFFERED'] = '1'

PRESBYCOR_DIR = Path(r"D:\Antigravity\Presbycor arquivos de pacientes")
OUTPUT_DIR = Path(r"C:\Users\3D_OCT\Documents\Antigravity\Presbycor")
CSV_PATH = OUTPUT_DIR / "Presbycor_Database_Completo.csv"
DPI = 200

print("Initializing EasyOCR...", flush=True)
reader = easyocr.Reader(['en'], gpu=False, verbose=False)
print("Ready.", flush=True)

def get_base_name(f): return re.sub(r"\s*\(\d+\)\s*$", "", Path(f).stem).strip().lower()

all_pdfs = list(PRESBYCOR_DIR.glob("**/*.pdf"))
if Path(r"D:\Downloads Comet").exists():
    all_pdfs.extend(Path(r"D:\Downloads Comet").glob("strategy_*.pdf"))
pdf_map = {get_base_name(p): p for p in all_pdfs}

def extract_from_merged(token, pattern):
    pat = re.compile(pattern, re.I)
    m = pat.search(token)
    if m:
        rest = token[m.end():]
        nm = re.search(r"[+-]?\d+[.,]\d+", rest)
        if nm: return nm.group().replace(",",".")
        nm = re.search(r"\d+[.,]\d+", rest)
        if nm: return nm.group().replace(",",".")
        nm = re.search(r"[+-]?\d+", rest)
        if nm: return nm.group()
    return ""

def find_after(words, pat_str):
    pat = re.compile(pat_str, re.I)
    for i, (y, x, t) in enumerate(words):
        if pat.search(t):
            for j in range(i+1, min(i+5, len(words))):
                if words[j][1] > x and words[j][1] - x < 250:
                    return words[j][2]
    return ""

def parse_section(tokens, header_y, eye="od"):
    ref_tokens = [t for t in tokens if header_y + 30 < t[0] < header_y + 130]
    oz_tokens = [t for t in tokens if header_y + 220 < t[0] < header_y + 350]
    
    res = {}
    for y, x, t in ref_tokens:
        if re.search(r"^spher", t, re.I):
            v = extract_from_merged(t, r"^spher")
            if v: res["sphere"] = v; break
    if "sphere" not in res:
        v = find_after(ref_tokens, r"^spher")
        nm = re.search(r"[+-]?\d+[.,]\d+", v)
        if nm: res["sphere"] = nm.group().replace(",", ".")
            
    for y, x, t in ref_tokens:
        if re.search(r"^cyl", t, re.I):
            v = extract_from_merged(t, r"^cyl")
            if v: res["cylinder"] = v; break
    if "cylinder" not in res:
        v = find_after(ref_tokens, r"^cyl")
        nm = re.search(r"[+-]?\d+[.,]\d+", v)
        if nm: res["cylinder"] = nm.group().replace(",", ".")
            
    for y, x, t in oz_tokens:
        if re.search(r"target", t, re.I):
            v = extract_from_merged(t, r"target\s*")
            if v: res["q_target"] = v; break
    if "q_target" not in res:
        v = find_after(oz_tokens, r"target")
        nm = re.search(r"[+-]?\d+[.,]\d+", v)
        if nm: res["q_target"] = nm.group().replace(",", ".")

    for y, x, t in oz_tokens:
        if re.search(r"optical|^oz$|^zone$", t, re.I):
            v = extract_from_merged(t, r"(optical|zone)\s*")
            if v: res["optical_zone"] = v; break
    if "optical_zone" not in res:
        v = find_after(oz_tokens, r"optical|zone")
        nm = re.search(r"\d+[.,]\d+", v)
        if nm: res["optical_zone"] = nm.group().replace(",", ".")
            
    return res

print("Reading CSV...", flush=True)
with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
    records = list(csv.DictReader(f))

# Clear bad extracted data from previous run
for rec in records:
    for k in rec.keys():
        if "Equi " in k or "Dual " in k or "Mono " in k:
            if k.endswith("(D)") or k.endswith("Q Target") or k.endswith("OZ (mm)"):
                rec[k] = ""

updated = 0
t0 = time.time()
times = []

# Process ALL to ensure they get correct values
to_process = records

print(f"Reprocessing {len(to_process)} records for Target Data (fixed sort)...", flush=True)

for i, rec in enumerate(to_process):
    t_f = time.time()
    source = rec.get("Source File")
    if not source: continue
    
    bname = get_base_name(source)
    if bname not in pdf_map:
        print(f"[{i+1}/{len(to_process)}] PDF not found: {source}", flush=True)
        continue
        
    pdf_path = pdf_map[bname]
    
    try:
        doc = fitz.open(str(pdf_path))
        page = doc[0]
        mat = fitz.Matrix(DPI/72, DPI/72)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
        doc.close()
        
        # OCR left half (OD)
        res_od = reader.readtext(img[:, :826], detail=1, paragraph=False)
        tokens_od = []
        for bbox, text, conf in res_od:
            xc = (bbox[0][0]+bbox[2][0])/2
            yc = (bbox[0][1]+bbox[2][1])/2
            tokens_od.append((yc, xc, str(text).strip()))
        # Sort by row (15px bins) then by X
        tokens_od.sort(key=lambda t: (int(t[0]) // 15, t[1]))
        
        # OCR right half (OS)
        res_os = reader.readtext(img[:, 826:], detail=1, paragraph=False)
        tokens_os = []
        for bbox, text, conf in res_os:
            xc = (bbox[0][0]+bbox[2][0])/2 + 826
            yc = (bbox[0][1]+bbox[2][1])/2
            tokens_os.append((yc, xc, str(text).strip()))
        tokens_os.sort(key=lambda t: (int(t[0]) // 15, t[1]))
        
        headers_od = {}; headers_os = {}
        for y, x, t in tokens_od:
            tl = t.lower()
            if "equi" in tl: headers_od["equi"] = y
            elif "dual" in tl: headers_od["dual"] = y
            elif "mono" in tl: headers_od["mono"] = y
        for y, x, t in tokens_os:
            tl = t.lower()
            if "equi" in tl: headers_os["equi"] = y
            elif "dual" in tl: headers_os["dual"] = y
            elif "mono" in tl: headers_os["mono"] = y
            
        for sec in ["equi", "dual", "mono"]:
            if sec in headers_od:
                res = parse_section(tokens_od, headers_od[sec], "od")
                prefix = f"OD {sec.capitalize()}"
                if "sphere" in res: rec[f"{prefix} Sphere (D)"] = res["sphere"]
                if "cylinder" in res: rec[f"{prefix} Cylinder (D)"] = res["cylinder"]
                if "q_target" in res: rec[f"{prefix} Q Target"] = res["q_target"]
                if "optical_zone" in res: rec[f"{prefix} OZ (mm)"] = res["optical_zone"]
            if sec in headers_os:
                res = parse_section(tokens_os, headers_os[sec], "os")
                prefix = f"OS {sec.capitalize()}"
                if "sphere" in res: rec[f"{prefix} Sphere (D)"] = res["sphere"]
                if "cylinder" in res: rec[f"{prefix} Cylinder (D)"] = res["cylinder"]
                if "q_target" in res: rec[f"{prefix} Q Target"] = res["q_target"]
                if "optical_zone" in res: rec[f"{prefix} OZ (mm)"] = res["optical_zone"]
                
        updated += 1
        elapsed = time.time() - t_f
        times.append(elapsed)
        eta = sum(times)/len(times) * (len(to_process)-i-1) / 60
        print(f"[{i+1}/{len(to_process)}] {source} | Updated | {elapsed:.1f}s | ETA: {eta:.1f}m", flush=True)
        
        if (i+1) % 10 == 0:
            with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
            print("  -> CSV Checkpoint saved.", flush=True)
            
    except Exception as e:
        print(f"[{i+1}/{len(to_process)}] Error {source}: {e}", flush=True)

with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

print(f"Finished fixing {updated} records in {(time.time()-t0)/60:.1f}m!", flush=True)
