import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

def rename_column_view(df):
    """Allow the user to select a column from the DataFrame and rename it."""
    try:
        root = tk.Tk()
        root.title("Rename Column")
        root.geometry("600x200")

        result = {"confirmed": False}

        # Frame for selecting the column
        select_frame = tk.Frame(root)
        select_frame.pack(pady=10)

        tk.Label(select_frame, text="Select Column to Rename").grid(row=0, column=0, padx=5, sticky="w")

        column_selector = ttk.Combobox(select_frame, values=list(df.columns), width=20)
        column_selector.grid(row=0, column=1, padx=5, sticky="w")
        column_selector.set(df.columns[0])  # default selection

        # Frame for entering the new name
        rename_frame = tk.Frame(root)
        rename_frame.pack(pady=10)

        tk.Label(rename_frame, text="New Column Name").grid(row=0, column=0, padx=5, sticky="w")
        new_name_entry = tk.Entry(rename_frame, width=20)
        new_name_entry.grid(row=0, column=1, padx=5, sticky="w")

        # Button actions
        def on_confirm():
            selected_column = column_selector.get()
            new_name = new_name_entry.get().strip()

            if not new_name:
                messagebox.showerror("Invalid Input", "New column name cannot be empty.")
                return

            result["confirmed"] = True
            result["target_name"] = selected_column
            result["new_name"] = new_name

            root.quit()
            root.destroy()

        def on_cancel():
            root.quit()
            root.destroy()

        # Button Frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Cancel", command=root.destroy).grid(row=0, column=1, padx=10)

        root.mainloop()

        if result["confirmed"]:
            return df, result["target_name"], result["new_name"]
        else:
            return None, None, None

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None
