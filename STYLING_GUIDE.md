# SpeedXToolKit Styling Guide

## Overview
All styling for SpeedXToolKit is now centralized in `styles.py`. This makes it easy to maintain consistency and change the entire app's appearance from one location.

## Quick Reference

### Change App Colors
Edit `styles.py` → `AppColors` class:
```python
class AppColors:
    BLUE = "#0272BA"        # Change brand blue
    PURPLE = "#593085"      # Change brand purple
    LIGHT_BLUE = "#abd2ff"  # Change panel backgrounds
    # ... etc
```

### Change Fonts
Edit `styles.py` → `AppFonts` class:
```python
class AppFonts:
    FAMILY = "Arial"  # Change to "Segoe UI", "Helvetica", etc.
    TITLE = (FAMILY, 30, "bold")   # (font, size, weight)
    SUBTITLE = (FAMILY, 18, "bold")
    BODY = (FAMILY, 11)
    # ... etc
```

### Change Button Styles
Edit `styles.py` → `ButtonStyles` class:
```python
class ButtonStyles:
    DEFAULT = {  # Toolbar buttons
        "width": 100,
        "height": 30,
        "corner_radius": 8,
        "fg_color": "white",
        "hover_color": "#f0f0f0",
        "text_color": "black",
        # ... etc
    }
    
    SIDEBAR = {  # Transform buttons
        # ... configuration
    }
    
    PLUGIN = {  # Plugin Apply/Refresh buttons
        # ... configuration
    }
    
    PRIMARY = {  # Primary action buttons (Apply in settings)
        # ... configuration
    }
    
    # Automatic theme updates
    @staticmethod
    def update_for_dark_mode():
        # Automatically called when switching to dark mode
        
    @staticmethod
    def update_for_light_mode():
        # Automatically called when switching to light mode
```

**Available Button Styles:**
- `ButtonStyles.DEFAULT` - Toolbar buttons (Settings, Load File, etc.)
- `ButtonStyles.SIDEBAR` - Transform buttons (Pivot Table, Rename Column, etc.)
- `ButtonStyles.TOGGLE` - Sidebar collapse button
- `ButtonStyles.TOGGLE_ALT` - Alternative toggle style
- `ButtonStyles.PLUGIN` - Plugin panel buttons (Apply, Refresh)
- `ButtonStyles.PRIMARY` - Primary action buttons (Apply in settings)

### Change Panel Backgrounds
Edit `styles.py` → `PanelStyles` class:
```python
class PanelStyles:
    HEADER = {
        "fg_color": AppColors.WHITE,
        "height": 50
    }
    TOOLBAR = {
        "fg_color": AppColors.LIGHT_BLUE,  # Change toolbar background
        # ... etc
    }
```

### Change Plugin Listbox Styles
Edit `styles.py` → `ListboxStyles` class:
```python
class ListboxStyles:
    PLUGIN_LIST = {
        "height": 5,
        "bg": "white",
        "fg": "black",
        "selectbackground": AppColors.BLUE,
        "selectforeground": "white"
    }
    
    # Automatic theme updates
    @staticmethod
    def update_for_dark_mode():
        # Called when switching to dark mode
        
    @staticmethod
    def update_for_light_mode():
        # Called when switching to light mode
```

### Change App Configuration
Edit `styles.py` → `AppConfig` class:
```python
class AppConfig:
    VERSION = "3.4"
    TITLE = "SpeedXToolKit"
    WINDOW_SIZE = "1280x780"
    APPEARANCE_MODE = "light"  # "light", "dark", or "system"
    COLOR_THEME = "blue"       # "blue", "green", or "dark-blue"
```

## Usage Examples

### In a New Component
```python
from styles import AppColors, AppFonts, ButtonStyles

class MyNewPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=AppColors.LIGHT_BLUE)
        
        # Use centralized fonts
        self.label = ctk.CTkLabel(
            self,
            text="My Label",
            font=AppFonts.TITLE,
            text_color=AppColors.BLACK
        )
        
        # Use centralized button style
        self.button = ctk.CTkButton(
            self,
            text="Click Me",
            **ButtonStyles.DEFAULT  # Unpack the style dict
        )
```

### Creating Custom Button Variants
Add new styles to `ButtonStyles` in `styles.py`:
```python
class ButtonStyles:
    # ... existing styles ...
    
    DANGER = {
        "width": 100,
        "height": 30,
        "corner_radius": 8,
        "fg_color": "#ff4444",
        "hover_color": "#cc0000",
        "text_color": AppColors.WHITE,
        "font": AppFonts.BODY
    }
```

Then use it:
```python
delete_btn = ctk.CTkButton(self, text="Delete", **ButtonStyles.DANGER)
```

## What Changed?

### Files Refactored
1. ✅ `styles.py` - **NEW** centralized styling file
2. ✅ `main.py` - Uses `AppConfig` for window settings
3. ✅ `views/main_view.py` - Uses centralized colors and config, refreshes all UI on theme change
4. ✅ `views/components/header_panel.py` - Uses `AppFonts` and `AppColors`
5. ✅ `views/components/toolbar_panel.py` - Uses `ButtonStyles` and `PanelStyles`
6. ✅ `views/components/sidebar_panel.py` - Uses all centralized styles
7. ✅ `views/components/plugin_panel.py` - Uses `ButtonStyles` and `AppColors`, supports theme refresh
8. ✅ `views/components/preview_panel.py` - Uses `AppColors` and `AppFonts`, supports theme refresh
9. ✅ `views/settings_view.py` - **NEW** settings dialog with light/dark mode toggle

### Benefits
- ✅ Single source of truth for all styling
- ✅ Easy to create themes (light/dark mode)
- ✅ Consistent styling across the entire app
- ✅ No more hunting for hardcoded values
- ✅ Easier for new developers to understand styling system
- ✅ Dynamic theme switching - all buttons and panels update instantly
- ✅ Plugin panel buttons included in centralized styling

## Common Styling Tasks

### Task: Make all buttons purple
```python
# In styles.py
class ButtonStyles:
    DEFAULT = {
        # ... other settings ...
        "fg_color": AppColors.PURPLE,  # Changed from WHITE
        "text_color": AppColors.WHITE,  # Changed from BLACK
    }
```

### Task: Increase all font sizes by 2 points
```python
# In styles.py
class AppFonts:
    TITLE = (FAMILY, 32, "bold")      # was 30
    SUBTITLE = (FAMILY, 20, "bold")   # was 18
    BODY = (FAMILY, 13)               # was 11
    BODY_LARGE = (FAMILY, 18, "italic")  # was 16
    SMALL = (FAMILY, 12)              # was 10
```

### Task: Enable dark mode
```python
# In styles.py
class AppConfig:
    APPEARANCE_MODE = "dark"  # Changed from "light"

# You may also want to adjust colors for dark mode:
class AppColors:
    LIGHT_BLUE = "#2a4a6a"  # Darker shade for dark mode
    # ... etc
```

### Task: Change the app window size
```python
# In styles.py
class AppConfig:
    WINDOW_SIZE = "1920x1080"  # Changed from "1280x780"
```

## Tips
- Always use the centralized styles instead of hardcoding values
- Test your changes by running `python main.py`
- If you need a new style variant, add it to `styles.py` first
- Keep related styles together in the same class
- Use descriptive names for new style variants

## Future Enhancements
Consider adding:
- Multiple theme presets (light, dark, high contrast)
- User-selectable themes via settings dialog
- Color blind friendly palettes
- Export/import theme files
