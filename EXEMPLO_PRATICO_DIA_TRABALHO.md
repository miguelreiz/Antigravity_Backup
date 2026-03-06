# 📖 EXEMPLO PRÁTICO: Um Dia de Trabalho no Corneal Remodeling

**Cenário:** Você está trabalhando no Capítulo 3 sobre biomecânica corneana.  
**Data:** Segunda-feira, 09:00  
**Objetivo:** Adicionar seção sobre Ambrósio e gerar infográficos

---

## ☀️ MANHÃ - 09:00

### 1. Abrir Terminal e Navegar para Projeto

```bash
# Comando
cd ~/Documents/Corneal_Remodeling

# Output esperado
# (você está agora dentro da pasta do projeto)
```

### 2. Ver Status Geral do Projeto

```bash
# Comando
./check_status.sh

# Output esperado
═══════════════════════════════════════════════════
  📊 CORNEAL REMODELING - PROJECT STATUS
═══════════════════════════════════════════════════

📚 CAPÍTULOS:
   Total: 3 capítulos

✍️  PALAVRAS:
   Total: 8450 palavras

🖼️  IMAGENS:
   Total: 7 imagens

📦 GIT STATUS:
   ✅ Nenhuma mudança pendente

🕒 ÚLTIMO COMMIT:
   a3b8d1b End of day: 2026-01-19

═══════════════════════════════════════════════════
```

**Interpretação:**
- ✅ Projeto tem 3 capítulos (1, 2, e 3)
- ✅ Total de 8.450 palavras já escritas
- ✅ 7 imagens criadas
- ✅ Nada pendente para salvar

### 3. (Opcional) Baixar Mudanças do GitHub

```bash
# Comando (se trabalha em múltiplos computadores)
git pull

# Output esperado (se nada mudou)
Already up to date.

# OU (se houve mudanças no outro computador)
Updating a3b8d1b..f7c2e9a
Fast-forward
 Chapter_03_Complete.md | 45 ++++++++++++++++++++
 1 file changed, 45 insertions(+)
```

---

## 🖊️ DURANTE O TRABALHO - 09:30 a 11:00

### Editando o Capítulo 3

```bash
# Abrir editor
open Chapter_03_Complete.md

# OU com VS Code
code Chapter_03_Complete.md
```

**Você adiciona:**
- Seção 3.5: "Contribuições de Ambrósio"
- 3 parágrafos sobre BAD-D
- 5 referências novas

### Salvar Progresso (10:30 - depois de 1 hora)

```bash
# Ver o que mudou
git status

# Output
On branch main
Changes not staged for commit:
  modified:   Chapter_03_Complete.md

# Ver detalhes das mudanças (opcional)
git diff Chapter_03_Complete.md

# Output (exemplo)
+## 3.5 Contribuições de Ambrósio Jr.
+
+O screening de ectasia evoluiu significativamente...
+[45 linhas adicionadas]

# Salvar
git add .
git commit -m "Cap 3: Adicionada seção 3.5 sobre Ambrósio (BAD-D)"

# Output
[main f8d3c21] Cap 3: Adicionada seção 3.5 sobre Ambrósio (BAD-D)
 1 file changed, 47 insertions(+)
```

---

## 🖼️ CRIAÇÃO DE INFOGRÁFICOS - 11:00 a 12:00

### Você usa Antigravity para gerar imagens

```bash
# (Trabalho feito via Antigravity chat)
# Gera 3 imagens:
# - biomechanics_timeline.png
# - bad_d_calculation.png
# - screening_flowchart.png

# As imagens são salvas automaticamente em:
# figures/chapter3/
```

### Verificar Imagens Criadas

```bash
# Listar imagens do capítulo 3
ls -lh figures/chapter3/

# Output
-rw-r--r--  1 user  staff   245K Jan 20 11:15 biomechanics_timeline.png
-rw-r--r--  1 user  staff   312K Jan 20 11:30 bad_d_calculation.png
-rw-r--r--  1 user  staff   198K Jan 20 11:45 screening_flowchart.png

# Contar total de imagens
find figures/chapter3/ -name "*.png" | wc -l

# Output
3
```

### Salvar Imagens no Git

