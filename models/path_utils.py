"""
Path utility module for handling resource paths in both development and packaged environments.
"""

import os
import sys
from pathlib import Path


def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for both development and PyInstaller packaged environments.
    
    Args:
        relative_path (str): Relative path to the resource
        
    Returns:
        Path: Absolute path to the resource
    """
    try:
        # If running in a PyInstaller bundle prefer an external resource placed
        # next to the executable (so users can replace assets without rebuilding).
        if getattr(sys, 'frozen', False):
            exe_dir = Path(sys.executable).parent
            external = exe_dir / relative_path
            if external.exists():
                return external
            # Fall back to the bundled resource inside _MEIPASS (if provided)
            try:
                return Path(sys._MEIPASS) / relative_path
            except Exception:
                # If something unexpected happens, fall through to development path
                pass

        # Normal development environment: resources live under project root
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from models/ to project root
        base_path = os.path.dirname(base_path)
        return Path(base_path) / relative_path
    except Exception:
        # As a final fallback, return the relative path as-is
        return Path(relative_path)


def get_presets_dir():
    """
    Get the path to the presets directory.
    
    Returns:
        Path: Path to the presets directory
    """
    # If running in a PyInstaller bundle prefer an external 'presets' folder next to the exe
    try:
        if getattr(sys, 'frozen', False):
            exe_dir = Path(sys.executable).parent
            external = exe_dir / 'presets'
            if external.exists():
                return external
            # fall back to bundled data inside _MEIPASS if available
            try:
                return Path(sys._MEIPASS) / 'presets'
            except Exception:
                return external
    except Exception:
        pass

    return get_resource_path("presets")


def ensure_presets_dir():
    """
    Ensure the presets directory exists, create it if it doesn't.
    
    Returns:
        Path: Path to the presets directory
    """
    presets_path = get_presets_dir()
    presets_path.mkdir(exist_ok=True)
    return presets_path