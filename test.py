# ...existing code...
from pathlib import Path
import pandas as pd
import numpy as np

CSV_PATH = Path(__file__).parent / 'test.csv'
path = CSV_PATH

df = pd.read_csv(path)

# DO NOT USE FUNCTIONS, DIRECTLY WRITE YOUR CODE BELOW

# ========================================================================
# ============================ START HERE ================================
# ========================================================================

# Editable variables
colour_compensation = "211020 CO CC Hestia & Thoth 96 well 20 uL.ixo (PlexPCR)"
kit_lot_number = "test_lot(Please change this)"
mix = "MG"

# Edit file metadata here
customisable_metadata: dict[str, str] = {
                            "Runfilecreated by user": "Speedx (Please change this)",
                            "Run Started": "",
                            "Cycler type": "LightCycler480 (Please change this)",
                            "Note": "For a more detailed report, please use the pdf format (Please change this)"}

# ========================================================================
# DO NOT EDIT BELOW THIS LINE
# ========================================================================

metadata: dict[str, str] = {"File Name": "Filename(s)", 
                            "Runfilecreated by user": "",
                            "Analysis cread by user": "Analysis created by",
                            "Run Started": "",
                            "Cycler type": "",
                            "Cycler Serial Number": "Instrument ID(s)",
                            "FastFinder Version": "FF analysis software version",
                            "Report created" : "Analysis created at (UTC)",
                            "Note": "",
                            "":""}

# Manually kept columns (preserve user's explicit selection order)
manual_keep = ['Sample ID', 'AssayResultTargetCode', 'Outcome', 'SampleType', 'Assay', 
               'Target_1_wells', #used to map wells
         'Target_1', 'Target_1_result', 'Target_1_cq',
         'Target_2', 'Target_2_result', 'Target_2_cq',
         'Target_3', 'Target_3_result', 'Target_3_cq']

# ========================================================================
# KEEPING DATA AND METADATA COLUMNS
# ========================================================================

# Add metadata values (the second value in each metadata pair) when non-empty.
# Preserve manual_keep order, then append metadata keys not already included.
meta_values = [v for v in metadata.values() if v]
additional = [v for v in meta_values if v not in manual_keep]

# Only keep columns that actually exist in the DataFrame to avoid KeyError.
keep_cols = [c for c in (manual_keep + additional) if c in df.columns]

df = df[keep_cols]

# Remove duplicate Target_1_wells values, keeping the first occurrence only
if 'Target_1_wells' in df.columns:
    # Drop exact duplicates in the Target_1_wells column while preserving row order
    df = df[~df['Target_1_wells'].duplicated(keep='first')].reset_index(drop=True)



# ========================================================================
# CORE LOGIC
# ========================================================================

# Build the `main_df` with the requested columns and mappings.
# - Plugin: renamed from `Assay`
# - Mix: use the `mix` variable
# - Colour compensation: use `colour_compensation` variable
# - Kit lot number: use `kit_lot_number` variable
# - Well: renamed from `Target_1_wells`
# - Sample name: renamed from `Sample ID`
# - Result/Overall results/Sample comment/Audit trail/LIMS warning: empty placeholders

n = len(df)
plugin_series = df['Assay'] if 'Assay' in df.columns else pd.Series([''] * n)
well_series = df['Target_1_wells'] if 'Target_1_wells' in df.columns else pd.Series([''] * n)
sample_series = df['Sample ID'] if 'Sample ID' in df.columns else pd.Series([''] * n)

main_df = pd.DataFrame({
    'Plugin': plugin_series.values,
    'Mix': [mix] * n,
    'Colour compensation': [colour_compensation] * n,
    'Kit lot number': [kit_lot_number] * n,
    'Well': well_series.values,
    'Sample name': sample_series.values,
    'Result': [''] * n,
    'Overall results': [''] * n,
    'Sample comment': [''] * n,
    'Audit trail': [''] * n,
    'LIMS warning': [''] * n,
})

# ========================================================================
# Add result logic based on Target_*_cq values from the original dataframe
# (placed here so metadata insertion below won't interfere with row alignment)
# ========================================================================

# Helper to determine whether a series cell 'has a value' (non-null and not empty)
def _has_value(series: pd.Series) -> pd.Series:
    return series.notna() & (series.astype(str).str.strip() != "")

if 'Target_1_cq' in df.columns:
    t1 = _has_value(df['Target_1_cq'])
else:
    # Create with df.index so boolean mask aligns with original rows
    t1 = pd.Series([False] * n, index=df.index)

if 'Target_2_cq' in df.columns:
    t2 = _has_value(df['Target_2_cq'])
else:
    t2 = pd.Series([False] * n, index=df.index)

if 'Target_3_cq' in df.columns:
    t3 = _has_value(df['Target_3_cq'])
else:
    t3 = pd.Series([False] * n, index=df.index)

# Build a mask of rows where SampleType == 'Regular'.
# If SampleType column is missing, treat no rows as Regular (so nothing is applied).
if 'SampleType' in df.columns:
    regular_mask = (df['SampleType'] == 'Regular')
    # ensure same index and boolean dtype
    regular_mask = pd.Series(regular_mask.values, index=df.index)
    # Also create mask for PositiveControl samples and a combined apply mask
    positive_mask = pd.Series((df['SampleType'] == 'PositiveControl').values, index=df.index)

else:
    regular_mask = pd.Series([False] * n, index=df.index)
    positive_mask = pd.Series([False] * n, index=df.index)

