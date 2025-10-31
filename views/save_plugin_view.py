import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np
from models.rename_column_model import *
from styles import TkinterDialogStyles

# ...existing code...
def save_plugin_view():
    """Prompt user for a plugin name. Returns None if cancelled or empty."""
    try:
        root = ctk.CTk()
        root.title("Plugin Name")
        root.geometry("300x120")
        root.resizable(False, False)
        root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

        first_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        first_frame.pack(pady=10, padx=10)

        ctk.CTkLabel(first_frame, text="Plugin Name", fg_color=TkinterDialogStyles.FRAME_BG, 
                 text_color=TkinterDialogStyles.LABEL_FG, font=TkinterDialogStyles.LABEL_FONT).grid(row=0, column=0, padx=5, sticky="w")
        target_name = ctk.CTkEntry(first_frame, width=26)
        target_name.grid(row=0, column=1, padx=5, sticky="w")

        canceled = {"value": False}

        def on_confirm():
            root.quit()

        def on_cancel():
            canceled["value"] = True
            root.quit()

        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=8)
        ctk.CTkButton(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=6)
        ctk.CTkButton(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=6)

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
