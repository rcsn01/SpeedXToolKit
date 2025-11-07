import pandas as pd
from controllers import processing_controller as pc


def make_store():
    return {'functions': []}


def test_drop_rename_pivot_keep_produce_custom_cancel(monkeypatch):
    df = pd.DataFrame({'A': [1], 'B': [2]})
    store = make_store()

    # Each view returns falsy -> function should return (None, store) or None appropriately
    monkeypatch.setattr(pc, 'drop_column_view', lambda d: None)
    res = pc.drop_column(df.copy(), store.copy())
    assert res == (None, store)

    monkeypatch.setattr(pc, 'rename_column_view', lambda d: None)
    assert pc.rename_column(df.copy(), store.copy()) == (None, store)

    monkeypatch.setattr(pc, 'pivot_table_view', lambda d: None)
    assert pc.pivot_table(df.copy(), store.copy()) == (None, store)

    monkeypatch.setattr(pc, 'keep_column_view', lambda d: None)
    assert pc.keep_column(df.copy(), store.copy()) == (None, store)

    monkeypatch.setattr(pc, 'produce_output_view', lambda d: None)
    assert pc.produce_output(df.copy(), store.copy()) == (None, store)

    monkeypatch.setattr(pc, 'custom_code_view', lambda: None)
    assert pc.custom_code(df.copy(), store.copy()) == (None, store)


def test_remove_empty_rows_cancel(monkeypatch):
    df = pd.DataFrame({'A': [1]})
    store = make_store()
    monkeypatch.setattr(pc, 'remove_empty_rows_view', lambda d: None)
    assert pc.remove_empty_rows(df.copy(), store.copy()) == (None, store)


def test_delta_calculation_missing_output(monkeypatch):
    df = pd.DataFrame({'A': [1]})
    store = make_store()
    called = {'w': False}
    monkeypatch.setattr(pc.messagebox, 'showwarning', lambda *a, **k: called.update({'w': True}))
    out_df, out_store = pc.delta_calculation(df.copy(), store.copy())
    assert out_df.equals(df)
    assert called['w'] is True
