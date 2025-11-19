import os
import shutil
import zipfile
from pathlib import Path
import sys

def package_release():
    # Configuration
    ROOT_DIR = Path(__file__).parent
    DIST_DIR = ROOT_DIR / "dist"
    PLUGINS_DIR = ROOT_DIR / "plugins"
    LATEST_DIR = ROOT_DIR / "latest"
    ZIP_NAME = "latest_release.zip"

    print(f"--- Starting Packaging Process ---")

    # 1. Check prerequisites
    if not DIST_DIR.exists():
        print(f"Error: '{DIST_DIR}' directory not found. Please run PyInstaller first.")
        sys.exit(1)

    # 2. Create/Clean "latest" folder
    if LATEST_DIR.exists():
        print(f"Cleaning existing '{LATEST_DIR.name}' directory...")
        shutil.rmtree(LATEST_DIR)
    
    LATEST_DIR.mkdir()
    print(f"Created directory: {LATEST_DIR}")

    # 3. Find and copy the latest .exe file
    exe_files = list(DIST_DIR.glob("*.exe"))
    if not exe_files:
        print(f"Error: No .exe files found in '{DIST_DIR}'")
        sys.exit(1)

    # Sort by modification time (newest first)
    latest_exe = max(exe_files, key=os.path.getmtime)
    
    dest_exe = LATEST_DIR / latest_exe.name
    shutil.copy2(latest_exe, dest_exe)
    print(f"Found and copied latest executable: {latest_exe.name}")

    # 4. Copy plugins
    # We create a 'plugins' subfolder inside 'latest' to maintain structure
    dest_plugins_dir = LATEST_DIR / "plugins"
    
    if PLUGINS_DIR.exists():
        # Copy the directory tree
        shutil.copytree(PLUGINS_DIR, dest_plugins_dir)
        print(f"Copied 'plugins' folder to: {dest_plugins_dir}")
    else:
        print(f"Warning: '{PLUGINS_DIR}' directory not found. Skipping plugins.")

    # 5. Turn folder into zip
    zip_path = ROOT_DIR / ZIP_NAME
    print(f"Creating zip archive: {zip_path.name}...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the latest directory
        for root, dirs, files in os.walk(LATEST_DIR):
            for file in files:
                file_path = Path(root) / file
                # Create relative path for the zip archive
                # This ensures the zip contains a top-level "latest" folder
                archive_name = file_path.relative_to(ROOT_DIR)
                zipf.write(file_path, archive_name)
                
    print(f"--- Success! ---")
    print(f"Package created at: {zip_path}")

if __name__ == "__main__":
    package_release()
