import pandas as pd
import os
from controllers import save_controller as sc


def test_save_dataframe_cancel(monkeypatch):
    df = pd.DataFrame({"a": [1]})
    # simulate user cancel
    monkeypatch.setattr(sc.filedialog, 'asksaveasfilename', lambda **k: '')
    assert sc.save_dataframe(df) is None


def test_save_dataframe_success(tmp_path, monkeypatch):
    df = pd.DataFrame({"a": [1]})
    out_file = tmp_path / 'out.csv'
    # simulate user selecting a file path
    monkeypatch.setattr(sc.filedialog, 'asksaveasfilename', lambda **k: str(out_file))
    res = sc.save_dataframe(df, default_filename='def.csv')
    assert res is True
    assert out_file.exists()


def test_save_dataframe_no_data():
    assert sc.save_dataframe(None) is None
