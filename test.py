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
plugin_name = "PlexPCR VHS (LC480) v2.1"
colour_compensation = "201210 SpeeDx Colour Comp.ixo (PlexPCR)"
kit_lot_number = "25040026"

# ========================================================================
# DO NOT EDIT BELOW THIS LINE
# ========================================================================

# Select the Target_1 set
df1 = df[['Sample ID', 'AssayCode', 'Target_1', 'Target_1_wells', 'Target_1_cq']].copy()

# Select the Target_2 set and rename columns so they match Target_1 column names
df2 = df[['Sample ID', 'AssayCode', 'Target_2', 'Target_2_wells', 'Target_2_cq']].copy()
df2 = df2.rename(columns={
	'Target_2': 'Target_1',
	'Target_2_wells': 'Target_1_wells',
	'Target_2_cq': 'Target_1_cq'
})

# Preserve original row order and ensure Target_1 row comes before Target_2 row
df1['__orig_idx'] = df1.index
df1['__kind'] = 1
df2['__orig_idx'] = df2.index
df2['__kind'] = 2

# Concatenate and sort to interleave rows per original record
df = pd.concat([df1, df2], ignore_index=True)
df = df.sort_values(['__orig_idx', '__kind']).drop(columns=['__orig_idx', '__kind']).reset_index(drop=True)

# Remove duplicated entries where AssayCode, Target_1 and Target_1_wells are identical.
# Keep the first occurrence so the original Target_1 row remains and Target_2
# duplicates (if any) are removed.
df = df.drop_duplicates(subset=['AssayCode', 'Target_1', 'Target_1_wells'], keep='first').reset_index(drop=True)

# Rename Target_1-style columns to the requested names
df = df.rename(columns={
    'AssayCode': 'Mix',
	'Target_1': 'Target',
	'Target_1_wells': 'Well',
	'Target_1_cq': 'Cq',
	'Sample ID': 'Sample name'
})
# Add requested empty columns and order the DataFrame columns as specified by the user
desired_order = [
	'Plugin', 'Mix', 'Colour compensation', 'Kit lot number', 'Well',
	'Sample name', 'Fluor', 'Target', 'Cq', 'Sample comment',
	'Audit trail', 'Warning', 'LIMS warning'
]
print(df)

# Ensure all requested columns exist (fill with empty strings) then reorder
for col in desired_order:
	if col not in df.columns:
		df[col] = ''

# Reorder the columns to match the requested order
df = df[desired_order]

# Populate the columns with the variable values
df['Plugin'] = plugin_name
df['Colour compensation'] = colour_compensation
df['Kit lot number'] = kit_lot_number

# Add metadata rows at the top of the DataFrame
metadata_rows = [
    ['Runfile created by user', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['Analysis created by user', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['Run Started', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['Cycler Serial Number', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['FastFinder Version', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['Report created', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['Note', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', ''],  # Empty line
    # Add column headers as a data row
    ['Plugin', 'Mix', 'Colour compensation', 'Kit lot number', 'Well', 
     'Sample name', 'Fluor', 'Target', 'Cq', 'Sample comment', 
     'Audit trail', 'Warning', 'LIMS warning']
]

# Create a metadata DataFrame with the same columns
metadata_df = pd.DataFrame(metadata_rows, columns=desired_order)

# Concatenate metadata with the main dataframe
df = pd.concat([metadata_df, df], ignore_index=True)

# Rename first column to 'File Name' and set the rest to empty strings
cols = ['File Name'] + [''] * (len(df.columns) - 1)
df.columns = cols

# ========================================================================
# ============================= END HERE =================================
# ========================= DO NOT EDIT BELOW ============================
# ========================================================================

print(df)
