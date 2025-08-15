import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np
from models.rename_column_model import *

# ...existing code...
def save_preset_view():
    """Prompt user for a preset name. Returns None if cancelled or empty."""
    try:
        root = tk.Tk()
        root.title("Preset Name")
        root.geometry("300x120")
        root.resizable(False, False)

        first_frame = tk.Frame(root)
        first_frame.pack(pady=10, padx=10)

        tk.Label(first_frame, text="Preset Name").grid(row=0, column=0, padx=5, sticky="w")
        target_name = tk.Entry(first_frame, width=26)
        target_name.grid(row=0, column=1, padx=5, sticky="w")

        canceled = {"value": False}

        def on_confirm():
            root.quit()

        def on_cancel():
            canceled["value"] = True
            root.quit()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=8)
        ttk.Button(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=6)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=6)

        root.mainloop()

        if canceled["value"]:
            return None
        name = target_name.get().strip()
        return name or None
    finally:
        try:
            root.destroy()
        except Exception:
            pass
# ...existing
