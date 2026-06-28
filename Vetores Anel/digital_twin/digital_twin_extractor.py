import os
import glob
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from skimage import feature, filters, measure
import warnings

warnings.filterwarnings('ignore')

spr_dir = r'D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP'
out_dir = r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch"
os.makedirs(out_dir, exist_ok=True)

# 1. Calibração da Escala Geométrica
# A imagem do Pentacam tem 416 pixels de largura.
# Um varredura Scheimpflug típica captura ~14mm de tecido (limbo a limbo).
WIDTH_PIXELS = 416
FOV_MM = 14.0
MM_PER_PIXEL = FOV_MM / float(WIDTH_PIXELS)
print(f"Escala estimada: {MM_PER_PIXEL:.4f} mm/pixel")

def fit_circle(x, y):
    """
    Fit a circle to given x, y points.
    Returns (xc, yc, R)
    """
    def calc_R(xc, yc):
        return np.sqrt((x - xc)**2 + (y - yc)**2)

    def f_2(c):
        Ri = calc_R(*c)
        return Ri - Ri.mean()

    center_estimate = np.mean(x), np.mean(y)
    center, _ = optimize.leastsq(f_2, center_estimate)
    xc, yc = center
    Ri = calc_R(xc, yc)
    R = Ri.mean()
    return xc, yc, R

# 2. Carregar o arquivo .SPR (Pega o primeiro válido)
spr_files = glob.glob(os.path.join(spr_dir, "*.SPR"))
target_file = spr_files[0] # Usar o primeiro da lista
print(f"Lendo Gêmeo Digital do paciente: {os.path.basename(target_file)}")

width = 416
slice_height = 256
pixels_per_slice = width * slice_height
offset = 2048

with open(target_file, 'rb') as f:
    raw_data = f.read()

img_data = raw_data[offset:]
arr = np.frombuffer(img_data, dtype=np.uint8)
num_slices = len(arr) // pixels_per_slice

valid_slices = []
for i in range(num_slices):
    s = arr[i*pixels_per_slice : (i+1)*pixels_per_slice].reshape((slice_height, width))
    if np.mean(s) > 10:
        valid_slices.append(s)

target_slice = valid_slices[len(valid_slices) // 2] # Pega a fatia central
img = target_slice

# 3. Processamento de Imagem (Edge Detection via Column Scan)
img_blur = filters.gaussian(img, sigma=2.0)
thresh = filters.threshold_otsu(img_blur)
binary = img_blur > thresh

ant_points = []
post_points = []

# Scan colunas centrais (ROI)
center_x = width // 2
roi_width = 150
start_col = center_x - roi_width // 2
end_col = center_x + roi_width // 2

for x in range(start_col, end_col):
    col_data = binary[:, x]
    bright_indices = np.where(col_data)[0]
    if len(bright_indices) > 5: # Pelo menos 5 pixels de espessura para ser córnea
        y_ant = bright_indices[0] # Primeiro bright pixel de cima pra baixo
        y_post = bright_indices[-1] # Último bright pixel
        ant_points.append([x, y_ant])
        post_points.append([x, y_post])

ant_points = np.array(ant_points)
post_points = np.array(post_points)

if len(ant_points) < 10:
    print("Falha ao detectar bordas suficientes.")
    exit(1)

# Converter Pixels para MM
# O eixo Y cresce para baixo na imagem. Vamos normalizar para um plano cartesiano real.
x_ant_mm = ant_points[:, 0] * MM_PER_PIXEL
y_ant_mm = -ant_points[:, 1] * MM_PER_PIXEL

x_post_mm = post_points[:, 0] * MM_PER_PIXEL
y_post_mm = -post_points[:, 1] * MM_PER_PIXEL

# 4. Ajuste Matemático (Curve Fitting)
xc_ant, yc_ant, r_ant = fit_circle(x_ant_mm, y_ant_mm)
xc_post, yc_post, r_post = fit_circle(x_post_mm, y_post_mm)

# Achar o apex (ponto mais alto) para calcular a espessura central
apex_idx = np.argmax(y_ant_mm)
apex_x_mm = x_ant_mm[apex_idx]

# Interpolação para achar o Y posterior no mesmo X
y_post_at_apex = np.interp(apex_x_mm, x_post_mm, y_post_mm)
ct_mm = abs(y_ant_mm[apex_idx] - y_post_at_apex)

print("\n--- Parâmetros do Gêmeo Digital (Extraídos do RAW) ---")
print(f"Raio Anterior (r_ant): {r_ant:.3f} mm")
print(f"Raio Posterior (r_post): {r_post:.3f} mm")
print(f"Espessura Central (ct): {ct_mm:.3f} mm")

# 5. Salvar JSON
patient_id = os.path.basename(target_file).replace('.SPR', '')
json_path = os.path.join(out_dir, "digital_twin.json")
twin_data = {
    "patient_id": patient_id,
    "r_ant": float(r_ant),
    "r_post": float(r_post),
    "ct": float(ct_mm),
    "diam": 10.0 # Standard FEM block size
}
with open(json_path, 'w') as f:
    json.dump(twin_data, f, indent=4)

# 6. Plotagem de Validação (Imagem)
plt.figure(figsize=(10, 6))
plt.imshow(img, cmap='gray')
plt.plot(ant_points[:, 0], ant_points[:, 1], 'r-', linewidth=2, label=f'Ant Edge (R={r_ant:.2f}mm)')
plt.plot(post_points[:, 0], post_points[:, 1], 'b-', linewidth=2, label=f'Post Edge (R={r_post:.2f}mm)')

plt.title(f'Gêmeo Digital: Extração de Córnea Bruta (.SPR)\nEspessura Central calculada: {ct_mm*1000:.0f} um', fontsize=14, fontweight='bold')
plt.legend()
plt.axis('off')
img_path = os.path.join(out_dir, "digital_twin_overlay.png")
plt.tight_layout()
plt.savefig(img_path, dpi=300, bbox_inches='tight')
print(f"\nSalvo overlay visual em: {img_path}")
print(f"Salvo dados JSON em: {json_path}")
