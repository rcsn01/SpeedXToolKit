import sys
import types
import pandas as pd

# Create a lightweight dummy `views` module to prevent importing GUI code during tests
dummy_views = types.ModuleType('views')
for name in [
    'drop_column_view', 'rename_column_view', 'pivot_table_view', 'delta_calculation_view',
    'produce_output_view', 'keep_column_view', 'custom_code_view', 'remove_empty_rows_view',
    'load_file_view', 'combine_file_view', 'manage_plugin_view', 'save_plugin_view'
]:
    setattr(dummy_views, name, lambda *a, **k: None)

sys.modules['views'] = dummy_views

from controllers.data_controller import DataController
from controllers import processing_controller as pc


def test_data_controller_load_save_apply(monkeypatch):
    dc = DataController()
    # monkeypatch import_files to return a df and essay info
    sample = pd.DataFrame({'A': [1]})
    monk = monkeypatch
    # patch the name imported into data_controller so load_file uses our stub
    monk.setattr('controllers.data_controller.import_files', lambda p: (sample, ('meta',)))
    res = dc.load_file('path.csv')
    assert isinstance(dc.df, pd.DataFrame)
    assert dc.store['metadata'] is not None

    # save when df present: monkeypatch save_file
    # patch save_file on the data_controller import as well
    monk.setattr('controllers.data_controller.save_file', lambda df, essay, store, default_filename=None: {'name': 's'})
    dc.current_essay = {'x': 1}
    out = dc.save()
    assert out == {'name': 's'}

    # apply_transform: function that modifies df
    def transformer(df, store):
        df2 = df.copy()
        df2['B'] = 1
        store['functions'].append(['tx'])
        return df2, store

    # ensure store has functions list expected by transformer
    dc.store = {'functions': []}
    res = dc.apply_transform(transformer)
    assert 'B' in dc.df.columns

    # combine_files: monkeypatch combined_file imported into data_controller
    monk.setattr('controllers.data_controller.combined_file', lambda: sample)
    combined = dc.combine_files()
    assert isinstance(combined, pd.DataFrame)

    # save_plugin_data with no df should return None
    dc_empty = DataController()
    assert dc_empty.save_plugin_data() is None

    # manage_plugins calls manage_plugin
    monk.setattr('controllers.data_controller.manage_plugin', lambda: 'ok')
    assert dc.manage_plugins() == 'ok'

    # apply_plugin_preset with no df returns None
    assert dc_empty.apply_plugin_preset('p') is None

    # has_data / get_dataframe
    assert dc.has_data() is True
    assert isinstance(dc.get_dataframe(), pd.DataFrame)
