import customtkinter as ctk
from PIL import Image, ImageTk
from models.path_utils import get_resource_path
from styles import AppColors, AppFonts, PanelStyles, AppConfig


class HeaderPanel(ctk.CTkFrame):
    def configure(self, *args, **kwargs):
        super().configure(*args, **kwargs)
        # Always refresh logo when configure is called (e.g., after theme change)
        self.refresh_logo()
    def refresh_logo(self):
        """Reload the logo based on current theme (dark/light)"""
        # Remove old logo label if exists
        if hasattr(self, 'logo_label'):
            self.logo_label.destroy()
        self._load_logo()
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
        self.title_label.pack(side="left", padx=(20, 10), pady=8)

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
        """Try to load and display logo using CTkImage"""
        try:
            light_path = get_resource_path("assets/logo.png")
            dark_path = get_resource_path("assets/logo-darkmode.png")
            
            light_img = None
            dark_img = None
            size = None

            if light_path.exists():
                light_img = Image.open(light_path)
                if size is None:
                     size = (max(1, light_img.width // 3), max(1, light_img.height // 3))
            
            if dark_path.exists():
                dark_img = Image.open(dark_path)
                if size is None:
                     size = (max(1, dark_img.width // 3), max(1, dark_img.height // 3))

            if light_img or dark_img:
                # Fallback if one is missing
                if not light_img: light_img = dark_img
                if not dark_img: dark_img = light_img
                
                logo_image = ctk.CTkImage(light_image=light_img, dark_image=dark_img, size=size)
                
                self.logo_label = ctk.CTkLabel(self, image=logo_image, text="")
                self.logo_label.pack(side="right", padx=(6, 8), pady=8)
                
        except Exception:
            pass
    
    def update_title(self, new_title):
        """Update the title text"""
        self.title = new_title
        self.title_label.config(text=new_title)
    
    def update_version(self, new_version):
        """Update the version text"""
        self.version = new_version
        self.version_label.config(text=new_version)