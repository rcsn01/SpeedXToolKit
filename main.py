import customtkinter as ctk
import sys
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

        # Load the main view
        MainView(self).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = XLSProcessorApp()
    app.mainloop()

#pyinstaller --onefile --windowed main.py

