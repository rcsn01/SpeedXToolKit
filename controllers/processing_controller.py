from views import *
from controllers.save_controller import *
from models import *
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def save_file(df, essay, store):
    if df is not None:
        save_dataframe(df)
    else:
        messagebox.showwarning("Warning", "No data to save!")
    store = save_preset(essay, store)
    return store

def save_preset(essay, store):
    name = save_preset_view()
    essay = essay_to_pickle(name, essay)
    return store + [essay]

def drop_column(df, essay):
    df, input = drop_column_view(df)
    if df is not None:
        processed_df = drop_column_model(df, input)
        essay = essay + (f"(drop_column_model!$!{input})",)
        if isinstance(processed_df, pd.DataFrame):
            return processed_df, essay
    else:
        return None

def rename_column(df, essay):
    df, target_name, new_name = rename_column_view(df)
    if df is not None:
        processed_df = rename_column_model(df, target_name, new_name)
        essay = essay + (f"(rename_column_model!$!{target_name}!$!{new_name})",)
        if isinstance(processed_df, pd.DataFrame):
            return processed_df, essay
    else:
        return None

def pivot_table(df, essay):
    df, target_name, new_name = pivot_table_view(df)
    if df is not None:
        processed_df = pivot_table_model(df, target_name, new_name)
        essay = essay + (f"(pivot_table_model!$!{target_name}!$!{new_name})",)
        if isinstance(processed_df, pd.DataFrame):
            return processed_df, essay
    else:
        return None

def delta_calculation(df, essay):
    df, var1, vaf2, delta= delta_calculation_view(df)
    if df is not None:
        processed_df = delta_calculation_model(df, var1, vaf2, delta)
        essay = essay + (f"(delta_calculation_model!$!{var1}!$!{vaf2}!$!{delta})",)
        if isinstance(processed_df, pd.DataFrame):
            return processed_df, essay
    else:
        return None

def produce_output(df, essay):
    df, var1 = produce_output_view(df)
    if df is not None:
        processed_df = produce_output_model(df, var1)
        essay = essay + (f"(produce_output_model!$!{var1})",)
        if isinstance(processed_df, pd.DataFrame):
            return processed_df, essay
    else:
        return None

def keep_column(df, essay):
    df, input = keep_column_view(df)
    if df is not None:
        processed_df = keep_column_model(df, input)
        essay = essay + (f"(keep_column_model!$!{input})",)
        if isinstance(processed_df, pd.DataFrame):
            return processed_df, essay
    else:
        return None

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

    df_with_format = df_with_format[df.columns[:2]]
    essay_info = df_to_tuple(df_with_format)

    if isinstance(processed_df, pd.DataFrame):
        return processed_df, essay_info
    else:
        print(type(processed_df))
        print("Model df is not a df.")

def find_essay(essay, store):
    for essays in store:
        if essays[2] == essay[1]:
            return essays

def load_preset(df, essay, store):
    original_df = df.copy()
    original_essay = essay
    original_store = store
    store = pickle_to_essay(store)
    matching = None
    for essays in store:
        if essays[1] == essay[0]:
            matching = essays

    response = None
    # Autosearch for matching
    # if matching != None:
    #     response = yes_no_gui("Preset found, type yes to apply, else no?")

    if response == True:
        if len(matching) >= 3:
            function_call = matching[3:]  # Extract function call string
            for individual_func in function_call:
                func_parts = individual_func.strip("()").split("!$!")
                
                if len(func_parts) < 1:
                    print("Invalid function call format.")
                    return original_df, original_essay, original_store

                func_name = func_parts[0]
                params = func_parts[1:]

                func = globals().get(func_name) or locals().get(func_name)

                if callable(func):
                    try:
                        df = func(df, *params)
                    except Exception as e:
                        print(f"[Error] Failed to apply function '{func_name}': {e}")
                        return original_df, original_essay, original_store
                else:
                    print(f"[Error] Function '{func_name}' not found.")
                    return original_df, original_essay, original_store
            return df, essay, store

    else:
    #elif response == False or response is None:
        matching = load_preset_view(store)
        if len(matching) >= 3:
            function_call = matching[3:]
            print(function_call)
            for individual_func in function_call:
                func_parts = individual_func.strip("()").split("!$!")
                
                if len(func_parts) < 1:
                    print("Invalid function call format.")
                    return original_df, original_essay, original_store

                func_name = func_parts[0]
                params = func_parts[1:]

                func = globals().get(func_name) or locals().get(func_name)

                if callable(func):
                    try:
                        df = func(df, *params)
                    except Exception as e:
                        print(f"[Error] Failed to apply function '{func_name}': {e}")
                        return original_df, original_essay, original_store
                else:
                    print(f"[Error] Function '{func_name}' not found.")
                    return original_df, original_essay, original_store
            return df, essay, store

    return df, essay, store

    
def combined_file():
    return combine_file_view()

