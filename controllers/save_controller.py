import pandas as pd
from tkinter.simpledialog import askstring
from tkinter import messagebox

def save_dataframe(df):
    """Save DataFrame to CSV or Excel."""
    try:
        file_format = askstring("Save File", "Enter file format to save (csv/xlsx):").strip().lower()
        file_name = askstring("Save File", "Enter file name (without extension):").strip()

        if file_format == "csv":
            file_path = f"{file_name}.csv"
            df.to_csv(file_path, index=False)
        elif file_format == "xlsx":
            file_path = f"{file_name}.xlsx"
            df.to_excel(file_path, index=False, engine="openpyxl")
        else:
            messagebox.showwarning("Error", "Invalid format. Please enter 'csv' or 'xlsx'.")
            return

        messagebox.showinfo("Success", f"File saved as {file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")
