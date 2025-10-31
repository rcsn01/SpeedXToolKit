import customtkinter as ctk
from tkinter import PhotoImage
from models.path_utils import get_resource_path
from styles import AppColors, AppFonts, PanelStyles, AppConfig


class HeaderPanel(ctk.CTkFrame):
    """Header panel with logo, title, and version"""
    
    def __init__(self, parent, title=None, version=None, bg_color=None):
        # Use centralized config as defaults
        if title is None:
            title = AppConfig.TITLE
        if version is None:
            version = AppConfig.VERSION
        if bg_color is None:
            bg_color = PanelStyles.HEADER["fg_color"]
            
        super().__init__(parent, fg_color=bg_color, height=PanelStyles.HEADER["height"])
        self.title = title
        self.version = version
        self.bg_color = bg_color
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the header UI components"""
        self.pack(fill="x", padx=0, pady=0)
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self, 
            text=self.title, 
            text_color=AppColors.BLACK, 
            font=AppFonts.TITLE
        )
        self.title_label.pack(side="left", padx=(10, 6), pady=8)

        # Small demo notice to the right of the title
        self.demo_label = ctk.CTkLabel(
            self,
            text="    for demonstration purposes only",
            text_color=AppColors.MEDIUM_GRAY,
            font=AppFonts.BODY_LARGE
        )
        # pack to the left so it appears immediately after the title
        self.demo_label.pack(side="left", padx=(0, 6), pady=14)
        
        # Version label
        self.version_label = ctk.CTkLabel(
            self, 
            text=self.version, 
            text_color=AppColors.BLACK, 
            font=AppFonts.SMALL
        )
        self.version_label.pack(side="right", padx=10, pady=8)
        
        # Try to load logo (placed after version so it's on the far right)
        self._load_logo()
    
    def _load_logo(self):
        """Try to load and display logo"""
        try:
            logo_path = get_resource_path("assets/logo.png")
            if logo_path.exists():
                logo_img = PhotoImage(file=str(logo_path))
                # subsample reduces size by integer factor
                logo_img = logo_img.subsample(3, 3)
                self.logo_label = ctk.CTkLabel(self, image=logo_img, text="")
                self.logo_label.image = logo_img  # Keep reference
                self.logo_label.pack(side="right", padx=(6, 8), pady=8)
        except Exception:
            # If loading fails, silently continue without logo
            pass
    
    def update_title(self, new_title):
        """Update the title text"""
        self.title = new_title
        self.title_label.config(text=new_title)
    
    def update_version(self, new_version):
        """Update the version text"""
        self.version = new_version
        self.version_label.config(text=new_version)