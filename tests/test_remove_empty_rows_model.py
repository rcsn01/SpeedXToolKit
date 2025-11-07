import pandas as pd
from models.remove_emtpy_rows_model import remove_empty_rows_model


def test_remove_empty_rows_basic():
    df = pd.DataFrame({
        "col": [1, None, "", "   ", "x"]
    })
    out = remove_empty_rows_model(df, "col")
    # Expect rows with values 1 and 'x' to remain
    assert len(out) == 2
    assert out.iloc[0]["col"] == 1
    assert out.iloc[1]["col"] == "x"


def test_remove_empty_rows_no_column():
    df = pd.DataFrame({"a": [1, 2]})
    out = remove_empty_rows_model(df, "missing")
    # Should return original DataFrame unchanged
    assert out.equals(df)


def test_remove_empty_rows_invalid_input():
    # Passing None should go through error handling and return None
    out = remove_empty_rows_model(None, "col")
    assert out is None
