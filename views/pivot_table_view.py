import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np
from models.pivot_table_model import *

def pivot_table_view(df):
    """Load Excel file and allow the user to confirm the header row."""
    try:
        root = tk.Tk()
        root.title("Pivot Table")
        root.geometry("1000x700")

        # Create the main frame
        first_frame = tk.Frame(root)
        first_frame.pack(pady=5)
        
        # Add title and input field for columns to drop
        tk.Label(first_frame, text="Target Column").grid(row=0, column=0, padx=5, sticky="w")
        var1 = tk.Entry(first_frame, width=70)
        var1.insert(0, '')  # Initialize the entry with empty string
        var1.grid(row=0, column=1, padx=5, sticky="w")

        second_frame = tk.Frame(root)
        second_frame.pack(pady=5)

        # Add title and input field for columns to drop
        tk.Label(second_frame, text="Value Column").grid(row=0, column=0, padx=5, sticky="w")
        var2 = tk.Entry(second_frame, width=70)
        var2.insert(0, '')  # Initialize the entry with empty string
        var2.grid(row=0, column=1, padx=5, sticky="w")
        
        # Process the user's input
        result = {"input": None}

        def on_confirm():
            """Confirm selection and close window."""
            try:
                result["target_name"] = var1.get()
                result["new_name"] = var2.get()
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
        target_name, new_name = result["target_name"], result["new_name"]
        return df, target_name, new_name

    except Exception as e:
        print("OHHH NOOOOOOOOO")
        print(f"Error: {e}")
        return None
