import os
import subprocess
import glob
import sys
import shutil

def export_chapters(output_dir="_Export_To_Drive"):
    """
    Converts Chapter_*_Complete.md files to DOCX using Pandoc.
    """
    
    # 1. Setup Output Directory
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except PermissionError:
            print(f"Error: Permission denied creating {output_dir}")
            return

    # 2. Find Chapter Files
    chapter_files = sorted(glob.glob("Chapter_*_Complete.md"))
    if not chapter_files:
        print("No 'Chapter_*_Complete.md' files found in the current directory.")
        return

    print(f"Found {len(chapter_files)} chapters to export.")

    # 3. Convert each chapter
    for md_file in chapter_files:
        base_name = os.path.splitext(md_file)[0]
        docx_name = f"{base_name}.docx"
        output_path = os.path.join(output_dir, docx_name)
        
        print(f"Converting {md_file} -> {output_path} ...", end=" ", flush=True)

        # Pandoc command
        # Use local binary
        pandoc_path = os.path.abspath("pandoc-3.8.3-x86_64/bin/pandoc")
        if not os.path.exists(pandoc_path):
             pandoc_path = "pandoc" # Fallback to system path

        cmd = [
            pandoc_path,
            md_file,
            "-o", output_path,
            "--resource-path=.", 
            "--toc" # Optional: Include Table of Contents
        ]

        try:
            existing_ref_doc = "reference.docx" # If the user had a style reference
            if os.path.exists(existing_ref_doc):
                 cmd.extend(["--reference-doc", existing_ref_doc])

            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("OK")
            else:
                print("FAILED")
                print(f"  Error: {result.stderr}")
        except FileNotFoundError:
            print("FAILED (Pandoc not found)")
            print("  Please ensure pandoc is installed: brew install pandoc")
            return
        except Exception as e:
            print(f"FAILED ({str(e)})")

    print(f"\nExport complete. Files are in: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    target_dir = "_Export_To_Drive"
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    
    print("--- PresbyCor Book Export ---")
    export_chapters(target_dir)
