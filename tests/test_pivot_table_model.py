import pandas as pd
from models.pivot_table_model import pivot_table_model


def test_pivot_table_basic():
    df = pd.DataFrame([
        {"id": 1, "category": "X", "value": "10"},
        {"id": 1, "category": "Y", "value": "20"},
        {"id": 2, "category": "X", "value": "5"},
    ])
    out = pivot_table_model(df, target="category", value="value")
    # Expect pivoted columns for categories X and Y plus index column 'id'
    assert "X" in out.columns or "Y" in out.columns
    assert "id" in out.columns


def test_pivot_table_invalid_non_numeric():
    df = pd.DataFrame([
        {"id": 1, "category": "X", "value": "10"},
        {"id": 1, "category": "Y", "value": "bad"},
    ])
    # When non-numeric values that are not missing-like are present, the
    # function returns the original DataFrame (and shows an error).
    out = pivot_table_model(df, target="category", value="value")
    # Because 'bad' is non-numeric and not missing, expect original df returned
    assert list(out.columns) == list(df.columns)


def test_pivot_table_missing_value_column_returns_original():
    df = pd.DataFrame([{"id": 1, "category": "X", "val": "10"}])
    out = pivot_table_model(df, target="category", value="value")
    assert list(out.columns) == list(df.columns)
