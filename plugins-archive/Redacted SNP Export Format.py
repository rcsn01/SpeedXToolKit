import pandas as pd

# Read the CSV file
df = pd.read_csv('test.csv')

# Create DataFrame for Target_1
df1 = df[['Sample ID', 'Target_1', 'Target_1_wells', 'Target_1_cq', 'Target_1_dye']].copy()
df1 = df1.rename(columns={'Sample ID': 'sample id', 'Target_1': 'target name', 'Target_1_wells': 'target well', 'Target_1_cq': 'target cq', 'Target_1_dye': 'target dye'})

# Create DataFrame for Target_2
df2 = df[['Sample ID', 'Target_2', 'Target_2_wells', 'Target_2_cq', 'Target_2_dye']].copy()
df2 = df2.rename(columns={'Sample ID': 'sample id', 'Target_2': 'target name', 'Target_2_wells': 'target well', 'Target_2_cq': 'target cq', 'Target_2_dye': 'target dye'})

# Create DataFrame for Target_3
df3 = df[['Sample ID', 'Target_3', 'Target_3_wells', 'Target_3_cq', 'Target_3_dye']].copy()
df3 = df3.rename(columns={'Sample ID': 'sample id', 'Target_3': 'target name', 'Target_3_wells': 'target well', 'Target_3_cq': 'target cq', 'Target_3_dye': 'target dye'})

dye_to_reporter = {
    'FAM': '465-510 (Auto)',
    'JOE': '533-580 (Auto)',
    'Atto610': '533-640 (Auto)'
}

dfs = []
for df in [df1, df2, df3]:
    target_name = df['target name'].iloc[0]
    dye = df['target dye'].iloc[0]
    reporter = dye_to_reporter.get(dye, 'Unknown')
    
    # Add column header row
    header_row = pd.DataFrame({
        'Detector': ['Detector'],
        'Reporter': ['Reporter'],
        'Start': ['Start'],
        'End': ['End'],
        'Threshold': ['Threshold']
    })
    dfs.append(header_row)
    
    table_df = pd.DataFrame({
        'Detector': [target_name],
        'Reporter': [reporter],
        'Start': ['(Auto)'],
        'End': ['(Auto)'],
        'Threshold': ['(Auto)']
    })
    dfs.append(table_df)
    
    # Add data header
    data_header = pd.DataFrame({
        'Detector': ['Well'],
        'Reporter': ['SampleName'],
        'Start': ['Ct'],
        'End': [''],
        'Threshold': ['']
    })
    dfs.append(data_header)
    
    # Transform df to match columns
    df_data = df[['target well', 'sample id', 'target cq']].rename(columns={
        'target well': 'Detector',
        'sample id': 'Reporter',
        'target cq': 'Start'
    })
    df_data['End'] = ''
    df_data['Threshold'] = ''
    dfs.append(df_data)

df = pd.concat(dfs, ignore_index=True)

# Remove the first row (duplicate header)
df = df.iloc[1:]

print(df.to_string(index=False))
