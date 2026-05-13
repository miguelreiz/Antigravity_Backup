import numpy as np
import os

def build_icrs_febio_model(filename="vector_simulation.feb", ring_arc=160, ring_axis=135, depth_pct=0.75):
    print("Iniciando conversao estrutural para FEBio (60.000 Hexaedros)...")
    
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
    
    # Gerando os Nos Matemáticos
    for ir, r in enumerate(r_edges):
        for it, theta in enumerate(t_edges):
            r_calc = max(r, 0.01) 
            x = r_calc * np.cos(theta)
            y = r_calc * np.sin(theta)
            
            Z_ant = np.sqrt(R_ant**2 - r_calc**2) - R_ant
            Z_post = np.sqrt(R_post**2 - r_calc**2) - R_post - 0.5  
            
            for iz, z_frac in enumerate(z_edges):
                z = Z_ant * (1 - z_frac) + Z_post * z_frac
                nodes.append((node_id, x, y, z))
                node_map[(ir, it, iz)] = node_id
                node_id += 1
                
    stroma_elements = []
    ring_elements = []
    
    anel_r_min = 2.4
    anel_r_max = 3.0
    # O anel ocupará cerca de 20% da espessura (100 um de 500 um).
    # Se a profundidade alvo é 75%, ele pode ir de 65% a 85%.
    anel_z_min = depth_pct - 0.1
    anel_z_max = depth_pct + 0.1
    
    ang_center = np.radians(ring_axis)
    arc_half = np.radians(ring_arc / 2.0)
    
    # Normalize angles to handle wrapping
    def angle_diff(a1, a2):
        d = a1 - a2
        return (d + np.pi) % (2 * np.pi) - np.pi

    elem_id = 1
    for ir in range(n_r):
        r_center = (r_edges[ir] + r_edges[ir+1]) / 2.0
        for it in range(n_t):
            it_next = (it + 1) % n_t
            t_center = t_edges[it]
            
            is_in_arc = abs(angle_diff(t_center, ang_center)) <= arc_half
                
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
                
                elem = (elem_id, n1, n2, n3, n4, n5, n6, n7, n8)
                
                if (anel_r_min <= r_center <= anel_r_max) and is_in_arc and (anel_z_min <= z_center <= anel_z_max):
                    ring_elements.append(elem)
                else:
                    stroma_elements.append(elem)
                elem_id += 1

    print(f"Escrevendo arquivo FEBio com {len(nodes)} nos e {len(stroma_elements)+len(ring_elements)} elementos...")
    
    # Criando o .feb file via formatacao de string XML
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
        f.write('<febio_spec version="4.0">\n')
        
        # MODULE
        f.write('\t<Module type="solid"/>\n')
        
        # MATERIALS (HGO para cornea e PMMA para o anel)
        f.write('\t<Material>\n')
        f.write('\t\t<material id="1" name="Cornea_Stroma" type="Holmes-Mow">\n')
        f.write('\t\t\t<density>1.0</density>\n')
        f.write('\t\t\t<E>0.03</E>\n') # Elasticidade base do estroma (MPa)
        f.write('\t\t\t<v>0.49</v>\n')
        f.write('\t\t\t<beta>2.5</beta>\n')
        f.write('\t\t</material>\n')
        
        f.write('\t\t<material id="2" name="PMMA_Ring" type="neo-Hookean">\n')
        f.write('\t\t\t<density>1.19</density>\n')
        f.write('\t\t\t<E>3000.0</E>\n') # PMMA é super rigido (~3 GPa)
        f.write('\t\t\t<v>0.3</v>\n')
        f.write('\t\t</material>\n')
        f.write('\t</Material>\n')
        
        # MESH
        f.write('\t<Mesh>\n')
        f.write('\t\t<Nodes name="Cornea">\n')
        for n in nodes:
            f.write(f'\t\t\t<node id="{n[0]}">{n[1]:.5f},{n[2]:.5f},{n[3]:.5f}</node>\n')
        f.write('\t\t</Nodes>\n')
        
        f.write('\t\t<Elements type="hex8" name="Part1_Stroma">\n')
        for e in stroma_elements:
            f.write(f'\t\t\t<elem id="{e[0]}">{e[1]},{e[2]},{e[3]},{e[4]},{e[5]},{e[6]},{e[7]},{e[8]}</elem>\n')
        f.write('\t\t</Elements>\n')
        
        if ring_elements:
            f.write('\t\t<Elements type="hex8" name="Part2_Ring">\n')
            for e in ring_elements:
                f.write(f'\t\t\t<elem id="{e[0]}">{e[1]},{e[2]},{e[3]},{e[4]},{e[5]},{e[6]},{e[7]},{e[8]}</elem>\n')
            f.write('\t\t</Elements>\n')
            
        f.write('\t</Mesh>\n')
        
        # MESH DOMAINS (Linkando material)
        f.write('\t<MeshDomains>\n')
        f.write('\t\t<SolidDomain name="Part1_Stroma" mat="Cornea_Stroma"/>\n')
        if ring_elements:
            f.write('\t\t<SolidDomain name="Part2_Ring" mat="PMMA_Ring"/>\n')
        f.write('\t</MeshDomains>\n')
        
        # BOUNDARY CONDITIONS (Borda escleral engastada)
        f.write('\t<Boundary>\n')
        f.write('\t\t<bc name="Scleral_Fixation" type="fix" node_set="@elem_list(Part1_Stroma)">\n')
        # Precisaria criar um set de nós de borda (r = 5.0) para fixar. Simplificado para o esqueleto.
        f.write('\t\t</bc>\n')
        f.write('\t</Boundary>\n')
        
        # STEP (Resolucao)
        f.write('\t<Step>\n')
        f.write('\t\t<step_size>0.1</step_size>\n')
        f.write('\t\t<max_retries>5</max_retries>\n')
        f.write('\t\t<opt_iter>10</opt_iter>\n')
        f.write('\t</Step>\n')
        
        f.write('</febio_spec>\n')
        
    print(f"Sucesso! Arquivo '{filename}' gerado com topologia HGO e PMMA integrada.")

if __name__ == '__main__':
    build_icrs_febio_model()
