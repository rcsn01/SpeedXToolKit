import sys
import pathlib
import pytest

# Ensure the project root is on sys.path so tests can import top-level packages like `models`.
_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


@pytest.fixture(autouse=True)
def patch_messageboxes(monkeypatch):
    """Replace messagebox handlers in model modules with no-ops to avoid GUI popups during tests."""
    module_names = [
        "models.remove_emtpy_rows_model",
        "models.keep_column_model",
        "models.rename_column_model",
        "models.drop_column_model",
        "models.delta_calculation_model",
        "models.pivot_table_model",
        "models.custom_code_model",
        "models.produce_output_model",
        "models.pickle",
        "models.dataframe_model",
        "models.essay_process_model",
        "models.path_utils",
    ]
    for name in module_names:
        try:
            mod = __import__(name, fromlist=["*"])
            if hasattr(mod, "messagebox"):
                try:
                    monkeypatch.setattr(mod.messagebox, "showerror", lambda *a, **k: None)
                except Exception:
                    pass
                try:
                    monkeypatch.setattr(mod.messagebox, "showinfo", lambda *a, **k: None)
                except Exception:
                    pass
        except Exception:
            # If a module isn't importable (not present), skip it silently
            pass
    yield
