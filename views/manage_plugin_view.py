import customtkinter as ctk
from views.ctk_dialogs import filedialog, showinfo, showwarning, showerror, askstring, askinteger, askyesno
from styles import TkinterDialogStyles, AppColors, AppFonts, ButtonStyles, PanelStyles, ListboxStyles
import os
import shutil
import pickle
import json
from models.path_utils import *
from styles import TkinterDialogStyles

def manage_plugin_view(tuple_list):
    """Display a GUI to select one tuple from a list of tuples."""
    selected_tuple = None  # This will store the user's selection

    def on_edit():
        # Get the selected index
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            plugin_name = listbox.get(index)

            try:
                plugins_dir = ensure_plugins_dir()
                plugin_path = plugins_dir / f"{plugin_name}.pkl"

                if plugin_path.exists():
                    with open(plugin_path, 'rb') as f:
                        plugin_data = pickle.load(f)

                    # Create edit window
                    edit_window = ctk.CTkToplevel(root)
                    edit_window.title(f"Edit Plugin: {plugin_name}")
                    edit_window.geometry("900x600")

                    # Plugin Name (read-only display)
                    name_frame = ctk.CTkFrame(edit_window, fg_color=TkinterDialogStyles.FRAME_BG)
                    name_frame.pack(fill="x", padx=10, pady=5)
                    ctk.CTkLabel(name_frame, text="Plugin Name:", width=15, anchor="w",
                                 font=TkinterDialogStyles.LABEL_BOLD_FONT, text_color=TkinterDialogStyles.LABEL_FG).pack(side="left")
                    ctk.CTkLabel(name_frame, text=plugin_data.get('name', 'Unknown'), anchor="w", font=AppFonts.BODY, text_color=TkinterDialogStyles.LABEL_FG).pack(side="left")

                    # Metadata (read-only display)
                    metadata_frame = ctk.CTkFrame(edit_window, fg_color=TkinterDialogStyles.FRAME_BG)
                    metadata_frame.pack(fill="x", padx=10, pady=5)
                    ctk.CTkLabel(metadata_frame, text="Metadata:", width=15, anchor="w",
                                 font=TkinterDialogStyles.LABEL_BOLD_FONT, text_color=TkinterDialogStyles.LABEL_FG).pack(side="left")
                    ctk.CTkLabel(metadata_frame, text=plugin_data.get('metadata', 'None'), anchor="w", font=AppFonts.BODY, text_color=TkinterDialogStyles.LABEL_FG).pack(side="left")

                    # Separator (CTk substitute for ttk.Separator)
                    ctk.CTkFrame(edit_window, height=2, fg_color=AppColors.MEDIUM_GRAY).pack(fill='x', padx=10, pady=10)

                    # Functions header
                    ctk.CTkLabel(edit_window, text="Edit Function Parameters:",
                                 font=TkinterDialogStyles.LABEL_BOLD_FONT, text_color=TkinterDialogStyles.LABEL_FG).pack(padx=10, pady=(5, 10), anchor="w")

                    # Create scrollable frame for functions
                    scrollable_frame = ctk.CTkScrollableFrame(edit_window)
                    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)

                    # Store text widgets for each argument
                    function_widgets = []

                    # Parse and display each function
                    functions = plugin_data.get('functions', [])
                    for func_idx, func in enumerate(functions):
                        if isinstance(func, list) and func:
                            func_name = func[0] if len(func) > 0 else "unknown"
                            func_args = func[1:] if len(func) > 1 else []

                            # Function container
                            func_frame = ctk.CTkFrame(scrollable_frame, fg_color=TkinterDialogStyles.FRAME_BG)
                            func_frame.pack(fill="x", padx=5, pady=5)
                            ctk.CTkLabel(func_frame, text=f"Function {func_idx + 1}: {func_name}",
                                         font=TkinterDialogStyles.LABEL_BOLD_FONT, text_color=TkinterDialogStyles.LABEL_FG).pack(anchor="w", padx=10, pady=(10, 5))

                            # Store function name
                            function_widgets.append({
                                'name': func_name,
                                'args': []
                            })

                            # Display each argument
                            for arg_idx, arg in enumerate(func_args):
                                arg_frame = ctk.CTkFrame(func_frame)
                                arg_frame.pack(fill="x", pady=3, padx=10)

                                ctk.CTkLabel(arg_frame, text=f"Argument {arg_idx + 1}:", width=12, anchor="w").pack(side="left")

                                # Insert the argument value (as JSON for complex types)
                                try:
                                    arg_str = json.dumps(arg, indent=2, ensure_ascii=False) if not isinstance(arg, str) else arg
                                except:
                                    arg_str = str(arg)

                                # Calculate height based on number of lines
                                line_count = arg_str.count('\n') + 1
                                # Set minimum height of 2, maximum of 20, otherwise use actual line count
                                text_height = max(2, min(20, line_count))

                                # Create text widget for the argument (supports multi-line)
                                arg_text = ctk.CTkTextbox(arg_frame, height=text_height * 20, wrap="word")
                                arg_text.pack(side="left", fill="both", expand=True, padx=5)

                                arg_text.insert("1.0", arg_str)

                                # Store the text widget
                                function_widgets[-1]['args'].append(arg_text)
                        else:
                            # Handle non-list functions
                            func_frame = ctk.CTkFrame(scrollable_frame, fg_color=TkinterDialogStyles.FRAME_BG)
                            func_frame.pack(fill="x", padx=5, pady=5)
                            ctk.CTkLabel(func_frame, text=f"Function {func_idx + 1}: {func}",
                                         font=TkinterDialogStyles.LABEL_BOLD_FONT, text_color=TkinterDialogStyles.LABEL_FG).pack(anchor="w", padx=10, pady=(10, 5))
                            ctk.CTkLabel(func_frame, text="(No editable parameters)", font=AppFonts.SMALL, text_color=TkinterDialogStyles.LABEL_FG).pack(padx=10, pady=5)
                            function_widgets.append({
                                'name': str(func),
                                'args': []
                            })

                    def save_changes():
                        try:
                            new_functions = []

                            for func_widget in function_widgets:
                                func_name = func_widget['name']
                                func_args = []

                                # Get values from text widgets
                                for arg_text_widget in func_widget['args']:
                                    arg_value = arg_text_widget.get("1.0", "end").strip()

                                    # Try to parse as JSON for complex types
                                    try:
                                        parsed_value = json.loads(arg_value)
                                        func_args.append(parsed_value)
                                    except json.JSONDecodeError:
                                        # If not valid JSON, treat as string
                                        func_args.append(arg_value)

                                # Build function list
                                if func_args:
                                    new_functions.append([func_name] + func_args)
                                else:
                                    new_functions.append([func_name])

                            # Create updated plugin data (keep original name and metadata)
                            updated_data = {
                                'name': plugin_data.get('name', ''),
                                'metadata': plugin_data.get('metadata', ''),
                                'functions': new_functions
                            }

                            # Save the updated plugin
                            with open(plugin_path, 'wb') as f:
                                pickle.dump(updated_data, f)

                            showinfo("Success", f"Plugin '{plugin_name}' updated successfully!")
                            edit_window.destroy()

                        except Exception as e:
                            showerror("Error", f"Failed to save plugin: {e}")

                    # Buttons
                    button_frame = ctk.CTkFrame(edit_window, fg_color=TkinterDialogStyles.FRAME_BG)
                    button_frame.pack(pady=10)

                    save_btn = ctk.CTkButton(button_frame, text="Save Changes", command=save_changes, **ButtonStyles.DEFAULT)
                    save_btn.pack(side="left", padx=5)

                    cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=edit_window.destroy, **ButtonStyles.DEFAULT)
                    cancel_btn.pack(side="left", padx=5)
                    
                else:
                    showerror("Error", f"Plugin file not found: {plugin_path}")

            except Exception as e:
                showerror("Error", f"Failed to load plugin: {e}")
        else:
            showwarning("No Selection", "Please select a plugin to edit.")

    def on_add():
        file_path = filedialog.askopenfilename(filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            try:
                plugins_dir = ensure_plugins_dir()
                destination = plugins_dir / os.path.basename(file_path)
                # Use copy instead of rename to preserve original file
                shutil.copy2(file_path, destination)
                plugin_name = os.path.splitext(os.path.basename(file_path))[0]
                showinfo("Success", f"Plugin added: {plugin_name}")
                # Add to the listbox display
                listbox.insert('end', plugin_name)
            except Exception as e:
                showerror("Error", f"Failed to add plugin: {e}")

    def on_remove():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            plugin_name = listbox.get(index)
            # Look for a .pkl file with this name in the plugins directory
            plugins_dir = ensure_plugins_dir()
            plugin_path = plugins_dir / f"{plugin_name}.pkl"
            if plugin_path.exists():
                try:
                    plugin_path.unlink()
                    showinfo("Success", f"Plugin removed: {plugin_name}")
                    listbox.delete(index)
                except Exception as e:
                    showerror("Error", f"Failed to remove plugin: {e}")
            else:
                showerror("Error", f"Plugin file not found: {plugin_path}")

    def on_cancel():
        nonlocal selected_tuple
        selected_tuple = None
        root.quit()
        root.destroy()

    # Create the main window
    root = ctk.CTk()
    root.title("Manage Plugins")
    root.configure(fg_color=PanelStyles.PREVIEW.get("fg_color", TkinterDialogStyles.DIALOG_BG))

    # Create a label
    if tuple_list:
        label_text = "Select a plugin from the list:"
    else:
        label_text = "No plugins found. Use 'Add' to import a plugin:"
    label = ctk.CTkLabel(root, text=label_text, font=AppFonts.BODY, text_color=TkinterDialogStyles.LABEL_FG)
    label.pack(pady=10)

    # Create a listbox with the names (first item of each tuple)
    # Note: CTk doesn't have a native Listbox, using tkinter Listbox
    listbox_frame = ctk.CTkFrame(root)
    listbox_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # CTk-backed selectable list adapter
    class _CTkListAdapter:
        def __init__(self, parent, styles=None):
            self.container = ctk.CTkScrollableFrame(parent, fg_color="transparent")
            self._rows = []
            self._selected = None
            self.styles = styles or {}

        def pack(self, **kwargs):
            self.container.pack(**kwargs)

        def insert(self, index, text):
            row_frame = ctk.CTkFrame(self.container, fg_color=TkinterDialogStyles.FRAME_BG)
            lbl = ctk.CTkLabel(row_frame, text=text, anchor="w", text_color=TkinterDialogStyles.LABEL_FG, font=AppFonts.BODY)
            lbl.pack(fill='x', padx=4, pady=2)

            def on_click(event=None, idx=len(self._rows)):
                self.select(idx)

            lbl.bind("<Button-1>", on_click)
            row_frame.pack(fill='x')
            self._rows.append({'frame': row_frame, 'label': lbl, 'text': text})

        def delete(self, start, end=None):
            try:
                if isinstance(start, int) and (end is None):
                    if 0 <= start < len(self._rows):
                        row = self._rows.pop(start)
                        try:
                            row['frame'].destroy()
                        except Exception:
                            pass
                        if self._selected == start:
                            self._selected = None
                        elif isinstance(self._selected, int) and self._selected > start:
                            self._selected -= 1
                else:
                    for r in self._rows:
                        try:
                            r['frame'].destroy()
                        except Exception:
                            pass
                    self._rows = []
                    self._selected = None
            except Exception:
                for r in self._rows:
                    try:
                        r['frame'].destroy()
                    except Exception:
                        pass
                self._rows = []
                self._selected = None

        def curselection(self):
            return (self._selected,) if self._selected is not None else ()

        def get(self, index):
            try:
                return self._rows[index]['text']
            except Exception:
                return None

        def select(self, index):
            if self._selected is not None and 0 <= self._selected < len(self._rows):
                prev = self._rows[self._selected]
                prev['label'].configure(text_color=TkinterDialogStyles.LABEL_FG, fg_color="transparent")
            if 0 <= index < len(self._rows):
                self._selected = index
                cur = self._rows[index]
                cur['label'].configure(text_color=ListboxStyles.PLUGIN_LIST.get('selectforeground', 'white'), fg_color=ListboxStyles.PLUGIN_LIST.get('selectbackground', AppColors.BLUE))
            else:
                self._selected = None

    listbox = _CTkListAdapter(listbox_frame)
    listbox.pack(fill="both", expand=True)

    for item in tuple_list:
        listbox.insert('end', item[0])  # Insert just the name (first element)

    # Create buttons
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=10)

    edit_button = ctk.CTkButton(button_frame, text="Edit", command=on_edit, **ButtonStyles.DEFAULT)
    edit_button.grid(row=0, column=0, padx=5)

    add_button = ctk.CTkButton(button_frame, text="Import", command=on_add, **ButtonStyles.DEFAULT)
    add_button.grid(row=0, column=1, padx=5)

    remove_button = ctk.CTkButton(button_frame, text="Remove", command=on_remove, **ButtonStyles.DEFAULT)
    remove_button.grid(row=0, column=2, padx=5)

    close_button = ctk.CTkButton(button_frame, text="Close", command=on_cancel, **ButtonStyles.DEFAULT)
    close_button.grid(row=0, column=3, padx=5)

    # Run the GUI
    root.mainloop()

    if selected_tuple:
        print("This is from manage plugin view: " + str(selected_tuple[0]))
    return selected_tuple

# Example usage:
if __name__ == "__main__":
    # Sample data - list of tuples where first element is the name
    data = [
        ("Apple", "Fruit", "Red"),
        ("Banana", "Fruit", "Yellow"),
        ("Carrot", "Vegetable", "Orange"),
        ("Spinach", "Vegetable", "Green")
    ]

    selected = manage_plugin_view(data)
    print(f"You selected: {selected}")