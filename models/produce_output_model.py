def produce_output_model(df, input_columns):
    """Create 'Output' column showing which input columns have non-zero, non-null values per row."""
    # If input is a string, convert it to a list (for backward compatibility)
    if isinstance(input_columns, str):
        input_columns = [col.strip() for col in input_columns.split(",") if col.strip()]

    # Filter only valid columns
    valid_columns = [col for col in input_columns if col in df.columns]

    if not valid_columns:
        # print("No valid columns provided.") # Optional: raise warning or just return
        return df  # Return original DataFrame if no valid columns

    # Apply row-wise function to collect non-zero, non-null column names
    df["Output"] = df[valid_columns].apply(
        lambda row: ", ".join(row.index[row.notna() & (row != 0)]),
        axis=1
    )

    return df
