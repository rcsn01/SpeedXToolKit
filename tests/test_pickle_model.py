import os
import pickle as pkl
import importlib
mp = importlib.import_module('models.pickle')
from models.pickle import essay_to_pickle, pickle_to_essay


def test_essay_to_and_from_pickle(tmp_path, monkeypatch):
    # Monkeypatch ensure_plugins_dir and get_plugins_dir on the module object to use tmp_path
    monkeypatch.setattr(mp, 'ensure_plugins_dir', lambda: tmp_path)
    monkeypatch.setattr(mp, 'get_plugins_dir', lambda: tmp_path)

    store = {'name': 't1', 'metadata': {}, 'functions': []}
    res = essay_to_pickle(store)
    assert res['name'] == 't1'
    # Ensure file created
    files = list(tmp_path.glob('*.pkl'))
    assert len(files) == 1

    # Now test loading into empty collection
    collection = pickle_to_essay(None)
    assert isinstance(collection, list)
    assert any(isinstance(item, dict) and item.get('name') == 't1' for item in collection)


def test_pickle_handles_duplicate_and_bad_files(tmp_path, monkeypatch):
    mp = __import__('models.pickle', fromlist=['*'])
    monkeypatch.setattr(mp, 'ensure_plugins_dir', lambda: tmp_path)
    monkeypatch.setattr(mp, 'get_plugins_dir', lambda: tmp_path)

    # create a good pkl
    good = {'name': 'dup', 'metadata': {}, 'functions': []}
    with open(tmp_path / 'good.pkl', 'wb') as f:
        pkl.dump(good, f)
    # create a duplicate with same name
    with open(tmp_path / 'good2.pkl', 'wb') as f:
        pkl.dump(good, f)
    # create a corrupted file
    (tmp_path / 'bad.pkl').write_text('not a pickle')

    collection = pickle_to_essay([])
    # duplicates should be merged into a single entry by name
    names = [c.get('name') for c in collection if isinstance(c, dict)]
    assert 'dup' in names
