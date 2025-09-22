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
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Normal development environment
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from models/ to project root
        base_path = os.path.dirname(base_path)
    
    return Path(base_path) / relative_path


def get_presets_dir():
    """
    Get the path to the presets directory.
    
    Returns:
        Path: Path to the presets directory
    """
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