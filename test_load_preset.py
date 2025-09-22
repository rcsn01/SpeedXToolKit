#!/usr/bin/env python3
"""
Test script to verify that load_preset_view works with empty preset list
"""

import os
import sys
import tkinter as tk

# Add the project root to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.load_preset_view import load_preset_view

def test_empty_presets():
    """Test load_preset_view with empty list"""
    print("Testing load_preset_view with empty preset list...")
    
    # Test with empty list (simulating no presets found)
    empty_list = []
    result = load_preset_view(empty_list)
    
    print(f"Result: {result}")
    
    if result is None:
        print("✓ User cancelled or no selection made")
    else:
        print(f"✓ User selected: {result}")

def test_with_presets():
    """Test load_preset_view with sample presets"""
    print("Testing load_preset_view with sample presets...")
    
    # Sample data - list of tuples where first element is the name
    sample_presets = [
        ("Sample Preset 1", "metadata1", ["function1", "function2"]),
        ("Sample Preset 2", "metadata2", ["function3"]),
        ("Sample Preset 3", "metadata3", [])
    ]
    
    result = load_preset_view(sample_presets)
    
    print(f"Result: {result}")
    
    if result is None:
        print("✓ User cancelled or no selection made")
    else:
        print(f"✓ User selected: {result}")

if __name__ == "__main__":
    print("Load Preset View Test")
    print("="*50)
    
    choice = input("Test with (1) empty presets or (2) sample presets? Enter 1 or 2: ")
    
    if choice == "1":
        test_empty_presets()
    elif choice == "2":
        test_with_presets()
    else:
        print("Invalid choice. Testing with empty presets...")
        test_empty_presets()