import numpy as np
import gmsh
import sys

def generate_hex_mesh():
    print("Gerando malha Hexaedrica Estruturada com Anel AJL Kiroshi Style...")
    
    # Resolucao ultra-fina para dar aquele visual premium do video
    n_r = 50   
    n_t = 120  
    n_z = 10   
    
    R_out = 5.0
    R_ant = 7.8
    R_post = 6.5
    
    r_edges = np.linspace(0, R_out, n_r + 1)
    t_edges = np.linspace(0, 2*np.pi, n_t + 1)[:-1]
    z_edges = np.linspace(0, 1, n_z + 1)
    
    nodes = []
    node_id = 1
    node_map = {}
    
    print("Calculando vertices...")
    for ir, r in enumerate(r_edges):
        for it, theta in enumerate(t_edges):
            r_calc = max(r, 0.01) 
            x = r_calc * np.cos(theta)
            y = r_calc * np.sin(theta)
            
            Z_ant = np.sqrt(R_ant**2 - r_calc**2) - R_ant
            Z_post = np.sqrt(R_post**2 - r_calc**2) - R_post - 0.5  
            
            for iz, z_frac in enumerate(z_edges):
                z = Z_ant * (1 - z_frac) + Z_post * z_frac
                nodes.append((x, y, z))
                node_map[(ir, it, iz)] = node_id
                node_id += 1
                
    print("Separando Estroma e Anel (PMMA)...")
    stroma_elements = []
    ring_elements = []
    
    # Parametros do anel
    anel_r_min = 2.4
    anel_r_max = 3.0
    anel_z_min = 0.6  # 60% profundidade
    anel_z_max = 0.8  # 80% profundidade
    
    # Angulos em radianos (Eixo 135, arco 160 = de 55 a 215)
    ang_min = np.radians(55)
    ang_max = np.radians(215)
    
    for ir in range(n_r):
        r_center = (r_edges[ir] + r_edges[ir+1]) / 2.0
        
        for it in range(n_t):
            it_next = (it + 1) % n_t
            t_center = t_edges[it] # Simplificado, arco é contínuo
            
            # Ajuste de angulo continuo entre 0 e 2pi
            is_in_arc = False
            if ang_min <= t_center <= ang_max:
                is_in_arc = True
                
            for iz in range(n_z):
                z_center = (z_edges[iz] + z_edges[iz+1]) / 2.0
                
                n1 = node_map[(ir, it, iz)]
                n2 = node_map[(ir+1, it, iz)]
                n3 = node_map[(ir+1, it_next, iz)]
                n4 = node_map[(ir, it_next, iz)]
                n5 = node_map[(ir, it, iz+1)]
                n6 = node_map[(ir+1, it, iz+1)]
                n7 = node_map[(ir+1, it_next, iz+1)]
                n8 = node_map[(ir, it_next, iz+1)]
                
                elem = [n1, n2, n3, n4, n5, n6, n7, n8]
                
                # Check se este bloco Hexaedrico pertence ao Anel
                if (anel_r_min <= r_center <= anel_r_max) and is_in_arc and (anel_z_min <= z_center <= anel_z_max):
                    ring_elements.append(elem)
                else:
                    stroma_elements.append(elem)

    print(f"Total Hexaedros Estroma: {len(stroma_elements)}")
    print(f"Total Hexaedros Anel PMMA: {len(ring_elements)}")

    gmsh.initialize(sys.argv)
    gmsh.model.add("Cornea_Kiroshi_Clone")
    
    # Entidade 1 = Estroma
    gmsh.model.addDiscreteEntity(3, 1)
    # Entidade 2 = Anel
    if len(ring_elements) > 0:
        gmsh.model.addDiscreteEntity(3, 2)
    
    node_tags = np.arange(1, len(nodes) + 1)
    node_coords = np.array(nodes).flatten()
    gmsh.model.mesh.addNodes(3, 1, node_tags, node_coords)
    
    # Hexaedros do Estroma
    stroma_tags = np.arange(1, len(stroma_elements) + 1)
    gmsh.model.mesh.addElementsByType(1, 5, stroma_tags, np.array(stroma_elements).flatten())
    
    # Hexaedros do Anel
    if len(ring_elements) > 0:
        # Importante: As tags dos elementos devem ser unicas globalmente
        ring_tags = np.arange(len(stroma_elements) + 1, len(stroma_elements) + len(ring_elements) + 1)
        gmsh.model.mesh.addElementsByType(2, 5, ring_tags, np.array(ring_elements).flatten())
    
    # ------------------ ESTETICA AJL / KIROSHI ------------------
    # Mostra arestas dos volumes e faces para ver a "teia"
    gmsh.option.setNumber("Mesh.VolumeEdges", 1)   
    gmsh.option.setNumber("Mesh.VolumeFaces", 1)
    # Linhas pretas de alta definicao
    gmsh.option.setNumber("Mesh.LineWidth", 1.5)
    
    # Core = (dim, tag), R, G, B, Alpha (0 a 255, onde 255 é solido e <255 é translucido)
    # Estroma: Azul Claro Translucido
    gmsh.model.setColor([(3, 1)], 100, 180, 255, 120) 
    
    # Anel: Laranja Intenso Solido
    if len(ring_elements) > 0:
        gmsh.model.setColor([(3, 2)], 255, 120, 0, 255) 
    
    # Background preto para parecer software medico dark mode
    # Background options removed to avoid exceptions
    
    gmsh.write("cornea_ajl_style.msh")
    
    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()
        
    gmsh.finalize()

if __name__ == '__main__':
    generate_hex_mesh()
