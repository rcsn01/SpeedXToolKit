from tkinter import messagebox


def keep_column_model(df, input_columns):
    """Filter specific columns from the DataFrame."""
    try:
        # If input is a string, convert it to a list (for backward compatibility)
        if isinstance(input_columns, str):
            input_columns = [col.strip() for col in input_columns.split(",")]

        selected_columns = [col for col in input_columns if col in df.columns]

        if not selected_columns:
            messagebox.showerror("Error", f"Column not detected: {input_columns}")
            return None

        return df[selected_columns]

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None