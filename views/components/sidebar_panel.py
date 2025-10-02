import tkinter as tk


class SidebarPanel(tk.Frame):
    """Collapsible sidebar with transform buttons"""
    
    def __init__(self, parent, controller, bg_color="#FFFFFF"):
        super().__init__(parent, bg=bg_color)
        self.controller = controller
        self.bg_color = bg_color
        self.side_visible = True
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the sidebar UI"""
        self.pack(side="left", fill="y")
        
        # Create left container for grid layout
        self.left_container = tk.Frame(self, bg=self.bg_color)
        self.left_container.pack(side="left", fill="y")
        
        # Create the actual side menu
        self.side_menu = tk.Frame(
            self.left_container, 
            width=200, 
            padx=6, 
            pady=6, 
            bg=self.bg_color
        )
        self.side_menu.grid(row=0, column=0, sticky='ns')
        
        # Add plugin panel
        from .plugin_panel import PluginPanel
        self.plugin_panel = PluginPanel(self.side_menu, self.controller, self.bg_color)
        self.plugin_panel.pack(fill='x')
        
        # Add transform label
        self.transform_label = tk.Label(
            self.side_menu, 
            text="Transform:", 
            bg="#dddddd", 
            font=("Arial", 10, "bold"), 
            bd=1, 
            relief='solid'
        )
        self.transform_label.pack(fill='x', pady=(8, 4))
        
        # Add transform buttons
        self._create_transform_buttons()
        
        # Toggle button for collapsing sidebar
        self.toggle_btn = tk.Button(
            self.left_container, 
            text="≡", 
            width=3, 
            command=self.toggle_side_panel
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
        
        for text, cmd in btn_specs:
            tk.Button(
                self.side_menu, 
                text=text, 
                command=cmd, 
                width=20
            ).pack(pady=2)
    
    def toggle_side_panel(self):
        """Toggle visibility of the side panel"""
        if self.side_visible:
            # Hide the side menu
            try:
                self.side_menu.grid_remove()
            except Exception:
                self.side_menu.pack_forget()
            self.side_visible = False
            self.toggle_btn.config(text='›')
        else:
            # Show the side menu
            try:
                self.side_menu.grid()
            except Exception:
                self.side_menu.pack(side='left', fill='y')
            self.side_visible = True
            self.toggle_btn.config(text='≡')
    
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
    
    def _create_transform_buttons(self):
        """Create transform operation buttons"""
        button_specs = [
            ("Pivot Table", self._on_pivot_table),
            ("Rename Column", self._on_rename_column),
            ("Keep Column", self._on_keep_column),
            ("Remove Column", self._on_drop_column),
            ("Delta Calculation", self._on_delta_calculation),
            ("Produce Output", self._on_produce_output),
            ("Custom Code", self._on_custom_code),
            ("Remove Empty Rows", self._on_remove_empty_rows),
        ]
        
        self.transform_buttons = {}
        for text, command in button_specs:
            btn = tk.Button(self.side_menu, text=text, command=command, width=20)
            btn.pack(pady=2)
            self.transform_buttons[text.lower().replace(" ", "_")] = btn
    
    def _create_toggle_button(self):
        """Create sidebar toggle button"""
        self.toggle_btn = tk.Button(
            self.left_container, 
            text="≡", 
            width=3, 
            command=self.toggle_side_panel
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
    
    def enable_transform_buttons(self, enabled=True):
        """Enable/disable all transform buttons"""
        state = "normal" if enabled else "disabled"
        for btn in self.transform_buttons.values():
            btn.config(state=state)