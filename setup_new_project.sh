#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# SETUP RÁPIDO - PROJETO CORNEAL REMODELING
# Baseado no projeto PresbyCor
# ═══════════════════════════════════════════════════════════════

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "═══════════════════════════════════════════════════════════════"
echo "  🚀 SETUP INICIAL - CORNEAL REMODELING PROJECT"
echo "  Baseado em: PresbyCor (Dr. Miguel Reis)"
echo "═══════════════════════════════════════════════════════════════"
echo -e "${NC}"

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÕES (EDITAR AQUI)
# ═══════════════════════════════════════════════════════════════

PROJECT_NAME="Corneal_Remodeling"
PROJECT_DIR="$HOME/Documents/$PROJECT_NAME"
AUTHOR_NAME="Dr. Miguel Reis"
AUTHOR_EMAIL="miguelreis@example.com"  # ⚠️ EDITAR
NUM_CHAPTERS=13  # Número de capítulos planejados

echo -e "${YELLOW}📋 Configurações:${NC}"
echo "   Nome do Projeto: $PROJECT_NAME"
echo "   Diretório: $PROJECT_DIR"
echo "   Autor: $AUTHOR_NAME"
echo "   Capítulos: $NUM_CHAPTERS"
echo ""

# Perguntar se quer continuar
read -p "Continuar com estas configurações? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelado."
    exit 1
fi

# ═══════════════════════════════════════════════════════════════
# PASSO 1: CRIAR ESTRUTURA DE DIRETÓRIOS
# ═══════════════════════════════════════════════════════════════

echo -e "\n${GREEN}[1/7] Criando estrutura de diretórios...${NC}"

# Criar diretório principal
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Criar subdiretórios principais
mkdir -p figures
mkdir -p _Export_To_Drive
mkdir -p Sources
mkdir -p .venv

# Criar subdiretórios para cada capítulo
for i in $(seq -f "%02g" 1 $NUM_CHAPTERS); do
    mkdir -p "figures/chapter$i"
done

echo -e "${GREEN}   ✅ Estrutura criada${NC}"

# ═══════════════════════════════════════════════════════════════
# PASSO 2: CRIAR .gitignore
# ═══════════════════════════════════════════════════════════════

echo -e "\n${GREEN}[2/7] Criando .gitignore...${NC}"

cat > .gitignore << 'EOL'
# MacOS
.DS_Store
.AppleDouble
.LSOverride
._*

# Thumbnails
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent

# Editor backups
*~
*.swp
*.swo
*.bak

# Word temporary files
~$*.doc*
~$*.xls*
*.tmp

# Python
.venv/
__pycache__/
*.pyc

# Binários grandes
pandoc-*/
*.exe
*.dmg
*.pkg

# Uploads temporários
.tmp.driveupload/

# Build outputs (comentar se quiser versionar)
# *.pdf
# *.epub
# *.docx
EOL

echo -e "${GREEN}   ✅ .gitignore criado${NC}"

# ═══════════════════════════════════════════════════════════════
# PASSO 3: INICIALIZAR GIT
# ═══════════════════════════════════════════════════════════════

echo -e "\n${GREEN}[3/7] Inicializando Git...${NC}"

git init
git config user.name "$AUTHOR_NAME"
git config user.email "$AUTHOR_EMAIL"

echo -e "${GREEN}   ✅ Git inicializado${NC}"

# ═══════════════════════════════════════════════════════════════
# PASSO 4: CRIAR DOCUMENTAÇÃO BASE
# ═══════════════════════════════════════════════════════════════

echo -e "\n${GREEN}[4/7] Criando documentação base...${NC}"

# README.md
cat > README.md << EOL
# $PROJECT_NAME

Livro técnico sobre remodelamento corneano e cirurgia refrativa.

## Estrutura

Este livro está organizado em:
- Prefácio e Metodologia
- $NUM_CHAPTERS Capítulos principais
- Glossário e Abreviações
- Bibliografia

