import tkinter as tk
from tkinter import filedialog, messagebox
from controllers.save_controller import *
import pandas as pd
from models.dataframe_model import *
from models.drop_column import *
from models.rename_target import *

# Global variables
speedx_blue_RGB = (32, 165, 221)  # RGB Blue
speedx_purple_RGB = (89, 48, 133)  # RGB Purple
white_RGB = (255, 255, 255)  # RGB White
speedx_blue_hex = "#20a5dd"  # hex Blue
speedx_purple_hex = "#593085"  # hex Purple
white_hex = "#FFFFFF"  # hex White

class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1="white", color2="black", **kwargs):
        super().__init__(parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = height  # Change limit to height for vertical gradient

        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)

        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            # Draw horizontal line for vertical gradient
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)

        self.lower("gradient")

class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.file_path = None
        self.df = None



        # Create a frame to hold the header content
        header_frame = tk.Frame(self, bg=white_hex)
        header_frame.pack(fill="x", anchor="n")  # Use 'anchor="n"' to anchor it to the top of the screen

        # Canvas for gradient title text (left-aligned)
        title_canvas = tk.Canvas(header_frame, bg=white_hex, highlightthickness=0, height=70)
        title_canvas.pack(fill="x")

        # Draw the gradient title text
        self.draw_gradient_text(title_canvas, "Universal Data Processor", speedx_blue_RGB, speedx_purple_RGB, font=("Arial", 40, "bold"))

        # Side menu frame
        self.side_menu = tk.Frame(self, width=200, padx=10, pady=20, bg=white_hex)
        self.side_menu.pack(side="left", fill="y", anchor="nw")

        # Gradient Button with line and hover effect
        def menu_button(parent, text, command):
            frame = tk.Frame(parent, bg=parent['bg'])
            frame.pack(fill="x", pady=(0, 8))
            
            # Canvas for gradient text
            canvas = Canvas(frame, height=40, bg=parent['bg'], highlightthickness=0)
            canvas.pack(fill="x")
            self.draw_gradient_text(canvas, text, speedx_blue_RGB, speedx_purple_RGB, font=("Arial", 14, "bold"))

            canvas.bind("<Button-1>", lambda e: command())  # Enable click event

            # Function to draw rounded rectangle without outline
            def draw_rounded_rect(canvas, x1, y1, x2, y2, radius=10, **kwargs):
                # Top-left and top-right corners
                canvas.create_oval(x1, y1, x1 + 2 * radius, y1 + 2 * radius, outline="", **kwargs)  # top-left corner
                canvas.create_oval(x2 - 2 * radius, y1, x2, y1 + 2 * radius, outline="", **kwargs)  # top-right corner
                # Top and bottom sides
                canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, outline="", **kwargs)  # top
                canvas.create_rectangle(x1, y1 + radius, x2, y2, outline="", **kwargs)  # bottom (straight)

            # Hover effect
            def on_hover(event):
                # Redraw the rounded background with hover colour
                canvas.delete("all")  # Clear the previous background and text
                draw_rounded_rect(canvas, 0, 0, frame.winfo_width(), 40, radius=10, fill="#20a5dd")  # Rounded background
                self.draw_gradient_text(canvas, text, white_RGB, white_RGB, font=("Arial", 14, "bold"))  # Redraw text over the new background

            def on_leave(event):
                canvas.config(bg=parent['bg'])

                # Redraw the rounded background with normal colour
                canvas.delete("all")  # Clear the previous background and text
                draw_rounded_rect(canvas, 0, 0, frame.winfo_width(), 40, radius=10, fill=parent['bg'])  # Rounded background
                self.draw_gradient_text(canvas, text, speedx_blue_RGB, speedx_purple_RGB, font=("Arial", 14, "bold"))  # Redraw text over the new background

            frame.bind("<Enter>", on_hover)
            frame.bind("<Leave>", on_leave)

            # Gradient line separator
            self.draw_gradient_line(frame, speedx_blue_RGB, speedx_purple_RGB)  # Default colour for line
            return frame


        # Attach menu buttons
        self.load_button = menu_button(self.side_menu, "Load XLS File", self.load_file)
        self.save_button = menu_button(self.side_menu, "Save Processed File", self.save_file)
        self.drop_column_button = menu_button(self.side_menu, "Drop Column", self.drop_column)
        self.rename_target_button = menu_button(self.side_menu, "Rename Target", self.rename_target)
        self.pivot_table_button = menu_button(self.side_menu, "Pivot Table", self.pivot_table)
        self.delta_calculation_button = menu_button(self.side_menu, "Delta Calculation", self.delta_calculation)
        self.combine_file_button = menu_button(self.side_menu, "Combine File", self.combine_file)

        # Bring buttons to the foreground to avoid clipping or overlapping issues
        self.load_button.lift()
        self.save_button.lift()
        self.drop_column_button.lift()
        self.rename_target_button.lift()
        self.pivot_table_button.lift()
        self.delta_calculation_button.lift()
        self.combine_file_button.lift()

        def draw_rounded_corners(self, canvas, radius, width, height):
            # Top-left corner
            canvas.create_oval(0, 0, 2 * radius, 2 * radius, outline="", fill=self.color1)
            # Top-right corner
            canvas.create_oval(width - 2 * radius, 0, width, 2 * radius, outline="", fill=self.color1)
            # Bottom-left corner
            canvas.create_oval(0, height - 2 * radius, 2 * radius, height, outline="", fill=self.color2)
            # Bottom-right corner
            canvas.create_oval(width - 2 * radius, height - 2 * radius, width, height, outline="", fill=self.color2)
            
            # Draw the four straight edges
            canvas.create_rectangle(radius, 0, width - radius, height, outline="", fill=self.color1)
            canvas.create_rectangle(0, radius, width, height - radius, outline="", fill=self.color2)


        # Create a frame for the preview content that will take the remaining space
        self.preview_frame = GradientFrame(self, color1=speedx_blue_hex, color2=speedx_purple_hex, highlightthickness=0)
        self.preview_frame.pack(side="left", fill="both", expand=True, anchor="nw")

        # DataFrame Preview (Center over gradient)
        self.preview_text = tk.Text(self.preview_frame, height=45, width=125, bg=white_hex, fg="black", highlightthickness=0)
        self.preview_text.place(relx=0.5, rely=0.5, anchor="center")  # Center preview inside the frame


        # Resize behavior
        self.bind("<Configure>", lambda e: self.preview_text.place(relx=0.5, rely=0.5, anchor="center"))

    def draw_gradient_text(self, canvas, text, start_colour, end_colour, font):
        x = 10
        y = 10
        num_chars = len(text)

        r1, g1, b1 = start_colour
        r2, g2, b2 = end_colour

        for i, char in enumerate(text):
            ratio = i / max(num_chars - 1, 1)  # Avoid division by zero
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            colour = f'#{r:02x}{g:02x}{b:02x}'

            text_id = canvas.create_text(x, y, text=char, fill=colour, font=font, anchor='nw')
            bbox = canvas.bbox(text_id)
            char_width = bbox[2] - bbox[0] if bbox else 15
            x += char_width

    def draw_gradient_line(self, parent, start_colour, end_colour):
        line = Canvas(parent, height=2, bg=parent['bg'], highlightthickness=0)
        line.pack(fill="x", pady=(0, 8))

        def render_line():
            line.delete("all")
            width = line.winfo_width()

            r1, g1, b1 = start_colour
            r2, g2, b2 = end_colour

            for i in range(width):
                ratio = i / max(width, 1)
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                colour = f'#{r:02x}{g:02x}{b:02x}'
                line.create_line(i, 0, i, 2, fill=colour)

        parent.after(50, render_line)

    # ================= Data Functions =================
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
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
