"""
Centralized styling configuration for SpeedXToolKit
All colors, fonts, button styles, and panel configurations are defined here.
Change the entire app's appearance by modifying this single file.

EDITING GUIDE:
- AppColors: Edit to change colors throughout the entire app (brand colors, backgrounds, text)
- AppFonts: Edit to change fonts, sizes, and text styles
- ButtonStyles: Edit to change button appearance (colors, sizes, hover effects)
- PanelStyles: Edit to change panel/frame backgrounds and dimensions
- AppConfig: Edit to change app settings (version, window size, default theme)
- ListboxStyles: Edit to change plugin list appearance
- TkinterDialogStyles: Edit to change dialog window styling (LEGACY - being phased out)
- RadioButtonStyles: Edit to change radio button appearance in settings dialog
"""


# ============================================================================
# COLOR PALETTE
# Edit this section to change colors used throughout the entire application
# ============================================================================
class AppColors:
    """Application color palette - SpeeDX brand colors and UI colors"""
    
    # SpeeDX Brand Colors (RGB tuples) - Used for image generation/processing
    # Edit these to change brand colors in RGB format
    BLUE_RGB = (32, 165, 221)
    PURPLE_RGB = (89, 48, 133)
    WHITE_RGB = (255, 255, 255)
    
    # SpeeDX Brand Colors (Hex) - Used throughout the UI
    # Edit these to change primary brand colors (buttons, accents, headers)
    BLUE = "#0272BA"      # Primary brand color - used for buttons, highlights
    PURPLE = "#593085"    # Secondary brand color - used for accents, dark mode
    WHITE = "#FFFFFF"     # White - used for backgrounds, text on dark
    
    # UI Colors - Supporting colors for interface elements
    # Edit these to change backgrounds, hover effects, and UI details
    LIGHT_BLUE = "#abd2ff"   # Toolbar and sidebar background
    LIGHT_GRAY = "#f0f0f0"   # Light backgrounds, hover effects
    MEDIUM_GRAY = "#949494"  # Borders, dividers
    DARK_GRAY = "#b1b1b1"    # Hover states, inactive elements
    HOVER_GRAY = "#c0c0c0"   # Button hover color
    BLACK = "#000000"        # Text color (light mode)


# ============================================================================
# TYPOGRAPHY
# Edit this section to change fonts, sizes, and text weights
# ============================================================================
class AppFonts:
    """Application typography - font families, sizes, and weights"""
    
    # Base font family - change this to use a different font throughout the app
    FAMILY = "Arial"
    
    # Font configurations as tuples: (family, size, weight)
    # Edit sizes (second number) to make text larger/smaller
    # Edit weight ("bold", "normal", "italic") to change text appearance
    TITLE = (FAMILY, 30, "italic", "bold")      # Large header text, slightly slanted
    SUBTITLE = (FAMILY, 18, "bold")     # Section headers
    BODY = (FAMILY, 12)                 # Normal text, buttons, labels
    BODY_LARGE = (FAMILY, 16, "italic") # Large body text
    SMALL = (FAMILY, 10)                # Small labels, footnotes


# ============================================================================
# BUTTON STYLES
# Edit this section to change button appearance (size, colors, hover effects)
# Each style dict can be modified independently for different button types
# ============================================================================
class ButtonStyles:
    """Reusable button style configurations"""
    
    # Default toolbar button style - Used for: Save, Load, Clear buttons in toolbar
    # Edit width/height to resize buttons, corner_radius to change roundness
    # Edit fg_color (background), hover_color (on mouse over), text_color
    DEFAULT = {
        "width": 100,            # Button width in pixels
        "height": 30,            # Button height in pixels
        "corner_radius": 8,      # Roundness of corners (0 = square, higher = rounder)
        "fg_color": "white",     # Background color (changes for dark mode)
        "hover_color": "#f0f0f0", # Color when mouse hovers over
        "text_color": "black",   # Text color (changes for dark mode)
    "font": AppFonts.BODY    # Font style
    }
    
    # Sidebar transform button style - Used for: Transform operation buttons
    # Edit these values to change sidebar button appearance
    SIDEBAR = {
        "width": 120,
        "height": 30,
        "corner_radius": 8,
        "fg_color": "white",
        "hover_color": "#f0f0f0",
        "text_color": "black",
    "font": AppFonts.BODY
    }
    
    # Sidebar toggle button style - Used for: Expand/collapse sidebar button
    # Small square button, edit size for larger/smaller toggle
    TOGGLE = {
        "width": 30,
        "height": 30,
        "corner_radius": 6,
        "fg_color": "white",
        "hover_color": "#c0c0c0",
    "font": AppFonts.BODY
    }
    
    # Toolbar toggle button (alternate style) - Used for: Various toolbar toggles
    TOGGLE_ALT = {
        "width": 10,
        "corner_radius": 8,
        "fg_color": "white",
        "hover_color": "#b1b1b1",
    "font": AppFonts.BODY
    }
    
    # Plugin panel buttons - Used for: Apply/Refresh buttons in plugin panel
    # Edit these to change plugin control button appearance
    PLUGIN = {
        "width": 70,
        "height": 30,
        "corner_radius": 8,
        "fg_color": "white",
        "hover_color": "#f0f0f0",
        "text_color": "black",
    "font": AppFonts.BODY
    }
    
    # Primary action button - Used for: Apply in settings, confirm dialogs
    # Uses brand colors (BLUE/PURPLE) for prominent call-to-action buttons
    PRIMARY = {
        "width": 100,
        "height": 30,
        "corner_radius": 8,
        "fg_color": AppColors.BLUE,     # Brand blue - makes it stand out
        "hover_color": AppColors.PURPLE, # Changes to purple on hover
        "text_color": "white",
    "font": AppFonts.BODY
    }
    
    # ========================================================================
    # THEME SWITCHING METHODS - Automatically updates buttons for dark/light mode
    # Don't edit these unless you want custom dark mode colors
    # ========================================================================
    @staticmethod
    def update_for_dark_mode():
        """Update button styles for dark mode - Auto-called when switching to dark mode"""
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
        """Update button styles for light mode - Auto-called when switching to light mode"""
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


