import pandas as pd
from tkinter import messagebox, filedialog
import os

def save_dataframe(df, default_filename=None):
    """Prompt for destination and save DataFrame as CSV.

    Args:
        df: DataFrame to save
        default_filename: Optional default filename to pre-fill in the save dialog

    Returns:
        True  - if file successfully saved
        None  - if user cancelled or no data
        False - on error
    """
    try:
        if df is None or df.empty:
            messagebox.showwarning("Save", "No data to save.")
            return None

        # Setup save dialog parameters
        save_options = {
            "title": "Save CSV",
            "defaultextension": ".csv",
            "filetypes": [("CSV files", "*.csv")],
            "confirmoverwrite": True
        }
        
        # Add initial filename if provided
        if default_filename:
            save_options["initialfile"] = default_filename

        file_path = filedialog.asksaveasfilename(**save_options)
        
        if not file_path:
            return None  # User cancelled

        if not file_path.lower().endswith('.csv'):
            file_path += '.csv'

        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"File saved: {file_path}")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {e}")
        return False
