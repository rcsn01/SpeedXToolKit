import pandas as pd
from tkinter import messagebox, filedialog

def save_dataframe(df):
    """Prompt for destination and save DataFrame as CSV.

    Returns:
        True  - if file successfully saved
        None  - if user cancelled or no data
        False - on error
    """
    try:
        if df is None or df.empty:
            messagebox.showwarning("Save", "No data to save.")
            return None

        file_path = filedialog.asksaveasfilename(
            title="Save CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            confirmoverwrite=True
        )
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
