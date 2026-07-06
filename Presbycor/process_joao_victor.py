import fitz, easyocr, numpy as np, re, time, csv
from pathlib import Path
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
os.environ['PYTHONUNBUFFERED'] = '1'

JOAO_VICTOR_DIR = Path(r"D:\Antigravity\Presbycor arquivos de pacientes\joao Victor")
CSV_PATH = Path(r"C:\Users\3D_OCT\Documents\Antigravity\Presbycor\Presbycor_Database_Completo.csv")
DPI = 200

print("Initializing EasyOCR...", flush=True)
reader = easyocr.Reader(['en'], gpu=False, verbose=False)
print("Ready.", flush=True)

def get_base_name(f): return re.sub(r"\s*\(\d+\)\s*$", "", Path(f).stem).strip().lower()

# Read existing CSV to get already processed files
print("Loading existing CSV...", flush=True)
with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
    existing_records = list(csv.DictReader(f))
    
existing_bases = {get_base_name(r.get("Source File", "")) for r in existing_records}

# Get new files and deduplicate
all_new_pdfs = list(JOAO_VICTOR_DIR.glob("**/*.pdf"))
pdf_map = {}
for p in all_new_pdfs:
    base = get_base_name(p)
    if base not in existing_bases:
        pdf_map[base] = p

to_process = list(pdf_map.values())
print(f"Found {len(all_new_pdfs)} files in joao Victor folder.")
print(f"After deduplication and skipping already processed, {len(to_process)} new unique files to process.")

# --- Helper functions from previous scripts ---
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

def parse_pre_op_section(tokens, header_y):
    res = {}
    tokens_sec = [t for t in tokens if header_y + 30 < t[0] < header_y + 350]
    
    mapping = {
        "sphere": r"^spher",
        "cylinder": r"^cyl",
        "axis": r"^axis",
        "k1": r"^k1",
        "k1_axis": r"axis", # Need context for K1 axis
        "k2": r"^k2",
        "ecc_e": r"ecc",
        "asph_q": r"asphericity",
        "pupillo": r"pupillo",
        "pachy": r"pachy",
        "min_add": r"add",
        "vd": r"vd",
        "cdva": r"cdva",
        "cnva": r"cnva"
    }
    
    for y, x, t in tokens_sec:
        tl = t.lower()
        if "spher" in tl and "sphere" not in res:
            res["sphere"] = extract_from_merged(t, r"spher") or find_after(tokens_sec, r"^spher")
        elif "cyl" in tl and "cylinder" not in res:
            res["cylinder"] = extract_from_merged(t, r"cyl") or find_after(tokens_sec, r"^cyl")
        elif "vd" in tl and "vd" not in res:
            res["vd"] = extract_from_merged(t, r"vd") or find_after(tokens_sec, r"vd")
        elif "k1" in tl and "k1" not in res:
            res["k1"] = extract_from_merged(t, r"k1") or find_after(tokens_sec, r"k1")
        elif "k2" in tl and "k2" not in res:
            res["k2"] = extract_from_merged(t, r"k2") or find_after(tokens_sec, r"k2")
        elif "eccent" in tl and "ecc_e" not in res:
            res["ecc_e"] = extract_from_merged(t, r"ecc") or find_after(tokens_sec, r"eccent")
        elif "asphericity" in tl and "asph_q" not in res:
            res["asph_q"] = extract_from_merged(t, r"asph") or find_after(tokens_sec, r"asph")
        elif "pupillom" in tl and "pupillo" not in res:
            res["pupillo"] = extract_from_merged(t, r"pupillo") or find_after(tokens_sec, r"pupillom")
        elif "pachym" in tl and "pachy" not in res:
            res["pachy"] = extract_from_merged(t, r"pachy") or find_after(tokens_sec, r"pachym")
        elif "min" in tl and "add" in tl and "min_add" not in res:
            res["min_add"] = extract_from_merged(t, r"add") or find_after(tokens_sec, r"add")
        elif "cdva" in tl and "cdva" not in res:
            res["cdva"] = extract_from_merged(t, r"cdva") or find_after(tokens_sec, r"cdva")
        elif "cnva" in tl and "cnva" not in res:
            res["cnva"] = extract_from_merged(t, r"cnva") or find_after(tokens_sec, r"cnva")
            
    # Clean extracted values
    for k in res:
        m = re.search(r"([+-]?\d+[.,]\d+)", str(res[k]))
        if m: res[k] = m.group(1).replace(",",".")
        else:
            m = re.search(r"([+-]?\d+)", str(res[k]))
            if m: res[k] = m.group(1)
            else: res[k] = ""
            
    return res

