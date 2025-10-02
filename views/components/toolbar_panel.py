import tkinter as tk


class ToolbarPanel(tk.Frame):
    """Top toolbar with main action buttons"""
    
    def __init__(self, parent, controller, bg_color="#FFFFFF"):
        super().__init__(parent, height=40, padx=10, pady=4, bg=bg_color)
        self.controller = controller
        self.bg_color = bg_color
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the toolbar UI components"""
        self.pack(side="top", fill="x")
        
        # Define button configurations
        button_configs = [
            ("Settings", self._on_settings),
            ("Load File", self._on_load_file),
            ("Manage Preset", self._on_manage_preset),
            ("Combine File", self._on_combine_file),
            ("Save File", self._on_save_file),
            ("Save Preset", self._on_save_preset),
        ]
        
        # Create buttons
        self.buttons = {}
        for text, command in button_configs:
            btn = tk.Button(self, text=text, command=command)
            btn.pack(side="left", padx=4)
            self.buttons[text.lower().replace(" ", "_")] = btn
    
    def _on_settings(self):
        """Handle settings button click"""
        if hasattr(self.controller, 'settings'):
            self.controller.settings()
    
    def _on_load_file(self):
        """Handle load file button click"""
        if hasattr(self.controller, 'load_file'):
            self.controller.load_file()
    
    def _on_manage_preset(self):
        """Handle manage preset button click"""
        if hasattr(self.controller, 'manage_preset'):
            self.controller.manage_preset()
    
    def _on_combine_file(self):
        """Handle combine file button click"""
        if hasattr(self.controller, 'combine_file'):
            self.controller.combine_file()
    
    def _on_save_file(self):
        """Handle save file button click"""
        if hasattr(self.controller, 'save_file'):
            self.controller.save_file()
    
    def _on_save_preset(self):
        """Handle save preset button click"""
        if hasattr(self.controller, 'save_preset'):
            self.controller.save_preset()
    
    def enable_button(self, button_name, enabled=True):
        """Enable/disable a specific button"""
        if button_name in self.buttons:
            state = "normal" if enabled else "disabled"
            self.buttons[button_name].config(state=state)
    
    def update_button_text(self, button_name, new_text):
        """Update button text"""
        if button_name in self.buttons:
            self.buttons[button_name].config(text=new_text)