import customtkinter as ctk
from styles import ButtonStyles, PanelStyles, AppFonts, AppColors


class SidebarPanel(ctk.CTkFrame):
    """Collapsible sidebar with transform buttons"""
    
    def __init__(self, parent, controller, bg_color=None):
        if bg_color is None:
            bg_color = PanelStyles.SIDEBAR["fg_color"]
            
        super().__init__(parent, fg_color=bg_color, width=PanelStyles.SIDEBAR["width"])
        self.controller = controller
        self.bg_color = bg_color
        self.side_visible = True
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the sidebar UI"""
        self.pack(side="left", fill="y", padx=0, pady=0)
        
        # Create left container for grid layout
        self.left_container = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.left_container.pack(side="left", fill="y")
        
        # Create the actual side menu
        self.side_menu = ctk.CTkFrame(
            self.left_container, 
            width=PanelStyles.SIDEBAR_MENU["width"],
            fg_color=PanelStyles.SIDEBAR_MENU["fg_color"]
        )
        self.side_menu.grid(row=0, column=0, sticky='ns', padx=6, pady=6)
        
        # Add plugin panel
        from .plugin_panel import PluginPanel
        self.plugin_panel = PluginPanel(self.side_menu, self.controller, self.bg_color)
        self.plugin_panel.pack(fill='x')
        
        # Add transform label
        self.transform_label = ctk.CTkLabel(
            self.side_menu, 
            text="Transform:", 
            text_color=AppColors.BLACK,
            font=AppFonts.SUBTITLE
        )
        self.transform_label.pack(fill='x', pady=(8, 4))
        
        # Add transform buttons
        self._create_transform_buttons()
        
        # Toggle button for collapsing sidebar
        self.toggle_btn = ctk.CTkButton(
            self.left_container, 
            text="≡", 
            command=self.toggle_side_panel,
            **ButtonStyles.TOGGLE_ALT
        )
        self.toggle_btn.grid(row=0, column=1, sticky='ns', padx=(4, 8), pady=6)
        
        # Configure grid weights
        self.left_container.grid_rowconfigure(0, weight=1)
    
    def _create_transform_buttons(self):
        """Create all the transform operation buttons"""
        btn_specs = [
            ("Pivot Table", self.controller.pivot_table),
            ("Rename Column", self.controller.rename_column),
            ("Keep Column", self.controller.keep_column),
            ("Remove Column", self.controller.drop_column),
            ("Delta Calculation", self.controller.delta_calculation),
            ("Produce Output", self.controller.produce_output),
            ("Custom Code", self.controller.custom_code),
            ("Remove Empty Rows", self.controller.remove_empty_rows),
        ]
        # Use centralized sidebar button style
        for text, cmd in btn_specs:
            btn = ctk.CTkButton(
                self.side_menu,
                text=text,
                command=cmd,
                **ButtonStyles.SIDEBAR
            )
            btn.pack(fill='x', pady=6, padx=6)
    
    def get_selected_plugin(self):
        """Get selected plugin from the plugin panel"""
        return self.plugin_panel.get_selected_plugin()
    
    def refresh_plugins(self):
        """Refresh plugins in the plugin panel"""
        self.plugin_panel._on_refresh_plugins()
        # Add toggle button
        self._create_toggle_button()
        
        # Configure grid
        try:
            self.left_container.grid_rowconfigure(0, weight=1)
        except Exception:
            pass
    
    def _create_toggle_button(self):
        """Create sidebar toggle button"""
        # Use CTkButton for consistency
        self.toggle_btn = ctk.CTkButton(
            self.left_container,
            text="≡",
            command=self.toggle_side_panel,
            **ButtonStyles.TOGGLE
        )
        self.toggle_btn.grid(row=0, column=1, sticky='ns', padx=(4, 8), pady=6)
    
    def toggle_side_panel(self):
        """Toggle sidebar visibility"""
        if self.side_visible:
            try:
                self.side_menu.grid_remove()
            except Exception:
                self.side_menu.forget()
            self.side_visible = False
            self.toggle_btn.config(text='›')
        else:
            try:
                self.side_menu.grid()
            except Exception:
                self.side_menu.pack(side='left', fill='y')
            self.side_visible = True
            self.toggle_btn.config(text='≡')
    
    # Transform button handlers
    def _on_pivot_table(self):
        if hasattr(self.controller, 'pivot_table'):
            self.controller.pivot_table()
    
    def _on_rename_column(self):
        if hasattr(self.controller, 'rename_column'):
            self.controller.rename_column()
    
    def _on_keep_column(self):
        if hasattr(self.controller, 'keep_column'):
            self.controller.keep_column()
    
    def _on_drop_column(self):
        if hasattr(self.controller, 'drop_column'):
            self.controller.drop_column()
    
    def _on_delta_calculation(self):
        if hasattr(self.controller, 'delta_calculation'):
            self.controller.delta_calculation()
    
    def _on_produce_output(self):
        if hasattr(self.controller, 'produce_output'):
            self.controller.produce_output()
    
    def _on_custom_code(self):
        if hasattr(self.controller, 'custom_code'):
            self.controller.custom_code()
    
    def _on_remove_empty_rows(self):
        if hasattr(self.controller, 'remove_empty_rows'):
            self.controller.remove_empty_rows()