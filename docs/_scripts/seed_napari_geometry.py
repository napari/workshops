"""Seed napari's saved window geometry to a reproducible size

Running this script once before any notebook execution sets the default
window size for all notebooks — without any per-notebook code. This is the
project's equivalent of a Sphinx conf.py for controlling viewer dimensions.

The mechanism: napari persists window_settings to its YAML configuration file
on close.  On the next launch it reads them back via ``_set_window_settings``.
Usage:
    python docs/_scripts/seed_napari_geometry.py   # via pixi run _seed-geometry
"""

import os
import sys
from pathlib import Path

import napari
from napari.utils._base import _DEFAULT_CONFIG_PATH
from qtpy.QtCore import QSettings
from qtpy.QtWidgets import QApplication

WIDTH = 1200
HEIGHT = 680

app = QApplication.instance() or QApplication(sys.argv)

viewer = napari.Viewer(show=True)
viewer.window._qt_window.resize(WIDTH, HEIGHT)
# process events to ensure the resize is applied before we save the settings
app.processEvents()

viewer.close()

# Diagnostic: print the YAML settings path and verify window_size was saved.
# napari persists to a YAML file (not QSettings).  The print output shows up
# in CI build logs so we can confirm the seed step works.
settings_path = Path(
    os.getenv('NAPARI_CONFIG', _DEFAULT_CONFIG_PATH)
).expanduser()
if settings_path.exists():
    raw = settings_path.read_text()
    # YAML serializes lists as multi-line by default, so check both formats
    found = (
        f'window_size: [{WIDTH}, {HEIGHT}]' in raw
        or f'window_size:\n  - {WIDTH}\n  - {HEIGHT}' in raw
    )
    if found:
        print(f"seed_napari_geometry: YAML settings OK — {WIDTH}x{HEIGHT} at {settings_path}")
    else:
        print(f"seed_napari_geometry: WARNING — window_size not {WIDTH}x{HEIGHT}!")
        print(f"  file: {settings_path}")
        print(f"  content:\n{raw}")
        print(f"  saved_size: check YAML content above")
else:
    # If settings_path doesn't exist, _save_current_window_settings may have
    # written to a different path (e.g. platformdirs with environment_marker).
    # Fall back to scanning for the napari config directory.
    alt_paths = list(Path(settings_path.parents[1]).rglob('napari/settings.yaml'))
    alt_paths += list(Path.home().rglob('.config/napari/**/settings.yaml'))
    print(f"seed_napari_geometry: WARNING — expected YAML not at {settings_path}")
    print(f"  searched: {alt_paths}")
