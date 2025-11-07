import sys
from pathlib import Path
import tempfile
import models.path_utils as pu


def test_get_resource_path_development(monkeypatch, tmp_path):
    # Monkeypatch __file__ base to simulate project layout
    # Ensure get_resource_path returns path under project root
    rp = pu.get_resource_path("assets/test.txt")
    assert isinstance(rp, Path)
    assert rp.name == "test.txt"


def test_ensure_plugins_dir_uses_custom_base(monkeypatch, tmp_path):
    # Force get_resource_path to return our tmp_path/plugins
    monkeypatch.setattr(pu, 'get_resource_path', lambda rel: tmp_path / rel)
    plugins_path = pu.ensure_plugins_dir()
    assert plugins_path.exists()
    assert plugins_path.name == 'plugins'


def test_get_resource_path_frozen(monkeypatch, tmp_path):
    # Simulate PyInstaller frozen exe where external resource exists
    monkeypatch.setattr(pu.sys, 'frozen', True)
    fake_exe = tmp_path / 'app.exe'
    fake_exe.write_text('')
    monkeypatch.setattr(pu.sys, 'executable', str(fake_exe))
    # create an external resource next to exe
    external = fake_exe.parent / 'assets' / 'f.txt'
    external.parent.mkdir(parents=True, exist_ok=True)
    external.write_text('ok')
    res = pu.get_resource_path('assets/f.txt')
    assert res.exists()
    assert res == external

def test_get_plugins_dir_frozen(monkeypatch, tmp_path):
    monkeypatch.setattr(pu.sys, 'frozen', True)
    fake_exe = tmp_path / 'app.exe'
    fake_exe.write_text('')
    monkeypatch.setattr(pu.sys, 'executable', str(fake_exe))
    # If external plugins dir doesn't exist, get_plugins_dir should fall back
    res = pu.get_plugins_dir()
    assert isinstance(res, Path)
