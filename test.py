# ...existing code...
from pathlib import Path
import pandas as pd
import numpy as np

CSV_PATH = Path(__file__).parent / 'test.csv'
path = CSV_PATH

df = pd.read_csv(path)

# Editable variables at top of file
# VIABILITY THRESHOLDS
CT_GAT = 29.7
CT_NED = 30.6
NG_GAT = 30.6
NG_NED = 32

# INDEX THRESHOLDS
CT_INDEX_THRESHOLD = 1.57
NG_INDEX_THRESHOLD = 1.46

# DECIMAL PRECISION
DECIMAL_PRECISION = 2  # Number of decimal places to round CT/NG/EC values

# ========================================================================
# DO NOT EDIT BELOW THIS LINE
# ========================================================================

# Evaluate CT columns
df['CT Index'] = pd.NA

ct_cols = ['CT GAT', 'CT NED']
df_ct = df.reindex(columns=ct_cols)  # missing cols become NaN
# A row is 'missing' if all CT columns are NaN
ct_missing_mask = df_ct.apply(lambda row: all(pd.isna(x) for x in row), axis=1)
# Start with empty values
df['Sample Interpretation for CT'] = ''
df.loc[ct_missing_mask, 'Sample Interpretation for CT'] = 'CT not detected'

# Now apply thresholds: convert CT columns to numeric (coerce errors -> NaN)
ct_num = df_ct.apply(lambda col: pd.to_numeric(col, errors='coerce'))


# Calculate delta between CT NED and CT GAT and compute index = (2^delta)/2
# Use numeric Ct values (ct_num) so non-numeric become NaN
if 'CT GAT' in ct_num.columns and 'CT NED' in ct_num.columns:
    # delta = CT_NED - CT_GAT (positive delta means CT_NED larger)
    delta = ct_num['CT NED'] - ct_num['CT GAT']
    ct_index = (2 ** delta) / 2
    # Persist CT Index column
    df['CT Index'] = ct_index
    # Only consider rows where both numeric Ct values exist
    ct_both_numeric = (~ct_num['CT GAT'].isna()) & (~ct_num['CT NED'].isna())
    # Viable when index > threshold, Unviable when index <= threshold
    ct_viable_mask = ct_both_numeric & (ct_index > CT_INDEX_THRESHOLD)
    ct_unviable_mask = ct_both_numeric & (ct_index <= CT_INDEX_THRESHOLD)
    # Only set values where we haven't already set an interpretation (don't overwrite)
    empty_ct_field = df['Sample Interpretation for CT'].eq('')
    df.loc[ct_viable_mask & empty_ct_field, 'Sample Interpretation for CT'] = 'CT detected, Viable'
    df.loc[ct_unviable_mask & empty_ct_field, 'Sample Interpretation for CT'] = 'CT detected, Non-Viable'

# Evaluate NG columns
df['NG Index'] = pd.NA

ng_cols = ['NG GAT', 'NG NED']
df_ng = df.reindex(columns=ng_cols)
ng_missing_mask = df_ng.apply(lambda row: all(pd.isna(x) for x in row), axis=1)
# Start with empty values
df['Sample Interpretation for NG'] = ''
df.loc[ng_missing_mask, 'Sample Interpretation for NG'] = 'NG not detected'

# Thresholds for NG
ng_num = df_ng.apply(lambda col: pd.to_numeric(col, errors='coerce'))
ng_detect_mask = pd.Series(False, index=df.index)

# Calculate delta between NG NED and NG GAT and compute index = (2^delta)/2
if 'NG GAT' in ng_num.columns and 'NG NED' in ng_num.columns:
    delta_ng = ng_num['NG NED'] - ng_num['NG GAT']
    ng_index = (2 ** delta_ng) / 2
    # Persist NG Index column
    df['NG Index'] = ng_index
    # Only consider rows where both numeric NG values exist
    ng_both_numeric = (~ng_num['NG GAT'].isna()) & (~ng_num['NG NED'].isna())
    # Viable when index > threshold, Unviable when index <= threshold
    ng_viable_mask = ng_both_numeric & (ng_index > NG_INDEX_THRESHOLD)
    ng_unviable_mask = ng_both_numeric & (ng_index <= NG_INDEX_THRESHOLD)
    # Only set values where we haven't already set an interpretation (don't overwrite)
    empty_ng_field = df['Sample Interpretation for NG'].eq('')
    df.loc[ng_viable_mask & empty_ng_field, 'Sample Interpretation for NG'] = 'NG detected, Viable'
    df.loc[ng_unviable_mask & empty_ng_field, 'Sample Interpretation for NG'] = 'NG detected, Non-Viable'

# If any CT column exceeds its threshold mark as detected/indeterminate
ct_detect_mask = pd.Series(False, index=df.index)
if 'CT GAT' in ct_num.columns:
    ct_detect_mask = ct_detect_mask | (ct_num['CT GAT'] > CT_GAT)
if 'CT NED' in ct_num.columns:
    ct_detect_mask = ct_detect_mask | (ct_num['CT NED'] > CT_NED)
df.loc[ct_detect_mask, 'Sample Interpretation for CT'] = 'CT detected, Indeterminate Viability'

if 'NG GAT' in ng_num.columns:
    ng_detect_mask = ng_detect_mask | (ng_num['NG GAT'] > NG_GAT)
if 'NG NED' in ng_num.columns:
    ng_detect_mask = ng_detect_mask | (ng_num['NG NED'] > NG_NED)
df.loc[ng_detect_mask, 'Sample Interpretation for NG'] = 'NG detected, Indeterminate Viability'

# If EC is NaN, mark both interpretations as invalid and request repeat/re-extraction
if 'EC' in df.columns:
    ec_missing_mask = df['EC'].isna()
    msg = 'Invalid EC, repeat test/re-extract sample'
    df.loc[ec_missing_mask, 'Sample Interpretation for CT'] = msg
    df.loc[ec_missing_mask, 'Sample Interpretation for NG'] = msg

# Round specified columns to configured decimal precision
columns_to_round = ['CT GAT', 'CT NED', 'EC', 'NG GAT', 'NG NED', 'CT Index', 'NG Index']
for col in columns_to_round:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(DECIMAL_PRECISION)

print(df.to_string(index=False))
