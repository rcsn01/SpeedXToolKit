import customtkinter as ctk
from tkinter import Text, Scrollbar
import pandas as pd
import os
from styles import AppColors, AppFonts, PanelStyles


class PreviewPanel(ctk.CTkFrame):
    """Data preview panel with scrollable text widget"""
    
    def __init__(self, parent, bg_color=None):
        if bg_color is None:
            bg_color = PanelStyles.PREVIEW["fg_color"]
        super().__init__(parent, fg_color=bg_color)
        self.bg_color = bg_color
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the preview panel UI"""
        self.pack(side="left", fill="both", expand=True)
        
        # Title frame to hold label and file path
        self.title_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.title_frame.pack(side="top", fill="x", padx=12, pady=(8, 0))
        
        # Title label for the preview
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="File Preview",
            text_color=AppColors.BLACK,
            font=AppFonts.BODY
        )
        self.title_label.pack(side="left")
        
        # File path label (initially empty)
        self.file_path_label = ctk.CTkLabel(
            self.title_frame,
            text="",
            text_color=AppColors.MEDIUM_GRAY,
            font=AppFonts.SMALL
        )
        self.file_path_label.pack(side="left", padx=(10, 0))

        # Create scrollable text frame
        self.text_scroll_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
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
        self.y_scrollbar = Scrollbar(self.text_scroll_frame)
        self.y_scrollbar.pack(side="right", fill="y")
        
        # Horizontal scrollbar
        self.x_scrollbar = Scrollbar(self.text_scroll_frame, orient="horizontal")
        self.x_scrollbar.pack(side="bottom", fill="x")
    
    def _create_text_widget(self):
        """Create the main text widget for data preview"""
        # Determine text colors based on current theme
        bg_color = AppColors.WHITE
        fg_color = AppColors.BLACK
        
        self.preview_text = Text(
            self.text_scroll_frame,
            height=45,
            width=125,
            bg=bg_color,
            fg=fg_color,
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
            self.file_path_label.configure(text=f"({filename})")
        else:
            self.file_path_label.configure(text="")
        
        # Clear existing content
        self.preview_text.delete("1.0", "end")
        
        if df is not None and isinstance(df, pd.DataFrame):
            preview_text = df.to_string(index=False)
            self.preview_text.insert("end", preview_text)
        elif text is not None:
            self.preview_text.insert("end", text)
        else:
            self.preview_text.insert("end", "No data loaded.")
    
    def clear_preview(self):
        """Clear all preview content"""
        self.preview_text.delete("1.0", "end")
    
    def get_preview_text(self):
        """Get current preview text content"""
        return self.preview_text.get("1.0", "end")
    
    def set_font(self, font_family="Courier", font_size=10):
        """Set preview text font"""
        self.preview_text.config(font=(font_family, font_size))
    
    def set_background_color(self, color):
        """Set preview background color"""
        self.bg_color = color
        self.config(bg=color)
        self.text_scroll_frame.config(bg=color)
        self.preview_text.config(bg=color)
    
    def refresh_colors(self):
        """Refresh colors when theme changes"""
        # Update panel backgrounds
        self.configure(fg_color=AppColors.WHITE)
        self.title_frame.configure(fg_color=AppColors.WHITE)
        self.text_scroll_frame.configure(fg_color=AppColors.WHITE)
        
        # Update labels
        self.title_label.configure(text_color=AppColors.BLACK)
        self.file_path_label.configure(text_color=AppColors.MEDIUM_GRAY)
        
        # Update text widget colors
        self.preview_text.config(
            bg=AppColors.WHITE,
            fg=AppColors.BLACK
        )
        
        # Store updated bg_color
        self.bg_color = AppColors.WHITE