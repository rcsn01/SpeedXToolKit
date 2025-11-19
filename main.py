import customtkinter as ctk
import sys
import os
sys.setrecursionlimit(2000)

from views.main_view import MainView
from styles import AppConfig

class XLSProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(AppConfig.TITLE)
        self.geometry(AppConfig.WINDOW_SIZE)

        # Always check app_config.json for appearance_mode and switch if needed
        appearance_mode = AppConfig.load_appearance_mode()
        from views.settings_view import SettingsDialog
        # Use the same theme switching logic as settings dialog
        ctk.set_appearance_mode(appearance_mode)
        ctk.set_default_color_theme(AppConfig.COLOR_THEME)
        # Call the internal method to update all colors/styles
        SettingsDialog._update_colors_for_mode(appearance_mode)

    # Set application icon (window and taskbar)
        icon_png_path = os.path.join(os.path.dirname(__file__), "assets", "pearl.png")
        icon_ico_path = os.path.join(os.path.dirname(__file__), "assets", "pearl.ico")
        try:
            # Set window icon (top left)
            from PIL import Image, ImageTk
            icon_img = Image.open(icon_png_path)
            icon_photo = ImageTk.PhotoImage(icon_img)
            self.iconphoto(False, icon_photo)
            # Set taskbar icon (Windows only)
            self.iconbitmap(icon_ico_path)
        except Exception as e:
            print(f"Could not set app icon: {e}")

        # Load the main view
        self.main_view = MainView(self)
        self.main_view.pack(fill="both", expand=True)
        # Force all UI components to update colors for current theme
        self.main_view._refresh_ui_colors()

if __name__ == "__main__":
    app = XLSProcessorApp()
    app.mainloop()

