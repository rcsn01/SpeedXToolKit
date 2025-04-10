def pivot_table_model(df, target, value):
    # If target or value is missing, return the original DataFrame
    if not target or not value:
        return df, None

    # Determine index columns by excluding target and value columns
    index_columns = [col for col in df.columns if col not in [target, value]]
    
    try:
        # Pivot the dataframe
        df_pivot = df.pivot_table(index=index_columns, 
                                  columns=target, 
                                  values=value, 
                                  aggfunc="first").reset_index()
        #df_pivot.columns.name = None
        id_df = df_pivot[index_columns]
        target_df = df_pivot.drop(index_columns, axis=1)
        return df_pivot

    except Exception as e:
        print(f"Error: {e}")
        return df, None  # Return original DataFrame if pivoting fails