Veja o arquivo [README_Book_Structure.md](README_Book_Structure.md) para estrutura detalhada.

## Workflow

- **Versionamento:** Git + GitHub
- **Visualização:** scripts em Python
- **Exportação:** DOCX via Pandoc

## Autor

**$AUTHOR_NAME**

---

**Última Atualização:** $(date '+%Y-%m-%d')  
**Versão:** 0.1 (Setup Inicial)
EOL

# PROGRESS.md
cat > PROGRESS.md << EOL
# PROJECT PROGRESS DASHBOARD
Última atualização: $(date '+%Y-%m-%d')

## Status dos Capítulos

| Capítulo | Status | Palavras | Imagens | Referências | Última Edição |
|----------|--------|----------|---------|-------------|---------------|
EOL

for i in $(seq -f "%02g" 1 $NUM_CHAPTERS); do
    echo "| $i       | 🆕 0%   | 0       | 0       | 0           | -             |" >> PROGRESS.md
done

cat >> PROGRESS.md << 'EOL'

**Legenda:**
- ✅ Finalizado
- 🔄 Em revisão
- 📝 Em redação
- 🆕 Iniciado
- ⬜ Não iniciado

## Próximas Tarefas

- [ ] Definir estrutura dos capítulos
- [ ] Iniciar Capítulo 1
- [ ] Configurar GitHub (opcional)

## Comandos Úteis

```bash
# Ver status
./check_status.sh

# Salvar progresso
git add . && git commit -m "Descrição"

# Gerar DOCX
python3 export_to_drive.py
```
EOL

# Master TOC
cat > Master_TOC.md << EOL
# $PROJECT_NAME - Índice Geral

## Elementos Iniciais

1. Prefácio e Metodologia

## Capítulos Principais
EOL

for i in $(seq 1 $NUM_CHAPTERS); do
    printf "%2d. Capítulo %02d - [TÍTULO A DEFINIR]\n" $i $i >> Master_TOC.md
done

cat >> Master_TOC.md << 'EOL'

## Elementos Finais

- Bibliografia Consolidada
- Glossário e Abreviações
- Sobre o Autor

---

**Total:** Prefácio + XX Capítulos + 3 Elementos Finais
EOL

echo -e "${GREEN}   ✅ Documentação criada${NC}"

# ═══════════════════════════════════════════════════════════════
# PASSO 5: CRIAR SCRIPTS DE AUTOMAÇÃO
# ═══════════════════════════════════════════════════════════════

echo -e "\n${GREEN}[5/7] Criando scripts de automação...${NC}"

# check_status.sh
cat > check_status.sh << 'EOL'
#!/bin/bash

echo "═══════════════════════════════════════════════════"
echo "  📊 CORNEAL REMODELING - PROJECT STATUS"
echo "═══════════════════════════════════════════════════"
echo ""

# Contar capítulos
echo "📚 CAPÍTULOS:"
total_chapters=$(ls -1 Chapter_*_Complete.md 2>/dev/null | wc -l | tr -d ' ')
echo "   Total: $total_chapters capítulos"
echo ""

# Contar palavras
echo "✍️  PALAVRAS:"
if ls Chapter_*_Complete.md 1> /dev/null 2>&1; then
    total_words=$(wc -w Chapter_*_Complete.md 2>/dev/null | tail -1 | awk '{print $1}')
    echo "   Total: $total_words palavras"
else
    echo "   Total: 0 palavras (nenhum capítulo ainda)"
fi
echo ""

