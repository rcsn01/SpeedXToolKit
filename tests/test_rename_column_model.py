import pandas as pd
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

    # conflict when new name exists should return None
    conflict = rename_column_model(df, "a", "b")
    assert conflict is None


def test_rename_column_invalid_df():
    # non-dataframe passed should return None
    res = rename_column_model(None, "a", "b")
    assert res is None
