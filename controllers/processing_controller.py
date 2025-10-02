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
            store['functions'].append(["drop_column_model", input])
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
            store['functions'].append(["rename_column_model", target_name, new_name])
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
            store['functions'].append(["pivot_table_model", target_name, new_name])
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
            store['functions'].append(["delta_calculation_model", var1, vaf2, delta])
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
            store['functions'].append(["produce_output_model", var1])
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
            store['functions'].append(["keep_column_model", input])
        return processed_df, store
    return None, store

def custom_code(df, store):
    """Open custom code view, execute code, and log the action."""
    view_result = custom_code_view()
    if not view_result:
        return None, store
    code = view_result["code"]
    processed_df = custom_code_model(df, code)
    if isinstance(processed_df, pd.DataFrame):
        if 'functions' in store:
            store['functions'].append(["custom_code_model", code])
        return processed_df, store
    return None, store

def df_to_tuple(df):
    if len(df.columns) < 2:
        print("processing controller df_to_tuple error")
    
    first_col_tuple = tuple(df.iloc[:, 0].values)
    second_col_tuple = tuple(df.iloc[:, 1].values)

    return (first_col_tuple, second_col_tuple)


def remove_empty_rows(df, store):
    """Remove empty rows based on user-selected column and log the action."""
    view_result = remove_empty_rows_view(df)
    if not view_result:
        return None, store
    df, target_name = view_result
    processed_df = remove_empty_rows_model(df, target_name)
    if isinstance(processed_df, pd.DataFrame):
        if 'functions' in store:
            store['functions'].append(["remove_empty_rows_model", target_name])
        return processed_df, store
    return None, store


def import_files(file_path): 
    df, header_row, keep_input = load_file_view(file_path)
    if df is None or header_row is None:
        messagebox.showerror("Load Failed", "File could not be loaded or header not detected.")
        return None
    df_with_format, df_with_header = essay_process_model(df, header_row)
    if df_with_header is None:
        messagebox.showerror("Processing Failed", "Unable to process file structure.")
        return None
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

def show_plugins():
    return pickle_to_essay([])

def apply_plugin(df, plugin):
    """Apply a plugin/preset to df. `plugin` may be:
    - a preset name (str)
    - a preset dict as returned by pickle_to_essay
    - a selection tuple (name, metadata, functions)

    Returns (new_df, new_store)
    """
    original_df = df.copy() if isinstance(df, pd.DataFrame) else df

    # Resolve plugin to a preset dict
    presets = pickle_to_essay([])
    chosen = None
    try:
        if isinstance(plugin, dict):
            chosen = plugin
        elif isinstance(plugin, str):
            chosen = next((p for p in presets if isinstance(p, dict) and p.get('name') == plugin), None)
        elif isinstance(plugin, (list, tuple)) and plugin:
            # Could be (name, metadata, functions) tuple or a sequence where first item is name
            chosen_name = plugin[0]
            chosen = next((p for p in presets if isinstance(p, dict) and p.get('name') == chosen_name), None)
    except Exception:
        chosen = None

    if not chosen:
        # nothing to apply
        return df, {"name": None, "metadata": None, "functions": []}

    # Adopt chosen preset store
    store = {"name": chosen.get('name'), "metadata": chosen.get('metadata'), "functions": list(chosen.get('functions', []))}

    func_map = {
        'drop_column_model': lambda frame, col: drop_column_model(frame, col),
        'rename_column_model': lambda frame, target, new: rename_column_model(frame, target, new),
        'pivot_table_model': lambda frame, target, new: pivot_table_model(frame, target, new),
        'delta_calculation_model': lambda frame, v1, v2, d: delta_calculation_model(frame, v1, v2, d),
        'produce_output_model': lambda frame, v1: produce_output_model(frame, v1),
        'keep_column_model': lambda frame, cols: keep_column_model(frame, cols),
        'custom_code_model': lambda frame, code: custom_code_model(frame, code),
        'remove_empty_rows_model': lambda frame, col: remove_empty_rows_model(frame, col),
    }

    rebuilt_df = original_df
    for entry in store.get('functions', []):
        try:
            name = entry[0]
            params = entry[1:]
            func = func_map.get(name)
            if func and isinstance(rebuilt_df, pd.DataFrame):
                rebuilt_df = func(rebuilt_df, *params)
        except Exception as e:
            print(f"[Preset Replay] Failed on {entry}: {e}")
            continue

    if isinstance(rebuilt_df, pd.DataFrame):
        return rebuilt_df, store
    return original_df, store

def manage_preset():
    """Manage presets - view, add, remove, or select presets.

    Returns (rebuilt_df, updated_store)
    """
    presets = pickle_to_essay([])  # list of dict presets
    
    # Build compatibility tuples for existing selection view: (name, metadata, functions)
    selection_data = []
    for p in presets:
        if isinstance(p, dict):
            selection_data.append((p.get('name'), p.get('metadata'), p.get('functions', [])))

    manage_preset_view(selection_data)

    
def combined_file():
    return combine_file_view()

