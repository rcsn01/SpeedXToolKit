def drop_column_model(df, drop_input):
    """Drop specific columns from the DataFrame."""
    # If input is a string, convert it to a list (for backward compatibility)
    if isinstance(drop_input, str):
        drop_input = [col.strip() for col in drop_input.split(",")]

    columns_to_drop = [col for col in drop_input if col in df.columns]

    if not columns_to_drop:
        # print("No valid columns found to drop.") # Optional: raise warning
        return df  # Return original DataFrame if no valid columns to drop

    return df.drop(columns=columns_to_drop)
