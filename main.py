import customtkinter as ctk
import sys
import os
from PIL import Image, ImageTk
sys.setrecursionlimit(2000)

from views.main_view import MainView
from styles import AppConfig

# Set appearance mode and default color theme using centralized config
ctk.set_appearance_mode(AppConfig.APPEARANCE_MODE)  # Options: "light", "dark", "system"
ctk.set_default_color_theme(AppConfig.COLOR_THEME)  # Options: "blue", "green", "dark-blue"

class XLSProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(AppConfig.TITLE)
        self.geometry(AppConfig.WINDOW_SIZE)

        # Set application icon (window and taskbar)
        import tkinter as tk
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
        MainView(self).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = XLSProcessorApp()
    app.mainloop()

#pyinstaller --onefile --windowed main.py

