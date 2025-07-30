import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

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
                
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        common_cols = list(set(df1.columns).intersection(set(df2.columns)))

        """Display all columns with checkboxes and allow user to select which ones to keep."""
        root = tk.Tk()  # Or use tk.Toplevel() if this is a popup in an existing Tkinter app
        root.title("Remove Columns")
        root.geometry("500x500")

        result = {"confirmed": False, "selected_columns": []}
        checkbox_vars = {}

        def on_confirm():
            selected = [col for col, var in checkbox_vars.items() if var.get()]
            if not selected:
                messagebox.showwarning("No columns selected", "Please select at least one column to remove.")
                return
            result["confirmed"] = True
            result["selected_columns"] = selected
            # Closing the window
            root.destroy()
            root.quit()  # (Optional: `destroy()` is usually enough to exit mainloop)
        
        # Instruction label
        tk.Label(root, text="Select the columns to merge on:", 
                font=("Arial", 12, "bold")).pack(pady=10)

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
            var = tk.BooleanVar(master=root)  # explicitly bind to root
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
            rstring = ", ".join(result["selected_columns"])
            #print(rstring)
            return pd.merge(df1, df2, on=result["selected_columns"])
        else:
            return None, None
    except Exception as e:
        print("OHHH NOOOOOOOOO")
        print(f"Error: {e}")
        return None