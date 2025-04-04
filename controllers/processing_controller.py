from views import *
from controllers.save_controller import *
from models import *
import pandas as pd

def save_file(df):
    if df is not None:
        save_dataframe(df)
    else:
        messagebox.showwarning("Warning", "No data to save!")

def drop_column(df):
    df, input = drop_column_view(df)
    processed_df = drop_column_model(df, input)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df
    else:
        print("Model df is not a df.")

def rename_column(df):
    df, target_name, new_name = rename_column_view(df)
    processed_df = rename_column_model(df, target_name, new_name)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df
    else:
        print("Model df is not a df.")

def pivot_table(df):
    df, target_name, new_name = pivot_table_view(df)
    processed_df = pivot_table_model(df, target_name, new_name)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df
    else:
        print("Model df is not a df.")

def delta_calculation(df):
    df, var1, vaf2, delta= delta_calculation_view(df)
    processed_df = delta_calculation_model(df, var1, vaf2, delta)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df
    else:
        print("Model df is not a df.")

def produce_output(df):
    if df is not None:
        df = delta_calculation_view(df)

def keep_column(df):
    df, input = keep_column_view(df)
    print(df)
    print(input)
    processed_df = keep_column_model(df, input)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df
    else:
        print("Model df is not a df.")


def import_files(file_path):
    df, header_row, keep_input = load_file_view(file_path)
    df_with_format, df_with_header = essay_process_model(df, header_row)
    df_with_header = keep_column_model(df_with_header, keep_input)

    processed_df = clear_undefined(df_with_header)
    if isinstance(processed_df, pd.DataFrame):
        return processed_df
    else:
        print(type(processed_df))
        print("Model df is not a df.")
