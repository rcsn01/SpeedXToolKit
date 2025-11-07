import os
import sys
import pickle
from pathlib import Path

import importlib
import models.path_utils as pu
mp = importlib.import_module('models.pickle')


def test_get_resource_path_development(tmp_path, monkeypatch):
    # Ensure frozen is False and returned path is under project root
    monkeypatch.setattr(sys, 'frozen', False, raising=False)
    p = pu.get_resource_path('some/resource.txt')
    assert isinstance(p, Path)


def test_get_plugins_dir_and_ensure(tmp_path, monkeypatch):
    # Monkeypatch get_resource_path to return our temp plugins dir
    plugins = tmp_path / 'plugins'
    monkeypatch.setattr(pu, 'get_resource_path', lambda rel: plugins)
    # Ensure the function returns the path and that ensure_plugins_dir creates it
    path = pu.get_plugins_dir()
    assert path == plugins
    # remove if exists then call ensure
    if path.exists():
        for p in path.iterdir():
            p.unlink()
        path.rmdir()
    res = pu.ensure_plugins_dir()
    assert res.exists()


def test_essay_to_pickle_and_pickle_to_essay(tmp_path, monkeypatch):
    # Force plugins dir to our temp folder
    plugins = tmp_path / 'plugins'
    plugins.mkdir()
    # Make both ensure_plugins_dir and get_plugins_dir return our temp plugins dir
    monkeypatch.setattr(mp, 'ensure_plugins_dir', lambda: plugins)
    monkeypatch.setattr(mp, 'get_plugins_dir', lambda: plugins)

    store = {'name': 't1', 'metadata': {'x': 1}, 'functions': []}
    out = mp.essay_to_pickle(store.copy())
    assert out['name'] == 't1'
    # file exists
    f = plugins / 't1.pkl'
    assert f.exists()

    # Now test pickle_to_essay loads it
    loaded = mp.pickle_to_essay([])
    assert any(isinstance(item, dict) and item.get('name') == 't1' for item in loaded)


def test_essay_to_pickle_type_error():
    try:
        mp.essay_to_pickle('not a dict')
        assert False, 'TypeError expected'
    except TypeError:
        pass
