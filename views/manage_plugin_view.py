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

    def on_view():
        # Get the selected index
        selection = listbox.curselection()
        if selection:  # If something is selected
            index = selection[0]
            plugin_name = listbox.get(index)

            # Load and display plugin contents
            try:
                plugins_dir = ensure_plugins_dir()
                plugin_path = plugins_dir / f"{plugin_name}.pkl"

                if plugin_path.exists():
                    with open(plugin_path, 'rb') as f:
                        plugin_data = pickle.load(f)

                    # Create a new window to display plugin contents
                    view_window = tk.Toplevel(root)
                    view_window.title(f"Plugin Contents: {plugin_name}")
                    view_window.geometry("600x400")
                    
                    # Create scrollable text widget
                    text_frame = tk.Frame(view_window)
                    text_frame.pack(fill="both", expand=True, padx=10, pady=10)
                    
                    scrollbar = tk.Scrollbar(text_frame)
                    scrollbar.pack(side="right", fill="y")
                    
                    text_widget = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set)
                    text_widget.pack(side="left", fill="both", expand=True)
                    scrollbar.config(command=text_widget.yview)
                    # Format and display plugin data
                    content = f"Plugin Name: {plugin_data.get('name', 'Unknown')}\n\n"
                    content += f"Metadata: {plugin_data.get('metadata', 'None')}\n\n"
                    content += "Functions Applied:\n"

                    functions = plugin_data.get('functions', [])
                    if functions:
                        for i, func in enumerate(functions, 1):
                            if isinstance(func, list) and func:
                                func_name = func[0]
                                func_args = func[1:] if len(func) > 1 else []
                                content += f"  {i}. {func_name}({', '.join(map(str, func_args))})\n"
                            else:
                                content += f"  {i}. {func}\n"
                    else:
                        content += "  No functions recorded\n"
                    
                    text_widget.insert("1.0", content)
                    text_widget.config(state="disabled")  # Make read-only
                    
                    # Add close button
                    close_btn = ttk.Button(view_window, text="Close", command=view_window.destroy)
                    close_btn.pack(pady=10)
                    
                else:
                    messagebox.showerror("Error", f"Plugin file not found: {plugin_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load plugin: {e}")
        else:
            messagebox.showwarning("No Selection", "Please select a plugin to view.")

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
                    edit_window.geometry("700x500")
                    
                    # Plugin Name
                    name_frame = tk.Frame(edit_window)
                    name_frame.pack(fill="x", padx=10, pady=5)
                    tk.Label(name_frame, text="Plugin Name:", width=15, anchor="w").pack(side="left")
                    name_var = tk.StringVar(value=plugin_data.get('name', ''))
                    name_entry = ttk.Entry(name_frame, textvariable=name_var, width=50)
                    name_entry.pack(side="left", fill="x", expand=True)
                    
                    # Metadata
                    metadata_frame = tk.Frame(edit_window)
                    metadata_frame.pack(fill="x", padx=10, pady=5)
                    tk.Label(metadata_frame, text="Metadata:", width=15, anchor="w").pack(side="left")
                    metadata_var = tk.StringVar(value=plugin_data.get('metadata', ''))
                    metadata_entry = ttk.Entry(metadata_frame, textvariable=metadata_var, width=50)
                    metadata_entry.pack(side="left", fill="x", expand=True)
                    
                    # Functions list header with toggle button
                    header_frame = tk.Frame(edit_window)
                    header_frame.pack(fill="x", padx=10, pady=(10, 5))
                    
                    tk.Label(header_frame, text="Functions (JSON format - preserves all data types):").pack(side="left")
                    
                    # Toggle for viewing escape sequences
                    view_mode = tk.StringVar(value="json")  # "json" or "pretty"
                    
                    def toggle_view():
                        current_content = functions_text.get("1.0", tk.END).strip()
                        
                        if view_mode.get() == "json":
                            # Switch to pretty mode - convert \n to actual newlines
                            try:
                                # Parse as JSON first to validate
                                data = json.loads(current_content)
                                # Convert to pretty format with actual newlines
                                pretty_content = json.dumps(data, indent=2, ensure_ascii=False)
                                # Replace escape sequences with actual characters for display
                                pretty_content = pretty_content.encode().decode('unicode_escape')
                                
                                functions_text.delete("1.0", tk.END)
                                functions_text.insert("1.0", pretty_content)
                                view_mode.set("pretty")
                                toggle_btn.config(text="View: Pretty ↻ Switch to JSON")
                            except:
                                messagebox.showwarning("Warning", "Cannot switch view - invalid JSON format")
                        else:
                            # Switch back to JSON mode - convert actual newlines to \n
                            try:
                                # Encode to handle escape sequences properly
                                json_content = current_content.encode('unicode_escape').decode('ascii')
                                # Parse to validate and reformat
                                data = json.loads(json_content)
                                json_content = json.dumps(data, indent=2, ensure_ascii=False)
                                
                                functions_text.delete("1.0", tk.END)
                                functions_text.insert("1.0", json_content)
                                view_mode.set("json")
                                toggle_btn.config(text="View: JSON ↻ Switch to Pretty")
                            except Exception as e:
                                messagebox.showwarning("Warning", f"Cannot switch view: {e}")
                    
                    toggle_btn = ttk.Button(header_frame, text="View: JSON ↻ Switch to Pretty", command=toggle_view)
                    toggle_btn.pack(side="right", padx=5)
                    
                    # Functions list
                    text_frame = tk.Frame(edit_window)
                    text_frame.pack(fill="both", expand=True, padx=10, pady=5)
                    
                    scrollbar = tk.Scrollbar(text_frame)
                    scrollbar.pack(side="right", fill="y")
                    
                    functions_text = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set, height=15)
                    functions_text.pack(side="left", fill="both", expand=True)
                    scrollbar.config(command=functions_text.yview)
                    
                    # Populate functions text widget with JSON format
                    functions = plugin_data.get('functions', [])
                    try:
                        # Pretty print JSON with indentation for readability
                        # ensure_ascii=False preserves unicode and special characters
                        json_str = json.dumps(functions, indent=2, ensure_ascii=False)
                        functions_text.insert("1.0", json_str)
                    except Exception as e:
                        # Fallback to string representation if JSON fails
                        functions_text.insert("1.0", str(functions))
                    
                    def save_changes():
                        try:
                            # Parse functions from text widget as JSON
                            functions_content = functions_text.get("1.0", tk.END).strip()
                            new_functions = []
                            
                            if functions_content:
                                try:
                                    # Try to parse as JSON
                                    new_functions = json.loads(functions_content)
                                    
                                    # Validate that it's a list
                                    if not isinstance(new_functions, list):
                                        messagebox.showerror("Error", "Functions must be a JSON array (list). Example:\n[\n  [\"function_name\", \"arg1\", \"arg2\"],\n  [\"another_function\", {\"key\": \"value\"}]\n]")
                                        return
                                        
                                except json.JSONDecodeError as e:
                                    messagebox.showerror("Error", f"Invalid JSON format:\n{str(e)}\n\nPlease ensure your functions are in valid JSON format.")
                                    return
                            
                            # Create updated plugin data
                            updated_data = {
                                'name': name_var.get(),
                                'metadata': metadata_var.get(),
                                'functions': new_functions
                            }
                            
                            # Get new filename from the name field
                            new_plugin_name = name_var.get()
                            new_plugin_path = plugins_dir / f"{new_plugin_name}.pkl"
                            
                            # Save the updated plugin
                            with open(new_plugin_path, 'wb') as f:
                                pickle.dump(updated_data, f)
                            
                            # If name changed, delete old file and update listbox
                            if new_plugin_name != plugin_name:
                                plugin_path.unlink()
                                listbox.delete(index)
                                listbox.insert(index, new_plugin_name)
                            
                            messagebox.showinfo("Success", f"Plugin '{new_plugin_name}' updated successfully!")
                            edit_window.destroy()
                            
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to save plugin: {e}")
                    
                    # Buttons
                    button_frame = tk.Frame(edit_window)
                    button_frame.pack(pady=10)
                    
                    save_btn = ttk.Button(button_frame, text="Save", command=save_changes)
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

    view_button = ttk.Button(button_frame, text="View", command=on_view)
    view_button.grid(row=0, column=0, padx=5)

    edit_button = ttk.Button(button_frame, text="Edit", command=on_edit)
    edit_button.grid(row=0, column=1, padx=5)

    add_button = ttk.Button(button_frame, text="Import", command=on_add)
    add_button.grid(row=0, column=2, padx=5)

    remove_button = ttk.Button(button_frame, text="Remove", command=on_remove)
    remove_button.grid(row=0, column=3, padx=5)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_button.grid(row=0, column=4, padx=5)

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