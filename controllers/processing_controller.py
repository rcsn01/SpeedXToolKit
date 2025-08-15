from views import *
from controllers.save_controller import *
from models import *
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def save_file(df, essay, store):
    if df is None:
        messagebox.showwarning("Warning", "No data to save!")
        return store
    result = save_dataframe(df)
    # Only proceed to save preset if user actually saved the file (result True)
    if result is True:
        store = save_preset(store)
    return store

def save_preset(store):
    name = save_preset_view()
    # If user cancelled or empty input -> do nothing
    if not name:
        return store
    store['name'] = name
    store = essay_to_pickle(store)
    return store

def drop_column(df, store):
    """Drop a selected column and record the action in store['functions']."""
    view_result = drop_column_view(df)
    if not view_result:
        return None, store
    df, input = view_result
    processed_df = drop_column_model(df, input)
    if isinstance(processed_df, pd.DataFrame):
        if 'functions' in store:
            store['functions'].append(f"drop_column_model!$!{input}")
        return processed_df, store
    return None, store

def rename_column(df, store):
    """Rename a column and log the action."""
    view_result = rename_column_view(df)
    if not view_result:
        return None, store
    df, target_name, new_name = view_result
    processed_df = rename_column_model(df, target_name, new_name)
    if isinstance(processed_df, pd.DataFrame):
        if 'functions' in store:
            store['functions'].append(f"rename_column_model!$!{target_name}!$!{new_name}")
        return processed_df, store
    return None, store

def pivot_table(df, store):
    """Create a pivot table and log the action."""
    view_result = pivot_table_view(df)
    if not view_result:
        return None, store
    df, target_name, new_name = view_result
    processed_df = pivot_table_model(df, target_name, new_name)
    if isinstance(processed_df, pd.DataFrame):
        if 'functions' in store:
            store['functions'].append(f"pivot_table_model!$!{target_name}!$!{new_name}")
        return processed_df, store
    return None, store

def delta_calculation(df, store):
    """Perform delta calculation (requires Output column) and log the action."""
    if 'Output' not in df.columns:
        messagebox.showwarning("Missing Output Column", "Please generate output before using delta calculation.")
        return df, store
    view_result = delta_calculation_view(df)
    if not view_result:
        return df, store
    df, var1, vaf2, delta = view_result
    processed_df = delta_calculation_model(df, var1, vaf2, delta)
    if isinstance(processed_df, pd.DataFrame):
        if 'functions' in store:
            store['functions'].append(f"delta_calculation_model!$!{var1}!$!{vaf2}!$!{delta}")
        return processed_df, store
    return None, store

def produce_output(df, store):
    """Produce output column and log the action."""
    view_result = produce_output_view(df)
    if not view_result:
        return None, store
    df, var1 = view_result
    processed_df = produce_output_model(df, var1)
    if isinstance(processed_df, pd.DataFrame):
        if 'functions' in store:
            store['functions'].append(f"produce_output_model!$!{var1}")
        return processed_df, store
    return None, store

def keep_column(df, store):
    """Keep only selected columns and log the action."""
    view_result = keep_column_view(df)
    if not view_result:
        return None, store
    df, input = view_result
    processed_df = keep_column_model(df, input)
    if isinstance(processed_df, pd.DataFrame):
        if 'functions' in store:
            store['functions'].append(f"keep_column_model!$!{input}")
        return processed_df, store
    return None, store

def df_to_tuple(df):
    if len(df.columns) < 2:
        print("processing controller df_to_tuple error")
    
    first_col_tuple = tuple(df.iloc[:, 0].values)
    second_col_tuple = tuple(df.iloc[:, 1].values)

    return (first_col_tuple, second_col_tuple)


def import_files(file_path): 
    df, header_row, keep_input = load_file_view(file_path)
    df_with_format, df_with_header = essay_process_model(df, header_row)
    
    df_with_header = keep_column_model(df_with_header, keep_input)
    processed_df = clear_undefined(df_with_header)
    essay_info = None
    if df_with_format is not None and df is not None:
        try:
            df_with_format_slice = df_with_format[df.columns[:2]]
            essay_info = df_to_tuple(df_with_format_slice)
        except Exception:
            pass

    if isinstance(processed_df, pd.DataFrame):
        return processed_df, essay_info
    else:
        print(type(processed_df))
        print("Model df is not a df.")

def find_essay(essay, store):
    for essays in store:
        if essays[2] == essay[1]:
            return essays

def load_preset(df, store):
    """Load a dict-based preset from disk and replay its function history.

    Returns (rebuilt_df, updated_store)
    """
    original_df = df.copy() if isinstance(df, pd.DataFrame) else df
    presets = pickle_to_essay([])  # list of dict presets
    if not presets:
        messagebox.showinfo("Presets", "No presets found.")
        return df, store

    # Build compatibility tuples for existing selection view: (name, metadata, *functions)
    selection_data = []
    for p in presets:
        if isinstance(p, dict):
            selection_data.append((p.get('name'), p.get('metadata'), *p.get('functions', [])))

    chosen_tuple = load_preset_view(selection_data)
    if not chosen_tuple:
        return df, store
    chosen_name = chosen_tuple[0]
    chosen = next((p for p in presets if isinstance(p, dict) and p.get('name') == chosen_name), None)
    if not chosen:
        return df, store

    # Adopt chosen preset store
    store = {"name": chosen.get('name'), "metadata": chosen.get('metadata'), "functions": list(chosen.get('functions', []))}

    func_map = {
        'drop_column_model': lambda frame, col: drop_column_model(frame, col),
        'rename_column_model': lambda frame, target, new: rename_column_model(frame, target, new),
        'pivot_table_model': lambda frame, target, new: pivot_table_model(frame, target, new),
        'delta_calculation_model': lambda frame, v1, v2, d: delta_calculation_model(frame, v1, v2, d),
        'produce_output_model': lambda frame, v1: produce_output_model(frame, v1),
        'keep_column_model': lambda frame, cols: keep_column_model(frame, cols),
    }
    rebuilt_df = original_df
    for entry in store.get('functions', []):
        try:
            parts = entry.split('!$!')
            name = parts[0]
            params = parts[1:]
            func = func_map.get(name)
            if func and isinstance(rebuilt_df, pd.DataFrame):
                rebuilt_df = func(rebuilt_df, *params)
        except Exception as e:
            print(f"[Preset Replay] Failed on {entry}: {e}")
            continue

    if isinstance(rebuilt_df, pd.DataFrame):
        return rebuilt_df, store
    return original_df, store

    
def combined_file():
    return combine_file_view()

