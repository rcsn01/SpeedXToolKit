import pandas as pd
from models.drop_column_model import drop_column_model


def test_drop_column_basic():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    out = drop_column_model(df, "b")
    assert "b" not in out.columns
    assert list(out.columns) == ["a", "c"]


def test_drop_column_no_valid_columns():
    df = pd.DataFrame({"a": [1]})
    out = drop_column_model(df, ["x", "y"])  # no valid columns
    # Should return original DataFrame unchanged
    assert out.equals(df)


def test_drop_column_with_comma_string():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    out = drop_column_model(df, " b , c ")
    assert list(out.columns) == ["a"]
