import pandas as pd
def essay_process_model(df, header_row):
    # Show preview and get header row + user-selected columns

    # Extract the format section (rows from the first row to header row)
    df_with_format = df.iloc[:header_row]  # Save first-row-to-header as format
    df_with_format.reset_index(drop=True, inplace=True)

    df_with_header = df.iloc[header_row:]
    df_with_header.columns = df_with_header.iloc[0]
    df_with_header = df_with_header[1:].reset_index(drop = True)

    return df_with_format, df_with_header  # Return both dataframes