# ============================================================================
# PANEL/FRAME STYLES
# Edit this section to change panel backgrounds, sizes, and layouts
# ============================================================================
class PanelStyles:
    """Panel/Frame style configurations"""
    
    # Header panel - Top section with SpeedXToolKit logo
    # Edit height to make header taller/shorter, fg_color for background
    HEADER = {
        "fg_color": AppColors.WHITE,  # Background color
        "height": 50                  # Height in pixels
    }
    
    # Toolbar panel - Contains Save, Load, Clear buttons
    # Edit height and fg_color to change toolbar appearance
    TOOLBAR = {
        "fg_color": AppColors.LIGHT_BLUE,  # Light blue background
        "height": 50,                      # Height in pixels
        "corner_radius": 0                 # 0 = square corners
    }
    
    # Sidebar panel - Left side with transformation buttons
    # Edit width to make sidebar wider/narrower
    SIDEBAR = {
        "fg_color": AppColors.LIGHT_BLUE,  # Matches toolbar color
        "width": 220                       # Width in pixels
    }
    
    # Sidebar menu - Inner menu container
    SIDEBAR_MENU = {
        "fg_color": AppColors.LIGHT_BLUE,
        "width": 200
    }
    
    # Preview panel - Right side showing data preview
    # Edit fg_color to change preview background
    PREVIEW = {
        "fg_color": AppColors.WHITE  # White background for data viewing
    }
    
    # ========================================================================
    # THEME SWITCHING - Updates toolbar and sidebar colors for dark/light mode
    # EDIT THESE to change toolbar/sidebar colors in DARK MODE
    # ========================================================================
    @staticmethod
    def update_for_dark_mode():
        """Update panel styles for dark mode - Auto-called when switching to dark mode
        
        EDIT THESE VALUES to change toolbar and sidebar colors in dark mode:
        - TOOLBAR fg_color: Background color of top toolbar (default: dark gray #2b2b2b)
        - SIDEBAR fg_color: Background color of left sidebar (default: dark gray #2b2b2b)
        - SIDEBAR_MENU fg_color: Background of sidebar menu (default: dark gray #2b2b2b)
        - HEADER fg_color: Background of header (default: darker gray #1a1a1a)
        - PREVIEW fg_color: Background of preview panel (default: dark gray #2b2b2b)
        """
        PanelStyles.TOOLBAR["fg_color"] = "#2b2b2b"      # Dark gray toolbar
        PanelStyles.SIDEBAR["fg_color"] = "#2b2b2b"      # Dark gray sidebar
        PanelStyles.SIDEBAR_MENU["fg_color"] = "#2b2b2b" # Dark gray sidebar menu
        PanelStyles.HEADER["fg_color"] = "#1a1a1a"       # Darker gray header
        PanelStyles.PREVIEW["fg_color"] = "#2b2b2b"      # Dark gray preview
    
    @staticmethod
    def update_for_light_mode():
        """Update panel styles for light mode - Auto-called when switching to light mode"""
        PanelStyles.TOOLBAR["fg_color"] = AppColors.LIGHT_BLUE  # Light blue toolbar
        PanelStyles.SIDEBAR["fg_color"] = AppColors.LIGHT_BLUE  # Light blue sidebar
        PanelStyles.SIDEBAR_MENU["fg_color"] = AppColors.LIGHT_BLUE
        PanelStyles.HEADER["fg_color"] = AppColors.WHITE        # White header
        PanelStyles.PREVIEW["fg_color"] = AppColors.WHITE       # White preview


