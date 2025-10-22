import tkinter as tk
import pandas as pd
import os


class PreviewPanel(tk.Frame):
    """Data preview panel with scrollable text widget"""
    
    def __init__(self, parent, bg_color="#FFFFFF"):
        super().__init__(parent, bg=bg_color)
        self.bg_color = bg_color
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the preview panel UI"""
        self.pack(side="left", fill="both", expand=True)
        
        # Title frame to hold label and file path
        self.title_frame = tk.Frame(self, bg=self.bg_color)
        self.title_frame.pack(side="top", fill="x", padx=12, pady=(8, 0))
        
        # Title label for the preview
        self.title_label = tk.Label(
            self.title_frame,
            text="File Preview",
            bg=self.bg_color,
            fg="black",
            font=("Arial", 11, "bold")
        )
        self.title_label.pack(side="left")
        
        # File path label (initially empty)
        self.file_path_label = tk.Label(
            self.title_frame,
            text="",
            bg=self.bg_color,
            fg="#555555",
            font=("Arial", 9)
        )
        self.file_path_label.pack(side="left", padx=(10, 0))

        # Create scrollable text frame
        self.text_scroll_frame = tk.Frame(self, bg=self.bg_color)
        self.text_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create scrollbars
        self._create_scrollbars()
        
        # Create text widget
        self._create_text_widget()
        
        # Configure scrollbars
        self._configure_scrollbars()
    
    def _create_scrollbars(self):
        """Create vertical and horizontal scrollbars"""
        # Vertical scrollbar
        self.y_scrollbar = tk.Scrollbar(self.text_scroll_frame)
        self.y_scrollbar.pack(side="right", fill="y")
        
        # Horizontal scrollbar
        self.x_scrollbar = tk.Scrollbar(self.text_scroll_frame, orient="horizontal")
        self.x_scrollbar.pack(side="bottom", fill="x")
    
    def _create_text_widget(self):
        """Create the main text widget for data preview"""
        self.preview_text = tk.Text(
            self.text_scroll_frame,
            height=45,
            width=125,
            bg=self.bg_color,
            fg="black",
            highlightthickness=0,
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set,
            wrap="none"
        )
        self.preview_text.pack(side="left", fill="both", expand=True)
    
    def _configure_scrollbars(self):
        """Configure scrollbar commands"""
        self.y_scrollbar.config(command=self.preview_text.yview)
        self.x_scrollbar.config(command=self.preview_text.xview)
    
    def update_preview(self, df=None, text=None, file_path=None):
        """Update the preview content
        
        Args:
            df: pandas DataFrame to display
            text: Text string to display (if df is None)
            file_path: File path to display in the header
        """
        # Update file path label - show only filename
        if file_path:
            filename = os.path.basename(file_path)
            self.file_path_label.config(text=f"({filename})")
        else:
            self.file_path_label.config(text="")
        
        # Clear existing content
        self.preview_text.delete(1.0, tk.END)
        
        if df is not None and isinstance(df, pd.DataFrame):
            preview_text = df.to_string(index=False)
            self.preview_text.insert(tk.END, preview_text)
        elif text is not None:
            self.preview_text.insert(tk.END, text)
        else:
            self.preview_text.insert(tk.END, "No data loaded.")
    
    def clear_preview(self):
        """Clear all preview content"""
        self.preview_text.delete(1.0, tk.END)
    
    def get_preview_text(self):
        """Get current preview text content"""
        return self.preview_text.get(1.0, tk.END)
    
    def set_font(self, font_family="Courier", font_size=10):
        """Set preview text font"""
        self.preview_text.config(font=(font_family, font_size))
    
    def set_background_color(self, color):
        """Set preview background color"""
        self.bg_color = color
        self.config(bg=color)
        self.text_scroll_frame.config(bg=color)
        self.preview_text.config(bg=color)