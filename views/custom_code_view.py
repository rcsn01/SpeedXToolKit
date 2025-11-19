import customtkinter as ctk
from views.ctk_dialogs import showinfo, showwarning, showerror, askstring, askinteger, askyesno
from styles import TkinterDialogStyles

def custom_code_view():
    """Display a dialog for user to input custom Python code to process the dataframe."""
    root = ctk.CTkToplevel()  # Use Toplevel for popup in existing app
    root.title("Custom Code Processing")
    root.geometry("600x400")
    root.resizable(True, True)
    root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

    # Ensure window is on top and modal
    root.lift()
    root.focus_force()
    root.grab_set()
    try:
        # Try to attach to the main window if available
        if hasattr(ctk, "_get_ancestor_window"):
            parent = ctk._get_ancestor_window()
            if parent:
                root.transient(parent)
    except Exception:
        pass

    result = {"confirmed": False, "code": ""}

    def on_confirm():
        code = code_text.get("1.0", "end-1c").strip()
        if not code:
            showwarning("No code entered", "Please enter some Python code to execute.")
            return
        result["confirmed"] = True
        result["code"] = code
        root.destroy()

    def on_cancel():
        result["confirmed"] = False
        result["code"] = ""
        root.destroy()

    # Instruction label
    ctk.CTkLabel(root, text="Enter Python code to process the dataframe.\nUse 'df' as the input dataframe variable.\nThe result should be assigned back to 'df'.",
             font=TkinterDialogStyles.LABEL_FONT, 
             text_color=TkinterDialogStyles.LABEL_FG).pack(pady=10, padx=10, anchor='s')

    # Text area for code input
    code_text = ctk.CTkTextbox(root, wrap="word", width=550, height=200, font=("Courier", 10),
                               fg_color=TkinterDialogStyles.CANVAS_BG, text_color=TkinterDialogStyles.LABEL_FG)
    code_text.pack(pady=10, padx=10, fill="both", expand=True)

    # Example code
    example_code = """# Example: Select and rename columns
df = df[['Sample ID', 'Target_1', 'Target_1_wells', 'Target_1_cq']].copy()
df = df.rename(columns={'Sample ID': 'sample id', 'Target_1': 'target name', 'Target_1_wells': 'target well', 'Target_1_cq': 'target cq'})"""
    code_text.insert("1.0", example_code)

    # Buttons frame
    button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
    button_frame.pack(pady=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=on_cancel, width=100)
    cancel_button.pack(side="left", padx=5)

    confirm_button = ctk.CTkButton(button_frame, text="Execute", command=on_confirm, width=100)
    confirm_button.pack(side="left", padx=5)

    # Wait for the window to close
    root.wait_window()

    return result