# ============================================================================
# APPLICATION CONFIGURATION
# Edit this section to change app settings, version, window size, defaults
# ============================================================================
class AppConfig:
    @staticmethod
    def load_appearance_mode():
        """Load appearance mode.

        Behavior:
        - Prefer a user-writable config stored in the user's AppData (Windows) or home directory.
        - When not present, fall back to a bundled config next to the code or inside the PyInstaller
          onefile temp directory (sys._MEIPASS).
        This makes the app work correctly when packaged with PyInstaller (onefile)
        and still persist user changes.
        """
        import json, os, sys

        # User config (writable) - prefer this for persistence
        user_dir = os.getenv("APPDATA") or os.path.expanduser("~")
        user_config_dir = os.path.join(user_dir, "SpeedXToolKit")
        user_config_path = os.path.join(user_config_dir, "app_config.json")

        # Check user config first
        try:
            if os.path.exists(user_config_path):
                with open(user_config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("appearance_mode", "light")
        except Exception:
            # ignore and try bundled config
            pass

        # If running frozen by PyInstaller, bundled files are extracted to _MEIPASS
        try:
            if getattr(sys, "frozen", False):
                bundled = os.path.join(sys._MEIPASS, "app_config.json")
            else:
                bundled = os.path.join(os.path.dirname(__file__), "app_config.json")

            if os.path.exists(bundled):
                with open(bundled, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("appearance_mode", "light")
        except Exception:
            pass

        return "light"

    @staticmethod
    def save_appearance_mode(mode):
        """Save appearance mode to a user-writable location.

        When the app is packaged with PyInstaller the application bundle is read-only,
        so we persist settings to a per-user config directory instead.
        """
        import json, os

        user_dir = os.getenv("APPDATA") or os.path.expanduser("~")
        user_config_dir = os.path.join(user_dir, "SpeedXToolKit")
        user_config_path = os.path.join(user_config_dir, "app_config.json")
        try:
            os.makedirs(user_config_dir, exist_ok=True)
            with open(user_config_path, "w", encoding="utf-8") as f:
                json.dump({"appearance_mode": mode}, f)
        except Exception:
            # Last resort: try to write next to module (may fail in frozen exe)
            try:
                config_path = os.path.join(os.path.dirname(__file__), "app_config.json")
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump({"appearance_mode": mode}, f)
            except Exception:
                pass
    LOGO_PATH = "assets/logo.png"
    LOGO_DARK_PATH = "assets/logo-darkmode.png"

    @staticmethod
    def get_logo_path():
        # Use dark mode logo if current mode is dark
        if AppColors.WHITE == "#1a1a1a" or AppColors.BLACK == "#ffffff":
            return AppConfig.LOGO_DARK_PATH
        return AppConfig.LOGO_PATH
    """Application-wide configuration constants"""
    
    # Edit these to change basic app settings
    VERSION = "3.6"                    # App version (displayed in UI)
    TITLE = "Pearl "                    # Window title
    WINDOW_SIZE = "1280x780"           # Default window size (WIDTHxHEIGHT)
    APPEARANCE_MODE = "light"          # Default theme: "light", "dark", or "system"
    COLOR_THEME = "blue"               # CustomTkinter theme: "blue", "green", "dark-blue"


# ============================================================================
# LISTBOX STYLES (Plugin List)
# Edit this section to change the appearance of the plugin list
# ============================================================================
class ListboxStyles:
    """Styles for Tkinter Listbox widgets (used for plugin list)"""
    
    # Plugin list appearance - Shows installed plugins
    # Edit height (number of visible rows), bg (background), fg (text color)
    # selectbackground/selectforeground = colors when item is selected
    PLUGIN_LIST = {
        "height": 5,                        # Number of visible rows
        "bg": "white",                      # Background color (changes for dark mode)
        "fg": "black",                      # Text color (changes for dark mode)
        "selectbackground": AppColors.BLUE, # Highlight color when selected
        "selectforeground": "white"         # Text color when selected
    }
    
    # ========================================================================
    # THEME SWITCHING - Auto-updates listbox for dark/light mode
    # ========================================================================
    @staticmethod
    def update_for_dark_mode():
        """Update listbox styles for dark mode - Auto-called when switching"""
        ListboxStyles.PLUGIN_LIST["bg"] = "#1a1a1a"
        ListboxStyles.PLUGIN_LIST["fg"] = "white"
        ListboxStyles.PLUGIN_LIST["selectbackground"] = AppColors.PURPLE
    
    @staticmethod
    def update_for_light_mode():
        """Update listbox styles for light mode - Auto-called when switching"""
        ListboxStyles.PLUGIN_LIST["bg"] = "white"
        ListboxStyles.PLUGIN_LIST["fg"] = "black"
        ListboxStyles.PLUGIN_LIST["selectbackground"] = AppColors.BLUE


# ============================================================================
# TKINTER DIALOG STYLES (LEGACY - Being Phased Out)
# Edit this section to change old Tkinter dialog appearance
# Most dialogs now use CustomTkinter, but kept for backward compatibility
# ============================================================================
class TkinterDialogStyles:
    """Styles for Tkinter dialog windows (pivot table, drop column, etc.)"""
    
    # Dialog window styling - Background and text colors for dialog windows
    DIALOG_BG = "white"   # Window background
    DIALOG_FG = "black"   # Default text color
    
    # Label styling - For text labels in dialogs
    LABEL_FONT = ("Arial", 10)           # Normal label font
    LABEL_BOLD_FONT = ("Arial", 12, "bold")  # Bold header font
    LABEL_FG = "black"                   # Label text color
    
    # Entry/Combobox styling - For input fields
    INPUT_WIDTH = 20      # Width of input fields
    INPUT_BG = "white"    # Input background color
    INPUT_FG = "black"    # Input text color
    
    # Frame styling - For container frames in dialogs
    FRAME_BG = "white"
    
    # Button styling
    BUTTON_PADDING = 10   # Padding around buttons
    
    # Checkbox styling - For checkbox elements
    CHECKBOX_BG = "white"
    CHECKBOX_FG = "black"
    
    # Canvas/Scrollbar styling - For scrollable areas
    CANVAS_BG = "white"
    
    # ========================================================================
    # THEME SWITCHING - Auto-updates dialogs for dark/light mode
    # ========================================================================
    @staticmethod
    def update_for_dark_mode():
        """Update Tkinter dialog styles for dark mode - Auto-called when switching"""
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
        """Update Tkinter dialog styles for light mode - Auto-called when switching"""
        TkinterDialogStyles.DIALOG_BG = "white"
        TkinterDialogStyles.DIALOG_FG = "black"
        TkinterDialogStyles.LABEL_FG = "black"
        TkinterDialogStyles.INPUT_BG = "white"
        TkinterDialogStyles.INPUT_FG = "black"
        TkinterDialogStyles.FRAME_BG = "white"
        TkinterDialogStyles.CHECKBOX_BG = "white"
        TkinterDialogStyles.CHECKBOX_FG = "black"
        TkinterDialogStyles.CANVAS_BG = "white"


# ============================================================================
# RADIO BUTTON STYLES
# Edit this section to change radio button appearance in settings dialog
# ============================================================================
class RadioButtonStyles:
    """Styles for CTkRadioButton widgets"""
    
    # Default radio button style - Used in settings dialog for theme selection
    # Edit text_color, fg_color (selected color), hover_color, border widths
    DEFAULT = {
        "font": AppFonts.BODY,              # Font style
        "text_color": AppColors.BLACK,      # Text color (changes for dark mode)
        "fg_color": AppColors.BLUE,         # Color when selected (brand blue)
        "hover_color": AppColors.DARK_GRAY, # Color when mouse hovers
        "border_width_checked": 6,          # Border thickness when selected
        "border_width_unchecked": 3         # Border thickness when not selected
    }
    
    # ========================================================================
    # THEME SWITCHING - Auto-updates radio buttons for dark/light mode
    # ========================================================================
    @staticmethod
    def update_for_dark_mode():
        """Update radio button styles for dark mode - Auto-called when switching"""
        # In dark mode make the radio indicator and text white for better contrast
        RadioButtonStyles.DEFAULT["text_color"] = "white"
        RadioButtonStyles.DEFAULT["fg_color"] = "white"
        RadioButtonStyles.DEFAULT["hover_color"] = AppColors.LIGHT_GRAY
    
    @staticmethod
    def update_for_light_mode():
        """Update radio button styles for light mode - Auto-called when switching"""
        RadioButtonStyles.DEFAULT["text_color"] = AppColors.BLACK
        RadioButtonStyles.DEFAULT["fg_color"] = AppColors.BLUE
        RadioButtonStyles.DEFAULT["hover_color"] = AppColors.DARK_GRAY


# ============================================================================
# LEGACY COMPATIBILITY
# DO NOT EDIT - This section maintains compatibility with old code
# Will be removed once all files are fully migrated to new style classes
# ============================================================================
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
