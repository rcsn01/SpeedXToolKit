import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.simpledialog import askstring

def filter_columns(df, input):
    """Filter specific columns from the DataFrame."""
    try:
        selected_columns = [col.strip() for col in input.split(",") if col.strip() in df.columns]

        if not selected_columns:
            print("No valid columns selected.")
            return None

        #print(df[selected_columns])
        return df[selected_columns]
    except Exception as e:
        print(f"Error: {e}")
        return None

def clear_undefined(df):
    """Replace 'undefined' and 'undetermined' values (case-insensitive and with possible spaces) in the DataFrame with NaN."""
    try:
        # Strip spaces and convert everything to lowercase before replacement
        df = df.map(lambda x: np.nan if isinstance(x, str) and x.strip().lower() in {"undefined", "undetermined"} else x)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def what_do_i_have(id_df, target_df):
    #print(len(id_df))
    #print(len(target_df))
    """Combine two DataFrames horizontally (side by side), adding an 'Outcome' column to target_df."""
    
    # Add the 'Outcome' column to target_df
    target_df['Outcome'] = target_df.apply(
        lambda row: ', '.join([col for col in target_df.columns if pd.notna(row[col])]), axis=1)
    
    # Concatenate the two DataFrames along the columns axis (axis=1)
    combined_df = pd.concat([id_df, target_df], axis=1)
    
    #print(len(combined_df))
    return combined_df



