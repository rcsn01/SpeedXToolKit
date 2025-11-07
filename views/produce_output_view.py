import customtkinter as ctk
from tkinter import messagebox
from styles import TkinterDialogStyles, ButtonStyles, AppFonts, PanelStyles


def produce_output_view(df):
    """Display all columns with checkboxes and allow user to select which ones to keep."""
    try:
        # Create main dialog
        root = ctk.CTk()  # Or use ctk.CTkToplevel() if this is a popup in an existing Tkinter app
        root.title("Output Selection")
        root.geometry("500x500")
        # Use centralized panel/dialog colors
        root.configure(fg_color=PanelStyles.PREVIEW.get("fg_color", TkinterDialogStyles.DIALOG_BG))

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
        ctk.CTkLabel(
            root,
            text="Select columns to be included in output:",
            font=AppFonts.BODY,
            fg_color=PanelStyles.PREVIEW.get("fg_color", TkinterDialogStyles.DIALOG_BG),
            text_color=TkinterDialogStyles.LABEL_FG,
        ).pack(pady=10)

        # Scrollable frame setup using customtkinter's CTkScrollableFrame
        checkbox_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        checkbox_frame.pack(fill="both", expand=True, padx=10, pady=5)
        # CTkScrollableFrame provides an internal scrollable area and scrollbar
        scrollable_frame = ctk.CTkScrollableFrame(checkbox_frame, fg_color=TkinterDialogStyles.FRAME_BG)
        scrollable_frame.pack(fill="both", expand=True)

        # Add checkboxes for each column (each BooleanVar now explicitly attached to `root`)
        for col in df.columns:
            var = ctk.BooleanVar(master=root)  # explicitly bind to root
            cb = ctk.CTkCheckBox(
                scrollable_frame,
                text=col,
                variable=var,
                text_color=TkinterDialogStyles.CHECKBOX_FG,
                anchor='w'
            )
            cb.pack(fill='x', anchor='w', pady=2)
            checkbox_vars[col] = var

        # Confirm/Cancel buttons
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=20)

        # Apply centralized button styles
        primary = ButtonStyles.PRIMARY
        default = ButtonStyles.DEFAULT

        ctk.CTkButton(
            button_frame,
            text="Confirm",
            command=on_confirm,
            width=primary.get("width"),
            height=primary.get("height"),
            corner_radius=primary.get("corner_radius"),
            fg_color=primary.get("fg_color"),
            hover_color=primary.get("hover_color"),
            text_color=primary.get("text_color"),
            font=primary.get("font"),
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=on_cancel,
            width=default.get("width"),
            height=default.get("height"),
            corner_radius=default.get("corner_radius"),
            fg_color=default.get("fg_color"),
            hover_color=default.get("hover_color"),
            text_color=default.get("text_color"),
            font=default.get("font"),
        ).grid(row=0, column=1, padx=10)

        root.mainloop()

        if result["confirmed"]:
            rstring = ", ".join(result["selected_columns"])
            return df, rstring
        else:
            return None, None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None
