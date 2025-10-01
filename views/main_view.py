import tkinter as tk
from tkinter import filedialog, messagebox, Canvas
from controllers.processing_controller import *
from controllers.save_controller import *
import pandas as pd
from models.dataframe_model import *

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
# Application version
APP_VERSION = "v0.2.0"

# Simplified UI: use basic Tkinter widgets (Label, Button, Frame) instead of custom gradient canvas

# Main user interface class
class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.file_path = None
        self.df = None  # Store the loaded DataFrame
        # Store is now a dictionary holding current preset information:
        # name: preset name (str or None)
        # metadata: metadata of the current dataframe (any structure, typically tuple)
        # functions: list of functions applied to the dataframe (list[str])
        self.store = {"name": None, "metadata": None, "functions": []}

        # Create a simple header
        header_frame = tk.Frame(self, bg=COLOURS["white_hex"], pady=8)
        header_frame.pack(fill="x")
        title_label = tk.Label(header_frame, text="SpeedXToolKit", bg=COLOURS["white_hex"], fg=COLOURS["blue_hex"], font=("Arial", 24, "bold"))
        title_label.pack(side="left", padx=10)
        version_label = tk.Label(header_frame, text=APP_VERSION, bg=COLOURS["white_hex"], fg="#555555", font=("Arial", 10))
        version_label.pack(side="right", padx=10)

        # Top menu: simple buttons
        self.top_menu = tk.Frame(self, height=40, padx=10, pady=4, bg=COLOURS["white_hex"])
        self.top_menu.pack(side="top", fill="x")
        tk.Button(self.top_menu, text="Load File", command=self.load_file).pack(side="left", padx=4)
        tk.Button(self.top_menu, text="Load Preset", command=self.load_preset).pack(side="left", padx=4)
        tk.Button(self.top_menu, text="Combine File", command=self.combine_file).pack(side="left", padx=4)
        tk.Button(self.top_menu, text="Save File", command=self.save_file).pack(side="left", padx=4)
        tk.Button(self.top_menu, text="Save Preset", command=self.save_preset).pack(side="left", padx=4)

        # Side menu: collapsible vertical buttons
        # Use a grid inside left_container so the toggle button sits to the RIGHT of the buttons
        self.left_container = tk.Frame(self, bg=COLOURS["white_hex"])
        self.left_container.pack(side="left", fill="y")

        # The actual side menu (starts visible) placed in column 0
        self.side_menu = tk.Frame(self.left_container, width=200, padx=6, pady=6, bg=COLOURS["white_hex"])
        self.side_menu.grid(row=0, column=0, sticky='ns')

        btn_specs = [
            ("Pivot Table", self.pivot_table),
            ("Rename Column", self.rename_column),
            ("Keep Column", self.keep_column),
            ("Remove Column", self.drop_column),
            ("Delta Calculation", self.delta_calculation),
            ("Produce Output", self.produce_output),
            ("Custom Code", self.custom_code),
            ("Remove Empty Rows", self.remove_empty_rows),
        ]
        for text, cmd in btn_specs:
            tk.Button(self.side_menu, text=text, command=cmd, width=20).pack(pady=2)

        # Toggle button that expands/collapses the side panel sits in column 1
        self.side_visible = True
        self.toggle_btn = tk.Button(self.left_container, text="≡", width=3, command=self.toggle_side_panel)
        self.toggle_btn.grid(row=0, column=1, sticky='ns', padx=(4,8), pady=6)

        # Make sure the left_container rows stretch vertically
        try:
            self.left_container.grid_rowconfigure(0, weight=1)
        except Exception:
            pass

        # Create a frame for the preview content that will take the remaining space
        self.preview_frame = tk.Frame(self, bg=COLOURS["white_hex"])
        self.preview_frame.pack(side="left", fill="both", expand=True)

        # DataFrame Preview (Center over gradient)
        text_scroll_frame = tk.Frame(self.preview_frame, bg=COLOURS["white_hex"])
        text_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Vertical scrollbar
        y_scrollbar = tk.Scrollbar(text_scroll_frame)
        y_scrollbar.pack(side="right", fill="y")

        # Horizontal scrollbar
        x_scrollbar = tk.Scrollbar(text_scroll_frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        # Correct: Do NOT overwrite self.preview_frame
        self.preview_text = tk.Text(
            text_scroll_frame, 
            height=45, 
            width=125, 
            bg=COLOURS["white_hex"], 
            fg="black", 
            highlightthickness=0,
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
            wrap="none"
        )
        self.preview_text.pack(side="left", fill="both", expand=True)

        # Hook up the scrollbars correctly
        y_scrollbar.config(command=self.preview_text.yview)
        x_scrollbar.config(command=self.preview_text.xview)


    def draw_gradient_text(self, canvas, text, start_colour, end_colour, font):
        x = 10
        y = 10
        num_chars = len(text)

        r1, g1, b1 = start_colour
        r2, g2, b2 = end_colour

        for i, char in enumerate(text):
            ratio = i / max(num_chars - 1, 1)  # Calculate ratio for gradient effect
            r = int(r1 + (r2 - r1) * ratio)  # Calculate new red value
            g = int(g1 + (g2 - g1) * ratio)  # Calculate new green value
            b = int(b1 + (b2 - b1) * ratio)  # Calculate new blue value
            colour = f'#{r:02x}{g:02x}{b:02x}'  # Convert RGB to hex

            text_id = canvas.create_text(x, y, text=char, fill=colour, font=font, anchor='nw')
            bbox = canvas.bbox(text_id)  # Get bounding box of text
            char_width = bbox[2] - bbox[0] if bbox else 15  # Calculate text width
            x += char_width  # Update x position for next character

    def toggle_side_panel(self):
        # Show or hide the side_menu frame
        if self.side_visible:
            # Hide using grid_remove so we can restore in the same grid position
            try:
                self.side_menu.grid_remove()
            except Exception:
                self.side_menu.forget()
            self.side_visible = False
            self.toggle_btn.config(text='›')
        else:
            # Restore the side_menu to its grid location
            try:
                self.side_menu.grid()
            except Exception:
                self.side_menu.pack(side='left', fill='y')
            self.side_visible = True
            self.toggle_btn.config(text='≡')
    

    # ================= Data Functions =================
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
            self.file_path = file_path
            result = import_files(file_path)
            if result and isinstance(result, tuple) and len(result) == 2:
                self.df, self.current_essay = result
                # Update store metadata when a new file is loaded
                self.store['metadata'] = self.current_essay
                self.store['functions'] = []  # reset function history on new load
            else:
                self.df = None
            if isinstance(self.df, pd.DataFrame):
                messagebox.showinfo("Success", "File loaded successfully!")
                self.display_dataframe_preview()
            else:
                messagebox.showwarning("Load Failed", "Could not load a valid dataset.")

    def display_dataframe_preview(self):
        # Clear any existing text in the text widget
        self.preview_text.delete(1.0, tk.END)
        if isinstance(self.df, pd.DataFrame):
            preview = self.df.to_string(index=False)
            self.preview_text.insert(tk.END, preview)
        else:
            self.preview_text.insert(tk.END, "No data loaded.")

    def save_file(self):
        if self.df is not None:
            self.store = save_file(self.df, self.current_essay, self.store)
            self.current_essay = None
        else:
            messagebox.showwarning("Warning", "No data to save!")

    def drop_column(self):
        if self.df is not None:
            results = drop_column(self.df, self.store)
            if results is not None:
                self.df, self.store = results
                self.display_dataframe_preview()

    def rename_column(self):
        if self.df is not None:
            results = rename_column(self.df, self.store)
            if results is not None:
                self.df, self.store = results
                self.display_dataframe_preview()

    def pivot_table(self):
        if self.df is not None:
            results = pivot_table(self.df, self.store)
            if results is not None:
                self.df, self.store = results
                self.display_dataframe_preview()

    def delta_calculation(self):
        if self.df is not None:
            results = delta_calculation(self.df, self.store)
            if results is not None:
                self.df, self.store = results
                self.display_dataframe_preview()

    def produce_output(self):
        if self.df is not None:
            results = produce_output(self.df, self.store)
            if results is not None:
                self.df, self.store = results
                self.display_dataframe_preview()

    def keep_column(self):
        if self.df is not None:
            results = keep_column(self.df, self.store)
            if results is not None:
                self.df, self.store = results
                self.display_dataframe_preview()

    def load_preset(self):
        if self.df is not None:
            self.df, self.store = load_preset(self.df, self.store)
            if isinstance(self.store, dict):
                self.current_essay = self.store.get('metadata')
            if isinstance(self.df, pd.DataFrame):
                self.display_dataframe_preview()
    
    def save_preset(self):
        if self.df is not None:
            self.store = save_preset(self.store)

    def custom_code(self):
        if self.df is not None:
            results = custom_code(self.df, self.store)
            if results is not None:
                self.df, self.store = results
                self.display_dataframe_preview()

    def remove_empty_rows(self):
        if self.df is not None:
            results = remove_empty_rows(self.df, self.store)
            if results is not None:
                self.df, self.store = results
                self.display_dataframe_preview()


    def combine_file(self):
        self.df = combined_file()
        self.display_dataframe_preview()