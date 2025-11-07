import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np
from models.pivot_table_model import *
from models.delta_calculation_model import *
from styles import TkinterDialogStyles

def delta_calculation_view(df):
    """Load Excel file and allow the user to confirm the header row."""
    try:
        root = ctk.CTk()
        root.title("Delta Calculation")
        # Make dialog wider so combo boxes and entry are readable
        root.geometry("400x220")
        root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

        # Create the main frame
        first_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        first_frame.pack(pady=5, padx=10, fill="x")

        # Add title and dropdown for first column
        ctk.CTkLabel(first_frame, text="First Column", fg_color=TkinterDialogStyles.FRAME_BG,
                     text_color=TkinterDialogStyles.LABEL_FG, font=TkinterDialogStyles.LABEL_FONT).grid(row=0, column=0, padx=5, sticky="w")
        # Allow the combo to be wide and expand horizontally
        var1 = ctk.CTkComboBox(first_frame, values=list(df.columns), width=50, state="readonly")
        first_frame.grid_columnconfigure(1, weight=1)
        var1.grid(row=0, column=1, padx=5, sticky="ew")

        # Add title and dropdown for second column
        ctk.CTkLabel(first_frame, text="Second Column", fg_color=TkinterDialogStyles.FRAME_BG,
                     text_color=TkinterDialogStyles.LABEL_FG, font=TkinterDialogStyles.LABEL_FONT).grid(row=1, column=0, padx=5, sticky="w")
        var2 = ctk.CTkComboBox(first_frame, values=list(df.columns), width=320, state="readonly")
        var2.grid(row=1, column=1, padx=5, sticky="ew")

        # Add title and input field for delta value
        ctk.CTkLabel(first_frame, text="Difference in value", fg_color=TkinterDialogStyles.FRAME_BG,
                     text_color=TkinterDialogStyles.LABEL_FG, font=TkinterDialogStyles.LABEL_FONT).grid(row=2, column=0, padx=5, sticky="w")
        var3 = ctk.CTkEntry(first_frame, width=160)
        var3.insert(0, '')  # Initialize the entry with empty string
        var3.grid(row=2, column=1, padx=5, sticky="ew")

        # Process the user's input
        result = {"input": None, "confirmed": False, "var1": "", "var2": "", "var3": ""}

        def on_confirm():
            """Confirm selection and close window."""
            try:
                result["confirmed"] = True
                result["var1"] = var1.get()
                result["var2"] = var2.get()
                result["var3"] = var3.get()
                root.quit()
                root.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for the header row.")

        def on_cancel():
            """Close window without confirming."""
            root.quit()
            root.destroy()

        # Buttons
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=10)

        # Run the window
        root.mainloop()

        if result.get("confirmed"):
            var1, var2, var3 = result["var1"], result["var2"], result["var3"]
            return df, var1, var2, var3
        else:
            return None

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None
