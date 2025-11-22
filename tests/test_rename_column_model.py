import pandas as pd
import pytest
from models.rename_column_model import rename_column_model


def test_rename_column_success():
    df = pd.DataFrame({"old": [1, 2]})
    out = rename_column_model(df, "old", "new")
    assert out is not None
    assert "new" in out.columns
    assert "old" not in out.columns


def test_rename_column_noop_and_conflict():
    df = pd.DataFrame({"a": [1], "b": [2]})
    # no-op when names are equal
    out = rename_column_model(df, "a", "a")
    assert out.equals(df)

    # conflict when new name exists should raise ValueError
    with pytest.raises(ValueError, match="already exists"):
        rename_column_model(df, "a", "b")


def test_rename_column_invalid_df():
    # non-dataframe passed should raise ValueError
    with pytest.raises(ValueError, match="Invalid DataFrame provided"):
        rename_column_model(None, "a", "b")
