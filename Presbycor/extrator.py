import sys
import subprocess
import threading
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Instalando bibliotecas necessárias (playwright)...")
    install("playwright")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright

import tkinter as tk

def run_browser():
    print("Iniciando navegador Chromium...")
    with sync_playwright() as p:
        # Abre o navegador visível para o usuário
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Pode não ser a URL direta do sistema, mas ajuda o usuário a começar
        page.goto("https://www.google.com")
        
        def extract():
            print("Extraindo HTML...")
            html_content = page.content()
            with open("calculos_presbycor.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("Salvo em calculos_presbycor.html!")
            browser.close()
            root.destroy()
            
        # Cria uma pequena janela sempre no topo para o usuário avisar quando terminou
        root = tk.Tk()
        root.title("Assistente Antigravity")
        root.geometry("450x250")
        root.attributes("-topmost", True)
        
        texto = (
            "Navegador Auxiliar Aberto!\n\n"
            "1. Use o navegador aberto para acessar o Presbycor.\n"
            "2. Coloque seu login e senha.\n"
            "3. Vá até a página onde aparecem os seus mais de 420 cálculos.\n\n"
            "4. Quando a página estiver carregada com os cálculos, clique abaixo:"
        )
        lbl = tk.Label(root, text=texto, wraplength=400, font=("Arial", 11))
        lbl.pack(pady=20)
        
        btn = tk.Button(root, text="Extrair Cálculos e Começar ML", command=extract, 
                        bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        btn.pack(pady=10)
        
        root.mainloop()

if __name__ == "__main__":
    run_browser()
