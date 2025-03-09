import tkinter as tk

from views.main_view import MainView

class XLSProcessorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XLS Processor")
        self.geometry("800x600")

        # Load the main view
        MainView(self).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = XLSProcessorApp()
    app.mainloop()