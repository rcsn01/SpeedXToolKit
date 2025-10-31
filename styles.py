"""
Centralized styling configuration for SpeedXToolKit
All colors, fonts, button styles, and panel configurations are defined here.
Change the entire app's appearance by modifying this single file.
"""


class AppColors:
    """Application color palette - SpeeDX brand colors and UI colors"""
    
    # SpeeDX Brand Colors (RGB tuples)
    BLUE_RGB = (32, 165, 221)
    PURPLE_RGB = (89, 48, 133)
    WHITE_RGB = (255, 255, 255)
    
    # SpeeDX Brand Colors (Hex)
    BLUE = "#0272BA"
    PURPLE = "#593085"
    WHITE = "#FFFFFF"
    
    # UI Colors
    LIGHT_BLUE = "#abd2ff"
    LIGHT_GRAY = "#f0f0f0"
    MEDIUM_GRAY = "#949494"
    DARK_GRAY = "#b1b1b1"
    HOVER_GRAY = "#c0c0c0"
    BLACK = "#000000"


class AppFonts:
    """Application typography - font families, sizes, and weights"""
    
    FAMILY = "Arial"
    
    # Font configurations as tuples: (family, size, weight)
    TITLE = (FAMILY, 30, "bold")
    SUBTITLE = (FAMILY, 18, "bold")
    BODY = (FAMILY, 11)
    BODY_LARGE = (FAMILY, 16, "italic")
    SMALL = (FAMILY, 10)


class ButtonStyles:
    """Reusable button style configurations"""
    
    # Default toolbar button style
    DEFAULT = {
        "width": 100,
        "height": 30,
        "corner_radius": 8,
        "fg_color": "white",
        "hover_color": "#f0f0f0",
        "text_color": "black",
        "font": AppFonts.BODY
    }
    
    # Sidebar transform button style
    SIDEBAR = {
        "width": 120,
        "height": 30,
        "corner_radius": 8,
        "fg_color": "white",
        "hover_color": "#f0f0f0",
        "text_color": "black",
        "font": AppFonts.BODY
    }
    
    # Sidebar toggle button style
    TOGGLE = {
        "width": 30,
        "height": 30,
        "corner_radius": 6,
        "fg_color": "white",
        "hover_color": "#c0c0c0",
        "font": AppFonts.BODY
    }
    
    # Toolbar toggle button (alternate style)
    TOGGLE_ALT = {
        "width": 10,
        "corner_radius": 8,
        "fg_color": "white",
        "hover_color": "#b1b1b1",
        "font": AppFonts.BODY
    }
    
    # Plugin panel buttons (Apply/Refresh)
    PLUGIN = {
        "width": 70,
        "height": 30,
        "corner_radius": 8,
        "fg_color": "white",
        "hover_color": "#f0f0f0",
        "text_color": "black",
        "font": AppFonts.BODY
    }
    
    # Primary action button (e.g., Apply in settings)
    PRIMARY = {
        "width": 100,
        "height": 30,
        "corner_radius": 8,
        "fg_color": AppColors.BLUE,
        "hover_color": AppColors.PURPLE,
        "text_color": "white",
        "font": AppFonts.BODY
    }
    
    @staticmethod
    def update_for_dark_mode():
        """Update button styles for dark mode"""
        ButtonStyles.DEFAULT["fg_color"] = "#404040"
        ButtonStyles.DEFAULT["hover_color"] = "#505050"
        ButtonStyles.DEFAULT["text_color"] = "white"
        
        ButtonStyles.SIDEBAR["fg_color"] = "#404040"
        ButtonStyles.SIDEBAR["hover_color"] = "#505050"
        ButtonStyles.SIDEBAR["text_color"] = "white"
        
        ButtonStyles.TOGGLE["fg_color"] = "#404040"
        ButtonStyles.TOGGLE["hover_color"] = "#505050"
        
        ButtonStyles.TOGGLE_ALT["fg_color"] = "#404040"
        ButtonStyles.TOGGLE_ALT["hover_color"] = "#505050"
        
        ButtonStyles.PLUGIN["fg_color"] = "#404040"
        ButtonStyles.PLUGIN["hover_color"] = "#505050"
        ButtonStyles.PLUGIN["text_color"] = "white"
    
    @staticmethod
    def update_for_light_mode():
        """Update button styles for light mode"""
        ButtonStyles.DEFAULT["fg_color"] = "white"
        ButtonStyles.DEFAULT["hover_color"] = "#f0f0f0"
        ButtonStyles.DEFAULT["text_color"] = "black"
        
        ButtonStyles.SIDEBAR["fg_color"] = "white"
        ButtonStyles.SIDEBAR["hover_color"] = "#f0f0f0"
        ButtonStyles.SIDEBAR["text_color"] = "black"
        
        ButtonStyles.TOGGLE["fg_color"] = "white"
        ButtonStyles.TOGGLE["hover_color"] = "#c0c0c0"
        
        ButtonStyles.TOGGLE_ALT["fg_color"] = "white"
        ButtonStyles.TOGGLE_ALT["hover_color"] = "#b1b1b1"
        
        ButtonStyles.PLUGIN["fg_color"] = "white"
        ButtonStyles.PLUGIN["hover_color"] = "#f0f0f0"
        ButtonStyles.PLUGIN["text_color"] = "black"


