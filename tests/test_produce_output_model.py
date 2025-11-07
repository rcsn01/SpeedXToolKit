import pandas as pd
from models.produce_output_model import produce_output_model


def test_produce_output_basic():
    df = pd.DataFrame({"A": [1, 0, None], "B": [0, 2, 3]})
    out = produce_output_model(df.copy(), ["A", "B"]) 
    assert 'Output' in out.columns
    assert out.iloc[0]['Output'] == 'A'
    assert out.iloc[1]['Output'] == 'B'
    # third row has B non-null -> 'B'
    assert out.iloc[2]['Output'] == 'B'


def test_produce_output_with_string_input():
    df = pd.DataFrame({"A": [1], "B": [0]})
    out = produce_output_model(df.copy(), "A,B")
    assert out.iloc[0]['Output'] == 'A'


def test_produce_output_no_valid_columns_returns_original():
    df = pd.DataFrame({"A": [1]})
    out = produce_output_model(df.copy(), ["missing"]) 
    # returns original DataFrame if no valid columns
    assert out.equals(df)
