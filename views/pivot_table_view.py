from logging import root
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from models.dataframe_model import *
import numpy as np
from models.pivot_table_model import *
from styles import TkinterDialogStyles

def pivot_table_view(df):
    """Display a view with dropdowns to select pivot table target and value columns."""
    try:
        root = ctk.CTk()
        root.title("Pivot Table")
        root.geometry("600x200")
        root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

        # Create the main frame
        first_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        first_frame.pack(pady=5)

        ctk.CTkLabel(first_frame, text="Select Target Column, this column should contain different target names. (e.g. SARS, MgPa, IC)", 
                     text_color=TkinterDialogStyles.LABEL_FG, font=TkinterDialogStyles.LABEL_FONT).grid(row=0, column=0, padx=5, sticky="w")

        # Target column dropdown
        second_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        second_frame.pack(pady=5)

        ctk.CTkLabel(second_frame, text="Target Column", text_color=TkinterDialogStyles.LABEL_FG, 
                     font=TkinterDialogStyles.LABEL_FONT).grid(row=1, column=0, padx=5, sticky="w")
        var1 = ctk.CTkComboBox(second_frame, values=list(df.columns), state="readonly", width=TkinterDialogStyles.INPUT_WIDTH * 8)
        var1.grid(row=1, column=1, padx=5, sticky="w")

        # Value column dropdown

        third_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        third_frame.pack(pady=5)
        ctk.CTkLabel(third_frame, text="Select Value Column, this column should contain the Cq values of the target.", 
                     text_color=TkinterDialogStyles.LABEL_FG, font=TkinterDialogStyles.LABEL_FONT).grid(row=0, column=0, padx=5, sticky="w")

        fourth_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        fourth_frame.pack(pady=5)
        ctk.CTkLabel(fourth_frame, text="Value Column", text_color=TkinterDialogStyles.LABEL_FG, 
                     font=TkinterDialogStyles.LABEL_FONT).grid(row=1, column=0, padx=5, sticky="w")
        var2 = ctk.CTkComboBox(fourth_frame, values=list(df.columns), state="readonly", width=TkinterDialogStyles.INPUT_WIDTH * 8)
        var2.grid(row=1, column=1, padx=5, sticky="w")

        result = {"confirmed": False, "target_name": "", "new_name": ""}

        def on_confirm():
            """Confirm selection and close window."""
            if not var1.get() or not var2.get():
                messagebox.showwarning("Missing Selection", "Please select both target and value columns.")
                return
            result["confirmed"] = True
            result["target_name"] = var1.get()
            result["new_name"] = var2.get()
            root.quit()
            root.destroy()

        def on_cancel():
            """Close window without confirming."""
            root.quit()
            root.destroy()

        # Buttons
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=TkinterDialogStyles.BUTTON_PADDING)
        ctk.CTkButton(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=TkinterDialogStyles.BUTTON_PADDING)

        root.mainloop()

        if result.get("confirmed"):
            return df, result["target_name"], result["new_name"]
        else:
            return None, None, None

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None
