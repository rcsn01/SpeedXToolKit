import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np
from models.rename_column_model import *

def rename_column_view(df):
    """Load Excel file and allow the user to confirm the header row."""
    try:

        root = tk.Tk()
        root.title("Rename Target")
        root.geometry("1000x700")

        # Create the main frame
        first_frame = tk.Frame(root)
        first_frame.pack(pady=5)
        
        # Add title and input field for columns to drop
        tk.Label(first_frame, text="Old Target Name").grid(row=0, column=0, padx=5, sticky="w")
        target_name = tk.Entry(first_frame, width=70)
        target_name.insert(0, '')  # Initialize the entry with empty string
        target_name.grid(row=0, column=1, padx=5, sticky="w")

        second_frame = tk.Frame(root)
        second_frame.pack(pady=5)

        # Add title and input field for columns to drop
        tk.Label(second_frame, text="New Target Name").grid(row=0, column=0, padx=5, sticky="w")
        new_name = tk.Entry(second_frame, width=70)
        new_name.insert(0, '')  # Initialize the entry with empty string
        new_name.grid(row=0, column=1, padx=5, sticky="w")
        
        # Process the user's input
        result = {"input": None}

        def on_confirm():
            """Confirm selection and close window."""
            try:
                result["target_name"] = target_name.get()
                result["new_name"] = new_name.get()
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
        print(f"Error: {e}")
        return None
