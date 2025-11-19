import pandas as pd
import pytest
from models.custom_code_model import custom_code_model


def test_custom_code_transform_add_column():
    df = pd.DataFrame({"a": [1, 2]})
    code = "df['b'] = df['a'] * 2"
    out = custom_code_model(df, code)
    assert 'b' in out.columns
    assert out['b'].tolist() == [2, 4]


def test_custom_code_invalid_return():
    df = pd.DataFrame({"a": [1]})
    # code that doesn't set df to a DataFrame
    code = "x = 5"
    out = custom_code_model(df, code)
    # The function will fall back to the original df (globals contain a copy)
    assert out.equals(df)


def test_custom_code_forced_non_dataframe():
    df = pd.DataFrame({"a": [1]})
    # code that sets df to a non-DataFrame should trigger the ValueError branch
    code = "df = 5"
    with pytest.raises(ValueError, match="The code must result in 'df' being a pandas DataFrame"):
        custom_code_model(df, code)
