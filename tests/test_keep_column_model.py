import pandas as pd
import pytest
from models.keep_column_model import keep_column_model


def test_keep_column_single_string():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    out = keep_column_model(df, "a")
    assert list(out.columns) == ["a"]
    assert out.iloc[0]["a"] == 1


def test_keep_column_list_and_missing():
    df = pd.DataFrame({"a": [1], "b": [2]})
    out = keep_column_model(df, ["a", "missing"])
    # Only existing columns are selected
    assert list(out.columns) == ["a"]

    # If no requested columns exist, function raises ValueError
    with pytest.raises(ValueError, match="Column not detected"):
        keep_column_model(df, ["x", "y"])


def test_keep_column_comma_string():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    out = keep_column_model(df, " b, a ")
    assert list(out.columns) == ["b", "a"]
