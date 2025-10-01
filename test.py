from pathlib import Path
import pandas as pd

CSV_PATH = Path(__file__).parent / 'test.csv'


def pivot_csv_simple(path):
    """Read CSV directly with pandas and pivot on 'Target Name' using 'CT' values.

    Assumes the CSV uses UTF-8 compatible encoding and comma delimiter.
    """
    if not path.exists():
        print(f"File not found: {path}")
        return

    # Read directly
    df = pd.read_csv(path)

    # Normalize simple column names (strip whitespace)
    df.columns = [str(c).strip() for c in df.columns]
    print('Columns:', df.columns.tolist())

    target_col = 'Target Name'
    ct_col = 'Cт'
    index_col = 'Well' if 'Well' in df.columns else df.columns[0]

    if target_col not in df.columns:
        print(f"Column {target_col!r} not found in CSV columns")
        return
    if ct_col not in df.columns:
        print(f"Column {ct_col!r} not found in CSV columns")
        return

    df[ct_col] = pd.to_numeric(df[ct_col], errors='coerce')
    usable = df.dropna(subset=[target_col, ct_col])
    print('Usable rows for pivot (non-null target & ct):', len(usable))
    if usable.empty:
        print('No usable rows for pivot. Showing sample rows:')
        print(df.head(20))
        return

    pt = usable.pivot_table(index=index_col, columns=target_col, values=ct_col, aggfunc='first')
    print('\nPivot result (shape={}):'.format(pt.shape))
    print(pt.head(20))


if __name__ == '__main__':
    pivot_csv_simple(CSV_PATH)
