# ...existing code...
from views.ctk_dialogs import messagebox
import pandas as pd

def remove_empty_rows_model(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Return a new DataFrame with rows removed where `column` is NaN, empty string,
    or only whitespace.
    """
    try:

        if df is None or not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")

        if column not in df.columns:
            # If the column doesn't exist, return df unchanged
            return df

        # Build a boolean mask: True for rows to keep
        # Consider NaN, None, empty string, or all-whitespace as empty
        def is_non_empty(val):
            # Treat pandas NA (pd.isna) as empty
            if pd.isna(val):
                return False
            # Convert to string and strip whitespace
            try:
                s = str(val).strip()
            except Exception:
                return True
            return len(s) > 0

        mask = df[column].apply(is_non_empty)

        # Filter and return a reset-index copy for cleanliness
        filtered = df.loc[mask].copy()
        filtered.reset_index(drop=True, inplace=True)
        return filtered

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return df  # Return original DataFrame on error
