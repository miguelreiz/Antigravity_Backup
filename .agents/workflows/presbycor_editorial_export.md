---
description: Exportar capítulos PresbyCor para Word com padrões editoriais internacionais
---

## Pré-requisitos

Confirmar que python e pip estão instalados:
```
python --version
pip install python-docx pillow
```

## Passos de Execução

// turbo
1. Instalar dependências:
```
pip install python-docx pillow requests
```

// turbo
2. Executar o script de exportação para TODOS os capítulos:
```
python ".agents\skills\presbycor_editorial\scripts\export_chapters_to_word.py" --all
```

3. Para um capítulo específico (ex: capítulo 3):
```
python ".agents\skills\presbycor_editorial\scripts\export_chapters_to_word.py" --chapter 3
```

4. Os arquivos Word exportados estarão em `_Distributable_Book\Word_Editorial\`

5. Verificar o relatório de exportação em `_Distributable_Book\Word_Editorial\EXPORT_REPORT.txt`
