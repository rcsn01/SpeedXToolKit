import pandas as pd
from tkinter.simpledialog import askinteger, askstring

def find_header_row(df):
    """Find the first row where more than 3 columns have data."""
    for i, row in df.iterrows():
        if row.count() > 3:
            return i
    return None

def choose_header(file_path):
    """Prompt user to manually select header row."""
    try:
        df = pd.read_excel(file_path, engine="xlrd", header=None)
        header_row = askinteger("Select Header", "Enter the row number where column names start (0-based index):")
        return header_row
    except Exception as e:
        print(f"Error: {e}")
        return None

def load_xls_with_auto_header(file_path):
    try:
        df = pd.read_excel(file_path, engine="xlrd", header=None)
        header_row = find_header_row(df)

        selection = askstring("Header Selection", f"Detected header at row {header_row}. Press 'Y' to accept, 'X' to manually input:")
        if selection and selection.upper() == "X":
            header_row = choose_header(file_path)

        df = pd.read_excel(file_path, engine="xlrd", header=header_row)
        print("Columns detected:", df.columns.tolist())

        return df
    except Exception as e:
        print(f"Error: {e}")
        return None
