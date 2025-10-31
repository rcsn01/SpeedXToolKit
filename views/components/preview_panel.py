import customtkinter as ctk
import os
import pandas as pd
from styles import AppColors, AppFonts, PanelStyles, TkinterDialogStyles


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
        
        # Create text widget (no external scrollbars)
        self._create_text_widget()
    
    def _create_text_widget(self):
        """Create the main CTkTextbox widget for data preview"""
        # Determine text colors based on current theme
        bg_color = AppColors.WHITE
        fg_color = AppColors.BLACK
        
        self.preview_text = ctk.CTkTextbox(
            self.text_scroll_frame,
            height=45,
            width=125,
            fg_color=bg_color,
            text_color=fg_color,
            wrap="none"
        )
        self.preview_text.pack(side="left", fill="both", expand=True)
        self.preview_text.configure(font=("Courier New", 12))
    
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
        # Detect dark mode
        is_dark = AppColors.WHITE == "#1a1a1a" or AppColors.BLACK == "#ffffff"
        if is_dark:
            bg = TkinterDialogStyles.DIALOG_BG  # dark background
            fg = TkinterDialogStyles.DIALOG_FG  # light text
        else:
            bg = AppColors.WHITE
            fg = AppColors.BLACK
        # Update panel backgrounds
        self.configure(fg_color=bg)
        self.title_frame.configure(fg_color=bg)
        self.text_scroll_frame.configure(fg_color=bg)
        # Update labels
        self.title_label.configure(text_color=fg)
        self.file_path_label.configure(text_color=AppColors.MEDIUM_GRAY)
        # Update text widget colors and font (monospaced)
        self.preview_text.configure(fg_color=bg, text_color=fg, font=("Courier New", 10))
        # Update scrollbar colors for theme
        self.y_scrollbar.configure(fg_color=TkinterDialogStyles.CANVAS_BG)
        self.x_scrollbar.configure(fg_color=TkinterDialogStyles.CANVAS_BG)
        # Store updated bg_color
        self.bg_color = bg