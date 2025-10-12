import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np
from models.pivot_table_model import *
from models.delta_calculation_model import *

def delta_calculation_view(df):
    """Load Excel file and allow the user to confirm the header row."""
    try:
        root = tk.Tk()
        root.title("Delta Calculation")
        root.geometry("300x200")

        # Create the main frame
        first_frame = tk.Frame(root)
        first_frame.pack(pady=5)
        
        # Add title and dropdown for first column
        tk.Label(first_frame, text="First Column").grid(row=0, column=0, padx=5, sticky="w")
        var1 = ttk.Combobox(first_frame, values=list(df.columns), width=15, state="readonly")
        var1.grid(row=0, column=1, padx=5, sticky="w")

        # Add title and dropdown for second column
        tk.Label(first_frame, text="Second Column").grid(row=1, column=0, padx=5, sticky="w")
        var2 = ttk.Combobox(first_frame, values=list(df.columns), width=15, state="readonly")
        var2.grid(row=1, column=1, padx=5, sticky="w")

        # Add title and input field for delta value
        tk.Label(first_frame, text="Difference in value").grid(row=2, column=0, padx=5, sticky="w")
        var3_var = tk.StringVar(value='')
        var3_entry = tk.Entry(first_frame, width=15, textvariable=var3_var)
        var3_entry.grid(row=2, column=1, padx=5, sticky="w")

        # Process the user's input
        result = {"input": None, "confirmed": False, "var1": "", "var2": "", "var3": ""}

        def update_confirm_state(*_):
            """Enable the confirm button only when all 3 fields are filled."""
            v1 = var1.get().strip()
            v2 = var2.get().strip()
            v3 = var3_var.get().strip()
            if v1 and v2 and v3:
                confirm_btn.config(state='normal')
            else:
                confirm_btn.config(state='disabled')

        def on_confirm():
            """Confirm selection and close window."""
            try:
                result["confirmed"] = True
                result["var1"] = var1.get()
                result["var2"] = var2.get()
                result["var3"] = var3_var.get()
                root.quit()
                root.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for the header row.")

        def on_cancel():
            """Close window without confirming."""
            root.quit()
            root.destroy()

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        confirm_btn = ttk.Button(button_frame, text="Confirm", command=on_confirm)
        confirm_btn.grid(row=0, column=0, padx=10)
        confirm_btn.config(state='disabled')  # start disabled

        ttk.Button(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=10)

        # Bind changes to update the confirm button state
        var1.bind('<<ComboboxSelected>>', update_confirm_state)
        var2.bind('<<ComboboxSelected>>', update_confirm_state)
        var3_var.trace_add('write', update_confirm_state)

        # Run the window
        root.mainloop()

        if result.get("confirmed"):
            var1_val, var2_val, var3_val = result["var1"], result["var2"], result["var3"]
            return df, var1_val, var2_val, var3_val
        else:
            return None, None, None, None
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None