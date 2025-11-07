import customtkinter as ctk
import pandas as pd
from tkinter import messagebox
from styles import TkinterDialogStyles

def remove_empty_rows_view(df):
    """Allow the user to select a column from the DataFrame and rename it."""
    try:
        root = ctk.CTk()
        root.title("Remove Empty Rows")
        # Slightly smaller window but allow selector to be wider and expand
        root.geometry("480x180")
        root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

        result = {"confirmed": False, "target_name": ""}

        # Frame for selecting the column
        select_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        select_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(select_frame, text="Select column to detect empty rows from.",
                     fg_color=TkinterDialogStyles.FRAME_BG, text_color=TkinterDialogStyles.LABEL_FG,
                     font=TkinterDialogStyles.LABEL_FONT).grid(row=0, column=0, padx=5, sticky="w")

        # Make the selector wider and allow it to expand if layout changes
        column_selector = ctk.CTkComboBox(select_frame, values=list(df.columns), width=360, state="readonly")
        select_frame.grid_columnconfigure(1, weight=1)
        column_selector.grid(row=0, column=1, padx=5, sticky="ew")
        column_selector.set(df.columns[0])  # default selection

        # Frame for entering the new name (placeholder for future UI)
        rename_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
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
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=10)

        root.mainloop()

        if result["confirmed"]:
            return df, result["target_name"]
        else:
            return None, None

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None
