import pickle
import os
from pathlib import Path
from typing import List, Dict, Any

def essay_to_pickle(store: Dict[str, Any]):
    """Persist a single preset store dict {name, metadata, functions} to presets/<name>.pkl."""
    if not isinstance(store, dict):
        raise TypeError("store must be a dict with keys: name, metadata, functions")
    name = store.get('name')
    if not name:
        # Auto-generate a name if missing
        name = 'preset_' + str(len(store.get('functions', [])))
        store['name'] = name

    os.makedirs("presets", exist_ok=True)
    filename = f"presets/{name}.pkl"
    with open(filename, 'wb') as f:
        pickle.dump(store, f)
    return store

def pickle_to_essay(collection):
    """Load all dict-based presets from presets/*.pkl and merge into a collection.

    collection can be:
      - a list of preset dicts
      - a dict mapping preset name -> preset dict
      - None (treated as empty list)
    Returns the updated collection in the same structural type passed in.
    """
    presets_path = Path("presets")
    if not presets_path.exists():
        return collection

    # Normalize to working list
    input_was_dict = False
    if collection is None:
        working: List[Dict[str, Any]] = []
    elif isinstance(collection, dict):
        # Assume mapping name->preset
        input_was_dict = True
        working = list(collection.values())
    elif isinstance(collection, list):
        working = [c for c in collection if isinstance(c, dict)]
    else:
        working = []

    existing_names = {c.get('name') for c in working if isinstance(c, dict) and c.get('name')}

    for file in presets_path.glob('*.pkl'):
        try:
            with open(file, 'rb') as f:
                loaded = pickle.load(f)
            if isinstance(loaded, dict) and loaded.get('name') and loaded.get('name') not in existing_names:
                working.append(loaded)
                existing_names.add(loaded.get('name'))
        except (pickle.PickleError, EOFError) as e:
            print(f"Error loading {file.name}: {e}")
        except Exception as e:
            print(f"Unexpected error with {file.name}: {e}")

    if input_was_dict:
        return {item.get('name'): item for item in working if item.get('name')}
    return working

