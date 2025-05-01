import tkinter as tk
from tkinter import filedialog, messagebox, Canvas
from controllers.processing_controller import *
from controllers.save_controller import *
import pandas as pd
from models.dataframe_model import *
from models.drop_column_model import *
from models.rename_column_model import *

# Global variables
# Define colour constants used in the app (SpeeDX colors)
COLOURS = {
    "blue_rgb": (32, 165, 221), #SDX Blue
    "purple_rgb": (89, 48, 133), #SDX Purple
    "white_rgb": (255, 255, 255), # White in RGB
    "blue_hex": "#20a5dd", #SDX Blue
    "purple_hex": "#593085", #SDX Purple
    "white_hex": "#FFFFFF" # White in hex
}

# Class for creating a gradient canvas frame (background)
class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1="white", color2="black", **kwargs):
        super().__init__(parent, **kwargs)
        self._color1 = color1 # Start color for gradient
        self._color2 = color2 # End color for gradient
        self.bind("<Configure>", self._draw_gradient) # Redraw gradient when resizing

    def _draw_gradient(self, event=None):
        self.delete("gradient")  # Remove any existing gradient
        width = self.winfo_width()  # Get width of the canvas
        height = self.winfo_height()  # Get height of the canvas
        limit = height  # Use height as the limit for the gradient (vertical gradient)

        # Convert color to RGB
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)

        # Calculate the color difference between start and end colors
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit

        # Draw a gradient line from top to bottom
        for i in range(limit):
            nr = int(r1 + (r_ratio * i))  # New red value
            ng = int(g1 + (g_ratio * i))  # New green value
            nb = int(b1 + (b_ratio * i))  # New blue value
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)  # Convert to hex
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)  # Draw horizontal line for vertical gradient

        self.lower("gradient")  # Ensure the gradient stays behind other elements



class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.file_path = None
        self.df = None  # Store the loaded DataFrame
        #store is the a list of tuple, the tuple consisst of three item, first item is the naem of the preset, the second itme is the meta data, the third is all the fuctiions
        self.store = []
        #current_essay is the meta data that belongs to self.df
        self.current_essay = None


        self.grid(row=0, column=0, sticky="nsew")  # Make the frame expand to the entire window
        master.grid_rowconfigure(0, weight=1)  # Allow the row to expand
        master.grid_columnconfigure(0, weight=1)  # Allow the column to expand

        # Title Label
        tk.Label(self, text="XLS Processor", font=("Arial", 18, "bold")).grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Load File Button
        self.load_button = tk.Button(self, text="Load XLS File", command=self.load_file)
        self.load_button.grid(row=1, column=0, padx=0, pady=5, sticky="w")

        # Load Preset Button
        self.load_preset_button = tk.Button(self, text="Load Presets", command=self.load_preset)
        self.load_preset_button.grid(row=1, column=1, padx=0, pady=5, sticky="w")

        # Save Preset Button
        self.load_preset_button = tk.Button(self, text="Save Presets", command=self.save_preset)
        self.load_preset_button.grid(row=1, column=2, padx=0, pady=5, sticky="w")

        # Save File Button
        self.save_button = tk.Button(self, text="Save Processed File", command=self.save_file, state=tk.DISABLED)
        self.save_button.grid(row=1, column=3, padx=0, pady=5, sticky="w")

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

        self.combine_file_button = tk.Button(self.button_frame, text="Load Preset", command=self.load_preset)
        self.combine_file_button.grid(row=7, column=0, padx=0, pady=5, sticky="w")


    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            self.file_path = file_path
            self.df, self.current_essay = import_files(file_path)
            if self.df is not None:
                messagebox.showinfo("Success", "File loaded successfully!")
                self.save_button.config(state=tk.NORMAL)

                self.display_dataframe_preview()

    def display_dataframe_preview(self):
        self.preview_text.delete(1.0, tk.END)
        preview = self.df.to_string(index=False)
        self.preview_text.insert(tk.END, preview)

    def save_file(self):
        if self.df is not None:
            self.store = save_file(self.df, self.current_essay, self.store)
            self.current_essay = None
        else:
            messagebox.showwarning("Warning", "No data to save!")

    def drop_column(self):
        if self.df is not None:
            self.df, self.current_essay = drop_column(self.df, self.current_essay)
            self.display_dataframe_preview()

    def rename_column(self):
        if self.df is not None:
            self.df, self.current_essay = rename_column(self.df, self.current_essay)
            self.display_dataframe_preview()

    def pivot_table(self):
        if self.df is not None:
            self.df, self.current_essay = pivot_table(self.df, self.current_essay)
            self.display_dataframe_preview()

    def delta_calculation(self):
        if self.df is not None:
            self.df, self.current_essay = delta_calculation(self.df, self.current_essay)
            self.display_dataframe_preview()

    def produce_output(self):
        if self.df is not None:
            self.df, self.current_essay = produce_output(self.df, self.current_essay)
            self.display_dataframe_preview()

    def keep_column(self):
        if self.df is not None:
            self.df, self.current_essay = keep_column(self.df, self.current_essay)
            self.display_dataframe_preview()

    def load_preset(self):
        if self.df is not None:
            self.df, self.current_essay, self.store = load_preset(self.df, self.current_essay, self.store)
            self.display_dataframe_preview()

    def save_preset(self):
        if self.df is not None:
            self.store = save_preset(self.current_essay, self.store)

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
