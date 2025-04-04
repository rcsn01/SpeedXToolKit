import tkinter as tk
from tkinter import filedialog, messagebox
from controllers.save_controller import *
import pandas as pd
from controllers.processing_controller import *

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

        # Load File Button
        self.load_preset_button = tk.Button(self, text="Load Presets", command=self.load_preset)
        self.load_preset_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Save File Button
        self.save_button = tk.Button(self, text="Save Processed File", command=self.save_file, state=tk.DISABLED)
        self.save_button.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # DataFrame Preview Label
        self.preview_label = tk.Label(self, text="DataFrame Preview:")
        self.preview_label.grid(row=2, column=1, padx=10, pady=5, columnspan=2, sticky="w")

        # Text widget for displaying the DataFrame preview
        self.preview_text = tk.Text(self, height=40, width=150)
        self.preview_text.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

        self.button_frame = tk.Frame(self, padx=0, pady=10)
        self.button_frame.grid(row=3, column = 0, padx=5, pady=10)

        # Additional buttons
        self.drop_column_button = tk.Button(self.button_frame, text="Drop Column", command=self.drop_column)
        self.drop_column_button.grid(row=0, column=0, padx=0, pady=5, sticky="w")

        self.rename_target_button = tk.Button(self.button_frame, text="Rename Column", command=self.rename_column)
        self.rename_target_button.grid(row=1, column=0, padx=0, pady=5, sticky="w")

        self.pivot_table_button = tk.Button(self.button_frame, text="Pivot Table", command=self.pivot_table)
        self.pivot_table_button.grid(row=2, column=0, padx=0, pady=5, sticky="w")

        self.delta_calculation_button = tk.Button(self.button_frame, text="Delta Calculation", command=self.delta_calculation)
        self.delta_calculation_button.grid(row=3, column=0, padx=0, pady=5, sticky="w")

        self.combine_file_button = tk.Button(self.button_frame, text="Combine File", command=self.combine_file)
        self.combine_file_button.grid(row=4, column=0, padx=0, pady=5, sticky="w")

        self.combine_file_button = tk.Button(self.button_frame, text="Produce Out Put", command=self.produce_output)
        self.combine_file_button.grid(row=5, column=0, padx=0, pady=5, sticky="w")

        self.combine_file_button = tk.Button(self.button_frame, text="Keep Input", command=self.keep_column)
        self.combine_file_button.grid(row=6, column=0, padx=0, pady=5, sticky="w")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            self.file_path = file_path
            self.df = import_files(file_path)
            if self.df is not None:
                messagebox.showinfo("Success", "File loaded successfully!")
                self.save_button.config(state=tk.NORMAL)

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

    def load_preset(self):
        pass

    def save_file(self):
        if self.df is not None:
            save_dataframe(self.df)
        else:
            messagebox.showwarning("Warning", "No data to save!")

    def drop_column(self):
        if self.df is not None:
            self.df = drop_column(self.df)
            self.display_dataframe_preview()

    def rename_column(self):
        if self.df is not None:
            self.df = rename_column(self.df)
            self.display_dataframe_preview()

    def pivot_table(self):
        if self.df is not None:
            self.df = pivot_table(self.df)
            self.display_dataframe_preview()

    def delta_calculation(self):
        if self.df is not None:
            self.df = delta_calculation(self.df)
            self.display_dataframe_preview()

    def produce_output(self):
        if self.df is not None:
            self.df = delta_calculation(self.df)
            self.display_dataframe_preview()

    def keep_column(self):
        if self.df is not None:
            self.df = keep_column(self.df)
            self.display_dataframe_preview()

    def combine_file(self):
        if self.df is not None:
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx")])
            if file_path:
                df_to_combine = load_xls(file_path)
                if df_to_combine is not None:
                    self.df = pd.concat([self.df, df_to_combine], ignore_index=True)
                    messagebox.showinfo("Success", "Files combined.")
                    self.display_dataframe_preview()
                else:
                    messagebox.showerror("Error", "Failed to load second file.")
        else:
            messagebox.showwarning("Warning", "No data loaded!")
