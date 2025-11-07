import pandas as pd
from models.essay_process_model import essay_process_model


def test_essay_process_invalid_inputs():
    assert essay_process_model(None, 0) == (None, None)
    assert essay_process_model(pd.DataFrame(), None) == (None, None)


def test_essay_process_header_and_dedup():
    # create DataFrame where first N rows are format, then header row, then data
    df = pd.DataFrame([
        ["meta1", "meta2"],
        ["HeaderA", "HeaderA"],
        ["val1", "val2"],
    ])
    format_df, header_df = essay_process_model(df, 1)
    # format_df should include rows before header_row (index 0)
    assert len(format_df) == 1
    # header_df should have columns deduped: 'HeaderA' and 'HeaderA (1)'
    assert 'HeaderA' in header_df.columns
    assert any('HeaderA' in c for c in header_df.columns)
