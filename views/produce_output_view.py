import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np
from models.drop_column_model import *

def produce_output_view(df):
    """Load Excel file and allow the user to confirm the header row."""
    try:
        root = tk.Tk()
        root.title("Produce Output")
        root.geometry("1000x700")

        # Create the main frame
        columns_frame = tk.Frame(root)
        columns_frame.pack(pady=5)
        
        # Add title and input field for columns to drop
        tk.Label(columns_frame, text="Columns to include in output:").grid(row=0, column=0, padx=5, sticky="w")
        var1 = tk.Entry(columns_frame, width=70)
        var1.insert(0, '')  # Initialize the entry with empty string
        var1.grid(row=0, column=1, padx=5, sticky="w")
        
        # Process the user's input
        result = {"var1": None}

        def on_confirm():
            """Confirm selection and close window."""
            try:
                result["var1"] = var1.get()
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
        input = result["var1"]

        return df, input

    except Exception as e:
        print(f"Error: {e}")
        return None