t0 = time.time()
times = []
new_records = []

for i, pdf_path in enumerate(to_process):
    t_f = time.time()
    try:
        doc = fitz.open(str(pdf_path))
        page = doc[0]
        mat = fitz.Matrix(DPI/72, DPI/72)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
        doc.close()
        
        # 1. Extract Patient Info & Dominant Eye
        res_full = reader.readtext(img[:500, :], detail=1, paragraph=False)
        tokens_full = []
        for bbox, text, conf in res_full:
            xc = (bbox[0][0]+bbox[2][0])/2
            yc = (bbox[0][1]+bbox[2][1])/2
            tokens_full.append((yc, xc, str(text).strip()))
        
        patient_name = find_after(tokens_full, r"patient")
        dob = find_after(tokens_full, r"naissance|birth")
        age = find_after(tokens_full, r"age")
        if age: age = re.sub(r"[^\d]", "", age)
        creation = find_after(tokens_full, r"creation")
        surgeon = find_after(tokens_full, r"surgeon")
        
        # Dominant eye
        od_dom = ""
        os_dom = ""
        dom_tokens = [t for t in tokens_full if 410 < t[0] < 450]
        dom_tokens.sort(key=lambda t: t[1])
        for y, x, t in dom_tokens:
            if t.lower() in ["yes", "no"]:
                if x < 1000: od_dom = t.lower()
                else: os_dom = t.lower()
                
        rec = {
            "Source File": pdf_path.name,
            "Patient Name": patient_name,
            "Date of Birth": dob,
            "Age (years)": age,
            "Creation Date": creation,
            "Surgeon": surgeon,
            "OD Dominant": od_dom,
            "OS Dominant": os_dom
        }
        
        # 2. Left / Right OCR
        res_od = reader.readtext(img[:, :826], detail=1, paragraph=False)
        tokens_od = [( (bbox[0][1]+bbox[2][1])/2, (bbox[0][0]+bbox[2][0])/2, str(text).strip() ) for bbox, text, conf in res_od]
        tokens_od.sort(key=lambda t: (int(t[0]) // 15, t[1]))
        
        res_os = reader.readtext(img[:, 826:], detail=1, paragraph=False)
        tokens_os = [( (bbox[0][1]+bbox[2][1])/2, (bbox[0][0]+bbox[2][0])/2 + 826, str(text).strip() ) for bbox, text, conf in res_os]
        tokens_os.sort(key=lambda t: (int(t[0]) // 15, t[1]))
        
        headers_od = {}; headers_os = {}
        for y, x, t in tokens_od:
            tl = t.lower()
            if "pre" in tl and "operative" in tl: headers_od["pre"] = y
            elif "equi" in tl: headers_od["equi"] = y
            elif "dual" in tl: headers_od["dual"] = y
            elif "mono" in tl: headers_od["mono"] = y
        for y, x, t in tokens_os:
            tl = t.lower()
            if "pre" in tl and "operative" in tl: headers_os["pre"] = y
            elif "equi" in tl: headers_os["equi"] = y
            elif "dual" in tl: headers_os["dual"] = y
            elif "mono" in tl: headers_os["mono"] = y
            
        # Parse Pre-Op
        if "pre" in headers_od:
            res = parse_pre_op_section(tokens_od, headers_od["pre"])
            rec["OD Pre Sphere (D)"] = res.get("sphere", "")
            rec["OD Pre Cylinder (D)"] = res.get("cylinder", "")
            rec["OD Pre VD (mm)"] = res.get("vd", "")
            rec["OD Pre K1 (D)"] = res.get("k1", "")
            rec["OD Pre K2 (D)"] = res.get("k2", "")
            rec["OD Pre Ecc E"] = res.get("ecc_e", "")
            rec["OD Pre Asph Q"] = res.get("asph_q", "")
            rec["OD Pre Pupillo (mm)"] = res.get("pupillo", "")
            rec["OD Pre Pachy (um)"] = res.get("pachy", "")
            rec["OD Pre Min Add (D)"] = res.get("min_add", "")
            rec["OD Pre CDVA Log"] = res.get("cdva", "")
            rec["OD Pre CNVA Log"] = res.get("cnva", "")
            
        if "pre" in headers_os:
            res = parse_pre_op_section(tokens_os, headers_os["pre"])
            rec["OS Pre Sphere (D)"] = res.get("sphere", "")
            rec["OS Pre Cylinder (D)"] = res.get("cylinder", "")
            rec["OS Pre VD (mm)"] = res.get("vd", "")
            rec["OS Pre K1 (D)"] = res.get("k1", "")
            rec["OS Pre K2 (D)"] = res.get("k2", "")
            rec["OS Pre Ecc E"] = res.get("ecc_e", "")
            rec["OS Pre Asph Q"] = res.get("asph_q", "")
            rec["OS Pre Pupillo (mm)"] = res.get("pupillo", "")
            rec["OS Pre Pachy (um)"] = res.get("pachy", "")
            rec["OS Pre Min Add (D)"] = res.get("min_add", "")
            rec["OS Pre CDVA Log"] = res.get("cdva", "")
            rec["OS Pre CNVA Log"] = res.get("cnva", "")
            
        # Parse Targets
        for sec in ["equi", "dual", "mono"]:
            if sec in headers_od:
                res = parse_section(tokens_od, headers_od[sec], "od")
                prefix = f"OD {sec.capitalize()}"
                rec[f"{prefix} Sphere (D)"] = res.get("sphere", "")
                rec[f"{prefix} Cylinder (D)"] = res.get("cylinder", "")
                rec[f"{prefix} Q Target"] = res.get("q_target", "")
                rec[f"{prefix} OZ (mm)"] = res.get("optical_zone", "")
            if sec in headers_os:
                res = parse_section(tokens_os, headers_os[sec], "os")
                prefix = f"OS {sec.capitalize()}"
                rec[f"{prefix} Sphere (D)"] = res.get("sphere", "")
                rec[f"{prefix} Cylinder (D)"] = res.get("cylinder", "")
                rec[f"{prefix} Q Target"] = res.get("q_target", "")
                rec[f"{prefix} OZ (mm)"] = res.get("optical_zone", "")

        # Align keys with existing CSV
        final_rec = {k: rec.get(k, "") for k in existing_records[0].keys()}
        new_records.append(final_rec)
        
        elapsed = time.time() - t_f
        times.append(elapsed)
        eta = sum(times)/len(times) * (len(to_process)-i-1) / 60
        print(f"[{i+1}/{len(to_process)}] {pdf_path.name} | {elapsed:.1f}s | ETA: {eta:.1f}m", flush=True)
            
    except Exception as e:
        print(f"[{i+1}/{len(to_process)}] Error {pdf_path.name}: {e}", flush=True)

# Append to CSV
with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=existing_records[0].keys())
    writer.writerows(new_records)

print(f"Finished adding {len(new_records)} new records in {(time.time()-t0)/60:.1f}m!", flush=True)
