# ...existing code...
import pandas as pd

def remove_empty_rows_model(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Return a new DataFrame with rows removed where `column` is NaN, empty string,
    or only whitespace.
    """
    if df is None or column not in df.columns:
        return df
    s = df[column].astype(object)
    mask_nan = s.isna()
    mask_empty = s.fillna('').astype(str).str.strip() == ''
    keep = ~(mask_nan | mask_empty)
    return df.loc[keep].copy()
# ...existing code...