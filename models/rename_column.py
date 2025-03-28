import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *
import numpy as np

def rename_column(df, target_name, new_name):
    """Renames the target column in the given DataFrame."""
    if target_name not in df.columns:
        messagebox.showerror("Error", f"Column '{target_name}' not found in DataFrame.")
        return df
    df = df.rename(columns={target_name: new_name})
    #print(df)
    return df