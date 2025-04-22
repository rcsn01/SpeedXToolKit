import pickle
import os
from pathlib import Path

def essay_to_pickle(name, essay):
    print(type(essay))
    
    # Combine name with essay content
    essay_data = (name,) + essay  # Ensure essay is converted to tuple if it isn't already
    
    # Create presets directory if it doesn't exist
    os.makedirs("presets", exist_ok=True)
    
    # Create filename (using the name with .pkl extension)
    filename = f"presets/{name}.pkl"
    
    # Save the data using pickle
    with open(filename, 'wb') as f:
        pickle.dump(essay_data, f)
    
    return(essay_data)

def pickle_to_essay(store):
    """
    Load all pickle files from the presets directory
    Returns a dictionary with {filename: loaded_object}
    """
    presets_dir="presets"
    presets_path = Path(presets_dir)
    
    # Check if directory exists
    if not presets_path.exists():
        print(f"Presets directory '{presets_dir}' not found!")
        return None
    
    # Process each .pkl file in directory
    for file in presets_path.glob("*.pkl"):
        try:
            with open(file, 'rb') as f:
                store.append(pickle.load(f))  # Use filename (without extension) as key
        except (pickle.PickleError, EOFError) as e:
            print(f"Error loading {file.name}: {e}")
        except Exception as e:
            print(f"Unexpected error with {file.name}: {e}")
    
    return store

