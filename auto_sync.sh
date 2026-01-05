#!/bin/bash

# Configuration
INTERVAL=10800 # 3 hours in seconds
BRANCH="main"

echo "=== Iniciando Sincronização Automática com GitHub (A cada 3 horas) ==="
echo "Pressione CTRL+C para parar o script."

while true; do
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo ""
    echo "[$TIMESTAMP] 🔄 Verificando atualizações..."

    # 1. Pull changes from remote (Download edits from other locations)
    echo "[$TIMESTAMP] ⬇️  Baixando alterações remotas (Git Pull)..."
    git pull origin $BRANCH --no-edit
    
    # 2. Add all local changes
    echo "[$TIMESTAMP] ➕ Adicionando arquivos locais..."
    git add .

    # 3. Commit changes (if any)
    if git diff-index --quiet HEAD --; then
        echo "[$TIMESTAMP] ℹ️  Nenhuma alteração local para enviar."
    else
        echo "[$TIMESTAMP] 📦 Salvando alterações locais (Commit)..."
        git commit -m "Auto-sync: $TIMESTAMP"
        
        # 4. Push changes to remote
        echo "[$TIMESTAMP] ⬆️  Enviando para o GitHub (Git Push)..."
        git push origin $BRANCH
        echo "[$TIMESTAMP] ✅ Sincronização concluída com sucesso."
    fi

    echo "[$TIMESTAMP] ⏳ Aguardando 3 horas para a próxima sincronização..."
    sleep $INTERVAL
done
