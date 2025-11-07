import pandas as pd
from models.delta_calculation_model import delta_calculation_model


def test_delta_calculation_basic_and_output_update():
    df = pd.DataFrame([
        {"A": "5", "B": "3", "Output": "A,B"},
        {"A": "2", "B": "8", "Output": "A,B"},
    ])
    out = delta_calculation_model(df.copy(), "A", "B", 1)
    # delta column should be present
    assert "delta" in out.columns
    # Check that output cells had the lower-name removed when abs(delta) > threshold
    assert out.iloc[0]["Output"] in ("A", "A")
    assert out.iloc[1]["Output"] in ("B", "B")


def test_delta_missing_column_returns_tuple():
    df = pd.DataFrame({"A": [1]})
    res = delta_calculation_model(df, "A", "missing", 0)
    # When a column is missing the function returns (df, None)
    assert isinstance(res, tuple)
    assert res[1] is None
