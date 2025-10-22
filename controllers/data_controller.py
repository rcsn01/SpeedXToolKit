"""
Data Controller - Manages application data state and operations.
Separates data management from UI concerns.
"""
import pandas as pd
import os
from .processing_controller import (
    import_files, save_file, combined_file,
    drop_column, rename_column, pivot_table, delta_calculation,
    produce_output, keep_column, custom_code, remove_empty_rows,
    save_plugin, manage_plugin, apply_plugin
)


class DataController:
    """Controller that manages DataFrame state and processing operations."""
    
    def __init__(self):
        """Initialize data controller with empty state."""
        self.file_path = None
        self.df = None  # Currently loaded DataFrame
        self.current_essay = None  # Current file metadata
        
        # Store holds current preset information
        self.store = {
            "name": None,           # preset name
            "metadata": None,       # dataframe metadata
            "functions": []         # list of applied functions
        }
    
    def load_file(self, file_path: str):
        """Load a file and update internal state.
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            The loaded DataFrame or None if loading failed
        """
        self.file_path = file_path
        result = import_files(file_path)
        
        if result and isinstance(result, tuple) and len(result) == 2:
            self.df, self.current_essay = result
            # Update store metadata when a new file is loaded
            self.store['metadata'] = self.current_essay
            self.store['functions'] = []  # reset function history on new load
        else:
            self.df = None
            
        return self.df
    
    def save(self):
        """Save the current DataFrame.
        
        Returns:
            Updated store dictionary
        """
        if self.df is None:
            return None
        
        # Generate default filename from original file path
        default_filename = None
        if self.file_path:
            # Get the original filename without extension
            base_name = os.path.splitext(os.path.basename(self.file_path))[0]
            # Append "_result" and add .csv extension
            default_filename = f"{base_name}_result.csv"
            
        self.store = save_file(self.df, self.current_essay, self.store, default_filename)
        self.current_essay = None
        return self.store
    
    def apply_transform(self, transform_func):
        """Apply a transformation function to the current DataFrame.
        
        Args:
            transform_func: A function that takes (df, store) and returns (new_df, new_store)
            
        Returns:
            The transformed DataFrame or None if transformation failed
        """
        if self.df is None:
            return None
            
        results = transform_func(self.df, self.store)
        tempdf, tempstore = results
        
        if tempdf is not None:
            self.df = tempdf
            self.store = tempstore
            
        return self.df
    
    def combine_files(self):
        """Combine multiple files into one.
        
        Returns:
            The combined DataFrame or None if operation failed
        """
        self.df = combined_file()
        return self.df
    
    def save_plugin_data(self):
        """Save current state as a plugin.
        
        Returns:
            Updated store dictionary or None if no data loaded
        """
        if self.df is None:
            return None
            
        self.store = save_plugin(self.store)
        return self.store
    
    def manage_plugins(self):
        """Open plugin management interface."""
        return manage_plugin()
    
    def apply_plugin_preset(self, plugin):
        """Apply a plugin/preset to the current DataFrame.
        
        Args:
            plugin: Plugin name, dict, or tuple to apply
            
        Returns:
            The transformed DataFrame or None if operation failed
        """
        if self.df is None:
            return None
            
        new_df, new_store = apply_plugin(self.df, plugin)
        
        if isinstance(new_df, pd.DataFrame):
            self.df = new_df
            self.store = new_store
            
        return self.df
    
    def has_data(self):
        """Check if a DataFrame is currently loaded.
        
        Returns:
            True if data is loaded, False otherwise
        """
        return self.df is not None
    
    def get_dataframe(self):
        """Get the current DataFrame.
        
        Returns:
            Current DataFrame or None
        """
        return self.df
