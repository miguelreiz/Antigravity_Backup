# GUIA COMPLETO: Versionamento, Organização e Visualização de Projetos de Livro Médico

**Baseado no Projeto:** PresbyCor: Modern Strategies for Presbyopia  
**Data:** Janeiro 2026  
**Objetivo:** Documentar comandos e práticas para replicar no projeto "Corneal Remodeling"

---

## 📋 TABELA DE CONTEÚDOS

1. [Estrutura de Organização](#1-estrutura-de-organização)
2. [Sistema de Versionamento Git](#2-sistema-de-versionamento-git)
3. [Scripts de Automação](#3-scripts-de-automação)
4. [Visualização e Monitoramento](#4-visualização-e-monitoramento)
5. [Workflow Diário Recomendado](#5-workflow-diário-recomendado)
6. [Integração com Google Drive](#6-integração-com-google-drive)
7. [Checklist de Setup Inicial](#7-checklist-de-setup-inicial)

---

## 1. ESTRUTURA DE ORGANIZAÇÃO

### 1.1 Arquitetura de Diretórios

```
Corneal_Remodeling/
├── .git/                           # Versionamento Git
├── .gitignore                      # Arquivos a ignorar
│
├── README.md                       # Visão geral do projeto
├── README_Book_Structure.md        # Estrutura detalhada
├── README_SETUP.md                 # Guia de instalação
│
├── Chapter_01_Complete.md          # Capítulos finalizados
├── Chapter_02_Complete.md
├── ...
│
├── figures/                        # TODAS as imagens do livro
│   ├── chapter1/                   # Organizadas por capítulo
│   │   ├── infographic_1_1_xxx.md  # Descrição em Markdown
│   │   └── infographic_1_1_xxx.png # Imagem gerada
│   ├── chapter2/
│   └── ...
│
├── _Export_To_Drive/               # Outputs para distribuição
│   ├── ENTREGA_IMAGENS_FINAL/      # Imagens empacotadas
│   └── Corneal_Remodeling_MASTER.docx
│
├── Bibliography_Consolidated.md   # Bibliografia única
├── Glossary_Abbreviations.md      # Glossário
├── About_Author.md                # Sobre o autor
│
├── *.py                           # Scripts de automação
├── *.sh                           # Shell scripts
└── .venv/                         # Python virtual environment

```

### 1.2 Convenções de Nomenclatura

**Arquivos de Capítulos:**
- `Chapter_01_Complete.md` (sempre com zero à esquerda, sempre "Complete")

**Imagens:**
- `infographic_1_1_nome_descritivo.png` (capítulo_número_descrição)
- `diagram_3_5_mechanism_xxx.png`
- `flowchart_12_2_decision_tree.png`

**Descrições de Infográficos:**
- `infographic_1_1_nome_descritivo.md` (mesmo nome da imagem, extensão .md)

---

## 2. SISTEMA DE VERSIONAMENTO GIT

### 2.1 Configuração Inicial

```bash
# Navegar para o diretório do projeto
cd /Users/miguelreis/Documents/Corneal_Remodeling

# Inicializar repositório Git
git init

# Configurar usuário (APENAS uma vez por projeto)
git config user.name "Dr. Miguel Reis"
git config user.email "seuemail@exemplo.com"

# Criar .gitignore (veja template abaixo)
# Adicionar todos os arquivos
git add .

# Primeiro commit
git commit -m "Initial commit: Project structure setup"
```

### 2.2 Template .gitignore

Criar arquivo `.gitignore` na raiz do projeto:

```gitignore
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

# Build outputs (comentar se quiser versionar PDFs)
# *.pdf
# *.epub
# *.docx

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
```

### 2.3 Conectar ao GitHub (opcional mas recomendado)

```bash
# Criar repositório no GitHub (via navegador)
# Depois conectar:

git remote add origin https://github.com/SEU_USUARIO/corneal-remodeling.git

# Verificar conexão
git remote -v

# Enviar pela primeira vez
git branch -M main
git push -u origin main
```

### 2.4 Comandos Git Essenciais Diários

```bash
# ============================================
# WORKFLOW DIÁRIO (executar no diretório raiz)
# ============================================

# 1. VER STATUS (o que mudou desde o último commit)
git status

# 2. VER DIFERENÇAS DETALHADAS
git diff                    # Ver mudanças linha por linha
git diff --stat             # Ver resumo de arquivos modificados

# 3. ADICIONAR MUDANÇAS
git add .                   # Adicionar TUDO
git add Chapter_03_Complete.md  # Adicionar arquivo específico
git add figures/chapter3/       # Adicionar pasta específica

# 4. SALVAR MUDANÇAS (Commit)
git commit -m "Cap 3: Adicionadas referências Ambrosio"

# 5. ENVIAR PARA GITHUB (se configurado)
git push origin main

# ============================================
# COMANDOS DE VISUALIZAÇÃO
# ============================================

# Ver histórico de commits (últimos 10)
git log --oneline -10

# Ver histórico completo com gráfico
git log --graph --oneline --all

# Ver quem modificou cada linha de um arquivo
git blame Chapter_05_Complete.md

# ============================================
# COMANDOS DE RECUPERAÇÃO (SEGURANÇA)
# ============================================

# Desfazer mudanças NÃO comitadas em um arquivo
git restore Chapter_03_Complete.md

# Ver diferenças entre commits
git diff HEAD~1 HEAD        # Comparar último commit com anterior

# Voltar para um commit anterior (CUIDADO!)
git log --oneline           # Ver lista de commits
git checkout abc1234        # Voltar para commit específico (modo "detached")
git checkout main           # Voltar para versão atual
```

### 2.5 Script de Auto-Sincronização (Avançado)

Usar o script `auto_sync.sh` para sincronizar automaticamente a cada 3 horas:

```bash
#!/bin/bash
# Arquivo: auto_sync.sh

# Configuração
INTERVAL=10800  # 3 horas em segundos
BRANCH="main"

echo "=== Iniciando Sincronização Automática com GitHub (A cada 3 horas) ==="
echo "Pressione CTRL+C para parar o script."

while true; do
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo ""
    echo "[$TIMESTAMP] 🔄 Verificando atualizações..."

    # 1. Pull changes from remote
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
```

**Para usar:**

```bash
# Tornar executável
chmod +x auto_sync.sh

# Executar (deixar rodando em terminal)
./auto_sync.sh

# Para parar: CTRL+C
```

---

## 3. SCRIPTS DE AUTOMAÇÃO

### 3.1 Package Images (Empacotar Imagens)

**Arquivo:** `package_images.py`

**O que faz:**
- Copia TODAS as imagens de `figures/` para `_Export_To_Drive/ENTREGA_IMAGENS_FINAL/`
- Organiza por capítulo
- Cria um manifesto CSV com lista de imagens

**Como usar:**

```bash
python3 package_images.py
```

**Quando usar:**
- Antes de enviar imagens para editor
- Ao finalizar um capítulo
- Antes de backup

### 3.2 Export to Drive (Exportar para Google Drive)

**Arquivo:** `export_to_drive.py`

**O que faz:**
- Combina todos os capítulos em um único arquivo Markdown
- Converte para DOCX usando Pandoc
- Salva em `_Export_To_Drive/`

**Como usar:**

```bash
python3 export_to_drive.py
```

### 3.3 Generate Master Book (Gerar Livro Completo)

**Arquivo:** `generate_master_book.py`

**O que faz:**
- Combina Prefácio + Capítulos + Bibliografia + Glossário
- Gera arquivo único `PresbyCor_MASTER_BOOK.md`
- Converte para DOCX com formatação

**Como usar:**

```bash
python3 generate_master_book.py
```

### 3.4 Publish Version (Publicar Versão)

**Arquivo:** `publish_version.py`

**O que faz:**
- Cria tag de versão no Git
- Gera DOCX e PDF
- Cria zip com todos os arquivos
- Registra no histórico

**Como usar:**

```bash
python3 publish_version.py --version 1.0 --message "Versão inicial finalizada"
```

---

## 4. VISUALIZAÇÃO E MONITORAMENTO

### 4.1 Comandos de Visualização de Progresso

```bash
# ============================================
# CONTAGEM DE PALAVRAS POR CAPÍTULO
# ============================================

# Contar palavras em um capítulo
wc -w Chapter_03_Complete.md

# Contar palavras em TODOS os capítulos
wc -w Chapter_*_Complete.md

# Contar linhas e palavras (resumo)
wc Chapter_*_Complete.md

# ============================================
# LISTAR TODAS AS IMAGENS
# ============================================

# Contar imagens por capítulo
ls -1 figures/chapter1/*.png | wc -l
ls -1 figures/chapter2/*.png | wc -l

# Contar TODAS as imagens
find figures/ -name "*.png" | wc -l

# Listar imagens com tamanho
du -h figures/chapter3/*.png

# ============================================
# VERIFICAR REFERÊNCIAS
# ============================================

# Procurar citações não fechadas
grep -n "\[^" Chapter_*_Complete.md

# Contar referências em um capítulo
grep -o "\[^[0-9]*\]" Chapter_03_Complete.md | sort -u | wc -l

# Procurar infográficos referenciados
grep -n "infographic_" Chapter_*_Complete.md
```

### 4.2 Dashboard de Progresso (Markdown)

Criar arquivo `PROGRESS.md` na raiz:

```markdown
# PROJECT PROGRESS DASHBOARD
Última atualização: 2026-01-20

## Status dos Capítulos

| Capítulo | Status | Palavras | Imagens | Referências | Última Edição |
|----------|--------|----------|---------|-------------|---------------|
| 01       | ✅ 100% | 3.200   | 3       | 5           | 2026-01-15    |
| 02       | ✅ 100% | 4.500   | 5       | 7           | 2026-01-16    |
| 03       | 🔄 80%  | 3.800   | 4       | 6           | 2026-01-20    |
| 04       | 📝 50%  | 2.100   | 2       | 3           | 2026-01-19    |
| 05       | 🆕 10%  | 400     | 0       | 0           | 2026-01-18    |

**Legenda:**
- ✅ Finalizado
- 🔄 Em revisão
- 📝 Em redação
- 🆕 Iniciado
- ⬜ Não iniciado

## Total de Imagens Geradas

```bash
find figures/ -name "*.png" | wc -l
```

Total: **45 imagens**

## Commits Recentes

```bash
git log --oneline -5
```

## Próximas Tarefas

- [ ] Finalizar Capítulo 3 - Referências Ambrósio
- [ ] Gerar infográficos Capítulo 4
- [ ] Revisar Capítulo 2 - Correções anatômicas
```

**Atualizar com:**

```bash
# Abrir arquivo
open PROGRESS.md

# Ou editar com VSCode
code PROGRESS.md
```

### 4.3 Script de Status Automático

Criar arquivo `check_status.sh`:

```bash
#!/bin/bash

echo "═══════════════════════════════════════════════════"
echo "  📊 CORNEAL REMODELING - PROJECT STATUS"
echo "═══════════════════════════════════════════════════"
echo ""

# Contar capítulos
echo "📚 CAPÍTULOS:"
total_chapters=$(ls -1 Chapter_*_Complete.md 2>/dev/null | wc -l)
echo "   Total: $total_chapters capítulos"
echo ""

# Contar palavras
echo "✍️  PALAVRAS:"
total_words=$(wc -w Chapter_*_Complete.md 2>/dev/null | tail -1 | awk '{print $1}')
echo "   Total: $total_words palavras"
echo ""

# Contar imagens
echo "🖼️  IMAGENS:"
total_images=$(find figures/ -name "*.png" 2>/dev/null | wc -l)
echo "   Total: $total_images imagens"
echo ""

# Git status
echo "📦 GIT STATUS:"
git status --short
echo ""

# Último commit
echo "🕒 ÚLTIMO COMMIT:"
git log --oneline -1
echo ""

echo "═══════════════════════════════════════════════════"
```

**Usar:**

```bash
chmod +x check_status.sh
./check_status.sh
```

---

## 5. WORKFLOW DIÁRIO RECOMENDADO

### Rotina Matinal (5 min)

```bash
# 1. Navegar para projeto
cd /Users/miguelreis/Documents/Corneal_Remodeling

# 2. Ver status do projeto
./check_status.sh

# 3. Baixar mudanças (se trabalha em múltiplos computadores)
git pull origin main

# 4. Ver o que mudou desde ontem
git log --oneline --since="yesterday"
```

### Durante o Trabalho

```bash
# Salvar progresso a cada 1-2 horas
git add .
git commit -m "Cap 3: Adicionado tópico sobre biomecânica"

# Ver diferenças antes de commitar
git diff
```

### Rotina Noturna (5 min)

```bash
# 1. Ver resumo do dia
git log --oneline --since="6 hours ago"

# 2. Salvar tudo
git add .
git commit -m "End of day: $(date '+%Y-%m-%d')"

# 3. Enviar para GitHub (backup)
git push origin main

# 4. Gerar preview DOCX (opcional)
python3 export_to_drive.py

# 5. Atualizar dashboard
./check_status.sh > DAILY_REPORT_$(date +%Y%m%d).txt
```

### Ao Finalizar um Capítulo

```bash
# 1. Gerar imagens
python3 package_images.py

# 2. Commit especial
git add .
git commit -m "MILESTONE: Capítulo 3 finalizado"

# 3. Criar tag
git tag -a v0.3 -m "Capítulo 3 completo"
git push origin v0.3

# 4. Gerar preview
python3 generate_master_book.py
```

---

## 6. INTEGRAÇÃO COM GOOGLE DRIVE

### 6.1 Método 1: Google Drive Desktop (Recomendado)

**Setup:**

```bash
# 1. Instalar Google Drive Desktop
# 2. Mover projeto para pasta sincronizada

mv /Users/miguelreis/Documents/Corneal_Remodeling \
   ~/Google\ Drive/My\ Drive/Projects/Corneal_Remodeling

# 3. Criar link simbólico (atalho)
ln -s ~/Google\ Drive/My\ Drive/Projects/Corneal_Remodeling \
      ~/Documents/Corneal_Remodeling

# 4. Trabalhar normalmente
# Arquivos são sincronizados automaticamente!
```

### 6.2 Método 2: Script de Upload Manual

Criar arquivo `sync_to_drive.sh`:

```bash
#!/bin/bash

EXPORT_DIR="_Export_To_Drive"
DRIVE_DIR="$HOME/Google Drive/My Drive/Corneal_Remodeling_Exports"

# Criar diretório se não existir
mkdir -p "$DRIVE_DIR"

# Copiar arquivos
echo "📤 Copiando para Google Drive..."
cp -r "$EXPORT_DIR/"* "$DRIVE_DIR/"

echo "✅ Sincronização completa!"
echo "📁 Localização: $DRIVE_DIR"
```

**Usar:**

```bash
chmod +x sync_to_drive.sh
./sync_to_drive.sh
```

---

## 7. CHECKLIST DE SETUP INICIAL

### Para Novo Projeto "Corneal Remodeling"

```markdown
## 🚀 SETUP INICIAL - CORNEAL REMODELING

### Passo 1: Estrutura Base
- [ ] Criar diretório principal: `mkdir Corneal_Remodeling`
- [ ] Navegar: `cd Corneal_Remodeling`
- [ ] Criar subdiretórios:
  ```bash
  mkdir figures _Export_To_Drive Sources
  mkdir figures/chapter{01..13}
  ```

### Passo 2: Git
- [ ] Inicializar: `git init`
- [ ] Configurar usuário:
  ```bash
  git config user.name "Dr. Miguel Reis"
  git config user.email "seu@email.com"
  ```
- [ ] Criar `.gitignore` (copiar template acima)
- [ ] Primeiro commit:
  ```bash
  git add .
  git commit -m "Initial commit: Project structure"
  ```

### Passo 3: GitHub (Opcional)
- [ ] Criar repositório em github.com
- [ ] Conectar:
  ```bash
  git remote add origin https://github.com/USER/corneal-remodeling.git
  git branch -M main
  git push -u origin main
  ```

### Passo 4: Documentação Base
- [ ] Criar `README.md`
- [ ] Criar `README_Book_Structure.md`
- [ ] Criar `PROGRESS.md`

### Passo 5: Scripts
- [ ] Copiar scripts do PresbyCor:
  - `package_images.py`
  - `check_status.sh`
  - `auto_sync.sh` (se usar GitHub)

### Passo 6: Python (se usar scripts)
- [ ] Criar virtual environment:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- [ ] Instalar dependências (se necessário)

### Passo 7: Teste
- [ ] Criar capítulo teste: `touch Chapter_01_Complete.md`
- [ ] Commit teste: `git add . && git commit -m "Test"`
- [ ] Executar `./check_status.sh`

✅ **Setup completo!**
```

---

## 8. COMANDOS RÁPIDOS (CHEAT SHEET)

```bash
# ═══════════════════════════════════════════
# NAVEGAÇÃO
# ═══════════════════════════════════════════
cd ~/Documents/Corneal_Remodeling    # Ir para projeto
ls -lh                                # Listar arquivos
tree -L 2                             # Ver estrutura (se instalado)

# ═══════════════════════════════════════════
# GIT - ROTINA DIÁRIA
# ═══════════════════════════════════════════
git status                            # Ver mudanças
git add .                             # Adicionar tudo
git commit -m "Mensagem"              # Salvar
git push                              # Enviar para GitHub
git pull                              # Baixar de GitHub
git log --oneline -10                 # Ver histórico

# ═══════════════════════════════════════════
# VISUALIZAÇÃO
# ═══════════════════════════════════════════
wc -w Chapter_*_Complete.md           # Contar palavras
find figures/ -name "*.png" | wc -l   # Contar imagens
./check_status.sh                     # Dashboard completo

# ═══════════════════════════════════════════
# AUTOMAÇÃO
# ═══════════════════════════════════════════
python3 package_images.py             # Empacotar imagens
python3 generate_master_book.py       # Gerar livro completo
python3 export_to_drive.py            # Exportar DOCX

# ═══════════════════════════════════════════
# BUSCA
# ═══════════════════════════════════════════
grep -r "termo" Chapter_*.md          # Buscar em capítulos
grep -n "TODO" Chapter_*.md           # Buscar TODOs
grep -o "\[^[0-9]*\]" Chapter_03.md   # Buscar referências
```

---

## 9. TROUBLESHOOTING COMUM

### Problema: Git dá erro de "unstaged changes"

```bash
# Solução 1: Adicionar e commitar
git add .
git commit -m "Fix: Salvando mudanças"

# Solução 2: Descartar mudanças (CUIDADO!)
git restore .
```

### Problema: Conflito ao fazer `git pull`

```bash
# Solução: Salvar mudanças locais, depois baixar
git stash              # Guardar mudanças temporariamente
git pull               # Baixar de GitHub
git stash pop          # Restaurar mudanças
```

### Problema: Script Python não funciona

```bash
# Verificar Python instalado
python3 --version

# Ativar ambiente virtual (se criado)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt  # se existir
```

---

## 10. REFERÊNCIAS E RECURSOS

### Documentação Git
- [Git Básico (Português)](https://git-scm.com/book/pt-br/v2)
- [GitHub Docs](https://docs.github.com)

### Scripts Python
- Baseados no projeto PresbyCor
- Localizados em raiz do projeto

### Estrutura BaseadaEm
- Projeto: PresbyCor (Dr. Miguel Reis, 2026)
- Conversation ID: ee202e79-67e7-4763-856e-3eaf1141da0e

---

**Versão:** 1.0  
**Data:** 2026-01-20  
**Autor:** Dr. Miguel Reis  
**Uso:** Documentação para projeto Corneal Remodeling
