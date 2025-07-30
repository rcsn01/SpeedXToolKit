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

# Main user interface class
class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.file_path = None
        self.df = None  # Store the loaded DataFrame
        #store is the a list of tuple, the tuple consisst of three item, first item is the naem of the preset, the second itme is the meta data, the third is all the fuctiions
        self.store = []
        #current_essay is the meta data that belongs to self.df
        self.current_essay = None

        # Create a frame to hold the header content
        header_frame = tk.Frame(self, bg=COLOURS["white_hex"])
        header_frame.pack(fill="x", anchor="n")  # Use 'anchor="n"' to anchor it to the top of the screen

        # Canvas for gradient title text (left-aligned)
        title_canvas = tk.Canvas(header_frame, bg=COLOURS["white_hex"], highlightthickness=0, height=70)
        title_canvas.pack(fill="x")

        # Draw the gradient title text
        self.draw_gradient_text(title_canvas, "Universal Data Processor", COLOURS["blue_rgb"], COLOURS["purple_rgb"], font=("Arial", 40, "bold"))

        # Side menu frame
        self.side_menu = tk.Frame(self, width=250, padx=10, pady=20, bg=COLOURS["white_hex"])
        self.side_menu.pack(side="left", fill="y", expand=False, anchor="nw")
        self.side_menu.pack_propagate(False) # Prevent side menu from resizing

        # Side menu frame
        self.top_menu = tk.Frame(self, height=100, padx=10, pady=20, bg=COLOURS["white_hex"])
        self.top_menu.pack(side="top", fill="x", expand=False, anchor="nw")
        self.top_menu.pack_propagate(False) # Prevent side menu from resizing

        # Function to draw rounded rectangle without outline
        def draw_rounded_rect(canvas, x1, y1, x2, y2, radius=10, **kwargs):
            # Top-left and top-right corners
            canvas.create_oval(x1, y1, x1 + 2 * radius, y1 + 2 * radius, outline="", **kwargs)  # top-left corner                
            canvas.create_oval(x2 - 2 * radius, y1, x2, y1 + 2 * radius, outline="", **kwargs)  # top-right corner
            # Top and bottom sides
            canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, outline="", **kwargs)  # top
            canvas.create_rectangle(x1, y1 + radius, x2, y2, outline="", **kwargs)  # bottom (straight)

        # Function to create a menu button with gradient and hover effect
        def side_menu_button(parent, text, command):
            frame = tk.Frame(parent, bg=parent['bg'])
            frame.pack(fill="x", pady=(0, 8))
            
            # Canvas for gradient text
            canvas = Canvas(frame, height=40, bg=parent['bg'], highlightthickness=0)
            canvas.pack(fill="both")
            self.draw_gradient_text(canvas, text, COLOURS["blue_rgb"], COLOURS["purple_rgb"], font=("Arial", 14, "bold"))

            canvas.bind("<Button-1>", lambda e: command())  # Enable click event

            # Hover effect for menu button
            def on_hover(event):
                # Redraw the rounded background with hover colour
                canvas.delete("all")  # Clear the previous background and text
                draw_rounded_rect(canvas, 0, 0, frame.winfo_width(), 40, radius=10, fill="#20a5dd")  # Rounded background
                self.draw_gradient_text(canvas, text, COLOURS["white_rgb"], COLOURS["white_rgb"], font=("Arial", 14, "bold"))  # Redraw text over the new background

            def on_leave(event):
                canvas.config(bg=parent['bg'])
                # Redraw the rounded background with normal colour
                canvas.delete("all")  # Clear the previous background and text
                draw_rounded_rect(canvas, 0, 0, frame.winfo_width(), 40, radius=10, fill=parent['bg'])  # Rounded background
                self.draw_gradient_text(canvas, text, COLOURS["blue_rgb"], COLOURS["purple_rgb"], font=("Arial", 14, "bold"))  # Redraw text over the new background

            frame.bind("<Enter>", on_hover)
            frame.bind("<Leave>", on_leave)

            # Gradient line separator after every button
            self.draw_gradient_line(frame, COLOURS["blue_rgb"], COLOURS["purple_rgb"])  # Default colour for line
            return frame

        # Function to draw rounded rectangle without outline (horizontal layout)
        def draw_rounded_rect_h(canvas, x1, y1, x2, y2, radius=10, **kwargs):

            # Center rectangle (middle section)
            canvas.create_rectangle(x1 , y1, x2, y2, outline="", **kwargs)

        # Function to create a horizontal toolbar menu button with gradient and hover effect
        def top_menu_button(parent, text, command):
            frame = tk.Frame(parent, bg=parent['bg'])
            frame.pack(side="left", padx=(0, 8))  # Horizontal packing

            # Canvas for gradient text
            canvas = Canvas(frame, width=150, height=40, bg=parent['bg'], highlightthickness=0)
            canvas.pack()

            self.draw_gradient_text(canvas, text, COLOURS["blue_rgb"], COLOURS["purple_rgb"], font=("Arial", 14, "bold"))
            canvas.bind("<Button-1>", lambda e: command())

            # Hover effect
            def on_hover(event):
                canvas.delete("all")
                draw_rounded_rect_h(canvas, 0, 0, canvas.winfo_width(), 40, radius=10, fill="#20a5dd")
                self.draw_gradient_text(canvas, text, COLOURS["white_rgb"], COLOURS["white_rgb"], font=("Arial", 14, "bold"))

            def on_leave(event):
                canvas.config(bg=parent['bg'])
                canvas.delete("all")
                draw_rounded_rect_h(canvas, 0, 0, canvas.winfo_width(), 40, radius=10, fill=parent['bg'])
                self.draw_gradient_text(canvas, text, COLOURS["blue_rgb"], COLOURS["purple_rgb"], font=("Arial", 14, "bold"))

            frame.bind("<Enter>", on_hover)
            frame.bind("<Leave>", on_leave)

            return frame



        # Attach menu buttons
        #self.load_button = side_menu_button(self.side_menu, "Load File", self.load_file)
        #self.combine_file_button = side_menu_button(self.side_menu, "Combine File", self.combine_file)
        self.load_button = top_menu_button(self.top_menu, "Load File", self.load_file)
        self.save_button = top_menu_button(self.top_menu, "Load Preset", self.load_preset)
        self.combine_file_button = top_menu_button(self.top_menu, "Combine File", self.combine_file)
        self.save_button = top_menu_button(self.top_menu, "Save File", self.save_file)
        self.save_button = top_menu_button(self.top_menu, "Save Preset", self.save_preset)


        self.pivot_table_button = side_menu_button(self.side_menu, "Pivot Table", self.pivot_table)
        self.rename_target_button = side_menu_button(self.side_menu, "Rename Column", self.rename_column)
        self.combine_file_button = side_menu_button(self.side_menu, "Keep Column", self.keep_column)
        self.drop_column_button = side_menu_button(self.side_menu, "Remove Column", self.drop_column)
        #self.combine_file_button = side_menu_button(self.side_menu, "Combine File", self.combine_file)
        #self.delta_calculation_button = side_menu_button(self.side_menu, "Delta Calculation", self.delta_calculation)
        self.combine_file_button = side_menu_button(self.side_menu, "Produce Output", self.produce_output)
        


        # Create a frame for the preview content that will take the remaining space
        self.preview_frame = GradientFrame(self, color1=COLOURS["blue_hex"], color2=COLOURS["purple_hex"], highlightthickness=0)
        self.preview_frame.pack(side="left", fill="both", expand=True, anchor="nw")

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
    
    # Function to draw a gradient line
    def draw_gradient_line(self, parent, start_colour, end_colour):
        line = Canvas(parent, height=2, bg=parent['bg'], highlightthickness=0)
        line.pack(fill="x", pady=(0, 8))

        def render_line():
            line.delete("all") # Clear any previous lines
            width = line.winfo_width() # Get the width of the line

            r1, g1, b1 = start_colour
            r2, g2, b2 = end_colour

            # Draw a gradient line horizontally
            for i in range(width):
                ratio = i / max(width, 1)
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                colour = f'#{r:02x}{g:02x}{b:02x}'
                line.create_line(i, 0, i, 2, fill=colour)

        parent.after(50, render_line)


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
    
    # Function to draw a gradient line
    def draw_gradient_line(self, parent, start_colour, end_colour):
        line = Canvas(parent, height=2, bg=parent['bg'], highlightthickness=0)
        line.pack(fill="x", pady=(0, 8))

        def render_line():
            line.delete("all") # Clear any previous lines
            width = line.winfo_width() # Get the width of the line

            r1, g1, b1 = start_colour
            r2, g2, b2 = end_colour

            # Draw a gradient line horizontally
            for i in range(width):
                ratio = i / max(width, 1)
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                colour = f'#{r:02x}{g:02x}{b:02x}'
                line.create_line(i, 0, i, 2, fill=colour)

        parent.after(50, render_line)

    # ================= Data Functions =================
    # Load an Excel file and display it in preview
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            self.file_path = file_path
            self.df, self.current_essay = import_files(file_path)
            if self.df is not None:
                messagebox.showinfo("Success", "File loaded successfully!")
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
            self.store = save_file(self.df, self.current_essay, self.store)
            self.current_essay = None
        else:
            messagebox.showwarning("Warning", "No data to save!")

    def drop_column(self):
        if self.df is not None:
            results = drop_column(self.df, self.current_essay)
            if results is not None:
                self.df, self.current_essay = results
                self.display_dataframe_preview()

    def rename_column(self):
        if self.df is not None:
            results = rename_column(self.df, self.current_essay)
            if results is not None:
                self.df, self.current_essay = results
                self.display_dataframe_preview()

    def pivot_table(self):
        if self.df is not None:
            results = pivot_table(self.df, self.current_essay)
            if results is not None:
                self.df, self.current_essay = results
                self.display_dataframe_preview()

    def delta_calculation(self):
        if self.df is not None:
            results = delta_calculation(self.df, self.current_essay)
            if results is not None:
                self.df, self.current_essay = results
                self.display_dataframe_preview()

    def produce_output(self):
        if self.df is not None:
            results = produce_output(self.df, self.current_essay)
            if results is not None:
                self.df, self.current_essay = results
                self.display_dataframe_preview()

    def keep_column(self):
        if self.df is not None:
            results = keep_column(self.df, self.current_essay)
            if results is not None:
                self.df, self.current_essay = results
                self.display_dataframe_preview()

    def load_preset(self):
        if self.df is not None:
            self.df, self.current_essay, self.store = load_preset(self.df, self.current_essay, self.store)
            self.display_dataframe_preview()
    
    def save_preset(self):
        if self.df is not None:
            self.store = save_preset(self.current_essay, self.store)

    def save_preset(self):
        if self.df is not None:
            self.store = save_preset(self.current_essay, self.store)

    def combine_file(self):
        self.df = combined_file()
        self.display_dataframe_preview()