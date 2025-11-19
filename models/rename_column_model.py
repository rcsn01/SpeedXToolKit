import pandas as pd
from models.dataframe_model import *

def rename_column_model(df, target_name, new_name):
    """Renames the target column in the given DataFrame."""
    # basic validation
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Invalid DataFrame provided.")

    if not isinstance(target_name, str) or not target_name.strip():
        raise ValueError("Target column name must be a non-empty string.")

    if target_name not in df.columns:
        raise ValueError(f"Column '{target_name}' not found in DataFrame.")

    if not isinstance(new_name, str) or not new_name.strip():
        raise ValueError("New column name must be a non-empty string.")

    # if the new name already exists (and is not the same as the target), reject to avoid duplicates
    if new_name in df.columns and new_name != target_name:
        raise ValueError(f"A column named '{new_name}' already exists. Please choose a different name.")

    # no-op if names are equal
    if new_name == target_name:
        # messagebox.showinfo("No changes", f"Column is already named '{new_name}'.") # Let controller handle info if needed
        return df

    return df.rename(columns={target_name: new_name})