#!/bin/bash
# Script para converter Word para PDF com imagens no Mac

echo "🔧 Convertendo PresbyCor para PDF profissional..."

# Método: Usar Mac Automator/AppleScript para abrir no Pages e exportar
osascript << EOF
tell application "Pages"
    activate
    set theDoc to open (POSIX file "/Users/miguelreis/Downloads/Takeout/NotebookLM/PresbyCor_ Modern Strategies for Presbyopia and La/PresbyCor_COMPLETE_BOOK.docx")
    delay 3
    tell theDoc
        export to file (POSIX file "/Users/miguelreis/Desktop/PresbyCor_Complete_Book_20260103_PDF.pdf") as PDF
    end tell
    close theDoc
end tell
EOF

echo "✅ PDF criado no Desktop: PresbyCor_Complete_Book_20260103_PDF.pdf"
