import pandas as pd
from tkinter import messagebox

def delta_calculation_model(df, column1, column2, delta):
    """
    Calculate the difference between two columns and append the result as a new column.
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    column1 (str): Name of first column to subtract from
    column2 (str): Name of second column to subtract
    """
    try:
        # If columns are missing, return the original DataFrame
        if column1 not in df.columns or column2 not in df.columns:
            messagebox.showerror("Error", "One or both specified columns not found in DataFrame")
            return df, None
        
        df[column1] = pd.to_numeric(df[column1], errors='coerce')
        df[column2] = pd.to_numeric(df[column2], errors='coerce')

        # Calculate delta and create new column
        df['delta'] = df[column1] - df[column2]

        # Get column index where we want to insert the new column
        col2_index = df.columns.get_loc(column2)

        # Reorder columns to place delta after column2
        cols = df.columns.tolist()
        cols.remove('delta')
        cols.insert(col2_index + 1, 'delta')
        df = df[cols]

        # Remove the column name with the lower value from 'output' if abs(delta) > delta
        if 'Output' in df.columns:
            for idx, row in df.iterrows():
                try:
                    threshold = float(delta)
                except Exception:
                    threshold = 0
                diff = abs(row['delta'])
                if diff > threshold:
                    # Remove the column name with the lower value from output
                    if row[column1] < row[column2]:
                        to_remove = column1
                    else:
                        to_remove = column2
                    # Remove the column name from the output cell if present
                    if isinstance(row['Output'], str):
                        # Remove exact match, comma, or space
                        new_output = ','.join([x for x in row['Output'].split(',') if x.strip() != to_remove])
                        df.at[idx, 'Output'] = new_output
        return df
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return df, None  # Return original DataFrame if operation fails