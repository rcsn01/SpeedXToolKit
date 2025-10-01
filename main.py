import tkinter as tk
import sys
sys.setrecursionlimit(2000)

from views.main_view import MainView

class XLSProcessorApp(tk.Tk):
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

