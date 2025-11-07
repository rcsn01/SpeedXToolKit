import pandas as pd
from views.ctk_dialogs import messagebox
from models.dataframe_model import *

def rename_column_model(df, target_name, new_name):
    """Renames the target column in the given DataFrame."""
    # basic validation
    if not isinstance(df, pd.DataFrame):
        messagebox.showerror("Error", "Invalid DataFrame provided.")
        return None

    if not isinstance(target_name, str) or not target_name.strip():
        messagebox.showerror("Error", "Target column name must be a non-empty string.")
        return None

    if target_name not in df.columns:
        messagebox.showerror("Error", f"Column '{target_name}' not found in DataFrame.")
        return None

    if not isinstance(new_name, str) or not new_name.strip():
        messagebox.showerror("Error", "New column name must be a non-empty string.")
        return None

    # if the new name already exists (and is not the same as the target), reject to avoid duplicates
    if new_name in df.columns and new_name != target_name:
        messagebox.showerror("Error", f"A column named '{new_name}' already exists. Please choose a different name.")
        return None

    # no-op if names are equal
    if new_name == target_name:
        messagebox.showinfo("No changes", f"Column is already named '{new_name}'.")
        return df

    return df.rename(columns={target_name: new_name})