import pandas as pd

from controllers import processing_controller as pc
from controllers import data_controller as dc_mod


def test_apply_plugin_replays_various_functions(monkeypatch):
    # Start with a dataframe with columns A,B,C
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]})

    # Monkeypatch model functions to return predictable transformations
    monkeypatch.setattr(pc, 'keep_column_model', lambda frame, cols: frame[[cols]] if cols in frame.columns else frame)
    monkeypatch.setattr(pc, 'drop_column_model', lambda frame, col: frame.drop(columns=[col]) if col in frame.columns else frame)
    monkeypatch.setattr(pc, 'rename_column_model', lambda frame, target, new: frame.rename(columns={target: new}) if target in frame.columns else frame)
    monkeypatch.setattr(pc, 'produce_output_model', lambda frame, v1: frame.assign(Output=frame[v1] if v1 in frame.columns else None))
    monkeypatch.setattr(pc, 'remove_empty_rows_model', lambda frame, col: frame.loc[frame[col].notna()] if col in frame.columns else frame)
    monkeypatch.setattr(pc, 'custom_code_model', lambda frame, code: frame.assign(X=1))
    monkeypatch.setattr(pc, 'pivot_table_model', lambda frame, t, n: frame)
    monkeypatch.setattr(pc, 'delta_calculation_model', lambda frame, v1, v2, d: frame)

    preset = {
        'name': 'p1',
        'metadata': None,
        'functions': [
            ['keep_column_model', 'A'],
            ['rename_column_model', 'A', 'A_renamed'],
            ['produce_output_model', 'A_renamed'],
            ['custom_code_model', "df['X']=1"],
        ]
    }

    new_df, store = pc.apply_plugin(df.copy(), preset)
    # After keep then rename, A_renamed should exist and Output created
    assert isinstance(new_df, pd.DataFrame)
    assert 'A_renamed' in new_df.columns or 'Output' in new_df.columns
    assert store['name'] == 'p1'


def test_apply_plugin_handles_exceptions_and_unmapped(monkeypatch):
    df = pd.DataFrame({'A': [1]})
    # A func that raises
    def bad(frame, *args):
        raise RuntimeError('fail')

    monkeypatch.setattr(pc, 'keep_column_model', lambda frame, cols: frame[[cols]])
    # Insert an unknown function name and a function that raises
    preset = {'name': 'bad', 'metadata': None, 'functions': [['unknown_model', 'X'], ['keep_column_model', 'A'], ['custom_code_model', 'code']]}

    # custom_code_model is patched to raise to test exception handling during replay
    monkeypatch.setattr(pc, 'custom_code_model', bad)

    new_df, store = pc.apply_plugin(df.copy(), preset)
    # Should have returned a DataFrame (replay continues past errors)
    assert isinstance(new_df, pd.DataFrame)


def test_data_controller_load_save_apply_transform(monkeypatch, tmp_path):
    controller = dc_mod.DataController()
    # import_files success
    sample = pd.DataFrame({'A': [1], 'B': [2]})
    # DataController imports processing functions into its module namespace,
    # so patch them on the data_controller module
    monkeypatch.setattr(dc_mod, 'import_files', lambda fp: (sample, ('m1', 'm2')))
    res = controller.load_file('f.csv')
    assert isinstance(res, pd.DataFrame)
    assert controller.store['metadata'] == ('m1', 'm2')

    # save() when df exists: patch save_file to return modified store
    monkeypatch.setattr(dc_mod, 'save_file', lambda df, essay, store, default_filename=None: {'saved': True})
    saved = controller.save()
    assert saved == {'saved': True}

    # apply_transform when df is None returns None
    controller2 = dc_mod.DataController()
    assert controller2.apply_transform(lambda d, s: (d, s)) is None

    # apply_transform when df present
    controller.df = sample.copy()
    def transform_func(d, s):
        return d.assign(Z=9), s
    out = controller.apply_transform(transform_func)
    assert 'Z' in controller.df.columns


def test_save_plugin_data_and_apply_plugin_preset(monkeypatch):
    controller = dc_mod.DataController()
    # No data -> save_plugin_data returns None
    assert controller.save_plugin_data() is None

    # With data, patch save_plugin and apply_plugin
    controller.df = pd.DataFrame({'A': [1]})
    monkeypatch.setattr(dc_mod, 'save_plugin', lambda store: {'name': 'p'})
    res = controller.save_plugin_data()
    assert res == {'name': 'p'}

    # apply_plugin_preset when df exists; patch apply_plugin
    monkeypatch.setattr(dc_mod, 'apply_plugin', lambda df, p: (df.assign(Y=2), {'name': 'applied'}))
    out = controller.apply_plugin_preset('p1')
    assert 'Y' in controller.df.columns
