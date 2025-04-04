def keep_column_model(df, input):
    """Filter specific columns from the DataFrame."""
    try:
        selected_columns = [col.strip() for col in input.split(",") if col.strip() in df.columns]

        if not selected_columns:
            print("No valid columns selected.")
            return None

        #print(df[selected_columns])
        return df[selected_columns]
    except Exception as e:
        print(f"Error: {e}")
        return None