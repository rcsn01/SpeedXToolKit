import tkinter as tk
from tkinter import filedialog, messagebox
from controllers.file_controller import load_xls_with_auto_header
from controllers.save_controller import save_dataframe
import pandas as pd
from models.dataframe_model import *

class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.file_path = None
        self.df = None  # Store the loaded DataFrame

        # Title Label
        tk.Label(self, text="XLS Processor", font=("Arial", 18, "bold")).pack(pady=10)

        # Load File Button
        self.load_button = tk.Button(self, text="Load XLS File", command=self.load_file)
        self.load_button.pack(pady=5)

        # Save File Button
        self.save_button = tk.Button(self, text="Save Processed File", command=self.save_file, state=tk.DISABLED)
        self.save_button.pack(pady=5)

        # DataFrame Preview Label
        self.preview_label = tk.Label(self, text="DataFrame Preview:")
        self.preview_label.pack(pady=5)

        # Text widget for displaying the DataFrame preview
        self.preview_text = tk.Text(self, height=200, width=500)
        self.preview_text.pack(pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx")])
        if file_path:
            self.file_path = file_path
            self.df = load_xls_with_auto_header(file_path)
            if self.df is not None:
                messagebox.showinfo("Success", "File loaded successfully!")
                self.save_button.config(state=tk.NORMAL)
                self.df = filter_columns(self.df)
                self.df = pivot_dataframe(self.df)
                self.df = clear_undefined(self.df)

                # Update the text widget with the DataFrame preview (first 5 rows)
                self.display_dataframe_preview()

    def display_dataframe_preview(self):
        # Clear any existing text in the text widget
        self.preview_text.delete(1.0, tk.END)
        
        # Convert the entire DataFrame to a string (without the index)
        preview = self.df.to_string(index=False)
        
        # Insert the preview into the text widget
        self.preview_text.insert(tk.END, preview)


    def save_file(self):
        if self.df is not None:
            save_dataframe(self.df)
        else:
            messagebox.showwarning("Warning", "No data to save!")
