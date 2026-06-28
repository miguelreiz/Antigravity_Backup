"""
febio_builder.py — Exportador de malha Gmsh → FEBio 4.0 XML (.feb).

Fase 4: Material Holzapfel-Gasser-Ogden (HGO) com orientação fibrilar
per-element calculada analiticamente a partir da geometria esférica.

O sistema de coordenadas local de cada elemento é:
  - N  = vetor radial (centro de curvatura → centróide do elemento)
  - T1 = vetor meridional (tangente ao plano lamelar, direção do polo)
  - T2 = vetor circunferencial (N × T1)

gamma=45° no HGO gera duas famílias de fibras a ±45° de T1,
reproduzindo a orientação ortogonal das lamelas estromais.
"""

import gmsh
import os
import numpy as np


def _compute_element_centroid(node_coords, node_ids):
    """Calcula o centróide de um elemento a partir dos nós."""
    coords = np.array([node_coords[int(nid)] for nid in node_ids])
    return coords.mean(axis=0)


def _compute_fiber_axes(centroid, r_ant=7.8):
    """
    Calcula os eixos locais de fibra (T1, T2) para um elemento
    baseando-se na geometria esférica da córnea.

    Parameters
    ----------
    centroid : array (3,)
        Centro geométrico do elemento (x, y, z).
    r_ant : float
        Raio de curvatura anterior.

    Returns
    -------
    a : array (3,) — vetor meridional T1 (normalizado)
    d : array (3,) — vetor circunferencial T2 (normalizado)
    """
    center_of_curvature = np.array([0.0, 0.0, -r_ant])
    radial = centroid - center_of_curvature
    norm_r = np.linalg.norm(radial)
    if norm_r < 1e-12:
        return np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])
    N = radial / norm_r

    # Vetor meridional: projeção do eixo Z no plano tangente lamelar
    z_axis = np.array([0.0, 0.0, 1.0])
    t1 = z_axis - np.dot(z_axis, N) * N
    norm_t1 = np.linalg.norm(t1)
    if norm_t1 < 1e-12:
        # Elemento no polo — usar X como referência
        x_axis = np.array([1.0, 0.0, 0.0])
        t1 = x_axis - np.dot(x_axis, N) * N
        norm_t1 = np.linalg.norm(t1)
    T1 = t1 / norm_t1

    # Vetor circunferencial: perpendicular a N e T1
    T2 = np.cross(N, T1)
    T2 = T2 / np.linalg.norm(T2)

    return T1, T2


