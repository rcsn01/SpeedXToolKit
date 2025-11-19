import customtkinter as ctk
import pandas as pd
from views.ctk_dialogs import showinfo, showwarning, showerror, askstring, askinteger, askyesno
from models.dataframe_model import *
import numpy as np
from models.rename_column_model import *
from styles import TkinterDialogStyles, AppColors, AppFonts, ButtonStyles

# ...existing code...
def save_plugin_view():
    """Prompt user for a plugin name. Returns None if cancelled or empty."""
    try:
        root = ctk.CTkToplevel()
        root.title("Plugin Name")
        # Make window slightly wider so plugin name field can be larger and more usable
        root.geometry("420x140")
        root.resizable(False, False)
        root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

        # Ensure window is on top and modal
        root.lift()
        root.focus_force()
        root.grab_set()
        try:
            if hasattr(ctk, "_get_ancestor_window"):
                parent = ctk._get_ancestor_window()
                if parent:
                    root.transient(parent)
        except Exception:
            pass

        first_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        first_frame.pack(pady=10, padx=10, fill='x')

        ctk.CTkLabel(first_frame, text="Plugin Name",
                     text_color=AppColors.BLACK, font=AppFonts.BODY).grid(row=0, column=0, padx=5, sticky="w")
        # Allow the entry to be wider and expand horizontally if frame layout changes
        target_name = ctk.CTkEntry(first_frame, width=TkinterDialogStyles.INPUT_WIDTH or 280)
        first_frame.grid_columnconfigure(1, weight=1)
        target_name.grid(row=0, column=1, padx=5, sticky="ew")

        canceled = {"value": False}

        def on_confirm():
            root.destroy()

        def on_cancel():
            canceled["value"] = True
            root.destroy()

        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=8)
        ctk.CTkButton(button_frame, text="Confirm", command=on_confirm, **ButtonStyles.DEFAULT).grid(row=0, column=0, padx=6)
        ctk.CTkButton(button_frame, text="Cancel", command=on_cancel, **ButtonStyles.DEFAULT).grid(row=0, column=1, padx=6)

        root.wait_window()

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
