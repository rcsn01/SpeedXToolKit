# ...existing code...
from pathlib import Path
import pandas as pd
import numpy as np

CSV_PATH = Path(__file__).parent / 'test2.csv'
path = CSV_PATH

df = pd.read_csv(path)

# DO NOT USE FUNCTIONS, DIRECTLY WRITE YOUR CODE BELOW

# ========================================================================
# ============================ START HERE ================================
# ========================================================================

# Editable variables
target_1 = "MgPa"
target_2 = "23S rRNA mutation"
target_3 = "IC"

# ========================================================================
# DO NOT EDIT BELOW THIS LINE
# ========================================================================

# ========================================================================
# KEEPING DATA
# ========================================================================

# Manually kept columns (preserve user's explicit selection order)
manual_keep = [
    'Sample ID', 'AssayResultTargetCode', 'SampleType',
    'Target_1', 'Target_1_wells', 'Target_1_dye', 'Target_1_cq', 'Target_1_notifications',
    'Target_2', 'Target_2_wells', 'Target_2_dye', 'Target_2_cq', 'Target_2_notifications',
    'Target_3', 'Target_3_wells', 'Target_3_dye', 'Target_3_cq', 'Target_3_notifications',
    ]

# Keep only columns that exist in the dataframe (preserve user's explicit order)
existing_cols = [c for c in manual_keep if c in df.columns]
missing = [c for c in manual_keep if c not in df.columns]
if missing:
    # Print a concise warning so the user knows which expected columns were absent
    print("Warning: the following expected columns were not found and will be skipped:", missing)
df = df[existing_cols]

# ========================================================================
# PIVOTING TABLE
# ========================================================================

# Stack all Target_1, Target_2, Target_3 into a long format first
id_cols = ['Sample ID', 'SampleType', 'Target_1_wells']

# Determine which Target columns exist
target_nums = []
for i in range(1, 10):  # Check Target_1 through Target_9
    if f'Target_{i}' in df.columns:
        target_nums.append(i)

# Collect all unique target names to ensure all columns exist
all_targets = set()
for i in target_nums:
    unique_vals = df[f'Target_{i}'].dropna().unique()
    all_targets.update([str(v) for v in unique_vals if str(v) != ''])

# Collect all target rows into a list
rows = []
for idx, row in df.iterrows():
    for i in target_nums:
        target_name = row.get(f'Target_{i}')
        if pd.notna(target_name) and target_name != '':
            rows.append({
                'Sample ID': row['Sample ID'],
                'SampleType': row['SampleType'],
                'Target_1_wells': row['Target_1_wells'],
                'Target': target_name,
                'Cq': row.get(f'Target_{i}_cq'),
                'Dye': row.get(f'Target_{i}_dye'),
                'Notifications': row.get(f'Target_{i}_notifications')
            })

long_df = pd.DataFrame(rows)

# Treat empty strings as missing
for col in ['Cq', 'Dye', 'Notifications']:
    if col in long_df.columns:
        long_df[col] = long_df[col].replace('', pd.NA)

# Pivot so each unique Target becomes its own set of columns
wide = long_df.pivot_table(
    index=id_cols,
    columns='Target',
    values=['Cq', 'Dye', 'Notifications'],
    aggfunc='first'
)

# Flatten MultiIndex columns: (field, target) -> "target field"
wide.columns = [f"{target} {field}" for field, target in wide.columns.to_flat_index()]

# Ensure ALL target columns exist (even if empty) by creating missing ones
for target in sorted(all_targets):
    for field in ['Cq', 'Dye', 'Notifications']:
        col_name = f"{target} {field}"
        if col_name not in wide.columns:
            wide[col_name] = pd.NA

# ==================== Re Order Colums ====================

# Reorder columns so all columns for each target are grouped together
ordered_cols = []
for target in sorted(all_targets):
    for field in ['Cq', 'Dye', 'Notifications']:
        col_name = f"{target} {field}"
        if col_name in wide.columns:
            ordered_cols.append(col_name)

# Reorder: keep index columns first, then ordered target columns
wide = wide[ordered_cols]

df = wide.reset_index()

# Rename "Target_1_wells" to "Well ID"
df = df.rename(columns={'Target_1_wells': 'Well ID'})

# Add "Overall Result" column after "Well ID"
# Insert it at position 3 (after Sample ID, SampleType, Well ID)
df.insert(3, 'Overall Result', '')

# ========================================================================
# Result Interpretation
# ========================================================================

# Helper to determine whether a series cell 'has a value' (non-null and not empty)
def _has_value(series: pd.Series) -> pd.Series:
    return series.notna() & (series.astype(str).str.strip() != "")

# Get number of rows
n = len(df)

if f'{target_1} Cq' in df.columns:
    t1 = _has_value(df[f'{target_1} Cq'])
else:
    # Create with df.index so boolean mask aligns with original rows
    t1 = pd.Series([False] * n, index=df.index)

if f'{target_2} Cq' in df.columns:
    t2 = _has_value(df[f'{target_2} Cq'])
else:
    t2 = pd.Series([False] * n, index=df.index)

if f'{target_3} Cq' in df.columns:
    t3 = _has_value(df[f'{target_3} Cq'])
else:
    t3 = pd.Series([False] * n, index=df.index)

# Build a mask of rows where SampleType == 'Regular'.
# If SampleType column is missing, treat no rows as Regular (so nothing is applied).
if 'SampleType' in df.columns:
    regular_mask = (df['SampleType'] == 'Regular')
    # ensure same index and boolean dtype
    regular_mask = pd.Series(regular_mask.values, index=df.index)
    # Also create mask for PositiveControl samples and NegativeControl samples
    positive_mask = pd.Series((df['SampleType'] == 'PositiveControl').values, index=df.index)
    negative_mask = pd.Series((df['SampleType'] == 'Negative control').values, index=df.index)


else:
    regular_mask = pd.Series([False] * n, index=df.index)
    positive_mask = pd.Series([False] * n, index=df.index)
    negative_mask = pd.Series([False] * n, index=df.index)

# Prepare default empty result/overall series and apply rules vectorised
# Use df.index so later boolean masks align correctly with these Series
overall_series = pd.Series([''] * n, index=df.index)

# Rule A: Only apply to Regular samples: t1 AND t2 AND t3 -> Positive, mutation detected
mask1 = regular_mask & t1 & t2 & t3
overall_series.loc[mask1] = "M. genitalium, 23S rRNA mutation detected."

# Rule B: Only apply to Regular samples
mask2 = regular_mask & t1 & (~t2) & t3
overall_series.loc[mask2] = "M. genitalium detected, 23S rRNA mutation not detected."

# Rule C: Only apply to Regular samples
mask3 = regular_mask & (~t1) & (~t2) & t3
overall_series.loc[mask3] = "M. genitalium not detected. IC valid"

# Rule D: Only apply to Regular samples: IC invalid
mask4 = regular_mask & (~t3)
overall_series.loc[mask4] = "IC invalid"

# ==================== Positive Control ========================

# Rule E: Positive Control is valid if t1 is detected
mask5 = positive_mask & t1
overall_series.loc[mask5] = "Positive Control valid."

# Rule F: Positive Control is invalid if t1 is not detected
mask6 = positive_mask & (~t1)
overall_series.loc[mask6] = "Positive Control invalid."

# Assign computed values back into the main output dataframe
df['Overall Result'] = overall_series.values

# ========================================================================
# ============================= END HERE =================================
# ========================= DO NOT EDIT BELOW ============================
# ========================================================================

# Write the final main table (with metadata rows prepended) to CSV
df.to_csv("results.csv", index=False)