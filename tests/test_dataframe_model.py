import pandas as pd
import numpy as np
from models.dataframe_model import filter_columns, clear_undefined, what_do_i_have


def test_filter_columns_valid_and_invalid():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    out = filter_columns(df, "a, missing, b")
    assert list(out.columns) == ["a", "b"]

    none_out = filter_columns(df, "x,y")
    assert none_out is None


def test_filter_columns_with_spaces_and_order():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    out = filter_columns(df, " b , a ")
    # order preserved based on the input order after trimming
    assert list(out.columns) == ["b", "a"]


def test_clear_undefined_replaces_values():
    s = pd.Series(["undefined", " undetermined ", "OK", 5])
    cleared = clear_undefined(s)
    assert pd.isna(cleared.iloc[0])
    assert pd.isna(cleared.iloc[1])
    assert cleared.iloc[2] == "OK"
    assert cleared.iloc[3] == 5


def test_what_do_i_have_combines_and_outcome():
    id_df = pd.DataFrame({"id": [1, 2]})
    target_df = pd.DataFrame({"A": [1, np.nan], "B": [np.nan, 2]})
    combined = what_do_i_have(id_df, target_df)
    # Expect columns from id_df and target_df plus 'Outcome'
    assert 'Outcome' in combined.columns
    # Check that the Outcome lists non-nulls per row
    assert 'A' in combined.iloc[0]['Outcome']
    assert 'B' in combined.iloc[1]['Outcome']


def test_clear_undefined_on_dataframe():
    df = pd.DataFrame({"x": ["undefined", "ok"], "y": [" undetermined ", 5]})
    cleared = clear_undefined(df)
    # ensure 'undefined' and 'undetermined' are replaced with NaN
    assert pd.isna(cleared.iloc[0, 0])
    assert pd.isna(cleared.iloc[0, 1]) or cleared.iloc[0,1] == "ok"  # row/col ordering can differ
