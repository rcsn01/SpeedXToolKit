import pandas as pd
import numpy as np

def produce_output_model(df, input):
    input_columns = [col.strip() for col in input.split(',') if col.strip()]

    if not input_columns:
        return df  # Return original DataFrame if no columns are specified

    try:
        # Verify each column exists in the DataFrame
        for col in input_columns:
            if col not in df.columns:
                raise ValueError(f"Column {col} not found in DataFrame")

        # Create the "Output" column containing column names where the row has values
        df["Output"] = df[input_columns].apply(
            lambda row: ", ".join(row.index[row.notna() & (row != 0)]), axis=1
        )

        return df  # Return the modified DataFrame\

    except Exception as e:
        print(f"Error processing input: {e}")
        return df  # Return original DataFrame in case of an error