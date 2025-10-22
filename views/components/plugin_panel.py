import customtkinter as ctk
from tkinter import messagebox, Listbox, END
from controllers.processing_controller import show_plugins
import pandas as pd


class PluginPanel(ctk.CTkFrame):
    """Plugin management panel with list and controls"""
    
    def __init__(self, parent, controller, bg_color="#FFFFFF"):
        super().__init__(parent, fg_color=bg_color)
        self.controller = controller
        self.bg_color = bg_color
        self.plugins_listbox = None
        self.no_plugins_label = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the plugin panel UI"""
        # Plugin label
        self.plugins_label = ctk.CTkLabel(
            self, 
            text="Plugins:", 
            text_color="black",
            font=("Arial", 18, "bold")
        )
        self.plugins_label.pack(fill='x', pady=(8, 4))
        
        # Plugin content frame
        self.plugins_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.plugins_frame.pack(fill='x', pady=(0, 8))
        
        # Load initial plugins
        self._load_plugins()
    
    def _load_plugins(self):
        """Load and display plugins"""
        try:
            plugins = show_plugins()
        except Exception:
            plugins = []
        
        if plugins:
            self._create_plugin_list(plugins)
            self._create_plugin_buttons()
        else:
            self._create_no_plugins_label()
    
    def _create_plugin_list(self, plugins):
        """Create the plugin listbox"""
        # Extract display items
        display_items = []
        for p in plugins:
            try:
                if isinstance(p, dict):
                    display_items.append(p.get('name', str(p)))
                elif isinstance(p, (list, tuple)) and p:
                    display_items.append(str(p[0]))
                else:
                    display_items.append(str(p))
            except Exception:
                display_items.append(str(p))
        
        # Create listbox (using standard tkinter Listbox as CTk doesn't have one)
        self.plugins_listbox = Listbox(self.plugins_frame, height=5)
        for item in display_items:
            self.plugins_listbox.insert(END, item)
        self.plugins_listbox.pack(fill='x')
    
    def _create_plugin_buttons(self):
        """Create Apply and Refresh buttons"""
        btn_frame = ctk.CTkFrame(self.plugins_frame, fg_color=self.bg_color)
        btn_frame.pack(pady=4)
        
        self.apply_btn = ctk.CTkButton(
            btn_frame, 
            text="Apply", 
            command=self._on_apply_plugin,
            width=70,
            height=30,
            corner_radius=8,
            fg_color="white",
            hover_color="#f0f0f0",
            text_color="black",
            font=("Arial", 11)
        )
        self.apply_btn.pack(side='left', padx=4)
        
        self.refresh_btn = ctk.CTkButton(
            btn_frame, 
            text="Refresh", 
            command=self._on_refresh_plugins,
            width=70,
            height=30,
            corner_radius=8,
            fg_color="white",
            hover_color="#f0f0f0",
            text_color="black",
            font=("Arial", 11)
        )
        self.refresh_btn.pack(side='left', padx=4)
    
    def _create_no_plugins_label(self):
        """Create 'no plugins' label"""
        self.no_plugins_label = ctk.CTkLabel(
            self.plugins_frame, 
            text="No plugins", 
            text_color="#777777"
        )
        self.no_plugins_label.pack(fill='x')
    
    def _on_apply_plugin(self):
        """Handle apply plugin button click"""
        if not self.plugins_listbox:
            return
        
        try:
            sel = self.plugins_listbox.curselection()
            if not sel:
                messagebox.showwarning("No selection", "Please select a plugin to apply.")
                return
            
            name = self.plugins_listbox.get(sel[0])
            
            # Check if data is loaded
            if not self.controller.data.has_data():
                messagebox.showwarning("No Data", "Please load a file first.")
                return
            
            # Apply plugin through data controller
            result = self.controller.data.apply_plugin_preset(name)
            
            if isinstance(result, pd.DataFrame):
                # Update preview
                if hasattr(self.controller, 'display_dataframe_preview'):
                    self.controller.display_dataframe_preview()
                messagebox.showinfo("Plugin Applied", f"Plugin '{name}' applied.")
            else:
                messagebox.showwarning("Apply Failed", f"Plugin '{name}' did not produce a valid DataFrame.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply plugin: {e}")
    
    def _on_refresh_plugins(self):
        """Handle refresh plugins button click"""
        try:
            new_plugins = show_plugins()
            items = []
            
            for p in new_plugins:
                try:
                    if isinstance(p, dict):
                        items.append(p.get('name', str(p)))
                    elif isinstance(p, (list, tuple)) and p:
                        items.append(str(p[0]))
                    else:
                        items.append(str(p))
                except Exception:
                    items.append(str(p))
            
            # Remove 'no plugins' label if it exists
            if self.no_plugins_label:
                try:
                    self.no_plugins_label.destroy()
                    self.no_plugins_label = None
                except Exception:
                    pass
            
            # Update or create listbox
            if self.plugins_listbox:
                self.plugins_listbox.delete(0, END)
                for item in items:
                    self.plugins_listbox.insert(END, item)
            else:
                self._create_plugin_list(new_plugins)
                if not hasattr(self, 'apply_btn'):
                    self._create_plugin_buttons()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh plugins: {e}")
    
    def get_selected_plugin(self):
        """Get the currently selected plugin"""
        if self.plugins_listbox:
            sel = self.plugins_listbox.curselection()
            if sel:
                return self.plugins_listbox.get(sel[0])
        return None