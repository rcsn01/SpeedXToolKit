import customtkinter as ctk
import pandas as pd
from views.ctk_dialogs import showinfo, showwarning, showerror, askstring, askinteger, askyesno
from models.dataframe_model import *
import numpy as np
from models.pivot_table_model import *
from models.delta_calculation_model import *
from styles import TkinterDialogStyles, AppFonts, ButtonStyles, PanelStyles

def delta_calculation_view(df):
    """Load Excel file and allow the user to confirm the header row."""
    try:
        root = ctk.CTkToplevel()
        root.title("Delta Calculation")
        # Make dialog wider so combo boxes and entry are readable
        root.geometry("420x240")
        root.configure(fg_color=PanelStyles.PREVIEW.get("fg_color", TkinterDialogStyles.DIALOG_BG))

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

        # Create the main frame
        first_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        first_frame.pack(pady=5, padx=10, fill="x")

        # Add title and dropdown for first column
        ctk.CTkLabel(
            first_frame,
            text="First Column",
            fg_color=TkinterDialogStyles.FRAME_BG,
            text_color=TkinterDialogStyles.LABEL_FG,
            font=AppFonts.BODY,
        ).grid(row=0, column=0, padx=5, sticky="w")
        # Allow the combo to be wide and expand horizontally
        var1 = ctk.CTkComboBox(first_frame, values=list(df.columns), width=TkinterDialogStyles.INPUT_WIDTH * 6, state="readonly")
        first_frame.grid_columnconfigure(1, weight=1)
        var1.grid(row=0, column=1, padx=5, sticky="ew")

        # Add title and dropdown for second column
        ctk.CTkLabel(
            first_frame,
            text="Second Column",
            fg_color=TkinterDialogStyles.FRAME_BG,
            text_color=TkinterDialogStyles.LABEL_FG,
            font=AppFonts.BODY,
        ).grid(row=1, column=0, padx=5, sticky="w")
        var2 = ctk.CTkComboBox(first_frame, values=list(df.columns), width=TkinterDialogStyles.INPUT_WIDTH * 6, state="readonly")
        var2.grid(row=1, column=1, padx=5, sticky="ew")

        # Add title and input field for delta value
        ctk.CTkLabel(
            first_frame,
            text="Difference in value",
            fg_color=TkinterDialogStyles.FRAME_BG,
            text_color=TkinterDialogStyles.LABEL_FG,
            font=AppFonts.BODY,
        ).grid(row=2, column=0, padx=5, sticky="w")
        var3 = ctk.CTkEntry(first_frame, width=TkinterDialogStyles.INPUT_WIDTH * 6)
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
                root.destroy()
            except ValueError:
                showerror("Invalid Input", "Please enter a valid integer for the header row.")

        def on_cancel():
            """Close window without confirming."""
            root.destroy()

        # Buttons
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=12)

        # Use centralized button styles
        primary = ButtonStyles.PRIMARY
        default = ButtonStyles.DEFAULT

        ctk.CTkButton(
            button_frame,
            text="Confirm",
            command=on_confirm,
            width=primary.get("width"),
            height=primary.get("height"),
            corner_radius=primary.get("corner_radius"),
            fg_color=primary.get("fg_color"),
            hover_color=primary.get("hover_color"),
            text_color=primary.get("text_color"),
            font=primary.get("font"),
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=on_cancel,
            width=default.get("width"),
            height=default.get("height"),
            corner_radius=default.get("corner_radius"),
            fg_color=default.get("fg_color"),
            hover_color=default.get("hover_color"),
            text_color=default.get("text_color"),
            font=default.get("font"),
        ).grid(row=0, column=1, padx=10)

        # Run the window
        root.wait_window()

        if result.get("confirmed"):
            var1, var2, var3 = result["var1"], result["var2"], result["var3"]
            return df, var1, var2, var3
        else:
            return None

    except Exception as e:
        showerror("Error", f"An error occurred: {e}")
        return None
