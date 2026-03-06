#!/usr/bin/env python3
"""
Script de Upload Automático para Google Drive
Exporta o livro PresbyCor completo para o Google Drive
"""

import os
import sys
import subprocess
from pathlib import Path
import webbrowser
import time

class GoogleDriveUploader:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.export_dir = self.base_dir / "_Export_To_Drive"
        self.master_file = self.export_dir / "PresbyCor_MASTER_BOOK.docx"
        
    def check_file_exists(self):
        """Verifica se o arquivo master existe"""
        if not self.master_file.exists():
            print(f"❌ Arquivo não encontrado: {self.master_file}")
            return False
        
        size_mb = self.master_file.stat().st_size / (1024 * 1024)
        print(f"✅ Arquivo encontrado: {self.master_file.name}")
        print(f"   Tamanho: {size_mb:.2f} MB")
        return True
    
    def upload_via_browser(self):
        """Método 1: Upload via navegador (mais confiável)"""
        print("\n" + "="*70)
        print("📤 MÉTODO 1: UPLOAD VIA NAVEGADOR")
        print("="*70)
        
        # Abrir pasta no Finder
        print("\n1️⃣ Abrindo pasta no Finder...")
        subprocess.run(['open', '-R', str(self.master_file)])
        time.sleep(1)
        
        # Abrir Google Drive no navegador
        print("2️⃣ Abrindo Google Drive no navegador...")
        webbrowser.open('https://drive.google.com/drive/my-drive')
        
        print("\n" + "─"*70)
        print("📋 INSTRUÇÕES:")
        print("─"*70)
        print("1. O Finder está aberto com o arquivo selecionado")
        print("2. O Google Drive está aberto no navegador")
        print("3. ARRASTE o arquivo 'PresbyCor_MASTER_BOOK.docx' para o navegador")
        print("   → Ou clique em '+ Novo' → 'Upload de arquivos'")
        print("\n4. Aguarde o upload completo (~5-10 minutos)")
        print("─"*70)
        
        return True
    
    def check_gdrive_cli(self):
        """Verifica se gdrive CLI está instalado"""
        try:
            result = subprocess.run(['which', 'gdrive'], 
                                  capture_output=True, 
                                  text=True)
            return result.returncode == 0
        except:
            return False
    
    def install_gdrive_cli(self):
        """Instala gdrive CLI via Homebrew"""
        print("\n📦 Instalando Google Drive CLI...")
        print("   Comando: brew install gdrive")
        
        response = input("\n⚠️  Deseja instalar gdrive CLI? (s/n): ").lower()
        if response == 's':
            try:
                subprocess.run(['brew', 'install', 'gdrive'], check=True)
                print("✅ gdrive instalado com sucesso!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Falha na instalação do gdrive")
                return False
        return False
    
    def upload_via_cli(self):
        """Método 2: Upload via CLI (automático)"""
        print("\n" + "="*70)
        print("📤 MÉTODO 2: UPLOAD AUTOMÁTICO VIA CLI")
        print("="*70)
        
        if not self.check_gdrive_cli():
            print("\n⚠️  gdrive CLI não está instalado")
            if not self.install_gdrive_cli():
                return False
        
        print("\n🔐 Autenticando com Google Drive...")
        print("   Você precisará autorizar o acesso no navegador")
        
        try:
            # Upload do arquivo
            cmd = ['gdrive', 'upload', str(self.master_file)]
            print(f"\n📤 Executando: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            print("\n✅ Upload concluído!")
            print(result.stdout)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Erro no upload: {e.stderr}")
            return False
        except FileNotFoundError:
            print("\n❌ Comando gdrive não encontrado")
            return False
    
    def create_google_docs_version(self):
        """Cria instruções para converter para Google Docs"""
        print("\n" + "="*70)
        print("📝 CONVERTER PARA GOOGLE DOCS (OPCIONAL)")
        print("="*70)
        print("\nApós o upload, você pode converter para Google Docs:")
        print("1. No Google Drive, clique com o botão direito no arquivo")
        print("2. Selecione 'Abrir com' → 'Google Docs'")
        print("3. O arquivo será aberto no Google Docs")
        print("4. Clique em 'Arquivo' → 'Salvar como Google Docs'")
        print("\n✅ Isso criará uma versão editável no Google Docs")
        print("   mantendo o arquivo Word original")
        
    def run(self):
        """Executa o processo de upload"""
        print("="*70)
        print("🚀 EXPORTADOR PARA GOOGLE DRIVE - PresbyCor")
        print("="*70)
        
        # Verificar arquivo
        if not self.check_file_exists():
            return False
        
        # Escolher método
        print("\n📋 MÉTODOS DISPONÍVEIS:")
        print("1. Upload via navegador (RECOMENDADO)")
        print("2. Upload automático via CLI (requer instalação)")
        
        choice = input("\nEscolha o método (1 ou 2): ").strip()
        
        if choice == "1":
            self.upload_via_browser()
            self.create_google_docs_version()
        elif choice == "2":
            if self.upload_via_cli():
                self.create_google_docs_version()
            else:
                print("\n⚠️  Tentando método alternativo...")
                self.upload_via_browser()
                self.create_google_docs_version()
        else:
            print("\n⚠️  Opção inválida. Usando método 1...")
            self.upload_via_browser()
            self.create_google_docs_version()
        
        print("\n" + "="*70)
        print("✅ PROCESSO CONCLUÍDO")
        print("="*70)
        print(f"\n📁 Arquivo: {self.master_file.name}")
        print(f"📊 Tamanho: {self.master_file.stat().st_size / (1024*1024):.2f} MB")
        print("\n💡 Dica: Após o upload, compartilhe o link com a editora!")
        
        return True

def main():
    base_dir = Path(__file__).parent
    uploader = GoogleDriveUploader(base_dir)
    
    try:
        uploader.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
