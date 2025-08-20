import pandas as pd

def essay_process_model(df, header_row):
    if df is None or header_row is None:
        return None, None
    if not isinstance(header_row, int) or header_row < 0 or header_row >= len(df):
        return None, None
    df_with_format = df.iloc[:header_row].copy()
    df_with_format.reset_index(drop=True, inplace=True)
    df_with_header = df.iloc[header_row:].copy()
    if df_with_header.empty:
        return df_with_format, None
    # Set first row as header
    raw_headers = df_with_header.iloc[0].astype(str).str.strip().tolist()
    deduped = []
    counts = {}
    for name in raw_headers:
        base = name if name != '' else 'Unnamed'
        counts[base] = counts.get(base, 0) + 1
        if counts[base] == 1:
            deduped.append(base)
        else:
            # Second occurrence becomes 'Name (1)', third 'Name (2)', etc.
            deduped.append(f"{base} ({counts[base]-1})")
    df_with_header.columns = deduped
    df_with_header = df_with_header[1:].reset_index(drop=True)
    return df_with_format, df_with_header