def export_to_febio(output_feb_file="model.feb", baseline=False):
    """
    Exporta a malha Gmsh atual para um arquivo .feb (FEBio 4.0).

    O material corneano é Holzapfel-Gasser-Ogden com orientação fibrilar
    per-element (MeshData/ElementData).

    Parameters
    ----------
    output_feb_file : str
        Caminho do arquivo .feb de saída.
    baseline : bool
        Se True, o anel recebe o mesmo material da córnea (baseline).
    """
    # ---- 1. Extrair nós ----
    nodeTags, nodeCoords, _ = gmsh.model.mesh.getNodes()
    nodes = {}
    for i, tag in enumerate(nodeTags):
        nodes[tag] = (nodeCoords[3 * i], nodeCoords[3 * i + 1], nodeCoords[3 * i + 2])

    # ---- 2. Funções auxiliares ----
    def get_solid_elements(pg_name):
        dimtags = gmsh.model.getPhysicalGroups()
        pg_tag = None
        for dim, tag in dimtags:
            if gmsh.model.getPhysicalName(dim, tag) == pg_name:
                pg_tag = tag
                break
        if pg_tag is None:
            return [], []

        entities = gmsh.model.getEntitiesForPhysicalGroup(3, pg_tag)
        hex_elems, penta_elems = [], []
        for e in entities:
            elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(3, e)
            for etype, etags, enodetags in zip(elemTypes, elemTags, elemNodeTags):
                if etype == 5:  # Hex8
                    for j, etag in enumerate(etags):
                        n = enodetags[8 * j : 8 * (j + 1)]
                        hex_elems.append((etag, n))
                elif etype == 6:  # Penta6
                    for j, etag in enumerate(etags):
                        n = enodetags[6 * j : 6 * (j + 1)]
                        penta_elems.append((etag, n))
        return hex_elems, penta_elems

    def get_surface_elements(pg_name):
        dimtags = gmsh.model.getPhysicalGroups()
        pg_tag = None
        for dim, tag in dimtags:
            if gmsh.model.getPhysicalName(dim, tag) == pg_name:
                pg_tag = tag
                break
        if pg_tag is None:
            return [], []

        entities = gmsh.model.getEntitiesForPhysicalGroup(2, pg_tag)
        quad_elems, tri_elems = [], []
        for e in entities:
            elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(2, e)
            for etype, etags, enodetags in zip(elemTypes, elemTags, elemNodeTags):
                if etype == 3:  # Quad4
                    for j, etag in enumerate(etags):
                        n = enodetags[4 * j : 4 * (j + 1)]
                        quad_elems.append((etag, n))
                elif etype == 2:  # Tri3
                    for j, etag in enumerate(etags):
                        n = enodetags[3 * j : 3 * (j + 1)]
                        tri_elems.append((etag, n))
        return quad_elems, tri_elems

    # ---- 3. Extrair malhas ----
    cornea_hex, cornea_penta = get_solid_elements("Cornea")
    ring_hex, ring_penta = get_solid_elements("Ring")
    posterior_quads, posterior_tris = get_surface_elements("PosteriorFace")
    limbus_quads, _ = get_surface_elements("LimbusFace")

    limbus_nodes = set()
    for _, n in limbus_quads:
        limbus_nodes.update(n)

    # ---- 4. Calcular eixos de fibra para cada elemento da córnea ----
    # Remontar cornea_hex em IDs locais sequenciais (lid) para MeshData
    all_cornea_elems = cornea_hex + cornea_penta
    fiber_data = []  # lista de (lid, a_vec, d_vec)
    for lid_idx, (etag, n) in enumerate(all_cornea_elems, start=1):
        centroid = _compute_element_centroid(nodes, n)
        a_vec, d_vec = _compute_fiber_axes(centroid)
        fiber_data.append((lid_idx, a_vec, d_vec))

    # ---- 5. Construir XML ----
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<febio_spec version="4.0">')
    lines.append('  <Module type="solid"/>')

    # -- Control --
    lines.append("  <Control>")
    lines.append("    <analysis>STATIC</analysis>")
    lines.append("    <time_steps>10</time_steps>")
    lines.append("    <step_size>0.1</step_size>")
    lines.append('    <solver type="solid">')
    lines.append("      <max_refs>15</max_refs>")
    lines.append("      <dtol>0.001</dtol>")
    lines.append("      <etol>0.01</etol>")
    lines.append("      <lsmin>0.01</lsmin>")
    lines.append("      <lsiter>5</lsiter>")
    lines.append("    </solver>")
    lines.append("  </Control>")

    # -- Material --
    # Parâmetros HGO para córnea humana (Simonini/Pandolfi 2015 + Kling 2010)
    #   c     = 0.005 MPa   (rigidez da matriz Neo-Hookean)
    #   k1    = 10.0 MPa    (rigidez das fibras de colágeno)
    #   k2    = 100.0        (não-linearidade exponencial)
    #   kappa = 0.15         (dispersão, 0=alinhado, 1/3=isotrópico)
    #   gamma = 45°          (±45° gera 2 famílias ortogonais de lamelas)
    #   k     = 100.0 MPa   (penalidade de incompressibilidade)
    lines.append("  <Material>")
    lines.append(
        '    <material id="1" name="Cornea" type="Holzapfel-Gasser-Ogden">'
    )
    lines.append("      <c>0.05</c>")
    lines.append("      <k1>2.0</k1>")
    lines.append("      <k2>50.0</k2>")
    lines.append("      <kappa>0.15</kappa>")
    lines.append("      <gamma>45.0</gamma>")
    lines.append("      <k>100.0</k>")
    lines.append("    </material>")
    lines.append('    <material id="2" name="Ring_PMMA" type="rigid body">')
    lines.append("      <density>1.19e-9</density>")
    lines.append("      <center_of_mass>0,0,0</center_of_mass>")
    lines.append("    </material>")
    lines.append("  </Material>")

    # -- Mesh --
    lines.append("  <Mesh>")
    lines.append('    <Nodes name="AllNodes">')
    for tag in sorted(nodes.keys()):
        x, y, z = nodes[tag]
        lines.append(f'      <node id="{tag}">{x:.6f},{y:.6f},{z:.6f}</node>')
    lines.append("    </Nodes>")

    # Elementos da Córnea (Hex8)
    lines.append('    <Elements type="hex8" name="Part_Cornea" mat="1">')
    for etag, n in cornea_hex:
        n_str = ",".join(str(int(nid)) for nid in n)
        lines.append(f'      <elem id="{etag}">{n_str}</elem>')
    lines.append("    </Elements>")

    # Elementos da Córnea (Penta6)
    if cornea_penta:
        lines.append('    <Elements type="penta6" name="Part_Cornea_Penta" mat="1">')
        for etag, n in cornea_penta:
            n_str = ",".join(str(int(nid)) for nid in n)
            lines.append(f'      <elem id="{etag}">{n_str}</elem>')
        lines.append("    </Elements>")

    # Elementos do Anel
    if len(ring_hex) > 0:
        ring_mat = "1" if baseline else "2"
        ring_mat_name = "Cornea" if baseline else "Ring_PMMA"

        lines.append(f'    <Elements type="hex8" name="Part_Ring" mat="{ring_mat}">')
        for etag, n in ring_hex:
            n_str = ",".join(str(int(nid)) for nid in n)
            lines.append(f'      <elem id="{etag}">{n_str}</elem>')
        lines.append("    </Elements>")
        if ring_penta:
            lines.append(
                f'    <Elements type="penta6" name="Part_Ring_Penta" mat="{ring_mat}">'
            )
            for etag, n in ring_penta:
                n_str = ",".join(str(int(nid)) for nid in n)
                lines.append(f'      <elem id="{etag}">{n_str}</elem>')
            lines.append("    </Elements>")

    # Surface Posterior
    lines.append('    <Surface name="Posterior_Face">')
    for etag, n in posterior_quads:
        n_str = ",".join(str(int(nid)) for nid in reversed(n))
        lines.append(f'      <quad4 id="{etag}">{n_str}</quad4>')
    for etag, n in posterior_tris:
        n_str = ",".join(str(int(nid)) for nid in reversed(n))
        lines.append(f'      <tri3 id="{etag}">{n_str}</tri3>')
    lines.append("    </Surface>")

    # NodeSet Limbus
    lines.append('    <NodeSet name="Limbus_Nodes">')
    n_str = ",".join(str(int(nid)) for nid in sorted(limbus_nodes))
    lines.append(f"      {n_str}")
    lines.append("    </NodeSet>")

    lines.append("  </Mesh>")

    # -- MeshDomains --
    lines.append("  <MeshDomains>")
    lines.append('    <SolidDomain name="Part_Cornea" mat="Cornea"/>')
    if cornea_penta:
        lines.append('    <SolidDomain name="Part_Cornea_Penta" mat="Cornea"/>')
    if len(ring_hex) > 0:
        lines.append(f'    <SolidDomain name="Part_Ring" mat="{ring_mat_name}"/>')
        if ring_penta:
            lines.append(
                f'    <SolidDomain name="Part_Ring_Penta" mat="{ring_mat_name}"/>'
            )
    lines.append("  </MeshDomains>")

    # -- MeshData: Orientação Fibrilar per-element --
    # FEBio 4 usa <ElementData type="mat_axis" elem_set="...">
    # com <elem lid="N"> e sub-tags <a> e <d> definindo os vetores.
    lines.append("  <MeshData>")

    # Hex8 da Córnea
    lines.append('    <ElementData type="mat_axis" elem_set="Part_Cornea">')
    hex_count = len(cornea_hex)
    for lid_idx, a_vec, d_vec in fiber_data[:hex_count]:
        a_s = f"{a_vec[0]:.6f},{a_vec[1]:.6f},{a_vec[2]:.6f}"
        d_s = f"{d_vec[0]:.6f},{d_vec[1]:.6f},{d_vec[2]:.6f}"
        lines.append(f'      <elem lid="{lid_idx}">')
        lines.append(f"        <a>{a_s}</a>")
        lines.append(f"        <d>{d_s}</d>")
        lines.append("      </elem>")
    lines.append("    </ElementData>")

    # Penta6 da Córnea
    if cornea_penta:
        lines.append(
            '    <ElementData type="mat_axis" elem_set="Part_Cornea_Penta">'
        )
        penta_lid = 1
        for lid_idx, a_vec, d_vec in fiber_data[hex_count:]:
            a_s = f"{a_vec[0]:.6f},{a_vec[1]:.6f},{a_vec[2]:.6f}"
            d_s = f"{d_vec[0]:.6f},{d_vec[1]:.6f},{d_vec[2]:.6f}"
            lines.append(f'      <elem lid="{penta_lid}">')
            lines.append(f"        <a>{a_s}</a>")
            lines.append(f"        <d>{d_s}</d>")
            lines.append("      </elem>")
            penta_lid += 1
        lines.append("    </ElementData>")

    lines.append("  </MeshData>")

    # -- Boundary --
    lines.append("  <Boundary>")
    lines.append(
        '    <bc name="FixLimbus" type="zero displacement" node_set="Limbus_Nodes">'
    )
    lines.append("      <x_dof>1</x_dof>")
    lines.append("      <y_dof>1</y_dof>")
    lines.append("      <z_dof>1</z_dof>")
    lines.append("    </bc>")
    lines.append("  </Boundary>")

    # -- Loads: IOP = 15 mmHg ≈ 0.002 MPa --
    lines.append("  <Loads>")
    lines.append(
        '    <surface_load name="IOP" type="pressure" surface="Posterior_Face">'
    )
    lines.append('      <pressure lc="1">-0.002</pressure>')
    lines.append("      <linear>0</linear>")
    lines.append("      <symmetric_stiffness>1</symmetric_stiffness>")
    lines.append("    </surface_load>")
    lines.append("  </Loads>")

    # -- LoadData --
    lines.append("  <LoadData>")
    lines.append('    <load_controller id="1" type="loadcurve">')
    lines.append("      <interpolate>LINEAR</interpolate>")
    lines.append("      <points>")
    lines.append("        <pt>0,0</pt>")
    lines.append("        <pt>1,1</pt>")
    lines.append("      </points>")
    lines.append("    </load_controller>")
    lines.append("  </LoadData>")

    # -- Output --
    base_name = os.path.basename(output_feb_file).replace(".feb", "")
    disp_csv = f"disp_{base_name}.csv"
    stress_csv = f"stress_{base_name}.csv"

    lines.append("  <Output>")
    lines.append('    <plotfile type="febio">')
    lines.append('      <var type="displacement"/>')
    lines.append('      <var type="stress"/>')
    lines.append('      <var type="strain energy density"/>')
    lines.append('      <var type="Lagrange strain"/>')
    lines.append("    </plotfile>")
    lines.append("    <logfile>")
    lines.append(
        f'      <node_data file="{disp_csv}" data="ux;uy;uz" delim=","/>'
    )
    lines.append(
        f'      <element_data file="{stress_csv}" data="sx;sy;sz;sxy;syz;sxz" delim=","/>'
    )
    lines.append("    </logfile>")
    lines.append("  </Output>")

    lines.append("</febio_spec>")

    with open(output_feb_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"FEBio file saved to {output_feb_file}")
