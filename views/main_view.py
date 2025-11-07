import customtkinter as ctk
from views.ctk_dialogs import filedialog, showinfo, showwarning, showerror, askstring, askinteger, askyesno
import pandas as pd
from controllers.data_controller import DataController
from controllers.processing_controller import (
    drop_column, rename_column, pivot_table, delta_calculation,
    produce_output, keep_column, custom_code, remove_empty_rows
)
from .components import HeaderPanel, ToolbarPanel, SidebarPanel, PreviewPanel
from .settings_view import SettingsDialog
from styles import AppColors, PanelStyles, AppConfig, ButtonStyles

# Main application view using component-based architecture
class MainView(ctk.CTkFrame):
    """Main application view using component-based architecture"""
    
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Initialize data controller
        self.data = DataController()
        
        # Setup UI components
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the main UI using components"""
        # Use centralized panel styles for correct theme
        self.header = HeaderPanel(self, title=AppConfig.TITLE, version=AppConfig.VERSION, bg_color=PanelStyles.HEADER["fg_color"])
        self.toolbar = ToolbarPanel(self, controller=self, bg_color=PanelStyles.TOOLBAR["fg_color"])
        self.sidebar = SidebarPanel(self, controller=self, bg_color=PanelStyles.SIDEBAR["fg_color"])
        self.preview = PreviewPanel(self, bg_color=PanelStyles.PREVIEW["fg_color"])

    # ================= Data Functions =================
    def settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self.winfo_toplevel(), on_apply_callback=self._on_settings_applied)
        self.wait_window(dialog)
    
    def _on_settings_applied(self, settings_result):
        """Handle settings changes"""
        if settings_result:
            # Refresh UI components to apply new colors
            self._refresh_ui_colors()
    
    def _refresh_ui_colors(self):
        """Refresh all UI components to apply new colors from styles"""
        # Update header
        self.header.configure(fg_color=PanelStyles.HEADER["fg_color"])
        # Dynamically set text colors based on theme
        is_dark = AppColors.WHITE == "#1a1a1a" or AppColors.BLACK == "#ffffff"
        header_text_color = AppColors.BLACK if not is_dark else AppColors.BLACK
        version_text_color = AppColors.BLACK if not is_dark else AppColors.BLACK
        demo_text_color = AppColors.MEDIUM_GRAY
        self.header.title_label.configure(text_color=header_text_color)
        self.header.version_label.configure(text_color=version_text_color)
        self.header.demo_label.configure(text_color=demo_text_color)
        self.header.refresh_logo()

        # Update toolbar
        self.toolbar.configure(fg_color=PanelStyles.TOOLBAR["fg_color"])
        for btn_name, btn in self.toolbar.buttons.items():
            btn.configure(
                fg_color=ButtonStyles.DEFAULT["fg_color"],
                hover_color=ButtonStyles.DEFAULT["hover_color"],
                text_color=ButtonStyles.DEFAULT["text_color"]
            )

        # Update sidebar
        self.sidebar.configure(fg_color=PanelStyles.SIDEBAR["fg_color"])
        self.sidebar.left_container.configure(fg_color=PanelStyles.SIDEBAR["fg_color"])
        self.sidebar.side_menu.configure(fg_color=PanelStyles.SIDEBAR_MENU["fg_color"])
        self.sidebar.transform_label.configure(text_color=AppColors.BLACK)

        if hasattr(self.sidebar, 'toggle_btn'):
            self.sidebar.toggle_btn.configure(
                fg_color=ButtonStyles.TOGGLE_ALT["fg_color"],
                hover_color=ButtonStyles.TOGGLE_ALT["hover_color"]
            )

        for widget in self.sidebar.side_menu.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget != self.sidebar.toggle_btn:
                widget.configure(
                    fg_color=ButtonStyles.SIDEBAR["fg_color"],
                    hover_color=ButtonStyles.SIDEBAR["hover_color"],
                    text_color=ButtonStyles.SIDEBAR["text_color"]
                )

        if hasattr(self.sidebar, 'plugin_panel'):
            self.sidebar.plugin_panel.refresh_colors()

        # Update preview panel
        self.preview.refresh_colors()

    # Load an Excel file and display it in preview
    def load_file(self):
        # Updated: combined first filter so *.csv appears immediately
        file_path = filedialog.askopenfilename(
            title="Select data file",
            filetypes=[
                ("Data files", "*.xls *.xlsx *.csv"),
                ("Excel (xls)", "*.xls"),
                ("Excel (xlsx)", "*.xlsx"),
                ("CSV", "*.csv"),
                ("All files", "*.*"),
            ]
        )
        if file_path:
            # Basic validation (in case user picked unsupported type via All files)
            if not file_path.lower().endswith((".xls", ".xlsx", ".csv")):
                showwarning("Unsupported", "Please select an .xls, .xlsx, or .csv file.")
                return
            
            df = self.data.load_file(file_path)
            
            if isinstance(df, pd.DataFrame):
                showinfo("Success", "File loaded successfully!")
                self.display_dataframe_preview()
            else:
                showwarning("Load Failed", "Could not load a valid dataset.")

    def display_dataframe_preview(self):
        """Update the preview panel with current dataframe"""
        self.preview.update_preview(
            df=self.data.get_dataframe(),
            file_path=self.data.file_path
        )

    def save_file(self):
        if self.data.has_data():
            self.data.save()
        else:
            showwarning("Warning", "No data to save!")

    def _apply_transform(self, transform_func):
        """Helper method to apply transformations and update preview"""
        if self.data.has_data():
            result = self.data.apply_transform(transform_func)
            if result is not None:
                self.display_dataframe_preview()
        else:
            showwarning("Warning", "No data loaded!")

    def drop_column(self):
        self._apply_transform(drop_column)

    def rename_column(self):
        self._apply_transform(rename_column)

    def pivot_table(self):
        self._apply_transform(pivot_table)

    def delta_calculation(self):
        self._apply_transform(delta_calculation)

    def produce_output(self):
        self._apply_transform(produce_output)

    def keep_column(self):
        self._apply_transform(keep_column)

    def manage_plugin(self):
        self.data.manage_plugins()

    def save_plugin(self):
        if self.data.has_data():
            self.data.save_plugin_data()

    def custom_code(self):
        self._apply_transform(custom_code)

    def remove_empty_rows(self):
        self._apply_transform(remove_empty_rows)


    def combine_file(self):
        """Combine multiple files into one"""
        self.data.combine_files()
        if self.data.has_data():
            self.display_dataframe_preview()