import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
from models.dataframe_model import *


def find_header_row(df):
    """Find the first row where more than 3 columns have data."""
    for i, row in df.iterrows():
        if row.count() > 3:
            return i
    return None

def truncate_text(value, max_length=20):
    """Truncate text if it exceeds the max length, adding '...' at the end."""
    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length] + "..."
    return value

def format_dataframe(df, max_length=20):
    """Apply truncation to all text values in the DataFrame."""
    return df.applymap(lambda x: truncate_text(str(x), max_length))

def file_preview(df, header_row, file_path, root):
    """Display the entire file with truncated text for long cells."""
    
    df_truncated = format_dataframe(df)  # Truncate long text before displaying

    # Create frame with scrollbar
    frame = tk.Frame(root)
    frame.pack(pady=5, padx=5, fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    text_widget = tk.Text(frame, wrap="none", height=20, width=80, yscrollcommand=scrollbar.set)
    text_widget.insert("1.0", df_truncated.to_string(index=True))
    text_widget.config(state="disabled")
    text_widget.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=text_widget.yview)

    # Header selection
    header_frame = tk.Frame(root)
    header_frame.pack(pady=5)
    
    tk.Label(header_frame, text="Header Row:").grid(row=0, column=0, padx=5, sticky="w")
    header_input = tk.Entry(header_frame, width=5)
    header_input.insert(0, str(header_row))
    header_input.grid(row=0, column=1, padx=5, sticky="w")

    # Columns to keep
    columns_frame = tk.Frame(root)
    columns_frame.pack(pady=5)

    tk.Label(columns_frame, text="Columns to Keep:").grid(row=0, column=0, padx=5, sticky="w")
    keep_input = tk.Entry(columns_frame, width=70)
    keep_input.insert(0, "Well, Well Position, Sample Name, Target Name, CT")
    keep_input.grid(row=0, column=1, padx=5, sticky="w")

    # Pivot Target Name & Pivot Value Name - Side by Side
    pivot_frame = tk.Frame(root)
    pivot_frame.pack(pady=5)

    tk.Label(pivot_frame, text="Pivot Target:").grid(row=0, column=0, padx=5, sticky="e")
    target_name = tk.Entry(pivot_frame, width=12)
    target_name.insert(0, "Target Name")
    target_name.grid(row=0, column=1, padx=5)

    tk.Label(pivot_frame, text="Pivot Value:").grid(row=0, column=2, padx=5, sticky="e")
    value_name = tk.Entry(pivot_frame, width=12)
    value_name.insert(0, "CT")
    value_name.grid(row=0, column=3, padx=5)

    # Store result
    result = {"header_row": None}

    def on_confirm():
        """Confirm selection and close window."""
        try:
            user_header_row = int(header_input.get())
            result["header_row"] = user_header_row
            result["keep_input"] = keep_input.get()
            result["target_name"] = target_name.get()
            result["value_name"] = value_name.get()
            root.quit()
            root.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for the header row.")

    def on_cancel():
        """Close window without confirming."""
        root.quit()
        root.destroy()

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=10)

    # Run the window
    root.mainloop()

    return result["header_row"], result["keep_input"], result["target_name"], result["value_name"]


def load_xls(file_path):
    """Load Excel file and allow the user to confirm the header row."""
    try:
        df = pd.read_excel(file_path, engine="xlrd", header=None)
        header_row = find_header_row(df)

        if header_row is not None:
            # Create a Tkinter window for preview and header selection
            root = tk.Tk()
            root.title("Header Row Preview")
            root.geometry("1000x700")

            #print("1AABBBBBABBAAA")
            header_row, keep_input, target_name, value_name = file_preview(df, header_row, file_path, root)  # Show preview and input options
            #print(header_row)
            #print("2AAAAA")
            # Main loop to keep the window open
            #root.mainloop()

            # Once confirmed, reload the dataframe with the chosen header
            df_with_header = pd.read_excel(file_path, engine="xlrd", header=header_row)
            #print("Columns detected:", df_with_header.columns.tolist())

            #print("returnhereee!!!!!!!!")
            #print(df_with_header)
            #print(keep_input)
            loaded_df = filter_columns(df_with_header, keep_input)
            #print("aaaa")
            #print(loaded_df)
            if target_name:
                id_df, target_df = pivot_dataframe(loaded_df, target_name, value_name)
                #print("bbbb")
                target_df = clear_undefined(target_df)
                #print("cccc")
                loaded_df = what_do_i_have(id_df, target_df)
            return loaded_df

    except Exception as e:
        print(f"Error: {e}")
        return None
