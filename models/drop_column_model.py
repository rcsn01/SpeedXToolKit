import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np


def drop_column_model(df, keep_input):
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
