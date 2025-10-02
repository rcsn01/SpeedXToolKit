import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def custom_code_view():
    """Display a dialog for user to input custom Python code to process the dataframe."""
    root = tk.Toplevel()  # Use Toplevel for popup in existing app
    root.title("Custom Code Processing")
    root.geometry("600x400")
    root.resizable(True, True)

    result = {"confirmed": False, "code": ""}

    def on_confirm():
        code = code_text.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("No code entered", "Please enter some Python code to execute.")
            return
        result["confirmed"] = True
        result["code"] = code
        root.destroy()

    def on_cancel():
        result["confirmed"] = False
        result["code"] = ""
        root.destroy()

    # Instruction label
    tk.Label(root, text="Enter Python code to process the dataframe.\nUse 'df' as the input dataframe variable.\nThe result should be assigned back to 'df'.",
             font=("Arial", 10)).pack(pady=10, padx=10, anchor='s')

    # Text area for code input
    code_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=("Courier", 10))
    code_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Example code
    example_code = """# Example: Select and rename columns
df = df[['Sample ID', 'Target_1', 'Target_1_wells', 'Target_1_cq']].copy()
df = df.rename(columns={'Sample ID': 'sample id', 'Target_1': 'target name', 'Target_1_wells': 'target well', 'Target_1_cq': 'target cq'})"""
    code_text.insert(tk.END, example_code)

    # Buttons frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel, width=10)
    cancel_button.pack(side=tk.LEFT, padx=5)

    confirm_button = tk.Button(button_frame, text="Execute", command=on_confirm, width=10)
    confirm_button.pack(side=tk.LEFT, padx=5)

    # Wait for the window to close
    root.wait_window()

    return result