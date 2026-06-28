"""
mesh_generator.py — Gerador de malha 3D Hex8 para simulação biomecânica corneana.

Gera duas geometrias distintas via Gmsh:
  - Baseline (has_ring=False): córnea perfeitamente esférica.
  - Ring     (has_ring=True):  córnea com bump anterior (Lei dos Volumes)
                               e cavidade PMMA interna.

Perfis de anel suportados: 'triangular' (Ferrara) e 'oval' (Keraring).
"""

import gmsh
import math
import numpy as np


def generate_cornea_ring_mesh(
    output_filename="cornea_with_ring.msh",
    has_ring=True,
    r_ant=7.8,
    r_post=6.5,
    ct=0.55,
    diam=10.0,
    ring_depth_frac=0.70,
    ring_diam=5.0,
    ring_thick=0.200,
    ring_base=0.600,
    ring_profile="triangular",
    mesh_size=0.15,
):
    """
    Gera uma malha 3D Hex8 da córnea pressurizada.

    Parameters
    ----------
    output_filename : str
        Nome do arquivo de saída .msh.
    has_ring : bool
        Se True, inclui cavidade do anel + bump anterior.
    r_ant, r_post : float
        Raios de curvatura anterior e posterior (mm).
    ct : float
        Espessura central da córnea (mm).
    diam : float
        Diâmetro corneano total (mm).
    ring_depth_frac : float
        Fração da espessura corneana onde a base do anel é posicionada (0–1).
    ring_diam : float
        Diâmetro do anel (mm).
    ring_thick : float
        Espessura (altura) do anel (mm).
    ring_base : float
        Largura da base do anel (mm).
    ring_profile : str
        'triangular' ou 'oval'.
    mesh_size : float
        Tamanho característico dos elementos.
    """
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.option.setNumber("Mesh.RecombineAll", 1)
    gmsh.option.setNumber("Mesh.Algorithm", 8)
    gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 1)

    gmsh.model.add("Cornea")
    factory = gmsh.model.geo

    # Centros de curvatura
    c_ant_z = -r_ant
    c_post_z = -ct - r_post

    # Pontos posteriores
    p_center_post = factory.addPoint(0, 0, c_post_z, mesh_size)
    p_top_post = factory.addPoint(0, 0, -ct, mesh_size)

    # Limbo anterior
    angle_limbus_ant = math.asin((diam / 2) / r_ant)
    x_limb_ant = r_ant * math.sin(angle_limbus_ant)
    z_limb_ant = c_ant_z + r_ant * math.cos(angle_limbus_ant)
    p_limb_ant = factory.addPoint(x_limb_ant, 0, z_limb_ant, mesh_size)

    # Limbo posterior
    x_limb_post = x_limb_ant
    z_limb_post = c_post_z + math.sqrt(r_post**2 - x_limb_post**2)
    p_limb_post = factory.addPoint(x_limb_post, 0, z_limb_post, mesh_size)

    # ---- Superfície Anterior ----
    if has_ring:
        r_ring = ring_diam / 2.0
        bump_height = ring_thick * 0.8  # 80% de transmissão geométrica

        num_pts = 30
        x_vals = np.linspace(0, x_limb_ant, num_pts)
        pts_ant = []
        for x in x_vals:
            z_sphere = c_ant_z + math.sqrt(r_ant**2 - x**2)
            if abs(x - r_ring) < ring_base / 2:
                norm_dist = (x - r_ring) / (ring_base / 2)
                bump = bump_height * 0.5 * (1 + math.cos(norm_dist * math.pi))
                z = z_sphere + bump
            else:
                z = z_sphere
            pts_ant.append(factory.addPoint(x, 0, z, mesh_size))

        l_ant = factory.addSpline(pts_ant)
        p_top_ant = pts_ant[0]
        p_limb_ant = pts_ant[-1]  # último ponto do spline = limbo
    else:
        p_center_ant = factory.addPoint(0, 0, c_ant_z, mesh_size)
        p_top_ant = factory.addPoint(0, 0, 0, mesh_size)
        l_ant = factory.addCircleArc(p_top_ant, p_center_ant, p_limb_ant)

    # Linhas comuns
    l_post = factory.addCircleArc(p_limb_post, p_center_post, p_top_post)
    l_limb = factory.addLine(p_limb_ant, p_limb_post)
    l_axis = factory.addLine(p_top_post, p_top_ant)

    if has_ring:
        # ---- Cavidade do Anel ----
        r_ring = ring_diam / 2.0
        z_ant_ring = c_ant_z + math.sqrt(r_ant**2 - r_ring**2)
        z_post_ring = c_post_z + math.sqrt(r_post**2 - r_ring**2)
        thickness_at_ring = z_ant_ring - z_post_ring
        z_ring_base = z_ant_ring - (thickness_at_ring * ring_depth_frac)

        p_ring_in = factory.addPoint(
            r_ring - ring_base / 2.0, 0, z_ring_base, mesh_size / 3.0
        )
        p_ring_out = factory.addPoint(
            r_ring + ring_base / 2.0, 0, z_ring_base, mesh_size / 3.0
        )
        p_ring_top = factory.addPoint(
            r_ring, 0, z_ring_base + ring_thick, mesh_size / 3.0
        )

        l_ring_base = factory.addLine(p_ring_in, p_ring_out)

        if ring_profile == "triangular":
            l_ring_out_top = factory.addLine(p_ring_out, p_ring_top)
            l_ring_top_in = factory.addLine(p_ring_top, p_ring_in)
            cl_ring = factory.addCurveLoop(
                [l_ring_base, l_ring_out_top, l_ring_top_in]
            )
        else:  # oval
            R_arc = (ring_base**2) / (8.0 * ring_thick) + (ring_thick / 2.0)
            z_center = z_ring_base + ring_thick - R_arc
            p_ring_center = factory.addPoint(
                r_ring, 0, z_center, mesh_size / 3.0
            )
            l_ring_dome = factory.addCircleArc(
                p_ring_out, p_ring_center, p_ring_in
            )
            cl_ring = factory.addCurveLoop([l_ring_base, l_ring_dome])

        s_ring = factory.addPlaneSurface([cl_ring])
        cl_cornea_outer = factory.addCurveLoop([l_ant, l_limb, l_post, l_axis])
        s_cornea = factory.addPlaneSurface([cl_cornea_outer, cl_ring])

        factory.synchronize()
        gmsh.model.mesh.setRecombine(2, s_ring)
        gmsh.model.mesh.setRecombine(2, s_cornea)

        # Revolve 360° (4 × 90°)
        ext_ring_1 = factory.revolve(
            [(2, s_ring)], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        ext_ring_2 = factory.revolve(
            [ext_ring_1[0]], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        ext_ring_3 = factory.revolve(
            [ext_ring_2[0]], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        ext_ring_4 = factory.revolve(
            [ext_ring_3[0]], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        vol_ring = [e[1][1] for e in [ext_ring_1, ext_ring_2, ext_ring_3, ext_ring_4]]

        ext_c1 = factory.revolve(
            [(2, s_cornea)], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        ext_c2 = factory.revolve(
            [ext_c1[0]], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        ext_c3 = factory.revolve(
            [ext_c2[0]], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        ext_c4 = factory.revolve(
            [ext_c3[0]], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        vol_cornea = [e[1][1] for e in [ext_c1, ext_c2, ext_c3, ext_c4]]

        factory.synchronize()
        gmsh.model.addPhysicalGroup(3, vol_cornea, name="Cornea")
        gmsh.model.addPhysicalGroup(3, vol_ring, name="Ring")

    else:
        cl_cornea_outer = factory.addCurveLoop([l_ant, l_limb, l_post, l_axis])
        s_cornea = factory.addPlaneSurface([cl_cornea_outer])

        factory.synchronize()
        gmsh.model.mesh.setRecombine(2, s_cornea)

        ext_c1 = factory.revolve(
            [(2, s_cornea)], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        ext_c2 = factory.revolve(
            [ext_c1[0]], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        ext_c3 = factory.revolve(
            [ext_c2[0]], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        ext_c4 = factory.revolve(
            [ext_c3[0]], 0, 0, 0, 0, 0, 1, math.pi / 2,
            numElements=[10], recombine=True,
        )
        vol_cornea = [e[1][1] for e in [ext_c1, ext_c2, ext_c3, ext_c4]]

        factory.synchronize()
        gmsh.model.addPhysicalGroup(3, vol_cornea, name="Cornea")

    # ---- Identificação de Faces de Contorno (Bounding Box) ----
    surfaces = gmsh.model.getEntities(2)
    posterior_faces = []
    limbus_faces = []

    expected_zmax_post = -ct
    expected_zmin_post = c_post_z + math.sqrt(r_post**2 - (diam/2)**2)
    expected_max_xy = diam / 2

    for dim, tag in surfaces:
        try:
            bbox = gmsh.model.getBoundingBox(dim, tag)
            max_xy = max(abs(bbox[0]), abs(bbox[1]), abs(bbox[3]), abs(bbox[4]))
            zmin, zmax = bbox[2], bbox[5]

            # Posterior: cobre toda a extensão Z da córnea
            if (
                abs(zmin - expected_zmin_post) < 0.15
                and abs(zmax - expected_zmax_post) < 0.15
                and abs(max_xy - expected_max_xy) < 0.15
            ):
                posterior_faces.append(tag)
            # Limbo: faixa vertical estreita na borda
            if (
                abs(zmin - expected_zmin_post) < 0.15
                and abs(zmax - z_limb_ant) < 0.15
                and abs(max_xy - expected_max_xy) < 0.15
            ):
                limbus_faces.append(tag)
        except Exception:
            pass

    if posterior_faces:
        gmsh.model.addPhysicalGroup(2, posterior_faces, name="PosteriorFace")
    if limbus_faces:
        gmsh.model.addPhysicalGroup(2, limbus_faces, name="LimbusFace")

    gmsh.model.mesh.generate(3)
    gmsh.write(output_filename)

    print(f"Mesh generated and saved to {output_filename}")
    return output_filename


if __name__ == "__main__":
    generate_cornea_ring_mesh("cornea_baseline.msh", has_ring=False)
    gmsh.finalize()
    generate_cornea_ring_mesh(
        "cornea_triangular.msh", has_ring=True, ring_profile="triangular"
    )
    gmsh.finalize()
    generate_cornea_ring_mesh(
        "cornea_oval.msh", has_ring=True, ring_profile="oval"
    )
    gmsh.finalize()