# Contar imagens
echo "🖼️  IMAGENS:"
total_images=$(find figures/ -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
echo "   Total: $total_images imagens"
echo ""

# Git status
echo "📦 GIT STATUS:"
if [ -d .git ]; then
    git status --short
    if [ -z "$(git status --short)" ]; then
        echo "   ✅ Nenhuma mudança pendente"
    fi
else
    echo "   ⚠️  Git não inicializado"
fi
echo ""

# Último commit
echo "🕒 ÚLTIMO COMMIT:"
if [ -d .git ]; then
    git log --oneline -1 2>/dev/null || echo "   (nenhum commit ainda)"
else
    echo "   (Git não inicializado)"
fi
echo ""

echo "═══════════════════════════════════════════════════"
EOL

chmod +x check_status.sh

# package_images.py (simplificado)
cat > package_images.py << 'EOL'
import os
import shutil
import glob

def package_images():
    source_root = "figures"
    dest_root = "_Export_To_Drive/ENTREGA_IMAGENS_FINAL"
    
    # Setup Destination
    if os.path.exists(dest_root):
        shutil.rmtree(dest_root)
    os.makedirs(dest_root, exist_ok=True)
    
    print(f"📦 Empacotando imagens: {source_root} -> {dest_root}")
    
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.tiff']
    total_copied = 0
    
    # Get all chapter directories
    chapters = [d for d in os.listdir(source_root) 
                if os.path.isdir(os.path.join(source_root, d))]
    
    for chapter in sorted(chapters):
        chapter_source = os.path.join(source_root, chapter)
        chapter_dest = os.path.join(dest_root, chapter)
        
        # Find images
        images = []
        for ext in image_extensions:
            images.extend(glob.glob(os.path.join(chapter_source, ext)))
            
        if images:
            os.makedirs(chapter_dest, exist_ok=True)
            print(f"  📂 {chapter} ({len(images)} imagens)")
            
            for img_path in sorted(images):
                img_name = os.path.basename(img_path)
                dest_path = os.path.join(chapter_dest, img_name)
                shutil.copy2(img_path, dest_path)
                total_copied += 1

    print(f"\n✅ SUCESSO! {total_copied} imagens copiadas para {dest_root}")

if __name__ == "__main__":
    package_images()
EOL

echo -e "${GREEN}   ✅ Scripts criados${NC}"

# ═══════════════════════════════════════════════════════════════
# PASSO 6: PRIMEIRO COMMIT
# ═══════════════════════════════════════════════════════════════

echo -e "\n${GREEN}[6/7] Criando primeiro commit...${NC}"

git add .
git commit -m "Initial commit: Project structure setup"

echo -e "${GREEN}   ✅ Commit inicial criado${NC}"

# ═══════════════════════════════════════════════════════════════
# PASSO 7: RESUMO E PRÓXIMOS PASSOS
# ═══════════════════════════════════════════════════════════════

echo -e "\n${GREEN}[7/7] Setup completo!${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ PROJETO CRIADO COM SUCESSO!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📁 Localização:${NC}"
echo "   $PROJECT_DIR"
echo ""
echo -e "${YELLOW}📊 Estrutura criada:${NC}"
tree -L 2 "$PROJECT_DIR" 2>/dev/null || ls -la "$PROJECT_DIR"
echo ""
echo -e "${YELLOW}🚀 Próximos Passos:${NC}"
echo ""
echo "1. Navegar para o projeto:"
echo "   ${BLUE}cd $PROJECT_DIR${NC}"
echo ""
echo "2. Ver status do projeto:"
echo "   ${BLUE}./check_status.sh${NC}"
echo ""
echo "3. Criar primeiro capítulo:"
echo "   ${BLUE}touch Chapter_01_Complete.md${NC}"
echo "   ${BLUE}open Chapter_01_Complete.md${NC}"
echo ""
echo "4. (Opcional) Conectar ao GitHub:"
echo "   ${BLUE}# Criar repositório em github.com primeiro${NC}"
echo "   ${BLUE}git remote add origin https://github.com/USER/corneal-remodeling.git${NC}"
echo "   ${BLUE}git branch -M main${NC}"
echo "   ${BLUE}git push -u origin main${NC}"
echo ""
echo "5. Ler guia completo:"
echo "   ${BLUE}open WORKFLOW_GUIA_VERSIONAMENTO_ORGANIZACAO.md${NC}"
echo ""
echo -e "${GREEN}Bom trabalho! 🎉${NC}"
echo ""
