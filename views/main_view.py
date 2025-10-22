import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from controllers.data_controller import DataController
from controllers.processing_controller import (
    drop_column, rename_column, pivot_table, delta_calculation,
    produce_output, keep_column, custom_code, remove_empty_rows
)
from .components import HeaderPanel, ToolbarPanel, SidebarPanel, PreviewPanel

# Global variables
# Define colour constants used in the app (SpeeDX colors)
COLOURS = {
    "blue_rgb": (32, 165, 221), #SDX Blue
    "purple_rgb": (89, 48, 133), #SDX Purple
    "white_rgb": (255, 255, 255), # White in RGB
    "blue_hex": "#0272BA", #SDX Blue
    "purple_hex": "#593085", #SDX Purple
    "white_hex": "#FFFFFF", # White in hex
    "light_blue_hex": "#0272BA" # Light blue for header
}
# Application version
APP_VERSION = "3.3"

# Main application view using component-based architecture
class MainView(tk.Frame):
    """Main application view using component-based architecture"""
    
    def __init__(self, master):
        super().__init__(master)
        
        # Initialize data controller
        self.data = DataController()
        
        # Setup UI components
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the main UI using components"""
        # Header panel
        self.header = HeaderPanel(self, title="ToolKit", version=APP_VERSION, bg_color=COLOURS["white_hex"])
        
        # Toolbar panel
        self.toolbar = ToolbarPanel(self, controller=self, bg_color=COLOURS["light_blue_hex"])
        
        # Sidebar panel
        self.sidebar = SidebarPanel(self, controller=self, bg_color=COLOURS["light_blue_hex"])
        
        # Preview panel
        self.preview = PreviewPanel(self, bg_color=COLOURS["white_hex"])

    # ================= Data Functions =================
    def settings(self):
        """Open settings dialog (placeholder for now)."""
        messagebox.showinfo("Settings", "Settings dialog coming soon!")

    # Load an Excel file and display it in preview
    def load_file(self):
        # Updated: combined first filter so *.csv appears immediately
        file_path = filedialog.askopenfilename(
            title="Select data file",
            filetypes=[
                ("Data files", "*.xls *.xlsx *.csv"),
                ("Excel (xls)", "*.xls"),
                ("Excel (xlsx)", "*.xlsx"),
                ("CSV", "*.csv"),
                ("All files", "*.*"),
            ]
        )
        if file_path:
            # Basic validation (in case user picked unsupported type via All files)
            if not file_path.lower().endswith((".xls", ".xlsx", ".csv")):
                messagebox.showwarning("Unsupported", "Please select an .xls, .xlsx, or .csv file.")
                return
            
            df = self.data.load_file(file_path)
            
            if isinstance(df, pd.DataFrame):
                messagebox.showinfo("Success", "File loaded successfully!")
                self.display_dataframe_preview()
            else:
                messagebox.showwarning("Load Failed", "Could not load a valid dataset.")

    def display_dataframe_preview(self):
        """Update the preview panel with current dataframe"""
        self.preview.update_preview(
            df=self.data.get_dataframe(),
            file_path=self.data.file_path
        )

    def save_file(self):
        if self.data.has_data():
            self.data.save()
        else:
            messagebox.showwarning("Warning", "No data to save!")

    def _apply_transform(self, transform_func):
        """Helper method to apply transformations and update preview"""
        if self.data.has_data():
            result = self.data.apply_transform(transform_func)
            if result is not None:
                self.display_dataframe_preview()
        else:
            messagebox.showwarning("Warning", "No data loaded!")

    def drop_column(self):
        self._apply_transform(drop_column)

    def rename_column(self):
        self._apply_transform(rename_column)

    def pivot_table(self):
        self._apply_transform(pivot_table)

    def delta_calculation(self):
        self._apply_transform(delta_calculation)

    def produce_output(self):
        self._apply_transform(produce_output)

    def keep_column(self):
        self._apply_transform(keep_column)

    def manage_plugin(self):
        self.data.manage_plugins()

    def save_plugin(self):
        if self.data.has_data():
            self.data.save_plugin_data()

    def custom_code(self):
        self._apply_transform(custom_code)

    def remove_empty_rows(self):
        self._apply_transform(remove_empty_rows)


    def combine_file(self):
        """Combine multiple files into one"""
        self.data.combine_files()
        if self.data.has_data():
            self.display_dataframe_preview()