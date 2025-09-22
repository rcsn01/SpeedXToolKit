import pandas as pd

def custom_code_model(df, code):
    """Execute custom Python code on the DataFrame."""
    try:
        # Create a local namespace with df available
        local_vars = {'df': df.copy(), 'pd': pd}

        # Execute the code
        exec(code, {}, local_vars)

        # Get the modified df
        result_df = local_vars.get('df')
        if not isinstance(result_df, pd.DataFrame):
            raise ValueError("The code must result in 'df' being a pandas DataFrame.")

        return result_df

    except Exception as e:
        raise RuntimeError(f"Error executing custom code: {str(e)}")