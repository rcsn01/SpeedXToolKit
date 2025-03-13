import tkinter as tk
from tkinter import filedialog, messagebox
from controllers.file_controller import *
from controllers.save_controller import *
import pandas as pd
from models.dataframe_model import *

class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.file_path = None
        self.df = None  # Store the loaded DataFrame

        self.grid(row=0, column=0, sticky="nsew")  # Make the frame expand to the entire window
        master.grid_rowconfigure(0, weight=1)  # Allow the row to expand
        master.grid_columnconfigure(0, weight=1)  # Allow the column to expand

        # Title Label
        tk.Label(self, text="XLS Processor", font=("Arial", 18, "bold")).grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Load File Button
        self.load_button = tk.Button(self, text="Load XLS File", command=self.load_file)
        self.load_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Save File Button
        self.save_button = tk.Button(self, text="Save Processed File", command=self.save_file, state=tk.DISABLED)
        self.save_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # DataFrame Preview Label
        self.preview_label = tk.Label(self, text="DataFrame Preview:")
        self.preview_label.grid(row=2, column=1, padx=10, pady=5, columnspan=2, sticky="w")

        # Text widget for displaying the DataFrame preview
        self.preview_text = tk.Text(self, height=40, width=150)
        self.preview_text.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx")])
        if file_path:
            self.file_path = file_path
            self.df = load_xls(file_path)
            if self.df is not None:
                messagebox.showinfo("Success", "File loaded successfully!")
                self.save_button.config(state=tk.NORMAL)
                #print(self.df)
                #self.df = filter_columns(self.df)
                #print(self.df)
                #id_df, target_df = pivot_dataframe(self.df)
                #target_df = clear_undefined(target_df)
                #self.df = what_do_i_have(id_df, target_df)
                #print(self.df)

                # Update the text widget with the DataFrame preview (first 5 rows)
                self.display_dataframe_preview()

    def display_dataframe_preview(self):
        # Clear any existing text in the text widget
        self.preview_text.delete(1.0, tk.END)
        
        # Convert the entire DataFrame to a string (without the index)
        #print(self.df)
        #print("AAAAAFAGFK:GDKLFGDLKFAD:K")
        preview = self.df.to_string(index=False)
        
        # Insert the preview into the text widget
        self.preview_text.insert(tk.END, preview)

    def save_file(self):
        if self.df is not None:
            save_dataframe(self.df)
        else:
            messagebox.showwarning("Warning", "No data to save!")
