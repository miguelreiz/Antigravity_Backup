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

    # 2. Find Chapter Files in Order (Chapter_1, Chapter_2...)
    # Sorting alphabetically works for Chapter_1, Chapter_10... so we need natsort logic or manual key
    chapter_files = glob.glob("Chapter_*_Complete.md")
    
    # Custom sort key to handle 1, 2, 10 correctly
    def sort_key(filename):
        # Extract number between "Chapter_" and "_Complete"
        try:
            parts = filename.split('_')
            num_part = parts[1] # "1", "10", "5"
            # Handle "5_Plus" special case if it exists or just numbers
            if "Plus" in num_part:
                 return 5.5 # Place it after 5
            return float(num_part)
        except:
            return 999 

    chapter_files = sorted(chapter_files, key=sort_key)

    if not chapter_files:
        print("No chapter files found.")
        return

    print(f"Found {len(chapter_files)} chapters to combine.")

    # 3. Concatenate Markdown
    master_md_path = os.path.join(output_dir, "Temporary_Master.md")
    
    with open(master_md_path, "w", encoding="utf-8") as master_file:
        # Add Title Page
        master_file.write(f"% PresbyCor: Modern Strategies for Presbyopia and Laser Mechanics\n")
        master_file.write(f"% Dr. Miguel Reis\n")
        master_file.write(f"% 2024 Research Edition\n\n")
        master_file.write("\\newpage\n\n")

        for md_file in chapter_files:
            print(f"  Adding {md_file}...")
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                # Ensure each chapter starts on a new page (Pandoc feature)
                master_file.write(f"\n\\newpage\n\n") 
                master_file.write(content)
                master_file.write("\n\n")

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
