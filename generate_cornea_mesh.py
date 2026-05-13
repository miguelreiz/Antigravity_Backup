import gmsh
import math
import sys

def create_cornea_mesh():
    gmsh.initialize(sys.argv)
    gmsh.model.add("Cornea_ICRS")
    
    # Parametros da Cornea
    R_ant = 7.8      # Raio anterior
    R_post = 6.5     # Raio posterior
    CCT = 0.5        # Espessura central (500 microns)
    Dia = 10.0       # Diametro corneano simulado
    
    # Parametros do Anel (AJL PRO+ Style)
    R_anel = 2.5     # Raio de implantacao (zona optica 5.0)
    Esp_anel = 0.25  # 250 microns
    Base_anel = 0.60 # 600 microns de base
    Arco = 160.0     # Graus
    Prof_implante = 0.75 # 75% da profundidade
    
    # 1. CRIANDO A CORNEA (OpenCASCADE Kernel)
    # Criamos a esfera anterior
    sphere_ant = gmsh.model.occ.addSphere(0, 0, -R_ant, R_ant)
    # Criamos a esfera posterior (deslocada para dar a espessura)
    z_post = -(R_post + CCT)
    sphere_post = gmsh.model.occ.addSphere(0, 0, z_post, R_post)
    
    # Diferenca booleana para criar a "concha" da cornea
    cornea_shell, _ = gmsh.model.occ.cut([(3, sphere_ant)], [(3, sphere_post)])
    
    # Cilindro para cortar as bordas (diametro 10mm)
    cyl = gmsh.model.occ.addCylinder(0, 0, -10, 0, 0, 20, Dia/2.0)
    
    # Intersecao para obter a cornea final
    cornea, _ = gmsh.model.occ.intersect(cornea_shell, [(3, cyl)])
    
    # 2. CRIANDO O ANEL (ICRS)
    # Primeiro desenhamos o perfil prismatico/triangular em 2D no plano XZ
    # Base no raio 2.5, profundidade a 75%
    z_anel = -CCT * Prof_implante # Simplificado para teste
    
    p1 = gmsh.model.occ.addPoint(R_anel - Base_anel/2, 0, z_anel)
    p2 = gmsh.model.occ.addPoint(R_anel + Base_anel/2, 0, z_anel)
    p3 = gmsh.model.occ.addPoint(R_anel, 0, z_anel + Esp_anel)
    
    l1 = gmsh.model.occ.addLine(p1, p2)
    l2 = gmsh.model.occ.addLine(p2, p3)
    l3 = gmsh.model.occ.addLine(p3, p1)
    
    cl = gmsh.model.occ.addCurveLoop([l1, l2, l3])
    perfil = gmsh.model.occ.addPlaneSurface([cl])
    
    # Revolucao do perfil para criar o arco do anel (Sweep 160 graus)
    arco_rad = arco_rad = Arco * math.pi / 180.0
    # Extrude revolve: Dim, Tag, X, Y, Z (centro), aX, aY, aZ (eixo), angulo
    anel = gmsh.model.occ.revolve([(2, perfil)], 0,0,0, 0,0,1, arco_rad)
    
    # 3. CRIANDO O TUNEL (Boolean Cut)
    # Cortamos o anel de dentro da cornea para criar a cavidade
    # A ferramenta cut preserva o objeto original se configurada, mas aqui vamos 
    # subtrair para gerar o espaco oco, depois recolocar o anel como um volume separado.
    
    # Como as IDs podem mudar, pegamos a tag da cornea que e o ultimo volume
    cornea_tag = cornea[0][1]
    anel_tag = anel[1][1] # A extrusao retorna varios objetos (superficies e 1 volume). O volume é a entidade 3D.
    
    # Fragment booleano (Merge) mantem os dois volumes vizinhos (Cornea + Anel) conectados
    gmsh.model.occ.fragment([(3, cornea_tag)], [(3, anel_tag)])
    
    gmsh.model.occ.synchronize()
    
    # 4. CONFIGURACOES DE MALHA (Mesh)
    # Definindo tamanho dos elementos (Refinamento alto na area do anel)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.5)
    
    print("Gerando malha 3D...")
    gmsh.model.mesh.generate(3)
    
    # Salva o arquivo e abre a interface grafica para o cirurgiao visualizar
    gmsh.write("cornea_icrs.msh")
    
    print("Sucesso! Abrindo visualizador 3D do Gmsh...")
    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()
        
    gmsh.finalize()

if __name__ == '__main__':
    create_cornea_mesh()
