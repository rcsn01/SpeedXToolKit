import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

def remove_empty_rows_view(df):
    """Allow the user to select a column from the DataFrame and rename it."""
    try:
        root = tk.Tk()
        root.title("Remove Empty Rows")
        root.geometry("600x200")

        result = {"confirmed": False, "target_name": ""}

        # Frame for selecting the column
        select_frame = tk.Frame(root)
        select_frame.pack(pady=10)

        tk.Label(select_frame, text="Select column to detect empty rows from.").grid(row=0, column=0, padx=5, sticky="w")

        column_selector = ttk.Combobox(select_frame, values=list(df.columns), width=20)
        column_selector.grid(row=0, column=1, padx=5, sticky="w")
        column_selector.set(df.columns[0])  # default selection

        # Frame for entering the new name
        rename_frame = tk.Frame(root)
        rename_frame.pack(pady=10)

        # Button actions
        def on_confirm():
            selected_column = column_selector.get()

            if not selected_column:
                messagebox.showerror("Invalid Input", "You must select a column.")
                return

            result["confirmed"] = True
            result["target_name"] = selected_column

            root.quit()
            root.destroy()

        def on_cancel():
            root.quit()
            root.destroy()

        # Button Frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=10)

        root.mainloop()

        if result["confirmed"]:
            return df, result["target_name"]
        else:
            return None, None

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None
