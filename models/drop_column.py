import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np


def _process_input(df, keep_input):
    to_drop = keep_input.strip()
    
    if not to_drop:
        return df  # Return original DataFrame if no columns specified
    
    try:
        # Split the input into individual column names
        columns_to_drop = [col.strip() for col in to_drop.split(',')]
        
        # Verify each column exists in the DataFrame
        for col in columns_to_drop:
            if col not in df.columns:
                raise ValueError(f"Column {col} not found in DataFrame")
        
        # Drop the specified columns from the DataFrame
        df = df.drop(columns=columns_to_drop)
        
        return df  # Return the modified DataFrame
        
    except Exception as e:
        print(f"Error processing input: {e}")
        return df  # Return original DataFrame on error


def drop_column_window(root):
    # Create the main frame
    columns_frame = tk.Frame(root)
    columns_frame.pack(pady=5)
    
    # Add title and input field for columns to drop
    tk.Label(columns_frame, text="Columns to Drop:").grid(row=0, column=0, padx=5, sticky="w")
    keep_input = tk.Entry(columns_frame, width=70)
    keep_input.insert(0, '')  # Initialize the entry with empty string
    keep_input.grid(row=0, column=1, padx=5, sticky="w")
    
    # Process the user's input
    result = {"keep_input": None}

    def on_confirm():
        """Confirm selection and close window."""
        try:
            result["keep_input"] = keep_input.get()
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
    return result["keep_input"]


def drop_column(df):
    """Load Excel file and allow the user to confirm the header row."""
    try:

        root = tk.Tk()
        root.title("Drop column")
        root.geometry("1000x700")

        input = drop_column_window(root)
        processed_df = _process_input(df, input)
        return processed_df

    except Exception as e:
        print(f"Error: {e}")
        return None
