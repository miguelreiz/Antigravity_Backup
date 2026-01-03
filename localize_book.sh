#!/bin/bash
# Script de localização do livro PresbyCor para português lusófono

echo "🇧🇷 Aplicando localização em português nos Capítulos 5-13..."

for chap in {5..13}; do
    file="Chapter_${chap}_Complete.md"
    
    if [ -f "$file" ]; then
        echo "  📝 Processando $file..."
        
        # Backup
        cp "$file" "${file}.bak"
        
        # Substituições (case-insensitive onde apropriado)
        sed -i '' 's/wavefront aberrometry/aberrometria de frente de onda/gI' "$file"
        sed -i '' 's/wavefront pré-operatório/frente de onda pré-operatória/gI' "$file"
        sed -i '' 's/wavefront pós-operatório/frente de onda pós-operatória/gI' "$file"
        sed -i '' 's/Captura de Wavefront/Captura de Frente de Onda/g' "$file"
        sed -i '' 's/Wavefront-Optimized/Otimizado para Frente de Onda (Wavefront-Optimized)/g' "$file"
        sed -i '' 's/ wavefront / frente de onda /g' "$file"
        
        # Enhancement → Retoque cirúrgico
        sed -i '' 's/\benhancement\b/retoque cirúrgico/gI' "$file"
        sed -i '' 's/Enhancement/Retoque Cirúrgico/g' "$file"
        
        # Dry eye → Olho seco
        sed -i '' 's/dry eye/olho seco/gI' "$file"
        sed -i '' 's/Dry Eye/Olho Seco/g' "$file"
        
        # Retreatment → Retratamento
        sed -i '' 's/retreatment rate/taxa de retratamento/gI' "$file"
        sed -i '' 's/retreatment/retratamento/gI' "$file"
        sed -i '' 's/Retreatment/Retratamento/g' "$file"
        
        echo "  ✅ $file atualizado"
    fi
done

echo "✨ Localização completa!"
