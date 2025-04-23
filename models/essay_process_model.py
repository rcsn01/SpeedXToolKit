import pandas as pd
def essay_process_model(df, header_row):
    # Show preview and get header row + user-selected columns

    # Extract the format section (rows from the first row to header row)
    # Extract format section (top part of the file)
    df_with_format = df.iloc[:header_row].copy()
    df_with_format.reset_index(drop=True, inplace=True)

    # Extract data section (from header row onwards)
    df_with_header = df.iloc[header_row:].copy()

    # Set the first row as header
    df_with_header.columns = df_with_header.iloc[0].astype(str).str.strip()
    df_with_header = df_with_header[1:].reset_index(drop=True)  

    return df_with_format, df_with_header