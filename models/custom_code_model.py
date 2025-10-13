from tkinter import messagebox
import pandas as pd

def custom_code_model(df, code):
    """Execute custom Python code on the DataFrame."""
    try:
        # Provide a globals namespace that contains pandas and a copy of df.
        # Putting these in globals makes them directly available to user code (e.g. `pd.read_csv(...)`).
        global_ns = {'pd': pd, 'df': df.copy(), '__builtins__': __builtins__}

        # Execute the user code. We pass an empty locals dict so user-defined
        # names (including any new 'df') will appear in the locals namespace.
        local_vars = {}
        exec(code, global_ns, local_vars)

        # Prefer df from locals (user may assign a new df), fall back to globals.
        result_df = local_vars.get('df', global_ns.get('df'))
        if not isinstance(result_df, pd.DataFrame):
            raise ValueError("The code must result in 'df' being a pandas DataFrame.")

        return result_df

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")