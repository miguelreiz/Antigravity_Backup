import os
import re
import pathlib
import shutil
import subprocess

# Paths
WORKSPACE = r"c:\Users\3D_OCT\Documents\Antigravity\Ice"
DEST_DIR = r"D:\ICE_Apresentacao"

pathlib.Path(WORKSPACE).mkdir(parents=True, exist_ok=True)
pathlib.Path(DEST_DIR).mkdir(parents=True, exist_ok=True)

CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Files to map
# We will read from the existing Ambrossio files, replace content, and write to the new Paulo files.
FILE_MAPPING = {
    "apresentacao_ice_ambrosio.html": "apresentacao_ice_paulo.html",
    "ICE_Projeto_Pesquisa_Ambrosio.html": "ICE_Projeto_Pesquisa_Paulo.html",
    "ICE_Projeto_Pesquisa_Ambrosio.md": "ICE_Projeto_Pesquisa_Paulo.md",
    "ICE_Projeto_Pesquisa_Ambrosio.txt": "ICE_Projeto_Pesquisa_Paulo.txt",
}

def perform_replacements(text):
    # Replacements to redirect the project to Dr. Paulo Ferrara
    replacements = {
        # Full name & Title
        r"Prof\. Dr\. Renato Ambrósio Jr\.": "Dr. Paulo Ferrara",
        r"Prof\. Renato Ambrósio": "Dr. Paulo Ferrara",
        r"Dr\. Renato Ambrósio": "Dr. Paulo Ferrara",
        r"Dr\. Renato": "Dr. Paulo Ferrara",
        r"Renato Ambrósio": "Paulo Ferrara",
        
        # Short / possessive references
        r"Prof\. Ambrósio": "Dr. Paulo Ferrara",
        r"ao Prof\. Ambrósio": "ao Dr. Paulo Ferrara",
        r"do Prof\. Ambrósio": "do Dr. Paulo Ferrara",
        r"como o grupo BrAIn aplica": "como se aplica",
        r"do grupo BrAIn": "de validação",
        r"BrAIn / Prof\. Ambrósio": "Dr. Paulo Ferrara",
        
        # Institution and Location
        r"BrAIn / Rio de Janeiro": "Ferrara Clinic / Belo Horizonte",
        r"BrAIn — Rio de Janeiro": "Ferrara Clinic — Belo Horizonte",
        r"BrAIn": "Ferrara Clinic",
        r"Rio de Janeiro": "Belo Horizonte",
        
        # Specific mentions of Ambrósio's indices when referencing them as his group's TBI/BAD-D
        r"Acesso à base de dados do TBI e BAD-D": "Acesso à base de dados clínicos de ceratocone",
        r"base de dados do TBI e BAD-D": "base de dados clínicos",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    return text

# First, process and create the new files in WORKSPACE
for src_name, dst_name in FILE_MAPPING.items():
    src_path = os.path.join(WORKSPACE, src_name)
    dst_path = os.path.join(WORKSPACE, dst_name)
    
    if os.path.exists(src_path):
        print(f"Lendo {src_path} e gerando {dst_path} com referências ao Dr. Paulo Ferrara")
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        updated_content = perform_replacements(content)
        
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
    else:
        print(f"Aviso: arquivo de origem {src_path} não encontrado.")

# Generate PDFs for the new files
def generate_pdf(html_path, pdf_path):
    if not os.path.exists(CHROME):
        print(f"Chrome não encontrado em {CHROME}")
        return False
    html_url = pathlib.Path(html_path).as_uri()
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-dev-shm-usage",
        "--run-all-compositor-stages-before-draw",
        "--font-render-hinting=none",
        "--disable-web-security",
        "--allow-file-access-from-files",
        f"--print-to-pdf={pdf_path}",
        "--print-to-pdf-no-header",
        "--no-margins",
        "--virtual-time-budget=8000",
        html_url
    ]
    print(f"Executando Chrome headless para gerar PDF: {pdf_path}")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if res.returncode == 0 and os.path.exists(pdf_path):
        print(f"PDF gerado com sucesso: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
        return True
    else:
        print(f"Erro ao gerar PDF: {res.returncode}")
        print(res.stderr)
        return False

PROJ_HTML = os.path.join(WORKSPACE, "ICE_Projeto_Pesquisa_Paulo.html")
PROJ_PDF = os.path.join(WORKSPACE, "ICE_Projeto_Pesquisa_Paulo.pdf")
APRES_HTML = os.path.join(WORKSPACE, "apresentacao_ice_paulo.html")
APRES_PDF = os.path.join(WORKSPACE, "ICE_Apresentacao_Paulo.pdf")

generate_pdf(PROJ_HTML, PROJ_PDF)
generate_pdf(APRES_HTML, APRES_PDF)

# Copy all new files to D:\ICE_Apresentacao
new_files = [
    "apresentacao_ice_paulo.html",
    "ICE_Apresentacao_Paulo.pdf",
    "ICE_Projeto_Pesquisa_Paulo.html",
    "ICE_Projeto_Pesquisa_Paulo.pdf",
    "ICE_Projeto_Pesquisa_Paulo.md",
    "ICE_Projeto_Pesquisa_Paulo.txt"
]

for filename in new_files:
    src = os.path.join(WORKSPACE, filename)
    dst = os.path.join(DEST_DIR, filename)
    if os.path.exists(src):
        print(f"Copiando {filename} para {dst}")
        shutil.copy2(src, dst)

# Optional: Clean up old Ambrosio files in the D drive to avoid confusion if necessary, 
# or just let them be. The user can see both or delete them. We will keep them for safety.

print("Processo concluído com sucesso!")
