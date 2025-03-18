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

        # Additional buttons
        self.drop_column_button = tk.Button(self, text="Drop Column", command=self.drop_column)
        self.drop_column_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.rename_target_button = tk.Button(self, text="Rename Target", command=self.rename_target)
        self.rename_target_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.pivot_table_button = tk.Button(self, text="Pivot Table", command=self.pivot_table)
        self.pivot_table_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.delta_calculation_button = tk.Button(self, text="Delta Calculation", command=self.delta_calculation)
        self.delta_calculation_button.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.combine_file_button = tk.Button(self, text="Combine File", command=self.combine_file)
        self.combine_file_button.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx")])
        if file_path:
            self.file_path = file_path
            self.df = load_xls(file_path)
            if self.df is not None:
                messagebox.showinfo("Success", "File loaded successfully!")
                self.save_button.config(state=tk.NORMAL)
                self.display_dataframe_preview()

    def display_dataframe_preview(self):
        # Clear any existing text in the text widget
        self.preview_text.delete(1.0, tk.END)
        preview = self.df.to_string(index=False)
        
        # Insert the preview into the text widget
        self.preview_text.insert(tk.END, preview)

    def save_file(self):
        if self.df is not None:
            save_dataframe(self.df)
        else:
            messagebox.showwarning("Warning", "No data to save!")

    def drop_column(self):
        if self.df is not None:
            column_name = simpledialog.askstring("Input", "Enter the column name to drop:")
            if column_name in self.df.columns:
                self.df = self.df.drop(columns=[column_name])
                messagebox.showinfo("Success", f"Column '{column_name}' dropped.")
                self.display_dataframe_preview()
            else:
                messagebox.showerror("Error", "Column not found!")
        else:
            messagebox.showwarning("Warning", "No data loaded!")

    def rename_target(self):
        if self.df is not None:
            old_name = simpledialog.askstring("Input", "Enter the current column name:")
            if old_name in self.df.columns:
                new_name = simpledialog.askstring("Input", "Enter the new column name:")
                self.df = self.df.rename(columns={old_name: new_name})
                messagebox.showinfo("Success", f"Column '{old_name}' renamed to '{new_name}'.")
                self.display_dataframe_preview()
            else:
                messagebox.showerror("Error", "Column not found!")
        else:
            messagebox.showwarning("Warning", "No data loaded!")

    def pivot_table(self):
        if self.df is not None:
            index_column = simpledialog.askstring("Input", "Enter the column to pivot:")
            columns = simpledialog.askstring("Input", "Enter the columns for pivoting (comma separated):")
            values = simpledialog.askstring("Input", "Enter the values column:")
            
            columns = [col.strip() for col in columns.split(',')]
            pivot_df = self.df.pivot_table(index=index_column, columns=columns, values=values, aggfunc='sum')
            self.df = pivot_df
            messagebox.showinfo("Success", "Pivot table created.")
            self.display_dataframe_preview()
        else:
            messagebox.showwarning("Warning", "No data loaded!")

    def delta_calculation(self):
        if self.df is not None:
            column_name = simpledialog.askstring("Input", "Enter the column for delta calculation:")
            if column_name in self.df.columns:
                self.df['Delta'] = self.df[column_name].diff()
                messagebox.showinfo("Success", "Delta calculation added.")
                self.display_dataframe_preview()
            else:
                messagebox.showerror("Error", "Column not found!")
        else:
            messagebox.showwarning("Warning", "No data loaded!")

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
