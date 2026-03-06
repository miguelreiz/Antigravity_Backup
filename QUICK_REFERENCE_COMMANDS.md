# 📋 QUICK REFERENCE CARD
# Comandos Essenciais - Versionamento e Organização de Projetos de Livro

## 🚀 SETUP INICIAL (uma vez só)

```bash
# Opção A: Setup automático (RECOMENDADO)
cd ~/Downloads/Takeout/NotebookLM/PresbyCor*/
./setup_new_project.sh

# Opção B: Setup manual
mkdir -p ~/Documents/Corneal_Remodeling
cd ~/Documents/Corneal_Remodeling
git init
git config user.name "Seu Nome"
git config user.email "seu@email.com"
```

---

## 📅 ROTINA DIÁRIA

### Manhã (início do trabalho)
```bash
cd ~/Documents/Corneal_Remodeling
git pull                    # Baixar mudanças
./check_status.sh           # Ver status do projeto
```

### Durante o trabalho (a cada 1-2h)
```bash
git add .
git commit -m "Descrição do que fez"
```

### Noite (fim do trabalho)
```bash
git add .
git commit -m "End of day: $(date '+%Y-%m-%d')"
git push                    # Enviar para GitHub
```

---

## 🔍 COMANDOS DE VISUALIZAÇÃO

```bash
# Status geral do projeto
./check_status.sh

# Ver mudanças não salvas
git status
git diff

# Contar palavras
wc -w Chapter_*_Complete.md

# Contar imagens
find figures/ -name "*.png" | wc -l

# Ver histórico de commits
git log --oneline -10
```

---

## 💾 COMANDOS GIT ESSENCIAIS

```bash
# Ver o que mudou
git status                  # Resumo
git diff                    # Detalhado linha por linha

# Salvar mudanças
git add .                   # Adicionar TUDO
git add arquivo.md          # Adicionar arquivo específico
git commit -m "Mensagem"    # Salvar com descrição

# Sincronizar com GitHub
git push                    # Enviar
git pull                    # Baixar

# Ver histórico
git log --oneline -10       # Últimos 10 commits
git log --graph --all       # Com gráfico visual
```

---

## 🔧 SCRIPTS DE AUTOMAÇÃO

```bash
# Ver status do projeto
./check_status.sh

# Empacotar imagens para entrega
python3 package_images.py

# Gerar livro completo em DOCX
python3 generate_master_book.py

# Sincronização automática (deixar rodando)
./auto_sync.sh
```

---

## 📊 ANÁLISE E BUSCA

```bash
# Buscar termo nos capítulos
grep -r "termo" Chapter_*.md

# Buscar TODOs
grep -n "TODO" Chapter_*.md

# Contar referências em um capítulo
grep -o "\[^[0-9]*\]" Chapter_03_Complete.md | wc -l

# Ver arquivos modificados recentemente
ls -lt Chapter_*.md | head -5
```

---

## 🎯 MILESTONES (ao finalizar capítulo)

```bash
# 1. Empacotar imagens
python3 package_images.py

# 2. Commit especial
git add .
git commit -m "MILESTONE: Capítulo 3 finalizado"

# 3. Criar tag de versão
git tag -a v0.3 -m "Capítulo 3 completo"
git push origin v0.3

# 4. Gerar preview
python3 generate_master_book.py
```

---

## 🆘 TROUBLESHOOTING

```bash
# Desfazer mudanças NÃO salvas
git restore arquivo.md

# Guardar mudanças temporariamente (ao fazer pull)
git stash                   # Guardar
git pull                    # Baixar novidades
git stash pop               # Restaurar mudanças

# Ver diferença entre commits
git diff HEAD~1 HEAD

# Voltar para versão anterior (CUIDADO!)
git log --oneline           # Ver lista
git checkout abc1234        # Voltar (modo visualização)
git checkout main           # Voltar ao presente
```

---

## 📁 ESTRUTURA DE ARQUIVOS

```
Projeto/
├── Chapter_01_Complete.md      # Capítulos (sempre "Complete")
├── Chapter_02_Complete.md
├── figures/                    # TODAS as imagens
│   ├── chapter1/
│   │   ├── infographic_1_1_xxx.png
│   │   └── infographic_1_1_xxx.md
│   └── chapter2/
├── _Export_To_Drive/           # Outputs (DOCX, PDF)
├── Bibliography_Consolidated.md
├── Glossary_Abbreviations.md
├── README.md
├── PROGRESS.md
└── *.py, *.sh                  # Scripts
```

---

## 🔗 CONECTAR AO GITHUB (uma vez)

```bash
# 1. Criar repositório em github.com
# 2. Conectar:
git remote add origin https://github.com/USER/projeto.git
git branch -M main
git push -u origin main

# Depois, usar apenas:
git push    # Enviar
git pull    # Baixar
```

---

## 💡 DICAS

- **Commitar frequentemente** (a cada 1-2h)
- **Mensagens descritivas**: "Cap 3: Adicionadas refs Ambrósio"
- **Usar tags** para milestones: `git tag v1.0`
- **Backup** sempre no GitHub: `git push`
- **Ver status** antes de commitar: `git status`

---

## 📖 DOCUMENTAÇÃO COMPLETA

```bash
# Abrir guia completo
open WORKFLOW_GUIA_VERSIONAMENTO_ORGANIZACAO.md
```

---

**Versão:** 1.0  
**Projeto Base:** PresbyCor (Dr. Miguel Reis)  
**Data:** 2026-01-20
