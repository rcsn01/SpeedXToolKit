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
# None

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
# Build a stable list of target names detected earlier (from the long->wide conversion)
# `all_targets` was collected before pivoting; fall back to scanning columns if missing.
try:
    target_names = sorted(all_targets)
except NameError:
    # Derive from dataframe columns like "<target> Cq"
    target_names = sorted({col.rsplit(' ', 1)[0] for col in df.columns if col.endswith(' Cq')})

# Helper to check whole-word membership without using `re`.
def _has_word(s, words):
    if not isinstance(s, str):
        return False
    low = s.lower()
    # Replace non-alphanumeric characters with spaces, then check tokens
    tokens = ''.join(ch if ch.isalnum() else ' ' for ch in low).split()
    for w in words:
        if w.lower() in tokens:
            return True
    return False

# Identify internal-control-like targets (names containing 'ic', 'internal', or 'control')
ic_candidates = [t for t in target_names if _has_word(t, ['ic', 'internal', 'control'])]

def interpret_row(row):
    detected = []
    non_ic_targets = [t for t in target_names if t not in ic_candidates]

    for t in non_ic_targets:
        cq_col = f"{t} Cq"
        notif_col = f"{t} Notifications"

        # Consider a target 'detected' if it has a non-missing Cq or a notification indicating detection/mutation/pos
        has_cq = (cq_col in row.index and pd.notna(row[cq_col]))
        has_notif = False
        if notif_col in row.index and isinstance(row[notif_col], str):
            low_notif = row[notif_col].lower()
            # simple substring checks (case-insensitive)
            if any(k in low_notif for k in ('detect', 'mutation', 'pos', 'positive')):
                has_notif = True
        if has_cq or has_notif:
            detected.append(t)

    parts = []
    if non_ic_targets:
        if detected:
            parts.append(", ".join(detected) + " detected")

        # Report not-detected targets (those non-IC targets for which we found no evidence)
        not_detected = [t for t in non_ic_targets if t not in detected]
        if not_detected:
            parts.append(", ".join(not_detected) + " not detected")
    else:
        parts.append("No targets available")

    # Add IC status if an IC-like target exists
    if ic_candidates:
        ic_detected = False
        for ic in ic_candidates:
            ic_cq = f"{ic} Cq"
            ic_notif = f"{ic} Notifications"
            if (ic_cq in row.index and pd.notna(row[ic_cq])):
                ic_detected = True
                break
            if ic_notif in row.index and isinstance(row[ic_notif], str):
                low_ic_notif = row[ic_notif].lower()
                if any(k in low_ic_notif for k in ('detect', 'pos', 'positive')):
                    ic_detected = True
                    break
                ic_detected = True
                break
        parts.append("IC detected" if ic_detected else "IC not detected")

    return ", ".join(parts)

# Populate the Overall Result column using the interpretation function
if 'Overall Result' not in df.columns:
    df.insert(3, 'Overall Result', '')
df['Overall Result'] = df.apply(interpret_row, axis=1)



# ========================================================================
# ============================= END HERE =================================
# ========================= DO NOT EDIT BELOW ============================
# ========================================================================

# Write the final main table (with metadata rows prepended) to CSV
df.to_csv("results.csv", index=False)