import tkinter as tk
from models.path_utils import get_resource_path


class HeaderPanel(tk.Frame):
    """Header panel with logo, title, and version"""
    
    def __init__(self, parent, title="ToolKit", version="v0.3.0", bg_color="#abd2ff"):
        super().__init__(parent, bg=bg_color, pady=8)
        self.title = title
        self.version = version
        self.bg_color = bg_color
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the header UI components"""
        self.pack(fill="x")
        
        # Try to load logo
        self._load_logo()
        
        # Title label
        self.title_label = tk.Label(
            self, 
            text=self.title, 
            bg=self.bg_color, 
            fg="#000000", 
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(side="left", padx=10)
        
        # Version label
        self.version_label = tk.Label(
            self, 
            text=self.version, 
            bg=self.bg_color, 
            fg="#555555", 
            font=("Arial", 10)
        )
        self.version_label.pack(side="right", padx=10)
    
    def _load_logo(self):
        """Try to load and display logo"""
        try:
            logo_path = get_resource_path("assets/logo.png")
            if logo_path.exists():
                logo_img = tk.PhotoImage(file=str(logo_path))
                # subsample reduces size by integer factor
                logo_img = logo_img.subsample(3, 3)
                self.logo_label = tk.Label(self, image=logo_img, bg=self.bg_color)
                self.logo_label.image = logo_img  # Keep reference
                self.logo_label.pack(side="left", padx=(6, 8))
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