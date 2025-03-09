import pandas as pd

def find_header_row(df):
    """Find the first row where more than 3 columns have data."""
    for i, row in df.iterrows():
        non_empty_count = row.count()  # Count non-empty cells in the row
        if non_empty_count > 3:  # If more than 3 columns have data, use this row as the header
            return i
    return None  # Return None if no valid header is found


def choose_header(file_path):
    try:
        # Read the entire file first
        df = pd.read_excel(file_path, engine='xlrd', header=None)
        
        def truncate_text(text, max_length=50):
            """Truncate text if it's too long and add '...' at the end."""
            if isinstance(text, str) and len(text) > max_length:
                return text[:max_length] + "..."
            return text

        # Apply truncation to the first 50 rows and 5 columns
        df_preview = df.iloc[:100, :5].applymap(lambda x: truncate_text(x, max_length=50))

        # Display the truncated DataFrame
        print("Preview of the file (first 50 rows, first 5 columns, truncated text):")
        print(df_preview.to_string(index=True))

        # Ask the user for the row number where column names start
        header_row = int(input("\nEnter the row number where column names start (0-based index): "))

        return header_row
    except Exception as e:
        print(f"Error: {e}")
        return None

def load_xls_with_auto_header(file_path):
    try:
        # Read the entire file first without setting a header
        df = pd.read_excel(file_path, engine='xlrd', header=None)

        # Find the first row that has more than 3 non-empty columns
        header_row = find_header_row(df)
        print(f"\nDetected header at row {header_row}.")
        selection = input(f"header row is {header_row}, press Y to proceed, press X to manually input header row:")
        if selection == "X":
            header_row = choose_header(file_path)

        elif selection == "Y":
            if header_row is None:
                print("No valid header row found.")
                return None
            print("Auto header selected.")

        # Read the file again using the detected header row
        df = pd.read_excel(file_path, engine='xlrd', header=header_row)

        # Print column names
        print("\nColumns detected in the file:")
        print(df.columns.tolist())

        return df  # Returning the DataFrame

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
file_path = "241219 RA091 QS5Dx Sid RPGC gyrA Diomni Test.xls"  # Replace with your actual file path
df = load_xls_with_auto_header(file_path)


print(df.head)

#Well, Well Position, Sample Name, Target Name, CT


def filter_columns(df):
    try:
        # Show available columns
        print("\nAvailable columns:")
        for col in df.columns:
            print(col)

        # Ask the user for the columns they want to keep
        selected_columns = input("\nEnter the column names you want to keep (comma-separated): ").split(",")

        # Trim spaces and ensure valid columns
        selected_columns = [col.strip() for col in selected_columns if col.strip() in df.columns]

        if not selected_columns:
            print("No valid columns selected. Exiting.")
            return None

        # Filter the DataFrame
        filtered_df = df[selected_columns]

        print("\nFiltered DataFrame:")
        print(filtered_df.head())  # Show the first few rows of the filtered DataFrame

        return filtered_df  # Returning the filtered DataFrame

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
# Assuming 'df' is already loaded
filtered_df = filter_columns(df)


def pivot_dataframe(df):
    try:
        # Pivot the DataFrame
        df_pivot = df.pivot_table(index=["Well", "Well Position", "Sample Name"], columns="Target Name", values="CT", aggfunc="first").reset_index()

        # Fix column names
        df_pivot.columns.name = None  # Remove the column index name
        print("\nTransformed DataFrame:")
        print(df_pivot.head())  # Show first few rows

        return df_pivot
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
# Assuming 'df' is already loaded
df = pivot_dataframe(df)


import pandas as pd

def save_dataframe(df):
    try:
        if df is None or df.empty:
            print("DataFrame is empty. Nothing to save.")
            return

        # Ask the user for the desired file format
        file_format = input("Enter file format to save (csv/xlsx): ").strip().lower()

        # Ask for a filename
        file_name = input("Enter the file name (without extension): ").strip()

        if file_format == "csv":
            file_path = f"{file_name}.csv"
            df.to_csv(file_path, index=False)
            print(f"DataFrame saved as {file_path}")

        elif file_format == "xlsx":
            file_path = f"{file_name}.xlsx"
            df.to_excel(file_path, index=False, engine='openpyxl')  # Use openpyxl for writing
            print(f"DataFrame saved as {file_path}")

        else:
            print("Invalid format. Please enter 'csv' or 'xlsx'.")
    
    except Exception as e:
        print(f"Error: {e}")

# Example usage
# Assuming 'df' is already loaded
save_dataframe(df)
