import customtkinter as ctk
import sys
sys.setrecursionlimit(2000)

from views.main_view import MainView

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class XLSProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SpeedXToolKit")
        self.geometry("1280x780")

        # Load the main view
        MainView(self).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = XLSProcessorApp()
    app.mainloop()

#pyinstaller --onefile --windowed main.py

