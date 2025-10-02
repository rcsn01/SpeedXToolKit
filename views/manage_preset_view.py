import tkinter as tk
from tkinter import ttk
import os
import shutil
import pickle
from tkinter import filedialog, messagebox
from models.path_utils import ensure_presets_dir

def manage_preset_view(tuple_list):
    """Display a GUI to select one tuple from a list of tuples."""
    selected_tuple = None  # This will store the user's selection

    def on_view():
        # Get the selected index
        selection = listbox.curselection()
        if selection:  # If something is selected
            index = selection[0]
            preset_name = listbox.get(index)
            
            # Load and display preset contents
            try:
                presets_dir = ensure_presets_dir()
                preset_path = presets_dir / f"{preset_name}.pkl"
                
                if preset_path.exists():
                    with open(preset_path, 'rb') as f:
                        preset_data = pickle.load(f)
                    
                    # Create a new window to display preset contents
                    view_window = tk.Toplevel(root)
                    view_window.title(f"Preset Contents: {preset_name}")
                    view_window.geometry("600x400")
                    
                    # Create scrollable text widget
                    text_frame = tk.Frame(view_window)
                    text_frame.pack(fill="both", expand=True, padx=10, pady=10)
                    
                    scrollbar = tk.Scrollbar(text_frame)
                    scrollbar.pack(side="right", fill="y")
                    
                    text_widget = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set)
                    text_widget.pack(side="left", fill="both", expand=True)
                    scrollbar.config(command=text_widget.yview)
                    
                    # Format and display preset data
                    content = f"Preset Name: {preset_data.get('name', 'Unknown')}\n\n"
                    content += f"Metadata: {preset_data.get('metadata', 'None')}\n\n"
                    content += "Functions Applied:\n"
                    
                    functions = preset_data.get('functions', [])
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
                    messagebox.showerror("Error", f"Preset file not found: {preset_path}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load preset: {e}")
        else:
            messagebox.showwarning("No Selection", "Please select a preset to view.")

    def on_add():
        file_path = filedialog.askopenfilename(filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            try:
                presets_dir = ensure_presets_dir()
                destination = presets_dir / os.path.basename(file_path)
                # Use copy instead of rename to preserve original file
                shutil.copy2(file_path, destination)
                preset_name = os.path.splitext(os.path.basename(file_path))[0]
                messagebox.showinfo("Success", f"Preset added: {preset_name}")
                # Add to the listbox display
                listbox.insert(tk.END, preset_name)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add preset: {e}")

    def on_remove():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            preset_name = listbox.get(index)
            # Look for a .pkl file with this name in the presets directory
            presets_dir = ensure_presets_dir()
            preset_path = presets_dir / f"{preset_name}.pkl"
            if preset_path.exists():
                try:
                    preset_path.unlink()
                    messagebox.showinfo("Success", f"Preset removed: {preset_name}")
                    listbox.delete(index)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to remove preset: {e}")
            else:
                messagebox.showerror("Error", f"Preset file not found: {preset_path}")

    def on_cancel():
        nonlocal selected_tuple
        selected_tuple = None
        root.quit()
        root.destroy()

    # Create the main window
    root = tk.Tk()
    root.title("Manage Presets")

    # Create a label
    if tuple_list:
        label_text = "Select a preset from the list:"
    else:
        label_text = "No presets found. Use 'Add' to import a preset:"
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

    add_button = ttk.Button(button_frame, text="Add", command=on_add)
    add_button.grid(row=0, column=2, padx=5)

    remove_button = ttk.Button(button_frame, text="Remove", command=on_remove)
    remove_button.grid(row=0, column=3, padx=5)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_button.grid(row=0, column=4, padx=5)

    # Run the GUI
    root.mainloop()

    if selected_tuple:
        print("This is from manage preset view: " + str(selected_tuple[0]))
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
    
    selected = manage_preset_view(data)
    print(f"You selected: {selected}")