```bash
git add figures/chapter3/
git commit -m "Cap 3: Adicionados 3 infográficos (biomecânica)"

# Output
[main 9a2f7e3] Cap 3: Adicionados 3 infográficos (biomecânica)
 3 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 figures/chapter3/biomechanics_timeline.png
 create mode 100644 figures/chapter3/bad_d_calculation.png
 create mode 100644 figures/chapter3/screening_flowchart.png
```

---

## 🍽️ PAUSA ALMOÇO - 12:00

### Salvar Tudo Antes de Sair

```bash
# Ver status
git status

# Output (se você esqueceu algo)
Changes not staged for commit:
  modified:   Chapter_03_Complete.md

# Salvar tudo
git add .
git commit -m "Cap 3: Integradas imagens no texto"

# Enviar para GitHub (backup!)
git push

# Output
Enumerating objects: 8, done.
Counting objects: 100% (8/8), done.
To https://github.com/miguelreis/corneal-remodeling.git
   a3b8d1b..9a2f7e3  main -> main
```

**✅ Agora você pode desligar o computador com segurança!**

---

## ☕ TARDE - 14:00

### Retomar Trabalho (em OUTRO computador)

```bash
# Navegar para projeto (no outro computador)
cd ~/Documents/Corneal_Remodeling

# Baixar mudanças da manhã
git pull

# Output
Updating a3b8d1b..9a2f7e3
Fast-forward
 Chapter_03_Complete.md                           | 47 ++++++++++++++
 figures/chapter3/biomechanics_timeline.png       | Bin 0 -> 245678 bytes
 figures/chapter3/bad_d_calculation.png           | Bin 0 -> 319821 bytes
 figures/chapter3/screening_flowchart.png         | Bin 0 -> 198234 bytes
 4 files changed, 47 insertions(+)

# Ver status atualizado
./check_status.sh

# Output
📚 CAPÍTULOS:
   Total: 3 capítulos

✍️  PALAVRAS:
   Total: 8497 palavras  ⬅️ Aumentou!

🖼️  IMAGENS:
   Total: 10 imagens      ⬅️ Aumentou!
```

**✅ Tudo sincronizado automaticamente!**

---

## 📝 TARDE - Revisão e Bibliografia - 14:30 a 17:00

### Adicionar Referências

```bash
# Abrir bibliografia
open Bibliography_Consolidated.md

# Adicionar 5 novas referências sobre Ambrósio
# Salvar
```

### Verificar Citações no Texto

```bash
# Buscar todas as referências no Cap 3
grep -o "\[^[0-9]*\]" Chapter_03_Complete.md | sort -u

# Output
[^1]
[^2]
[^3]
[^8]
[^15]
[^16]
[^17]
[^18]
[^19]

# Contar quantas referências
grep -o "\[^[0-9]*\]" Chapter_03_Complete.md | sort -u | wc -l

# Output
9

# Buscar termo específico
grep -n "Ambrósio" Chapter_03_Complete.md

# Output
45:O trabalho de Ambrósio Jr. revolucionou o screening...
67:Segundo Ambrósio et al., o BAD-D demonstra...
```

### Salvar Bibliografia

```bash
git add Bibliography_Consolidated.md
git commit -m "Bibliografia: Adicionadas 5 refs sobre Ambrósio"

# Output
[main c4e7f92] Bibliografia: Adicionadas 5 refs sobre Ambrósio
 1 file changed, 15 insertions(+)
```

---

## 🏁 FIM DO DIA - 17:00

### 1. Ver Resumo do Dia

```bash
# Ver commits de hoje
git log --oneline --since="8 hours ago"

# Output
c4e7f92 Bibliografia: Adicionadas 5 refs sobre Ambrósio
9a2f7e3 Cap 3: Adicionados 3 infográficos (biomecânica)
f8d3c21 Cap 3: Adicionada seção 3.5 sobre Ambrósio (BAD-D)

# Ver estatísticas detalhadas
git log --stat --since="8 hours ago"

# Output
Chapter_03_Complete.md              | 47 +++++++++++++++++++++++++++
Bibliography_Consolidated.md         | 15 ++++++++++
figures/chapter3/biomechanics_timeline.png    | Bin 0 -> 245678 bytes
figures/chapter3/bad_d_calculation.png        | Bin 0 -> 319821 bytes
figures/chapter3/screening_flowchart.png      | Bin 0 -> 198234 bytes
5 files changed, 62 insertions(+)
```

### 2. Salvar Qualquer Mudança Restante

