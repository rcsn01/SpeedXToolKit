from views import *
from controllers.save_controller import *
from models import *
import pandas as pd

def save_file(df, essay, store):
    if df is not None:
        save_dataframe(df)
    else:
        messagebox.showwarning("Warning", "No data to save!")
    return store + [essay]

def drop_column(df, essay):
    df, input = drop_column_view(df)
    processed_df = drop_column_model(df, input)
    essay = essay + (f"(drop_column_model,{input})",)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df, essay
    else:
        print("Model df is not a df.")

def rename_column(df, essay):
    df, target_name, new_name = rename_column_view(df)
    processed_df = rename_column_model(df, target_name, new_name)
    essay = essay + (f"(rename_column_model,{target_name},{new_name})",)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df, essay
    else:
        print("Model df is not a df.")

def pivot_table(df, essay):
    df, target_name, new_name = pivot_table_view(df)
    processed_df = pivot_table_model(df, target_name, new_name)
    essay = essay + (f"(pivot_table_model,{target_name},{new_name})",)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df, essay
    else:
        print("Model df is not a df.")

def delta_calculation(df, essay):
    df, var1, vaf2, delta= delta_calculation_view(df)
    processed_df = delta_calculation_model(df, var1, vaf2, delta)
    essay = essay + (f"(delta_calculation_model,{var1},{vaf2},{delta})",)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df, essay
    else:
        print("Model df is not a df.")

def produce_output(df, essay):
    df, var1 = produce_output_view(df)
    processed_df = produce_output_model(df, var1)
    essay = essay + (f"(produce_output_model,{var1})",)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df, essay
    else:
        print("Model df is not a df.")

def keep_column(df, essay):
    df, input = keep_column_view(df)
    processed_df = keep_column_model(df, input)
    essay = essay + (f"(keep_column_model,{input})",)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df, essay
    else:
        print("Model df is not a df.")

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
        if essays[1] == essay[1]:
            return essays

def load_preset(df, essay, store):
    matching = find_essay(essay, store)

    if len(matching) >= 3:
        function_call = matching[2:]  # Extracting the function call string
        for individual_func in function_call:
            func_parts = individual_func.strip("()").split(",")  # Remove parentheses and split by comma
            
            if len(func_parts) < 1:
                raise ValueError("Invalid function call format.")

            func_name = func_parts[0]  # Extract function name
            params = func_parts[1:]  # Extract parameters (if any)

            # Get the function from globals() or locals()
            func = globals().get(func_name) or locals().get(func_name)

            if callable(func):
                df = func(df, *params)  # Pass parameters dynamically
            else:
                raise ValueError(f"Function '{func_name}' not found.")
        return df, essay, store
