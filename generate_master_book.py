import os
import subprocess
import glob

def generate_master_book(output_dir="_Export_To_Drive", master_filename="PresbyCor_MASTER_BOOK.docx"):
    """
    Combines all Chapter_*_Complete.md files into one Master.md
    and converts it to a single DOCX with images.
    """
    
    # 1. Setup Output Directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 2. Define File Sequence (Strict Order)
    # Front Matter
    files_to_combine = [
        "PDF_Frontmatter.md",
        "Preface_Methodology.md",
        "About_Author.md"
    ]

    # Chapters (Dynamic Sort)
    chapter_files = glob.glob("Chapter_*_Complete.md")
    
    def sort_key(filename):
        try:
            parts = filename.split('_')
            num_part = parts[1]
            if "Plus" in num_part: return 5.5
            return float(num_part)
        except: return 999 

    chapter_files = sorted(chapter_files, key=sort_key)
    files_to_combine.extend(chapter_files)

    # Back Matter
    files_to_combine.extend([
        "Glossary_Abbreviations.md",
        "Bibliography_Consolidated.md"
    ])

    print(f"DEBUG: Found {len(chapter_files)} chapters.")
    print(f"DEBUG: Total files to combine: {len(files_to_combine)}")

    # 3. Concatenate Markdown (With Sanitization)
    master_md_path = os.path.join(output_dir, "Temporary_Master.md")
    
    import re
    # Regex to find YAML header at start of file
    yaml_pattern = re.compile(r'^---\s*\n.*?\n---\s*\n', re.DOTALL)
    
    with open(master_md_path, "w", encoding="utf-8") as master_file:
        
        for i, md_file in enumerate(files_to_combine):
            if os.path.exists(md_file):
                print(f"  Adding {md_file}...")
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Special handling for PDF_Frontmatter.md (Keep YAML)
                    if i == 0 and "Frontmatter" in md_file:
                        # Write as is, just ensure newline at end
                        master_file.write(content.strip())
                        master_file.write("\n\n")
                        continue

                    # For all other files:
                    # 1. Strip YAML header if it exists
                    content = yaml_pattern.sub('', content)
                    
                    # 2. Replace horizontal rules '---' with '***' to avoid Pandoc confusion
                    # Match '---' on a line by itself, potentially surrounded by whitespace
                    content = re.sub(r'^\s*---\s*$', '***', content, flags=re.MULTILINE)
                    
                    # 3. Append with Page Break
                    master_file.write(f"\n\\newpage\n\n") 
                    master_file.write(content)
                    master_file.write("\n\n")
            else:
                print(f"WARNING: File {md_file} not found. Skipping.")

    # 4. Convert Master MD to DOCX
    output_docx_path = os.path.join(output_dir, master_filename)
    print(f"Converting Master MD -> {output_docx_path} ...")

    pandoc_path = os.path.abspath("pandoc-3.8.3-x86_64/bin/pandoc")
    if not os.path.exists(pandoc_path):
            pandoc_path = "pandoc" 

    cmd = [
        pandoc_path,
        master_md_path,
        "-o", output_docx_path,
        "--resource-path=.", # Crucial for finding images
        "--toc",
        "--toc-depth=2"
    ]

    try:
        existing_ref_doc = "reference.docx"
        if os.path.exists(existing_ref_doc):
                cmd.extend(["--reference-doc", existing_ref_doc])

        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"SUCCESS! Master Book created at:\n  {os.path.abspath(output_docx_path)}")
            # Cleanup temp file
            if os.path.exists(master_md_path):
                os.remove(master_md_path)
        else:
            print("FAILED")
            print(f"  Error: {result.stderr}")
            
    except Exception as e:
        print(f"FAILED ({str(e)})")

if __name__ == "__main__":
    generate_master_book()
