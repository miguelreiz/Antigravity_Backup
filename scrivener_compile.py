import os
import subprocess
import glob

def scrivener_compile(output_dir="_Distributable_Book", book_title="PresbyCor_Strategies", author="Dr. Miguel Reis"):
    """
    Simulates Scrivener's 'Compile' function.
    Generates:
    1. Golden Master DOCX (for KDP/Print)
    2. EPUB (for E-readers/Apple Books)
    
    New Features:
    - Auto-detects 'Cover.png' or 'cover.jpg'
    - Injects 'Comparative Analysis' section from figures/comparative
    """
    
    # 1. Setup Output Directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 2. Find Chapter Files in Order
    chapter_files = glob.glob("Chapter_*_Complete.md")
    
    def sort_key(filename):
        try:
            parts = filename.split('_')
            num_part = parts[1]
            if "Plus" in num_part: return 5.5
            return float(num_part)
        except: return 999 

    chapter_files = sorted(chapter_files, key=sort_key)

    if not chapter_files:
        print("No chapter files found.")
        return

    print(f"📖 Scrivener Compiler: Found {len(chapter_files)} chapters.")

    # 3. Look for Cover
    cover_image = None
    possible_covers = ["figures/cover/presbycor_cover.png", "Cover.png", "cover.png", "Cover.jpg", "cover.jpg", "figures/cover/Cover.png"]
    for c in possible_covers:
        if os.path.exists(c):
            cover_image = c
            print(f"🎨 Cover Found: {cover_image}")
            break
    
    if not cover_image:
        print("⚠️  No cover image found. Proceeding without it.")

    # 4. Concatenate Markdown (The Manuscript)
    master_md_path = os.path.join(output_dir, "Manuscript_Source.md")
    
    with open(master_md_path, "w", encoding="utf-8") as master_file:
        # Metadata Block for Pandoc
        master_file.write(f"---\n")
        master_file.write(f"title: {book_title.replace('_', ' ')}\n")
        master_file.write(f"author: {author}\n")
        master_file.write(f"rights: All Rights Reserved\n")
        master_file.write(f"language: pt-BR\n")
        if cover_image:
            master_file.write(f"cover-image: {os.path.abspath(cover_image)}\n")
        master_file.write(f"---\n\n")
        
        # Frontmatter Injection (Preface, About Author)
        frontmatter_files = ["Preface_Methodological.md", "About_Author.md"]
        for fm in frontmatter_files:
            if os.path.exists(fm):
                print(f"  Injecting Frontmatter: {fm}...")
                with open(fm, "r", encoding="utf-8") as f:
                     content = f.read()
                     master_file.write(f"\n\\newpage\n\n")
                     master_file.write(content)
                     master_file.write("\n\n")

        # Add Chapters
        for md_file in chapter_files:
            print(f"  Processed {md_file}...")
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                # Scrivener Page Break
                master_file.write(f"\n\\newpage\n\n") 
                master_file.write(content)
                master_file.write("\n\n")
        
        # Add Comparative Section (New Request)
        comparative_files = glob.glob("figures/comparative/*.md")
        if comparative_files:
            print("  Injecting Comparative Analysis Section...")
            master_file.write(f"\n\\newpage\n\n") 
            master_file.write(f"# Comparative Analysis of Techniques\n\n")
            
            for comp_file in comparative_files:
                with open(comp_file, "r", encoding="utf-8") as f:
                    comp_content = f.read()
                    master_file.write(comp_content)
                    master_file.write("\n\n")
                    
                    # Check for associated image (e.g., matching .png)
                    base_name = os.path.splitext(comp_file)[0]
                    img_png = f"{base_name}.png"
                    if os.path.exists(img_png):
                         master_file.write(f"![Comparative Visual]({img_png})\n\n")

    # 5. Generate Formats
    pandoc_path = os.path.abspath("pandoc-3.8.3-x86_64/bin/pandoc")
    if not os.path.exists(pandoc_path): pandoc_path = "pandoc"
    
    # Format A: DOCX (Golden Master)
    docx_path = os.path.join(output_dir, f"{book_title}_Master.docx")
    print(f"⚙️  Compiling DOCX: {docx_path}...")
    
    cmd_docx = [
        pandoc_path, master_md_path, "-o", docx_path,
        "--resource-path=.", "--toc", "--toc-depth=2"
    ]
    if cover_image: # Reference doc logic might override cover, but let's try
         pass 

    subprocess.run(cmd_docx, check=False)

    # Format B: EPUB (E-book)
    epub_path = os.path.join(output_dir, f"{book_title}.epub")
    print(f"⚙️  Compiling EPUB: {epub_path}...")
    
    cmd_epub = [
        pandoc_path, master_md_path, "-o", epub_path,
        "--resource-path=.", "--toc"
    ]
    if cover_image:
        cmd_epub.extend(["--epub-cover-image", cover_image])

    subprocess.run(cmd_epub, check=False)

    print(f"\n✅ Compile Complete! Files ready in folder: {output_dir}")

if __name__ == "__main__":
    scrivener_compile()
