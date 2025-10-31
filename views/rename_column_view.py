import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from styles import TkinterDialogStyles

def rename_column_view(df):
    """Allow the user to select a column from the DataFrame and rename it."""
    try:
        root = ctk.CTk()
        root.title("Rename Column")
        root.geometry("600x200")
        root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

        result = {"confirmed": False, "target_name": "", "new_name": ""}

        # Frame for selecting the column
        select_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        select_frame.pack(pady=10)

        ctk.CTkLabel(select_frame, text="Select Column to Rename", 
                     text_color=TkinterDialogStyles.LABEL_FG, font=TkinterDialogStyles.LABEL_FONT).grid(row=0, column=0, padx=5, sticky="w")

        column_selector = ctk.CTkComboBox(select_frame, values=list(df.columns), width=TkinterDialogStyles.INPUT_WIDTH * 8)
        column_selector.grid(row=0, column=1, padx=5, sticky="w")
        column_selector.set(df.columns[0])  # default selection

        # Frame for entering the new name
        rename_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        rename_frame.pack(pady=10)

        ctk.CTkLabel(rename_frame, text="New Column Name", 
                     text_color=TkinterDialogStyles.LABEL_FG, font=TkinterDialogStyles.LABEL_FONT).grid(row=0, column=0, padx=5, sticky="w")
        new_name_entry = ctk.CTkEntry(rename_frame, width=TkinterDialogStyles.INPUT_WIDTH * 8)
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
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=20)
        ctk.CTkButton(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=10)

        root.mainloop()

        if result["confirmed"]:
            return df, result["target_name"], result["new_name"]
        else:
            return None, None, None

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None
