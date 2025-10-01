import tkinter as tk
from tkinter import filedialog, messagebox, Canvas
from controllers.processing_controller import *
from controllers.save_controller import *
import pandas as pd
from models.dataframe_model import *
from models.path_utils import get_resource_path

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
APP_VERSION = "v0.3.0"

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

        # Create a simple header with a light blue background
        header_bg = "#abd2ff"  # light blue
        header_frame = tk.Frame(self, bg=header_bg, pady=8)
        header_frame.pack(fill="x")
        # Try to load a logo image from assets/logo.png and display to the left of the title
        try:
            logo_path = get_resource_path("assets/logo.png")
            if logo_path.exists():
                logo_img = tk.PhotoImage(file=str(logo_path))
                # subsample reduces size by integer factor (e.g., 2 => half size)
                logo_img = logo_img.subsample(2, 2)
                label = tk.Label(header_frame, image=logo_img, bg=header_bg)
                label.image = logo_img
                label.pack(side="left", padx=(6,8))
        except Exception:
            # If loading fails, silently continue without logo
            pass

        title_label = tk.Label(header_frame, text="ToolKit", bg=header_bg, fg="#000000", font=("Arial", 24, "bold"))
        title_label.pack(side="left", padx=10)
        version_label = tk.Label(header_frame, text=APP_VERSION, bg=header_bg, fg="#555555", font=("Arial", 10))
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

        # Plugins list: show available plugins above the side-menu buttons
        try:
            plugins = show_plugins()
        except Exception:
            plugins = []

        plugins_label = tk.Label(self.side_menu, text="Plugins:", bg="#dddddd", font=("Arial", 10, "bold"), bd=1, relief='solid')
        plugins_label.pack(fill='x', pady=(8,4))
        plugins_frame = tk.Frame(self.side_menu, bg=COLOURS["white_hex"])
        plugins_frame.pack(fill='x', pady=(0,8))
        if plugins:
            # If plugins is a list of tuples or dicts, try to extract readable names
            display_items = []
            for p in plugins:
                try:
                    if isinstance(p, dict):
                        display_items.append(p.get('name', str(p)))
                    elif isinstance(p, (list, tuple)) and p:
                        display_items.append(str(p[0]))
                    else:
                        display_items.append(str(p))
                except Exception:
                    display_items.append(str(p))

            self.plugins_listbox = tk.Listbox(plugins_frame, height=5)
            for item in display_items:
                self.plugins_listbox.insert(tk.END, item)
            self.plugins_listbox.pack(fill='x')

            # Apply button under the plugins list
            def on_apply_plugin():
                try:
                    sel = self.plugins_listbox.curselection()
                    if not sel:
                        messagebox.showwarning("No selection", "Please select a plugin to apply.")
                        return
                    name = self.plugins_listbox.get(sel[0])
                    # Call controller apply_plugin
                    new_df, new_store = apply_plugin(self.df, name)
                    if isinstance(new_df, pd.DataFrame):
                        self.df = new_df
                        self.store = new_store
                        self.display_dataframe_preview()
                        messagebox.showinfo("Plugin Applied", f"Plugin '{name}' applied.")
                    else:
                        messagebox.showwarning("Apply Failed", f"Plugin '{name}' did not produce a valid DataFrame.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to apply plugin: {e}")
            # Refresh handler: reload plugin list and update the listbox (or create it)
            def on_refresh_plugins():
                try:
                    new_plugins = show_plugins()
                    # Build display items
                    items = []
                    for p in new_plugins:
                        try:
                            if isinstance(p, dict):
                                items.append(p.get('name', str(p)))
                            elif isinstance(p, (list, tuple)) and p:
                                items.append(str(p[0]))
                            else:
                                items.append(str(p))
                        except Exception:
                            items.append(str(p))

                    # If a 'no plugins' label was shown, remove it
                    if hasattr(self, 'no_plugins_label') and self.no_plugins_label:
                        try:
                            self.no_plugins_label.destroy()
                            self.no_plugins_label = None
                        except Exception:
                            pass

                    # If listbox exists, replace contents; otherwise create it
                    if hasattr(self, 'plugins_listbox') and self.plugins_listbox:
                        self.plugins_listbox.delete(0, tk.END)
                        for it in items:
                            self.plugins_listbox.insert(tk.END, it)
                    else:
                        self.plugins_listbox = tk.Listbox(plugins_frame, height=5)
                        for it in items:
                            self.plugins_listbox.insert(tk.END, it)
                        self.plugins_listbox.pack(fill='x')

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to refresh plugins: {e}")

            # Buttons frame for Apply and Refresh
            btn_frame = tk.Frame(plugins_frame, bg=COLOURS["white_hex"])
            btn_frame.pack(pady=4)
            tk.Button(btn_frame, text="Apply", command=on_apply_plugin).pack(side='left', padx=4)
            tk.Button(btn_frame, text="Refresh", command=on_refresh_plugins).pack(side='left', padx=4)
        else:
            self.no_plugins_label = tk.Label(plugins_frame, text="No plugins", bg=COLOURS["white_hex"], fg="#777777")
            self.no_plugins_label.pack(fill='x')

        # Transform label: sits under the plugins area and above the side menu buttons
        # Slightly grey background for visual separation
        transform_label = tk.Label(self.side_menu, text="Transform:", bg="#dddddd", font=("Arial", 10, "bold"), bd=1, relief='solid')
        transform_label.pack(fill='x', pady=(8,4))

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