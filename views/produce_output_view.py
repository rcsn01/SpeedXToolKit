import customtkinter as ctk
from tkinter import messagebox
from styles import TkinterDialogStyles

def produce_output_view(df):
    try:
        """Display all columns with checkboxes and allow user to select which ones to keep."""
        root = ctk.CTk()  # Or use ctk.CTkToplevel() if this is a popup in an existing Tkinter app
        root.title("Output Selection")
        root.geometry("500x500")
        root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

        result = {"confirmed": False, "selected_columns": []}
        checkbox_vars = {}

        def on_confirm():
            selected = [col for col, var in checkbox_vars.items() if var.get()]
            if not selected:
                messagebox.showwarning("No columns selected", "Please select at least one column to keep.")
                return
            result["confirmed"] = True
            result["selected_columns"] = selected
            # Closing the window
            root.destroy()
            root.quit()  # (Optional: `destroy()` is usually enough to exit mainloop)

        def on_cancel():
            root.quit()
            root.destroy()

        # Instruction label
        ctk.CTkLabel(root, text="Select columns to be included in output:", 
                font=TkinterDialogStyles.LABEL_FONT, fg_color=TkinterDialogStyles.DIALOG_BG, 
                text_color=TkinterDialogStyles.LABEL_FG).pack(pady=10)

        # Scrollable frame setup
        checkbox_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        checkbox_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        canvas = tk.Canvas(checkbox_frame, fg_color=TkinterDialogStyles.CANVAS_BG)
        scrollbar = ctk.CTkScrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color=TkinterDialogStyles.FRAME_BG)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add checkboxes for each column (each BooleanVar now explicitly attached to `root`)
        for col in df.columns:
            var = ctk.BooleanVar(master=root)  # explicitly bind to root
            cb = ctk.CTkCheckBox(scrollable_frame, text=col, variable=var,
                              text_color=TkinterDialogStyles.CHECKBOX_FG)
            cb.pack(fill='x', anchor='w', pady=2)
            checkbox_vars[col] = var

        # Confirm/Cancel buttons
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=10)

        root.mainloop()

        if result["confirmed"]:
            rstring = ", ".join(result["selected_columns"])
            return df, rstring
        else:
            return None, None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None
