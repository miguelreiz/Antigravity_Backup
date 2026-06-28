import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def analyze_pentacam_layers():
    # Encontrar uma imagem bruta SPR do Pentacam
    pentacam_dir = r"D:\Pentacam_Database\AutoCSV\Pentacam\Pentacam.BMP"
    spr_files = glob.glob(os.path.join(pentacam_dir, "*.SPR"))
    
    if not spr_files:
        print("Nenhum arquivo SPR encontrado.")
        return
        
    img_path = spr_files[0]
    print(f"Analisando imagem: {os.path.basename(img_path)}")
    
    # Decodificar o arquivo .SPR (Pular header de 2048 bytes e ler matriz 500x500 uint8)
    try:
        with open(img_path, 'rb') as f:
            data = f.read()
            pixel_data = data[2048:2048+(500*500)]
            img = np.frombuffer(pixel_data, dtype=np.uint8).reshape((500, 500))
    except Exception as e:
        print(f"Falha ao decodificar SPR: {e}")
        return

    # Extrair um perfil de intensidade (A-scan) no centro e na região ínfero-temporal (IT)
    # Supondo que a córnea esteja na parte central da imagem.
    height, width = img.shape
    center_x = width // 2
    
    # Perfil Central
    profile_central = img[:, center_x]
    
    # Perfil Ínfero-Temporal (aproximadamente deslocado do centro, dependendo de como a imagem é gerada)
    # Em Scheimpflug, uma fatia geralmente cruza IT para SN. 
    # Vamos pegar colunas ligeiramente deslocadas para simular regiões.
    it_x = center_x - 50 # Deslocamento arbitrário para região lateral na fatia plana
    profile_it = img[:, it_x]
    
    # Plotar o perfil de densidade
    plt.figure(figsize=(10, 6))
    plt.plot(profile_central, label="A-Scan Central", color='blue')
    plt.plot(profile_it, label="A-Scan Ínfero-Temporal (IT)", color='red')
    plt.title("Perfil de Densidade Óptica (Scheimpflug A-Scan)")
    plt.xlabel("Profundidade Axial (pixels)")
    plt.ylabel("Intensidade (0-255)")
    plt.legend()
    plt.grid(True)
    
    output_plot = r"C:\Users\3D_OCT\.gemini\antigravity\brain\0acad2ee-04f3-4437-9637-d789354d9fd6\scratch\pentacam_layers_profile.png"
    plt.savefig(output_plot)
    print(f"Gráfico salvo em: {output_plot}")

    # Tentativa de identificar picos (camadas) no A-scan Central
    # Primeiro pico: Epitélio
    # Último pico: Endotélio/Descemet
    # Área central: Estroma
    print("\n[Análise Teórica de Picos]")
    # Encontrar onde a intensidade sobe acima do fundo (> 20)
    cornea_indices = np.where(profile_central > 20)[0]
    if len(cornea_indices) > 0:
        surface_idx = cornea_indices[0]
        endothelium_idx = cornea_indices[-1]
        print(f"Início da Córnea (Epitélio): Pixel {surface_idx}")
        print(f"Fim da Córnea (Endotélio/Descemet): Pixel {endothelium_idx}")
        print(f"Espessura total em pixels: {endothelium_idx - surface_idx}")
        
        stroma_start = surface_idx + int((endothelium_idx - surface_idx) * 0.1) # Pula o epitelio
        stroma_end = endothelium_idx - int((endothelium_idx - surface_idx) * 0.1)
        stroma_pixels = profile_central[stroma_start:stroma_end]
        
        # O estroma anterior costuma ser mais brilhante (maior backscattering) que o posterior.
        ant_stroma = np.mean(stroma_pixels[:len(stroma_pixels)//2])
        post_stroma = np.mean(stroma_pixels[len(stroma_pixels)//2:])
        print(f"Refletividade Média - Estroma Anterior: {ant_stroma:.2f}")
        print(f"Refletividade Média - Estroma Posterior: {post_stroma:.2f}")

if __name__ == "__main__":
    analyze_pentacam_layers()
