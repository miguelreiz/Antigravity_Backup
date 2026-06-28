import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

scratch_dir = r"C:\Users\3D_OCT\Documents\Antigravity\Vetores Anel\scratch"
patient = "EX001457"
msh_file = os.path.join(scratch_dir, f"{patient}_digital_twin.msh")
stress_file = os.path.join(scratch_dir, f"stress_{patient}_digital_twin.csv")
disp_file = os.path.join(scratch_dir, f"disp_{patient}_digital_twin.csv")

# Ler Coordenadas Originais do MSH (Simplificado)
# Para evitar parse complexo, leremos direto dos outputs. O FEBio loga por Elemento e por Nó.
# disp_*.csv tem: id, ux, uy, uz
# Mas não tem as coordenadas originais.
# Vamos fazer um parsing rudimentar do MSH para pegar as posições.
nodes = {}
with open(msh_file, 'r') as f:
    in_nodes = False
    for line in f:
        line = line.strip()
        if line == "$Nodes":
            in_nodes = True
            continue
        if line == "$EndNodes":
            break
        if in_nodes:
            parts = line.split()
            if len(parts) == 4: # node_id, x, y, z
                try:
                    nid = int(parts[0])
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    nodes[nid] = (x, y, z)
                except:
                    pass

print("Tentando parse Gmsh v4...")
import gmsh
gmsh.initialize()
gmsh.open(msh_file)
nodeTags, nodeCoords, _ = gmsh.model.mesh.getNodes()
for i, tag in enumerate(nodeTags):
    nodes[int(tag)] = (nodeCoords[3*i], nodeCoords[3*i+1], nodeCoords[3*i+2])
gmsh.finalize()

print(f"Lidos {len(nodes)} nós.")

# Ler Deslocamentos manualmente devido aos headers do FEBio
disp_dict = {}
try:
    with open(disp_file, 'r') as f:
        # Pega a última etapa de tempo
        current_time = 0
        for line in f:
            line = line.strip()
            if not line or line.startswith('*'):
                continue
            parts = line.split(',')
            if len(parts) == 4:
                try:
                    nid = int(parts[0])
                    ux, uy, uz = float(parts[1]), float(parts[2]), float(parts[3])
                    disp_dict[nid] = {'ux': ux, 'uy': uy, 'uz': uz} # Sobrescreve nas iterações seguintes, mantendo o final
                except ValueError:
                    pass
except Exception as e:
    print(f"Erro lendo deslocamento: {e}")
    exit(1)

# Montar posições deformadas
pts_orig = []
pts_def = []
for nid, coords in nodes.items():
    if nid in disp_dict:
        dx = disp_dict[nid]['ux']
        dy = disp_dict[nid]['uy']
        dz = disp_dict[nid]['uz']
        pts_orig.append([coords[0], coords[1], coords[2]])
        pts_def.append([coords[0]+dx, coords[1]+dy, coords[2]+dz])

pts_orig = np.array(pts_orig)
pts_def = np.array(pts_def)

# Focar em Y=0 (Plano X-Z central)
mask = np.abs(pts_orig[:, 1]) < 0.2
pts_slice = pts_def[mask]
pts_slice_orig = pts_orig[mask]

plt.figure(figsize=(12, 6))

plt.scatter(pts_slice_orig[:, 0], pts_slice_orig[:, 2], c='lightgray', s=10, label='Geometria Original (SPR)', alpha=0.5)
plt.scatter(pts_slice[:, 0], pts_slice[:, 2], c='red', s=15, label='Deformada (Pós IOP 15 mmHg + Anel)', alpha=0.8)

# Destacar a posição aproximada do Anel (x ~ 2.5)
ring_x = pts_slice[(pts_slice[:, 0] > 2.2) & (pts_slice[:, 0] < 2.8)]
if len(ring_x) > 0:
    plt.scatter(ring_x[:, 0], ring_x[:, 2], c='blue', s=20, label='Vetor do Anel')

plt.title(f"Gêmeo Digital: Simulação FEM (Paciente {patient})\nExtração Direta .SPR → Gmsh → FEBio", fontsize=14, fontweight='bold')
plt.xlabel("Raio (mm)", fontsize=12)
plt.ylabel("Eixo Z (mm)", fontsize=12)
plt.axis('equal')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

out_png = os.path.join(scratch_dir, f"{patient}_fem_slice.png")
plt.tight_layout()
plt.savefig(out_png, dpi=300, bbox_inches='tight')
print(f"Gráfico de perfil salvo em {out_png}")
