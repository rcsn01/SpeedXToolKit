import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from models.dataframe_model import *
import numpy as np
from models.pivot_table_model import *

def pivot_table_view(df):
    """Display a view with dropdowns to select pivot table target and value columns."""
    try:
        root = tk.Tk()
        root.title("Pivot Table")
        root.geometry("600x200")

        # Create the main frame
        first_frame = tk.Frame(root)
        first_frame.pack(pady=5)

        # Target column dropdown
        tk.Label(first_frame, text="Target Column").grid(row=0, column=0, padx=5, sticky="w")
        var1 = ttk.Combobox(first_frame, values=list(df.columns), state="readonly", width=20)
        var1.grid(row=0, column=1, padx=5, sticky="w")

        # Value column dropdown
        second_frame = tk.Frame(root)
        second_frame.pack(pady=5)

        tk.Label(second_frame, text="Value Column").grid(row=0, column=0, padx=5, sticky="w")
        var2 = ttk.Combobox(second_frame, values=list(df.columns), state="readonly", width=20)
        var2.grid(row=0, column=1, padx=5, sticky="w")

        result = {"confirmed": False}

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
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Cancel", command=root.destroy).grid(row=0, column=1, padx=10)

        root.mainloop()

        if result.get("confirmed"):
            return df, result["target_name"], result["new_name"]
        else:
            return None, None, None

    except Exception as e:
        print("OHHH NOOOOOOOOO")
        print(f"Error: {e}")
        return None
