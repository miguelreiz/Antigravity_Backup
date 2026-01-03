#!/bin/bash

OUTPUT="PresbyCor_FINAL_PREVIEW.md"
echo "# PresbyCor: Modern Strategies for Presbyopia and Laser Mechanics" > "$OUTPUT"
echo "## Dr. Miguel Reis" >> "$OUTPUT"
echo "### Preview de Implantação - $(date)" >> "$OUTPUT"
echo "" >> "$OUTPUT"

FILES=(
    "Preface_Methodology.md"
    "Chapter_1_Complete.md"
    "Chapter_2_Complete.md"
    "Chapter_3_Complete.md"
    "Chapter_4_Complete.md"
    "Chapter_5_Complete.md"
    "Chapter_6_Complete.md"
    "Chapter_7_Complete.md"
    "Chapter_8_Complete.md"
    "Chapter_9_Complete.md"
    "Chapter_10_Complete.md"
    "Chapter_11_Complete.md"
    "Chapter_12_Complete.md"
    "Chapter_13_Complete.md"
    "Bibliography_Consolidated.md"
    "Glossary_Abbreviations.md"
    "Appendices_Technical.md"
    "About_Author.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        echo "" >> "$OUTPUT"
        echo "<!-- START OF $file -->" >> "$OUTPUT"
        echo "" >> "$OUTPUT"
        cat "$file" >> "$OUTPUT"
        echo "" >> "$OUTPUT"
        echo "<!-- END OF $file -->" >> "$OUTPUT"
        echo "---" >> "$OUTPUT"
    else
        echo "WARNING: $file not found!"
    fi
done

echo "✅ Book consolidated into $OUTPUT"
