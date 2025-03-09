import pandas as pd
import numpy as np
from tkinter.simpledialog import askstring

def filter_columns(df):
    """Filter specific columns from the DataFrame."""
    try:
        selected_columns = askstring("Filter Columns", "Enter the column names you want to keep (comma-separated):")
        selected_columns = [col.strip() for col in selected_columns.split(",") if col.strip() in df.columns]

        if not selected_columns:
            print("No valid columns selected.")
            return None

        return df[selected_columns]
    except Exception as e:
        print(f"Error: {e}")
        return None

def pivot_dataframe(df):
    """Pivot the DataFrame to transform its structure."""
    target_column = askstring("Target Column", "Enter the target column name")
    value_column = askstring("Value Column", "Enter value column name")
    try:
        df_pivot = df.pivot_table(index=["Well", "Well Position", "Sample Name"], 
                                  columns=target_column, values=value_column, aggfunc="first").reset_index()
        df_pivot.columns.name = None
        return df_pivot
    except Exception as e:
        print(f"Error: {e}")
        return None

def clear_undefined(df):
    """Replace 'undefined' and 'undetermined' values (case-insensitive and with possible spaces) in the DataFrame with blank values."""
    try:
        # Use regex to replace all case variations of "undefined" and "undetermined" with NaN, trimming spaces
        df.replace({r"\s*undefined\s*": np.nan, r"\s*undetermined\s*": np.nan}, regex=True, inplace=True)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

