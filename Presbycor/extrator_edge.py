import sys
import tkinter as tk

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    from playwright.sync_api import sync_playwright

def run_browser():
    print("Iniciando o Microsoft Edge...")
    with sync_playwright() as p:
        # channel="msedge" obriga a usar o Edge nativo do seu Windows, sem precisar baixar nada!
        browser = p.chromium.launch(channel="msedge", headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://app.presbycor.com/strategies/liste")
        
        def extract():
            print("Extraindo os dados da página...")
            html_content = page.content()
            with open("calculos_presbycor.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("Dados salvos em calculos_presbycor.html!")
            browser.close()
            root.destroy()
            
        root = tk.Tk()
        root.title("Assistente Antigravity - Presbycor")
        root.geometry("450x250")
        root.attributes("-topmost", True)
        
        texto = (
            "Microsoft Edge Aberto!\n\n"
            "1. Na janela do Edge que abriu, acesse o Presbycor.\n"
            "2. Faça o seu login.\n"
            "3. Vá até a tela onde estão os seus 420 cálculos.\n\n"
            "4. Clique no botão abaixo para eu extrair os dados e começar o Machine Learning:"
        )
        lbl = tk.Label(root, text=texto, wraplength=400, font=("Arial", 11))
        lbl.pack(pady=20)
        
        btn = tk.Button(root, text="Extrair Cálculos", command=extract, 
                        bg="#0078D7", fg="white", font=("Arial", 12, "bold"))
        btn.pack(pady=10)
        
        root.mainloop()

if __name__ == "__main__":
    run_browser()
