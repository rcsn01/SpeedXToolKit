import pandas as pd
from controllers import processing_controller as pc


def make_df():
    return pd.DataFrame({"A": [1, 2], "B": [3, 4]})


def test_drop_rename_pivot_keep_produce_custom_remove(monkeypatch):
    df = make_df()
    store = {"functions": []}

    # drop_column
    monkeypatch.setattr(pc, 'drop_column_view', lambda d: (d, 'A'))
    out_df, out_store = pc.drop_column(df.copy(), store.copy())
    assert isinstance(out_df, pd.DataFrame)
    assert 'A' not in out_df.columns

    # rename_column
    monkeypatch.setattr(pc, 'rename_column_view', lambda d: (d, 'B', 'C'))
    out_df, out_store = pc.rename_column(df.copy(), store.copy())
    assert 'C' in out_df.columns

    # pivot_table (use simple pivot where index cols are created)
    monkeypatch.setattr(pc, 'pivot_table_view', lambda d: (d, 'A', 'val'))
    # create a dataframe matching expected structure
    pdf = pd.DataFrame([{'k': 1, 'A': 'X', 'val': '10'}, {'k': 1, 'A': 'Y', 'val': '20'}])
    out_df, out_store = pc.pivot_table(pdf, store.copy())
    assert isinstance(out_df, pd.DataFrame)

    # keep_column
    monkeypatch.setattr(pc, 'keep_column_view', lambda d: (d, 'B'))
    out_df, out_store = pc.keep_column(df.copy(), store.copy())
    assert list(out_df.columns) == ['B']

    # produce_output
    monkeypatch.setattr(pc, 'produce_output_view', lambda d: (d, 'A'))
    out_df, out_store = pc.produce_output(df.copy(), store.copy())
    assert 'Output' in out_df.columns

    # custom_code
    monkeypatch.setattr(pc, 'custom_code_view', lambda: {'code': "df['D']=1"})
    out_df, out_store = pc.custom_code(df.copy(), store.copy())
    assert 'D' in out_df.columns

    # remove_empty_rows
    monk = monkeypatch
    monk.setattr(pc, 'remove_empty_rows_view', lambda d: (d, 'A'))
    out = pc.remove_empty_rows(df.copy(), store.copy())
    # remove_empty_rows returns processed_df, store when successful
    assert isinstance(out, tuple)


def test_delta_and_import_and_save_plugin_and_apply(monkeypatch, tmp_path):
    # delta requires 'Output' column
    df = pd.DataFrame({'A': [1, 2], 'B': [2, 1], 'Output': ['A', 'B']})
    store = {'functions': []}
    monkeypatch.setattr(pc, 'delta_calculation_view', lambda d: (d, 'A', 'B', 0))
    out_df, out_store = pc.delta_calculation(df.copy(), store.copy())
    assert isinstance(out_df, pd.DataFrame)

    # import_files: monkeypatch load_file_view to return a small df and header_row
    sample = pd.DataFrame([['meta1', 'meta2'], ['H1', 'H2'], ['v1', 'v2']])
    monk = monkeypatch
    monk.setattr(pc, 'load_file_view', lambda path: (sample, 1, 'H1'))
    res = pc.import_files('somepath')
    assert res is None or isinstance(res, tuple)

    # save_plugin: monkeypatch save_plugin_view and essay_to_pickle
    monk.setattr(pc, 'save_plugin_view', lambda: 'preset1')
    monk.setattr(pc, 'essay_to_pickle', lambda s: {'name': 'preset1', 'metadata': None, 'functions': []})
    st = pc.save_plugin({'functions': []})
    assert st.get('name') == 'preset1'

    # show_plugins: monkeypatch pickle_to_essay
    monk.setattr(pc, 'pickle_to_essay', lambda c: [{'name': 'p1', 'metadata': None, 'functions': []}])
    assert pc.show_plugins() == [{'name': 'p1', 'metadata': None, 'functions': []}]

    # apply_plugin: create a preset that keeps only A
    presets = [{'name': 'p1', 'metadata': None, 'functions': [['keep_column_model', 'A']]}]
    monk.setattr(pc, 'pickle_to_essay', lambda c: presets)
    orig = pd.DataFrame({'A': [1], 'B': [2]})
    new_df, store = pc.apply_plugin(orig.copy(), 'p1')
    assert isinstance(new_df, pd.DataFrame)


def test_df_to_tuple_and_find_essay():
    df = pd.DataFrame({'c1': [1, 2], 'c2': [3, 4]})
    t = pc.df_to_tuple(df)
    assert isinstance(t, tuple) and len(t) == 2

    store = [(('a',), ('b',), 'meta')]
    # find_essay expects to find essays where essays[2] == essay[1]
    essay = (('x',), ('meta',))
    found = pc.find_essay(essay, store)
    assert found is None or isinstance(found, tuple)
