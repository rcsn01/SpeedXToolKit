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

import pickle
from pathlib import Path

def pickle_to_essay(store):
    """
    Load all pickle files from the presets directory, skipping tuples whose names are already in store.
    Returns the updated store list.
    """
    presets_dir = "presets"
    presets_path = Path(presets_dir)
    
    # Check if directory exists
    if not presets_path.exists():
        print(f"Presets directory '{presets_dir}' not found!")
        return store  # Return the original store if directory doesn't exist
    
    # Get set of existing names in store for quick lookup
    existing_names = {item[0] for item in store if isinstance(item, tuple) and len(item) > 0}
    
    # Process each .pkl file in directory
    for file in presets_path.glob("*.pkl"):
        try:
            with open(file, 'rb') as f:
                loaded_tuple = pickle.load(f)
                # Check if it's a tuple with at least one item and if the name is new
                if isinstance(loaded_tuple, tuple) and len(loaded_tuple) > 0 and loaded_tuple[0] not in existing_names:
                    store.append(loaded_tuple)
                    existing_names.add(loaded_tuple[0])  # Update the set with the new name
        except (pickle.PickleError, EOFError) as e:
            print(f"Error loading {file.name}: {e}")
        except Exception as e:
            print(f"Unexpected error with {file.name}: {e}")
    
    return store