```bash
git add .
git commit -m "End of day: $(date '+%Y-%m-%d') - Cap 3 progresso"

# Output
[main a7b9d43] End of day: 2026-01-20 - Cap 3 progresso
 1 file changed, 3 insertions(+), 1 deletion(-)
```

### 3. Enviar para GitHub (Backup Final)

```bash
git push

# Output
To https://github.com/miguelreis/corneal-remodeling.git
   9a2f7e3..a7b9d43  main -> main

✅ Backup completo!
```

### 4. (Opcional) Gerar Preview DOCX

```bash
python3 export_to_drive.py

# Output
📄 Gerando livro completo...
✅ DOCX criado: _Export_To_Drive/Corneal_Remodeling_MASTER.docx

# Abrir para revisar
open _Export_To_Drive/Corneal_Remodeling_MASTER.docx
```

### 5. Status Final do Dia

```bash
./check_status.sh

# Output
═══════════════════════════════════════════════════
  📊 CORNEAL REMODELING - PROJECT STATUS
═══════════════════════════════════════════════════

📚 CAPÍTULOS:
   Total: 3 capítulos

✍️  PALAVRAS:
   Total: 8512 palavras  ⬅️ +62 palavras hoje

🖼️  IMAGENS:
   Total: 10 imagens      ⬅️ +3 imagens hoje

📦 GIT STATUS:
   ✅ Nenhuma mudança pendente

🕒 ÚLTIMO COMMIT:
   a7b9d43 End of day: 2026-01-20 - Cap 3 progresso

═══════════════════════════════════════════════════
```

### 6. Criar Relatório do Dia (Opcional)

```bash
# Salvar log do dia em arquivo
./check_status.sh > DAILY_REPORT_$(date +%Y%m%d).txt

# Ver arquivo criado
cat DAILY_REPORT_20260120.txt
```

---

## 🎉 MILESTONE - AO FINALIZAR CAPÍTULO 3

### Quando Cap 3 estiver 100% completo

```bash
# 1. Empacotar imagens
python3 package_images.py

# Output
📦 Empacotando imagens: figures -> _Export_To_Drive/ENTREGA_IMAGENS_FINAL
  📂 chapter1 (3 imagens)
  📂 chapter2 (4 imagens)
  📂 chapter3 (10 imagens)

✅ SUCESSO! 17 imagens copiadas.

# 2. Commit especial de milestone
git add .
git commit -m "🎉 MILESTONE: Capítulo 3 FINALIZADO (8.512 palavras, 10 imagens)"

# 3. Criar tag de versão
git tag -a v0.3 -m "Capítulo 3 completo: Avaliação Pré-Operatória"
git push origin v0.3

# Output
To https://github.com/miguelreis/corneal-remodeling.git
 * [new tag]         v0.3 -> v0.3

# 4. Gerar livro completo
python3 generate_master_book.py

# Output
📚 Gerando livro master...
✅ Livro gerado: Corneal_Remodeling_MASTER.docx (245 páginas)

# 5. Atualizar PROGRESS.md manualmente
open PROGRESS.md
# Mudar linha do Cap 3:
# | 03  | 🆕 0%   | 0     | 0  | 0  | -        |
# PARA:
# | 03  | ✅ 100% | 8.512 | 10 | 9  | 2026-01-20 |
```

---

## 📊 RESUMO DO DIA

**O que foi feito:**
- ✅ Adicionada seção 3.5 (Ambrósio): 47 linhas
- ✅ Criados 3 infográficos
- ✅ Adicionadas 5 referências bibliográficas
- ✅ 4 commits realizados
- ✅ Backup no GitHub
- ✅ Preview DOCX gerado

**Comandos mais usados hoje:**
```
git status          (10x)
git add .           (4x)
git commit          (4x)
git push            (2x)
./check_status.sh   (3x)
```

**Progresso:**
- Palavras: 8.450 → 8.512 (+62)
- Imagens: 7 → 10 (+3)
- Capítulo 3: 85% → 100% ✅

---

## 💡 LIÇÕES APRENDIDAS

1. **Salve frequentemente** (a cada 1-2h)
2. **Mensagens descritivas** ajudam depois
3. **`git push` sempre** antes de fechar laptop
4. **`./check_status.sh`** mostra progresso motivador
5. **Tags** marcam milestones importantes

---

**Data:** 2026-01-20  
**Projeto:** Corneal Remodeling  
**Baseado em:** PresbyCor Workflow
