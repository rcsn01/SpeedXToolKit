import pandas as pd
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
            print("Error: One or both specified columns not found in DataFrame")
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
        
        return df
    
    except Exception as e:
        print(f"Error: {e}")
        return df, None  # Return original DataFrame if operation fails