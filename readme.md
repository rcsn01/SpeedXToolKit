# Universal Data Processor (SpeedXToolKit)
## Installation
```
python -m venv .venv
```
### Windows
```
.\.venv\Scripts\Activate.ps1
```
### macOS/Linux
```
source .venv/bin/activate
```
pip install -r requirements.txt

## Running
```
python main.py
```

## Building Executable (PyInstaller)
Example spec/command (adjust name):
```
pyinstaller --onefile --windowed --add-data "assets;assets" --name Pearl-3.6 --icon=assets/pearl.ico main.py
```
Recommended additions:
- Hidden imports if wildcard imports confuse analysis:
  hiddenimports=[
    'views.load_file_view','views.combine_file_view','views.delta_calculation_view',
    'views.keep_column_view','views.drop_column_view','views.produce_output_view','views.pivot_table_view',
    'models.delta_calculation_model','models.pivot_table_model'
  ]
- Add data (if distributing presets): datas=[('presets','presets')]


## Store Structure
```
store = {
  'name': <preset name>,
  'metadata': <essay_info tuple or None>,
  'functions': [list of encoded transformations]
}
```

## License
(Add desired license statement.)


