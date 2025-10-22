import customtkinter as ctk


class ToolbarPanel(ctk.CTkFrame):
    """Top toolbar with main action buttons"""
    
    def __init__(self, parent, controller, bg_color="#FFFFFF"):
        super().__init__(parent, fg_color=bg_color, height=50, corner_radius=0)
        self.controller = controller
        self.bg_color = bg_color
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the toolbar UI components"""
        self.pack(side="top", fill="x", padx=0, pady=0)
        
        # Define button configurations
        button_configs = [
            ("Settings", self._on_settings),
            ("Load File", self._on_load_file),
            ("Combine File", self._on_combine_file),
            ("Save File", self._on_save_file),
            ("Manage Plugin", self._on_manage_plugin),
            ("Save Plugin", self._on_save_plugin),
        ]
        
        # Create buttons with custom styling (no shadow)
        self.buttons = {}
        for text, command in button_configs:
            btn = ctk.CTkButton(
                self,
                text=text,
                command=command,
                width=100,
                height=30,
                corner_radius=8,
                fg_color="white",
                hover_color="#f0f0f0",
                text_color="black",
                font=("Arial", 11)
            )
            btn.pack(side="left", padx=6, pady=8)
            self.buttons[text.lower().replace(" ", "_")] = btn
    
    def _on_settings(self):
        """Handle settings button click"""
        if hasattr(self.controller, 'settings'):
            self.controller.settings()
    
    def _on_load_file(self):
        """Handle load file button click"""
        if hasattr(self.controller, 'load_file'):
            self.controller.load_file()
    
    def _on_manage_plugin(self):
        """Handle manage plugin button click"""
        if hasattr(self.controller, 'manage_plugin'):
            self.controller.manage_plugin()
    
    def _on_combine_file(self):
        """Handle combine file button click"""
        if hasattr(self.controller, 'combine_file'):
            self.controller.combine_file()
    
    def _on_save_file(self):
        """Handle save file button click"""
        if hasattr(self.controller, 'save_file'):
            self.controller.save_file()
    
    def _on_save_plugin(self):
        """Handle save plugin button click"""
        if hasattr(self.controller, 'save_plugin'):
            self.controller.save_plugin()
    
    def enable_button(self, button_name, enabled=True):
        """Enable/disable a specific button"""
        if button_name in self.buttons:
            state = "normal" if enabled else "disabled"
            self.buttons[button_name].config(state=state)
    
    def update_button_text(self, button_name, new_text):
        """Update button text"""
        if button_name in self.buttons:
            self.buttons[button_name].config(text=new_text)