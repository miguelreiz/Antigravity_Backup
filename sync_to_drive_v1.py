#!/usr/bin/env python3
"""
Script de Sincronização PresbyCor v1.0.1 → Google Drive
Sincroniza a versão mais recente do livro completo
"""

import os
import subprocess
import webbrowser
import time
from pathlib import Path

def sync_latest_version():
    """
    Sincroniza a versão mais recente (v1.0.1) para o Google Drive
    """
    
    base_dir = Path(__file__).parent
    export_dir = base_dir / "_Export_To_Drive"
    
    # Arquivo mais recente
    latest_file = export_dir / "PresbyCor_v1.0.1_20260116_1030.docx"
    
    print("="*80)
    print("🚀 SINCRONIZAÇÃO GOOGLE DRIVE - PresbyCor v1.0.1")
    print("="*80)
    
    # Verificar se o arquivo existe
    if not latest_file.exists():
        print(f"\n❌ ERRO: Arquivo não encontrado:")
        print(f"   {latest_file}")
        return False
    
    # Informações do arquivo
    size_mb = latest_file.stat().st_size / (1024 * 1024)
    print(f"\n✅ Arquivo localizado:")
    print(f"   📄 Nome: {latest_file.name}")
    print(f"   📊 Tamanho: {size_mb:.2f} MB")
    print(f"   📅 Versão: 1.0.1 (16 Janeiro 2026)")
    
    # Abrir pasta no Finder
    print(f"\n🔍 Abrindo pasta no Finder...")
    subprocess.run(['open', '-R', str(latest_file)])
    time.sleep(1.5)
    
    # Abrir Google Drive
    print("🌐 Abrindo Google Drive no navegador...")
    webbrowser.open('https://drive.google.com/drive/my-drive')
    time.sleep(1)
    
    # Instruções
    print("\n" + "─"*80)
    print("📋 INSTRUÇÕES DE UPLOAD:")
    print("─"*80)
    print("\n1️⃣ O Finder está aberto com o arquivo selecionado")
    print("   → Arquivo: PresbyCor_v1.0.1_20260116_1030.docx")
    print("\n2️⃣ O Google Drive está aberto no navegador")
    print("\n3️⃣ ARRASTE o arquivo para a janela do Google Drive")
    print("   → OU clique em '+ Novo' → 'Upload de arquivos'")
    print("\n4️⃣ Aguarde o upload completo (~5-10 minutos para 27 MB)")
    print("\n5️⃣ (OPCIONAL) Converter para Google Docs:")
    print("   → Clique com botão direito no arquivo")
    print("   → 'Abrir com' → 'Google Docs'")
    print("   → 'Arquivo' → 'Salvar como Google Docs'")
    
    print("\n" + "─"*80)
    print("💡 DICA: Após o upload, compartilhe o link para colaboração!")
    print("="*80)
    
    return True

def main():
    try:
        result = sync_latest_version()
        if result:
            print("\n✅ Processo de sincronização iniciado com sucesso!")
            print("\n⏳ Aguardando conclusão do upload manual...")
        else:
            print("\n❌ Erro ao iniciar sincronização")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
