import customtkinter as ctk
from styles import AppColors, AppFonts, ButtonStyles, AppConfig, ListboxStyles, TkinterDialogStyles, RadioButtonStyles, PanelStyles


class SettingsDialog(ctk.CTkToplevel):
    """Settings dialog for application configuration"""
    
    def __init__(self, parent, on_apply_callback=None):
        super().__init__(parent)
        
        self.on_apply_callback = on_apply_callback
        self.result = None
        
        # Configure dialog window - using centralized styling
        self.title("Settings")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(fg_color=TkinterDialogStyles.DIALOG_BG)
        
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
        # Main container - using centralized styling
        container = ctk.CTkFrame(self, fg_color=TkinterDialogStyles.FRAME_BG)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title - using centralized styling
        title_label = ctk.CTkLabel(
            container,
            text="Application Settings",
            font=TkinterDialogStyles.LABEL_BOLD_FONT,
            text_color=TkinterDialogStyles.LABEL_FG
        )
        title_label.pack(pady=(0, 20))
        
        # Appearance Mode Section - using centralized styling
        appearance_frame = ctk.CTkFrame(container, fg_color=TkinterDialogStyles.FRAME_BG)
        appearance_frame.pack(fill="x", pady=(0, 20))
        
        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="Appearance Mode:",
            font=TkinterDialogStyles.LABEL_FONT,
            text_color=TkinterDialogStyles.LABEL_FG
        )
        appearance_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Radio buttons for appearance mode
        # Use a safe default: if the runtime returns 'system', fall back to the saved config
        current_mode = ctk.get_appearance_mode().lower()
        if current_mode == "system":
            current_mode = AppConfig.load_appearance_mode()
        # Normalize to 'Light' or 'Dark' for the radio values
        normalized = "Light" if current_mode.lower() not in ("dark", "light") else current_mode.title()
        self.appearance_var = ctk.StringVar(value=normalized)
        
        radio_frame = ctk.CTkFrame(appearance_frame, fg_color=TkinterDialogStyles.FRAME_BG)
        radio_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Only offer Light and Dark options (remove 'System')
        modes = [
            ("Light", "Light"),
            ("Dark", "Dark"),
        ]
        
        for text, value in modes:
            radio = ctk.CTkRadioButton(
                radio_frame,
                text=text,
                variable=self.appearance_var,
                value=value,
                **RadioButtonStyles.DEFAULT,
            )
            radio.pack(anchor="w", pady=3, padx=4)
        
        # Buttons frame - using centralized styling
        button_frame = ctk.CTkFrame(container, fg_color=TkinterDialogStyles.FRAME_BG)
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
        # Accessibility: allow Enter to trigger Apply and set focus to the Apply button
        apply_btn.focus_set()
        self.bind("<Return>", lambda e: self._on_apply())
        
        # Bind escape key to cancel
        self.bind("<Escape>", lambda e: self._on_cancel())
    
    def _on_apply(self):
        """Apply settings and close dialog"""
        selected_mode = self.appearance_var.get()
        
        # Apply appearance mode
        ctk.set_appearance_mode(selected_mode)
        
        # Update config and persist
        AppConfig.APPEARANCE_MODE = selected_mode.lower()
        AppConfig.save_appearance_mode(selected_mode.lower())
        
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
            
            # Update panel styles for dark mode (toolbar and sidebar colors)
            PanelStyles.update_for_dark_mode()
            
            # Update listbox styles for dark mode
            ListboxStyles.update_for_dark_mode()
            
            # Update Tkinter dialog styles for dark mode
            TkinterDialogStyles.update_for_dark_mode()
            
            # Update radio button styles for dark mode
            RadioButtonStyles.update_for_dark_mode()
        else:
            # Light mode colors (restore defaults)
            AppColors.LIGHT_BLUE = "#abd2ff"
            AppColors.LIGHT_GRAY = "#f0f0f0"
            AppColors.WHITE = "#FFFFFF"
            AppColors.BLACK = "#000000"
            AppColors.MEDIUM_GRAY = "#949494"
            
            # Update button styles for light mode
            ButtonStyles.update_for_light_mode()
            
            # Update panel styles for light mode (toolbar and sidebar colors)
            PanelStyles.update_for_light_mode()
            
            # Update listbox styles for light mode
            ListboxStyles.update_for_light_mode()
            
            # Update Tkinter dialog styles for light mode
            TkinterDialogStyles.update_for_light_mode()
            
            # Update radio button styles for light mode
            RadioButtonStyles.update_for_light_mode()
    
    def _on_cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.destroy()
    
    def get_result(self):
        """Get the dialog result"""
        return self.result
