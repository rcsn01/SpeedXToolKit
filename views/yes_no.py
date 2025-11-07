import customtkinter as ctk
import pandas as pd
from views.ctk_dialogs import showinfo, showwarning, showerror, askstring, askinteger, askyesno
from styles import TkinterDialogStyles, AppFonts, ButtonStyles
import numpy as np

def yes_no_gui(question):
    """Load Excel file and allow the user to confirm the header row."""
    try:
        root = ctk.CTk()
        root.title(question)
        root.geometry("1000x700")
        root.configure(fg_color=TkinterDialogStyles.DIALOG_BG)

        # Create the main frame
        first_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        first_frame.pack(pady=5)
        
        # Add title and input field for columns to drop
        ctk.CTkLabel(first_frame, text=question, fg_color=TkinterDialogStyles.FRAME_BG, 
                 text_color=TkinterDialogStyles.LABEL_FG, font=TkinterDialogStyles.LABEL_FONT).grid(row=0, column=0, padx=5, sticky="w")
        target_name = ctk.CTkEntry(
            first_frame,
            width=TkinterDialogStyles.INPUT_WIDTH * 4,
            font=AppFonts.BODY,
        )
        target_name.insert(0, "")  # Initialize the entry with empty string
        target_name.grid(row=0, column=1, padx=5, sticky="w")
        
        # Process the user's input
        result = {"input": None}

        result = {"confirmed": False}

        def on_confirm():
            """Confirm selection and close window."""
            try:
                result["confirmed"] = True
                result["target_name"] = target_name.get()
                root.quit()
                root.destroy()
            except ValueError:
                showerror("Invalid Input", "Please enter a valid integer for the header row.")

        def on_cancel():
            root.quit()
            root.destroy()

        # Buttons
        button_frame = ctk.CTkFrame(root, fg_color=TkinterDialogStyles.FRAME_BG)
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Confirm",
            command=on_confirm,
            **ButtonStyles.PRIMARY,
        ).grid(row=0, column=0, padx=10)
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=on_cancel,
            **ButtonStyles.DEFAULT,
        ).grid(row=0, column=1, padx=10)

        # Run the window
        root.mainloop()


        if result.get("confirmed"):
            target_name = result["target_name"]
            if target_name == "yes":
                return True
            else:
                return False
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    yes_no_gui("testest")