# Prepare default empty result/overall series and apply rules vectorised
# Use df.index so later boolean masks align correctly with these Series
result_series = pd.Series([''] * n, index=df.index)
overall_series = pd.Series([''] * n, index=df.index)

# Rule A: Only apply to Regular samples: t1 AND t2 AND t3 -> Positive, mutation detected
mask1 = regular_mask & t1 & t2 & t3
result_series.loc[mask1] = "Positive"
overall_series.loc[mask1] = "M. genitalium, 23S rRNA mutation detected."

# Rule B: Only apply to Regular samples
mask2 = regular_mask & t1 & (~t2) & t3
result_series.loc[mask2] = "Positive"
overall_series.loc[mask2] = "M. genitalium detected, 23S rRNA mutation not detected."

# Rule C: Only apply to Regular samples
mask3 = regular_mask & (~t1) & (~t2) & t3
result_series.loc[mask3] = "Negative"
overall_series.loc[mask3] = "M. genitalium not detected. IC valid"

# Rule 6: Only apply to Regular samples: t1 AND t2 AND (NOT t3) -> Positive, mutation detected, IC invalid
mask6 = regular_mask & (~t3)
result_series.loc[mask6] = "Invalid"
overall_series.loc[mask6] = "IC invalid"

# Rule 6: Only apply to Regular samples: t1 AND t2 AND (NOT t3) -> Positive, mutation detected, IC invalid
mask6 = positive_mask & t1
result_series.loc[mask6] = "Positive"
overall_series.loc[mask6] = "Positive Control valid."

# Rule 6: Only apply to Regular samples: t1 AND t2 AND (NOT t3) -> Positive, mutation detected, IC invalid
mask6 = positive_mask & (~t1)
result_series.loc[mask6] = "Negative"
overall_series.loc[mask6] = "Positive Control invalid."

# Assign computed values back into the main output dataframe
main_df['Result'] = result_series.values
main_df['Overall results'] = overall_series.values

# ========================================================================
# META DATA INSERTION BLOCK (now inserts into `main_df`)
# ========================================================================

# Use the columns from main_df so metadata rows align with the final output table
cols = list(main_df.columns)
# Ensure there are at least two columns (Plugin and Mix are expected)
if len(cols) < 2:
    while len(cols) < 2:
        cols.append(f"MetaCol{len(cols)+1}")
    # Reindex main_df if we extended columns
    main_df = main_df.reindex(columns=cols).fillna("")

first_col, second_col = cols[0], cols[1]

meta_rows = []
for k, v in metadata.items():
    # Build an empty row for all main_df columns then set first and second
    row = {c: "" for c in cols}
    row[first_col] = k

    # Determine the value to insert. Priority:
    # 1) If metadata value is empty, use customisable_metadata[k] when present.
    # 2) If the resulting value is the name of a column in df, use the first
    #    non-empty value from that column.
    value_to_insert = v

    # If metadata literal is empty, try customisable_metadata for this key
    if (not isinstance(value_to_insert, str)) or (isinstance(value_to_insert, str) and value_to_insert.strip() == ""):
        cm_val = customisable_metadata.get(k) if isinstance(customisable_metadata, dict) else None
        if cm_val is not None:
            value_to_insert = cm_val

    # If value_to_insert names a df column, replace with first non-empty value
    try:
        if isinstance(value_to_insert, str) and value_to_insert and value_to_insert in df.columns:
            mask_val = _has_value(df[value_to_insert])
            # limit DataFrame lookups to Regular samples only
            mask_val = mask_val & regular_mask
            if mask_val.any():
                value_to_insert = df.loc[mask_val, value_to_insert].iloc[0]
    except Exception:
        # On unexpected error keep literal value_to_insert
        pass

    row[second_col] = value_to_insert
    meta_rows.append(row)

meta_df = pd.DataFrame(meta_rows, columns=cols)
# Build a single-row DataFrame containing a copy of the column headers (for readability)
header_row = pd.DataFrame([{c: c for c in cols}], columns=cols)
# Concatenate metadata rows, the header copy row, then the main output table
main_df = pd.concat([meta_df, header_row, main_df], ignore_index=True)

# Rename the first two columns to the values found in the absolute first row
# Use the very first row (index 0) so metadata's first entry can be used as column names
first_val = str(main_df.iloc[0, 0]) if not pd.isna(main_df.iloc[0, 0]) else main_df.columns[0]
second_val = str(main_df.iloc[0, 1]) if main_df.shape[1] > 1 and not pd.isna(main_df.iloc[0, 1]) else main_df.columns[1]
# Avoid empty string column names — keep original if empty after strip
if first_val.strip():
    main_df.rename(columns={main_df.columns[0]: first_val}, inplace=True)
if second_val.strip():
    main_df.rename(columns={main_df.columns[1]: second_val}, inplace=True)


# Set all other column names (from index 2 onward) to an empty string
# This keeps only the first two columns as meaningful names and makes
# the remaining column headers blank as requested.
if main_df.shape[1] > 2:
    cols_to_blank = list(main_df.columns[2:])
    # Map each remaining column name to an empty string (duplicates allowed)
    mapping = {c: "" for c in cols_to_blank}
    main_df.rename(columns=mapping, inplace=True)

df = main_df.iloc[1:]

# ========================================================================
# ============================= END HERE =================================
# ========================= DO NOT EDIT BELOW ============================
# ========================================================================

# Write the final main table (with metadata rows prepended) to CSV
df.to_csv("results.csv", index=False)