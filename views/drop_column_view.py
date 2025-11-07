import customtkinter as ctk
from tkinter import messagebox
from styles import TkinterDialogStyles, AppColors, AppFonts, ButtonStyles

def drop_column_view(df):
    """Display all columns with checkboxes and allow user to select which ones to keep."""
    try:
        root = ctk.CTk()
        root.title("Remove Columns")
        root.geometry("460x420")
        root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

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
            root.quit()

        def on_cancel():
            root.quit()
            root.destroy()

        # Instruction label (use centralized fonts/colors)
        ctk.CTkLabel(root, text="Select the columns you want to remove:",
                     font=AppFonts.BODY, text_color=AppColors.BLACK).pack(pady=10)

        # Scrollable frame setup
        scrollable_frame = ctk.CTkScrollableFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add checkboxes for each column
        for col in df.columns:
            var = ctk.BooleanVar(master=root)
            cb = ctk.CTkCheckBox(scrollable_frame, text=col, variable=var,
                                text_color=AppColors.BLACK)
            cb.pack(fill='x', anchor='w', pady=2)
            checkbox_vars[col] = var

        # Confirm/Cancel buttons
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=12)
        ctk.CTkButton(button_frame, text="Confirm", command=on_confirm, **ButtonStyles.DEFAULT).grid(row=0, column=0, padx=8)
        ctk.CTkButton(button_frame, text="Cancel", command=on_cancel, **ButtonStyles.DEFAULT).grid(row=0, column=1, padx=8)

        root.mainloop()

        if result["confirmed"]:
            rstring = ", ".join(result["selected_columns"])
            return df, rstring
        else:
            return None, None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None