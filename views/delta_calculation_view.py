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
        var3 = tk.Entry(first_frame, width=15)
        var3.insert(0, '')  # Initialize the entry with empty string
        var3.grid(row=2, column=1, padx=5, sticky="w")

        # Process the user's input
        result = {"input": None}

        result = {"confirmed": False}

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
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=10)

        # Run the window
        root.mainloop()

        if result.get("confirmed"):
            var1, var2, var3 = result["var1"], result["var2"], result["var3"]
            return df, var1, var2, var3
        else:
            return None, None, None, None
        


    except Exception as e:
        print("OHHH NOOOOOOOOO")
        print("Error: {e}")
        return None
