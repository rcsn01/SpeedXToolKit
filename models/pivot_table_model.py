import pandas as pd

def pivot_table_model(df, target, value):
    # If target or value is missing, return the original DataFrame
    if not target or not value:
        return df

    # Coerce values in the selected value column to numeric. This will produce
    # NaN for missing or non-convertible items. We allow NaN (missing values),
    # but we reject entries that are non-numeric *and* not originally NaN
    # (for example strings like 'N/A').
    if value not in df.columns:
        raise ValueError(f"Column '{value}' not found in the data.")
    # Work on a copy to avoid mutating the caller's DataFrame
    df = df.copy()

    # Treat common null-like strings as missing (so they become NaN after coercion)
    if df[value].dtype == object:
        df[value] = df[value].replace(
            to_replace=r'^\s*$|^(?i:nan|na|n/a|none)$', value=pd.NA, regex=True
        )

    # Coerce to numeric; this will set non-convertible entries to NaN
    coerced = pd.to_numeric(df[value], errors="coerce")

    # Determine which originals were explicitly missing-like
    orig = df[value]
    orig_is_missing = orig.isna() | orig.astype(str).str.strip().str.lower().isin(['', 'nan', 'na', 'n/a', 'none'])

    # Invalid if original wasn't missing-like but coercion produced NaN
    invalid_mask = ~orig_is_missing & coerced.isna()
    if invalid_mask.any():
        bad_vals = pd.Series(df.loc[invalid_mask, value].unique())
        sample = bad_vals.head(5).tolist()
        raise ValueError(
            f"Non-numeric values present in '{value}': {sample}. Convert or remove them before pivoting."
        )

    # Replace the column with the coerced numeric values (NaNs preserved)
    df[value] = coerced

    # Determine index columns by excluding target and value columns
    index_columns = [col for col in df.columns if col not in [target, value]]

    # Use groupby + unstack instead of pivot_table so rows where all
    # aggregated values are NaN are preserved. groupby(...).first()
    # will pick the first (possibly NaN) value for duplicate groups.
    grouped = df.groupby(index_columns + [target], dropna=False)[value].first()
    df_pivot = grouped.unstack(target)

    # Reset index to turn the index columns back into regular columns
    df_pivot = df_pivot.reset_index()
    return df_pivot