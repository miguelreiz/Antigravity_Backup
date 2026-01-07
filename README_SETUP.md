# PresbyCor Project Setup & Migration Guide

To work on this project on another computer (using Antigravity or just for editing), follow these steps.

## How to Sync Between Computers (Recommended: Google Drive / iCloud)

To have **automatic synchronization** (what you change here appears there automatically):

1.  **Move this entire specific folder** (`PresbyCor_ Modern Strategies for Presbyopia and La`) inside your **Google Drive** (or iCloud/OneDrive) folder on your computer.
2.  **Open the project** from that new location in VS Code.
3.  **On the other computer**, ensure Google Drive is installed. The folder will appear there automatically.
4.  Open that folder on the other computer.

**Result**: Any save you make is instantly uploaded and synced.

## Manual Move (Offline Method)
If you cannot use cloud sync, you can copy the folder manually:
1.  **Copy the entire folder** `PresbyCor_ Modern Strategies for Presbyopia and La`.

## Requirements
Most of the work is just Markdown text, which works anywhere.
However, to use the **Automated Export Script** (`export_to_drive.py`), you need:

1.  **Python 3**: Installed on most Macs by default.
2.  **Pandoc**: 
    *   This project currently includes a **portable version** of Pandoc in the folder (`pandoc-3.8.3-x86_64`).
    *   The script is configured to use this local version automatically.
    *   *Note*: If you move to a computer with a different architecture (e.g., Windows or Linux), you may need to install Pandoc manually or download the correct binary for that system.

## How to Export to Word
To generate the `.docx` files on the new computer:
1.  Open a terminal in this folder.
2.  Run the command:
    ```bash
    python3 export_to_drive.py
    ```
3.  The files will be created in the `_Export_To_Drive` folder.

## Antigravity (AI) Context
*   **Files**: Antigravity on the new computer will be able to read all the files, images, and this README. It will understand the current state of the book.
*   **Chat History**: The chat history from this specific session is stored locally on your old computer and **transferring it is not standard**.
    *   *Recommendation*: Don't worry about the chat history. Just verify that the files (Chapters and Figures) are correct. That is your "Source of Truth".
