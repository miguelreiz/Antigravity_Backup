import glob, os

files = sorted(glob.glob(r'D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP\*.SPR'))
print(f"Total SPR files: {len(files)}")

for fp in files[:15]:
    with open(fp, 'rb') as f:
        hdr = f.read(200)
    name1 = hdr[4:34].split(b'\x00')[0].decode('latin-1', 'ignore').strip()
    name2 = hdr[34:64].split(b'\x00')[0].decode('latin-1', 'ignore').strip()
    dob = hdr[64:94].split(b'\x00')[0].decode('latin-1', 'ignore').strip()
    full = (name2 + ' ' + name1).strip() if name2 else name1
    print(f"{os.path.basename(fp):20s} -> [{name1:30s}] [{name2:20s}] DOB:[{dob}] FULL:[{full}]")
