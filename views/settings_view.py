import customtkinter as ctk
from styles import AppColors, AppFonts, ButtonStyles, AppConfig, ListboxStyles, TkinterDialogStyles


class SettingsDialog(ctk.CTkToplevel):
    """Settings dialog for application configuration"""
    
    def __init__(self, parent, on_apply_callback=None):
        super().__init__(parent)
        
        self.on_apply_callback = on_apply_callback
        self.result = None
        
        # Configure dialog window
        self.title("Settings")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Center dialog on parent window
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (300 // 2)
        self.geometry(f"+{x}+{y}")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the settings dialog UI"""
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="Application Settings",
            font=AppFonts.SUBTITLE
        )
        title_label.pack(pady=(0, 20))
        
        # Appearance Mode Section
        appearance_frame = ctk.CTkFrame(container, fg_color=AppColors.LIGHT_BLUE)
        appearance_frame.pack(fill="x", pady=(0, 20))
        
        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="Appearance Mode:",
            font=AppFonts.BODY,
            text_color=AppColors.BLACK
        )
        appearance_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Radio buttons for appearance mode
        self.appearance_var = ctk.StringVar(value=ctk.get_appearance_mode())
        
        radio_frame = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        radio_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        modes = [
            ("Light", "Light"),
            ("Dark", "Dark"),
            ("System", "System")
        ]
        
        for text, value in modes:
            radio = ctk.CTkRadioButton(
                radio_frame,
                text=text,
                variable=self.appearance_var,
                value=value,
                font=AppFonts.BODY,
                text_color=AppColors.BLACK,
                fg_color=AppColors.BLUE,
                hover_color=AppColors.DARK_GRAY
            )
            radio.pack(anchor="w", pady=3)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            **ButtonStyles.DEFAULT
        )
        cancel_btn.pack(side="right", padx=(5, 0))
        
        # Apply button
        apply_btn = ctk.CTkButton(
            button_frame,
            text="Apply",
            command=self._on_apply,
            **ButtonStyles.PRIMARY
        )
        apply_btn.pack(side="right")
        
        # Bind escape key to cancel
        self.bind("<Escape>", lambda e: self._on_cancel())
    
    def _on_apply(self):
        """Apply settings and close dialog"""
        selected_mode = self.appearance_var.get()
        
        # Apply appearance mode
        ctk.set_appearance_mode(selected_mode)
        
        # Update config
        AppConfig.APPEARANCE_MODE = selected_mode.lower()
        
        # Update colors in styles.py based on mode
        self._update_colors_for_mode(selected_mode)
        
        self.result = {
            "appearance_mode": selected_mode
        }
        
        # Call callback if provided
        if self.on_apply_callback:
            self.on_apply_callback(self.result)
        
        self.destroy()
    
    def _update_colors_for_mode(self, mode):
        """Update AppColors and ButtonStyles based on the selected appearance mode"""
        if mode.lower() == "dark":
            # Dark mode colors
            AppColors.LIGHT_BLUE = "#2a3f5f"  # Darker blue for panels
            AppColors.LIGHT_GRAY = "#404040"  # Darker hover
            AppColors.WHITE = "#1a1a1a"  # Dark background
            AppColors.BLACK = "#ffffff"  # Light text
            AppColors.MEDIUM_GRAY = "#b0b0b0"  # Lighter gray for dark mode
            
            # Update button styles for dark mode
            ButtonStyles.update_for_dark_mode()
            
            # Update listbox styles for dark mode
            ListboxStyles.update_for_dark_mode()
            
            # Update Tkinter dialog styles for dark mode
            TkinterDialogStyles.update_for_dark_mode()
        else:
            # Light mode colors (restore defaults)
            AppColors.LIGHT_BLUE = "#abd2ff"
            AppColors.LIGHT_GRAY = "#f0f0f0"
            AppColors.WHITE = "#FFFFFF"
            AppColors.BLACK = "#000000"
            AppColors.MEDIUM_GRAY = "#949494"
            
            # Update button styles for light mode
            ButtonStyles.update_for_light_mode()
            
            # Update listbox styles for light mode
            ListboxStyles.update_for_light_mode()
            
            # Update Tkinter dialog styles for light mode
            TkinterDialogStyles.update_for_light_mode()
    
    def _on_cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.destroy()
    
    def get_result(self):
        """Get the dialog result"""
        return self.result
