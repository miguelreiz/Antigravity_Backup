# 📤 Guia: Como Salvar no Google Drive

## 📍 Localização Atual do Arquivo

**Caminho completo:**
```
/Users/miguelreis/Downloads/Takeout/NotebookLM/PresbyCor_ Modern Strategies for Presbyopia and La/_Export_To_Drive/PresbyCor_MASTER_BOOK.docx
```

**Tamanho:** 45 MB  
**Status:** ✅ Arquivo pronto para upload

---

## 🚀 Opções para Salvar no Google Drive

### **OPÇÃO 1: Upload Manual (Mais Simples) ⭐ RECOMENDADO**

#### Passo a Passo:

1. **Abra o Finder** (já deve estar aberto com o arquivo selecionado)
   - Ou navegue manualmente até: `Downloads/Takeout/NotebookLM/PresbyCor_ Modern Strategies for Presbyopia and La/_Export_To_Drive/`

2. **Acesse o Google Drive no navegador**
   - Abra: https://drive.google.com
   - Faça login com sua conta Google

3. **Crie uma pasta (opcional mas recomendado)**
   - Clique em **"+ Novo"** → **"Nova pasta"**
   - Nome sugerido: `PresbyCor - Livro Final`

4. **Faça o Upload**
   - Arraste o arquivo `PresbyCor_MASTER_BOOK.docx` do Finder para a janela do Google Drive
   - **OU** clique em **"+ Novo"** → **"Upload de arquivos"** → Selecione o arquivo

5. **Aguarde o Upload Completo**
   - Por ser 45 MB, levará alguns minutos
   - Você verá uma barra de progresso no canto inferior direito

6. **Confirme o Upload**
   - O arquivo aparecerá na pasta do Google Drive
   - Verifique se o tamanho está correto (45 MB)

---

### **OPÇÃO 2: Google Drive Desktop (Se Instalado)**

Se você tiver o **Google Drive for Desktop** instalado:

1. **Localize a pasta do Google Drive**
   - Normalmente em: `~/Google Drive/My Drive/`
   - Ou verifique no ícone do Google Drive na barra de menu

2. **Copie o arquivo**
   ```bash
   # Execute no terminal:
   cp "/Users/miguelreis/Downloads/Takeout/NotebookLM/PresbyCor_ Modern Strategies for Presbyopia and La/_Export_To_Drive/PresbyCor_MASTER_BOOK.docx" ~/Google\ Drive/My\ Drive/
   ```

3. **Aguarde a sincronização**
   - O ícone do Google Drive mostrará o status
   - Sincronização automática ocorrerá em poucos minutos

---

### **OPÇÃO 3: Linha de Comando com rclone (Avançado)**

Se você tiver `rclone` configurado:

```bash
# Instalar rclone (se não tiver)
brew install rclone

# Configurar Google Drive
rclone config

# Fazer upload
rclone copy "/Users/miguelreis/Downloads/Takeout/NotebookLM/PresbyCor_ Modern Strategies for Presbyopia and La/_Export_To_Drive/PresbyCor_MASTER_BOOK.docx" gdrive:PresbyCor/
```

---

## 📋 Checklist Pós-Upload

Após fazer o upload, verifique:

- [ ] Arquivo aparece no Google Drive
- [ ] Tamanho está correto (45 MB)
- [ ] Nome está correto: `PresbyCor_MASTER_BOOK.docx`
- [ ] Arquivo abre corretamente no Google Docs ou Word Online
- [ ] Todas as imagens estão visíveis
- [ ] Índice está funcionando

---

## 🔗 Compartilhamento com a Editora

Após o upload no Google Drive:

1. **Clique com botão direito** no arquivo
2. Selecione **"Compartilhar"**
3. Adicione o email da editora
4. Defina permissões:
   - **"Editor"** - se a editora precisar fazer alterações
   - **"Visualizador"** - apenas para leitura
5. Clique em **"Enviar"**

Ou gere um **link de compartilhamento**:
- Clique em **"Copiar link"**
- Envie o link para a editora

---

## ⚡ Atalho Rápido

**Comando para abrir o diretório no Finder:**
```bash
open "/Users/miguelreis/Downloads/Takeout/NotebookLM/PresbyCor_ Modern Strategies for Presbyopia and La/_Export_To_Drive"
```

**Comando para abrir o Google Drive no navegador:**
```bash
open "https://drive.google.com/drive/my-drive"
```

---

## 📞 Suporte

Se encontrar problemas:

1. **Arquivo muito grande?**
   - 45 MB está dentro do limite do Google Drive (até 5 TB por conta gratuita)
   - Upload pode levar 5-10 minutos dependendo da conexão

2. **Erro de upload?**
   - Verifique conexão com internet
   - Tente novamente
   - Ou divida em capítulos individuais (já disponíveis na mesma pasta)

3. **Google Drive Desktop não instalado?**
   - Download: https://www.google.com/drive/download/
   - Não é necessário para a Opção 1 (upload manual)

---

**📌 O Finder já deve estar aberto com o arquivo selecionado!**  
Agora é só arrastar para https://drive.google.com 🚀
