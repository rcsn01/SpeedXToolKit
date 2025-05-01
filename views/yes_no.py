import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger, askstring
import numpy as np

def yes_no_gui(question):
    """Load Excel file and allow the user to confirm the header row."""
    try:
        root = tk.Tk()
        root.title(question)
        root.geometry("1000x700")

        # Create the main frame
        first_frame = tk.Frame(root)
        first_frame.pack(pady=5)
        
        # Add title and input field for columns to drop
        tk.Label(first_frame, text=question).grid(row=0, column=0, padx=5, sticky="w")
        target_name = tk.Entry(first_frame, width=70)
        target_name.insert(0, '')  # Initialize the entry with empty string
        target_name.grid(row=0, column=1, padx=5, sticky="w")
        
        # Process the user's input
        result = {"input": None}

        def on_confirm():
            """Confirm selection and close window."""
            try:
                result["target_name"] = target_name.get()
                root.quit()
                root.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer for the header row.")

        def on_cancel():
            root.quit()
            root.destroy()

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Confirm", command=on_confirm).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=10)

        # Run the window
        root.mainloop()
        target_name = result["target_name"]
        if target_name == "yes":
            return True
        else:
            return False

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    yes_no_gui("testest")