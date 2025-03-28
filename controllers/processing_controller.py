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
