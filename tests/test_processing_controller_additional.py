import pandas as pd
import types

import controllers.processing_controller as pc


def test_import_files_load_failure(monkeypatch):
    # Simulate load_file_view failing to return a valid df/header
    monkeypatch.setattr(pc, 'load_file_view', lambda fp: (None, None, None))
    res = pc.import_files('dummy.csv')
    assert res is None


def test_import_files_processing_failed(monkeypatch):
    # Simulate load succeeds but essay_process_model returns (None, None)
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    monkeypatch.setattr(pc, 'load_file_view', lambda fp: (df, 0, ['A']))
    monkeypatch.setattr(pc, 'essay_process_model', lambda d, h: (None, None))
    res = pc.import_files('dummy.csv')
    assert res is None


def test_save_file_no_df(monkeypatch):
    store = {'functions': []}
    # Ensure save_dataframe is not called when df is None
    called = {'v': False}

    def fake_save_dataframe(df, default_filename=None):
        called['v'] = True

    monkeypatch.setattr(pc, 'save_dataframe', fake_save_dataframe)
    res_store = pc.save_file(None, None, store)
    assert res_store is store
    assert called['v'] is False


def test_save_plugin_cancel(monkeypatch):
    store = {'functions': []}
    monkeypatch.setattr(pc, 'save_plugin_view', lambda: '')
    res = pc.save_plugin(store.copy())
    assert res == store


def test_manage_plugin_calls_view(monkeypatch):
    called = {'data': None}
    # Make pickle_to_essay return a list with one preset dict
    monkeypatch.setattr(pc, 'pickle_to_essay', lambda lst: [{'name': 'p1', 'metadata': {}, 'functions': []}])

    def fake_manage_plugin_view(selection_data):
        called['data'] = selection_data

    monkeypatch.setattr(pc, 'manage_plugin_view', fake_manage_plugin_view)
    pc.manage_plugin()
    assert called['data'] is not None
    assert isinstance(called['data'], list)


def test_apply_plugin_with_dict(monkeypatch):
    # Build a small df
    df = pd.DataFrame({'X': [1, 2], 'Y': [3, 4]})
    preset = {'name': 'p1', 'metadata': {'m': 1}, 'functions': []}
    monkeypatch.setattr(pc, 'pickle_to_essay', lambda lst: [preset])
    new_df, store = pc.apply_plugin(df, preset)
    # Applying a preset with no functions should return the original df and store reflecting preset
    assert isinstance(new_df, pd.DataFrame)
    assert store['name'] == 'p1'
    assert store['functions'] == []


def test_df_to_tuple_and_find_essay():
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    t = pc.df_to_tuple(df)
    assert isinstance(t, tuple) and len(t) == 2
    # find_essay: create store list where essays[2] equals essay[1]
    essay = (('a',), ('b',))
    store = [[None, None, essay[1]], ['x', 'y', 'zzz']]
    found = pc.find_essay(essay, store)
    assert found == store[0]
