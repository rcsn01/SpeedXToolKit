import tkinter as tk
from tkinter import ttk

def load_preset_view(tuple_list):
    """Display a GUI to select one tuple from a list of tuples."""
    selected_tuple = None  # This will store the user's selection
    
    def on_select():
        nonlocal selected_tuple
        # Get the selected index
        selection = listbox.curselection()
        if selection:  # If something is selected
            index = selection[0]
            selected_tuple = tuple_list[index]
            root.quit()
            root.destroy()  # Close the window
    
    # Create the main window
    root = tk.Tk()
    root.title("Select an Item")
    
    # Create a label
    label = ttk.Label(root, text="Select an item from the list:")
    label.pack(pady=10)
    
    # Create a listbox with the names (first item of each tuple)
    listbox = tk.Listbox(root, width=40, height=10)
    for item in tuple_list:
        listbox.insert(tk.END, item[0])  # Insert just the name (first element)
    listbox.pack(pady=10, padx=10)
    
    # Create a select button
    select_button = ttk.Button(root, text="Select", command=on_select)
    select_button.pack(pady=10)
    
    # Run the GUI
    root.mainloop()
    
    
    print(selected_tuple[0])
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
    
    selected = load_preset_view(data)
    print(f"You selected: {selected}")