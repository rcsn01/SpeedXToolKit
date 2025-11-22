import pandas as pd
import traceback

def custom_code_model(df, code):
    """Execute custom Python code on the DataFrame."""
    # Provide a globals namespace that contains pandas and a copy of df.
    # Putting these in globals makes them directly available to user code (e.g. `pd.read_csv(...)`).
    global_ns = {'pd': pd, 'df': df.copy(), '__builtins__': __builtins__}

    # Execute the user code in a single shared namespace so functions
    # defined by the user can access module-level variables (e.g. target_names).
    exec(code, global_ns)

    # Prefer df from the execution namespace (user may assign a new df).
    result_df = global_ns.get('df')
    if not isinstance(result_df, pd.DataFrame):
        raise ValueError("The code must result in 'df' being a pandas DataFrame.")

    return result_df
