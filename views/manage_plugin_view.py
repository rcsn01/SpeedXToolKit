import tkinter as tk
from tkinter import ttk
import os
import shutil
import pickle
import json
from tkinter import filedialog, messagebox
from models.path_utils import *

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
                    edit_window = tk.Toplevel(root)
                    edit_window.title(f"Edit Plugin: {plugin_name}")
                    edit_window.geometry("900x600")
                    
                    # Plugin Name (read-only display)
                    name_frame = tk.Frame(edit_window)
                    name_frame.pack(fill="x", padx=10, pady=5)
                    tk.Label(name_frame, text="Plugin Name:", width=15, anchor="w", font=('TkDefaultFont', 9, 'bold')).pack(side="left")
                    tk.Label(name_frame, text=plugin_data.get('name', 'Unknown'), anchor="w").pack(side="left")
                    
                    # Metadata (read-only display)
                    metadata_frame = tk.Frame(edit_window)
                    metadata_frame.pack(fill="x", padx=10, pady=5)
                    tk.Label(metadata_frame, text="Metadata:", width=15, anchor="w", font=('TkDefaultFont', 9, 'bold')).pack(side="left")
                    tk.Label(metadata_frame, text=plugin_data.get('metadata', 'None'), anchor="w").pack(side="left")
                    
                    # Separator
                    ttk.Separator(edit_window, orient='horizontal').pack(fill='x', padx=10, pady=10)
                    
                    # Functions header
                    tk.Label(edit_window, text="Edit Function Parameters:", font=('TkDefaultFont', 10, 'bold')).pack(padx=10, pady=(5, 10), anchor="w")
                    
                    # Create scrollable frame for functions
                    canvas_frame = tk.Frame(edit_window)
                    canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)
                    
                    canvas = tk.Canvas(canvas_frame)
                    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
                    scrollable_frame = tk.Frame(canvas)
                    
                    scrollable_frame.bind(
                        "<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                    )
                    
                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)
                    
                    canvas.pack(side="left", fill="both", expand=True)
                    scrollbar.pack(side="right", fill="y")
                    
                    # Store text widgets for each argument
                    function_widgets = []
                    
                    # Parse and display each function
                    functions = plugin_data.get('functions', [])
                    for func_idx, func in enumerate(functions):
                        if isinstance(func, list) and func:
                            func_name = func[0] if len(func) > 0 else "unknown"
                            func_args = func[1:] if len(func) > 1 else []
                            
                            # Function container
                            func_frame = tk.LabelFrame(scrollable_frame, text=f"Function {func_idx + 1}: {func_name}", padx=10, pady=10)
                            func_frame.pack(fill="x", padx=5, pady=5)
                            
                            # Store function name
                            function_widgets.append({
                                'name': func_name,
                                'args': []
                            })
                            
                            # Display each argument
                            for arg_idx, arg in enumerate(func_args):
                                arg_frame = tk.Frame(func_frame)
                                arg_frame.pack(fill="x", pady=3)
                                
                                tk.Label(arg_frame, text=f"Argument {arg_idx + 1}:", width=12, anchor="w").pack(side="left")
                                
                                # Create text widget for the argument (supports multi-line)
                                arg_text = tk.Text(arg_frame, height=4, wrap="word")
                                arg_text.pack(side="left", fill="both", expand=True, padx=5)
                                
                                # Add scrollbar for text widget
                                arg_scrollbar = tk.Scrollbar(arg_frame, command=arg_text.yview)
                                arg_scrollbar.pack(side="right", fill="y")
                                arg_text.config(yscrollcommand=arg_scrollbar.set)
                                
                                # Insert the argument value (as JSON for complex types)
                                try:
                                    arg_str = json.dumps(arg, indent=2, ensure_ascii=False) if not isinstance(arg, str) else arg
                                except:
                                    arg_str = str(arg)
                                
                                arg_text.insert("1.0", arg_str)
                                
                                # Store the text widget
                                function_widgets[-1]['args'].append(arg_text)
                        else:
                            # Handle non-list functions
                            func_frame = tk.LabelFrame(scrollable_frame, text=f"Function {func_idx + 1}: {func}", padx=10, pady=10)
                            func_frame.pack(fill="x", padx=5, pady=5)
                            tk.Label(func_frame, text="(No editable parameters)", font=('TkDefaultFont', 8, 'italic')).pack()
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
                                    arg_value = arg_text_widget.get("1.0", tk.END).strip()
                                    
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
                            
                            messagebox.showinfo("Success", f"Plugin '{plugin_name}' updated successfully!")
                            edit_window.destroy()
                            
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to save plugin: {e}")
                    
                    # Buttons
                    button_frame = tk.Frame(edit_window)
                    button_frame.pack(pady=10)
                    
                    save_btn = ttk.Button(button_frame, text="Save Changes", command=save_changes)
                    save_btn.pack(side="left", padx=5)
                    
                    cancel_btn = ttk.Button(button_frame, text="Cancel", command=edit_window.destroy)
                    cancel_btn.pack(side="left", padx=5)
                    
                else:
                    messagebox.showerror("Error", f"Plugin file not found: {plugin_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load plugin: {e}")
        else:
            messagebox.showwarning("No Selection", "Please select a plugin to edit.")

    def on_add():
        file_path = filedialog.askopenfilename(filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            try:
                plugins_dir = ensure_plugins_dir()
                destination = plugins_dir / os.path.basename(file_path)
                # Use copy instead of rename to preserve original file
                shutil.copy2(file_path, destination)
                plugin_name = os.path.splitext(os.path.basename(file_path))[0]
                messagebox.showinfo("Success", f"Plugin added: {plugin_name}")
                # Add to the listbox display
                listbox.insert(tk.END, plugin_name)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add plugin: {e}")

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
                    messagebox.showinfo("Success", f"Plugin removed: {plugin_name}")
                    listbox.delete(index)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to remove plugin: {e}")
            else:
                messagebox.showerror("Error", f"Plugin file not found: {plugin_path}")

    def on_cancel():
        nonlocal selected_tuple
        selected_tuple = None
        root.quit()
        root.destroy()

    # Create the main window
    root = tk.Tk()
    root.title("Manage Plugins")

    # Create a label
    if tuple_list:
        label_text = "Select a plugin from the list:"
    else:
        label_text = "No plugins found. Use 'Add' to import a plugin:"
    label = ttk.Label(root, text=label_text)
    label.pack(pady=10)

    # Create a listbox with the names (first item of each tuple)
    listbox = tk.Listbox(root, width=40, height=10)
    for item in tuple_list:
        listbox.insert(tk.END, item[0])  # Insert just the name (first element)
    listbox.pack(pady=10, padx=10)

    # Create buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    edit_button = ttk.Button(button_frame, text="Edit", command=on_edit)
    edit_button.grid(row=0, column=0, padx=5)

    add_button = ttk.Button(button_frame, text="Import", command=on_add)
    add_button.grid(row=0, column=1, padx=5)

    remove_button = ttk.Button(button_frame, text="Remove", command=on_remove)
    remove_button.grid(row=0, column=2, padx=5)

    close_button = ttk.Button(button_frame, text="Close", command=on_cancel)
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