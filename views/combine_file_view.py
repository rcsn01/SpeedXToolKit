import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import csv

def combine_file_view():
    try:
        # Prompt for first file
        file1 = filedialog.askopenfilename(title="Select First CSV File", filetypes=[("CSV files", "*.csv")])
        if not file1:
            messagebox.showinfo("Cancelled", "No file selected.")
            return None

        # Prompt for second file
        file2 = filedialog.askopenfilename(title="Select Second CSV File", filetypes=[("CSV files", "*.csv")])
        if not file2:
            messagebox.showinfo("Cancelled", "No second file selected.")
            return None
                
        def _read_csv_with_fallback(path):
            encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1']
            last_err = None
            # Read small sample for delimiter sniffing
            for enc in encodings:
                try:
                    with open(path, 'r', encoding=enc, newline='') as f:
                        sample = f.read(2048)
                        f.seek(0)
                        # Delimiter detection
                        try:
                            dialect = csv.Sniffer().sniff(sample)
                            delim = dialect.delimiter
                        except csv.Error:
                            delim = ','
                        return pd.read_csv(f, delimiter=delim)
                except UnicodeDecodeError as e:
                    last_err = e
                    continue
                except Exception as e:
                    last_err = e
                    continue
            raise last_err if last_err else RuntimeError('Failed to read CSV with fallback encodings.')

        df1 = _read_csv_with_fallback(file1)
        df2 = _read_csv_with_fallback(file2)

        # If duplicate column names, disambiguate with (1), (2) style
        def _dedupe_cols(cols):
            counts = {}
            result = []
            for c in cols:
                base = (c or '').strip() or 'Unnamed'
                counts[base] = counts.get(base, 0) + 1
                if counts[base] == 1:
                    result.append(base)
                else:
                    result.append(f"{base} ({counts[base]-1})")
            return result
        df1.columns = _dedupe_cols(df1.columns)
        df2.columns = _dedupe_cols(df2.columns)

        common_cols = list(set(df1.columns).intersection(set(df2.columns)))
        if not common_cols:
            messagebox.showerror("No Common Columns", "The selected files share no column names to merge on.")
            return None

        """Display all columns with checkboxes and allow user to select which ones to keep."""
        root = tk.Tk()  # Or use tk.Toplevel() if embedded
        root.title("Combine Files - Select Join Columns")
        root.geometry("520x560")

        result = {"confirmed": False, "selected_columns": []}
        checkbox_vars = {}

        def on_confirm():
            selected = [col for col, var in checkbox_vars.items() if var.get()]
            if not selected:
                messagebox.showwarning("No columns selected", "Please select at least one column to remove.")
                return
            result["confirmed"] = True
            result["selected_columns"] = selected
            root.destroy()
            root.quit()

        # File info display
        info_frame = tk.Frame(root)
        info_frame.pack(fill='x', padx=10, pady=(10,4))
        tk.Label(info_frame, text=f"File 1: {file1}", anchor='w', wraplength=480, justify='left').pack(fill='x')
        tk.Label(info_frame, text=f"File 2: {file2}", anchor='w', wraplength=480, justify='left').pack(fill='x', pady=(2,6))

        # Instruction label
        tk.Label(root, text="Select the columns to merge on (only common columns listed):", 
                 font=("Arial", 11, "bold"), wraplength=480, justify='left').pack(pady=4, padx=10, anchor='w')

        # Scrollable frame setup
        checkbox_frame = tk.Frame(root)
        checkbox_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        canvas = tk.Canvas(checkbox_frame)
        scrollbar = ttk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add checkboxes for each column (each BooleanVar now explicitly attached to `root`)
        for col in common_cols:
            var = tk.BooleanVar(master=root)
            cb = tk.Checkbutton(scrollable_frame, text=col, variable=var, anchor='w', padx=10)
            cb.pack(fill='x', anchor='w')
            checkbox_vars[col] = var

        # Confirm/Cancel buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Cancel", command=root.destroy).grid(row=0, column=1, padx=10)

        root.mainloop()

        if result["confirmed"]:
            return pd.merge(df1, df2, on=result["selected_columns"])
        return None
    except Exception as e:
        print("OHHH NOOOOOOOOO")
        print(f"Error: {e}")
        try:
            messagebox.showerror("Combine Failed", f"Failed to combine files:\n{e}")
        except Exception:
            pass
        return None