class PanelStyles:
    """Panel/Frame style configurations"""
    
    HEADER = {
        "fg_color": AppColors.WHITE,
        "height": 50
    }
    
    TOOLBAR = {
        "fg_color": AppColors.LIGHT_BLUE,
        "height": 50,
        "corner_radius": 0
    }
    
    SIDEBAR = {
        "fg_color": AppColors.LIGHT_BLUE,
        "width": 220
    }
    
    SIDEBAR_MENU = {
        "fg_color": AppColors.LIGHT_BLUE,
        "width": 200
    }
    
    PREVIEW = {
        "fg_color": AppColors.WHITE
    }


class AppConfig:
    """Application-wide configuration constants"""
    
    VERSION = "3.4"
    TITLE = "SpeedXToolKit"
    WINDOW_SIZE = "1280x780"
    APPEARANCE_MODE = "light"  # Options: "light", "dark", "system"
    COLOR_THEME = "blue"  # Options: "blue", "green", "dark-blue"


class ListboxStyles:
    """Styles for Tkinter Listbox widgets (used for plugin list)"""
    
    PLUGIN_LIST = {
        "height": 5,
        "bg": "white",
        "fg": "black",
        "selectbackground": AppColors.BLUE,
        "selectforeground": "white"
    }
    
    @staticmethod
    def update_for_dark_mode():
        """Update listbox styles for dark mode"""
        ListboxStyles.PLUGIN_LIST["bg"] = "#1a1a1a"
        ListboxStyles.PLUGIN_LIST["fg"] = "white"
        ListboxStyles.PLUGIN_LIST["selectbackground"] = AppColors.PURPLE
    
    @staticmethod
    def update_for_light_mode():
        """Update listbox styles for light mode"""
        ListboxStyles.PLUGIN_LIST["bg"] = "white"
        ListboxStyles.PLUGIN_LIST["fg"] = "black"
        ListboxStyles.PLUGIN_LIST["selectbackground"] = AppColors.BLUE


class TkinterDialogStyles:
    """Styles for Tkinter dialog windows (pivot table, drop column, etc.)"""
    
    # Dialog window styling
    DIALOG_BG = "white"
    DIALOG_FG = "black"
    
    # Label styling
    LABEL_FONT = ("Arial", 10)
    LABEL_BOLD_FONT = ("Arial", 12, "bold")
    LABEL_FG = "black"
    
    # Entry/Combobox styling
    INPUT_WIDTH = 20
    INPUT_BG = "white"
    INPUT_FG = "black"
    
    # Frame styling
    FRAME_BG = "white"
    
    # Button styling (using ttk.Button defaults)
    BUTTON_PADDING = 10
    
    # Checkbox styling
    CHECKBOX_BG = "white"
    CHECKBOX_FG = "black"
    
    # Canvas/Scrollbar styling
    CANVAS_BG = "white"
    
    @staticmethod
    def update_for_dark_mode():
        """Update Tkinter dialog styles for dark mode"""
        TkinterDialogStyles.DIALOG_BG = "#2b2b2b"
        TkinterDialogStyles.DIALOG_FG = "white"
        TkinterDialogStyles.LABEL_FG = "white"
        TkinterDialogStyles.INPUT_BG = "#3c3c3c"
        TkinterDialogStyles.INPUT_FG = "white"
        TkinterDialogStyles.FRAME_BG = "#2b2b2b"
        TkinterDialogStyles.CHECKBOX_BG = "#2b2b2b"
        TkinterDialogStyles.CHECKBOX_FG = "white"
        TkinterDialogStyles.CANVAS_BG = "#2b2b2b"
    
    @staticmethod
    def update_for_light_mode():
        """Update Tkinter dialog styles for light mode"""
        TkinterDialogStyles.DIALOG_BG = "white"
        TkinterDialogStyles.DIALOG_FG = "black"
        TkinterDialogStyles.LABEL_FG = "black"
        TkinterDialogStyles.INPUT_BG = "white"
        TkinterDialogStyles.INPUT_FG = "black"
        TkinterDialogStyles.FRAME_BG = "white"
        TkinterDialogStyles.CHECKBOX_BG = "white"
        TkinterDialogStyles.CHECKBOX_FG = "black"
        TkinterDialogStyles.CANVAS_BG = "white"


# Legacy compatibility - for backward compatibility with existing code
# Remove this section once all files are migrated to new style classes
COLOURS = {
    "blue_rgb": AppColors.BLUE_RGB,
    "purple_rgb": AppColors.PURPLE_RGB,
    "white_rgb": AppColors.WHITE_RGB,
    "blue_hex": AppColors.BLUE,
    "purple_hex": AppColors.PURPLE,
    "white_hex": AppColors.WHITE,
    "light_blue_hex": AppColors.LIGHT_BLUE
}
