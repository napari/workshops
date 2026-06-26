"""Seed napari's saved window geometry to a reproducible size

Running this script once before any notebook execution sets the default
window size for all notebooks — without any per-notebook code. This is the
project's equivalent of a Sphinx conf.py for controlling viewer dimensions.

The mechanism: napari persists window settings to its YAML configuration file
on close (``_save_current_window_settings``). On the next launch it reads
them back via ``_set_window_settings`` in ``Window.show()``.

Usage:
    python docs/_scripts/seed_napari_geometry.py   # via pixi run _seed-geometry
"""

import os
import sys
from pathlib import Path

import napari
from napari.utils._base import _DEFAULT_CONFIG_PATH
from qtpy.QtWidgets import QApplication

WIDTH = 1200
HEIGHT = 680

app = QApplication.instance() or QApplication(sys.argv)

viewer = napari.Viewer(show=True)
viewer.window._qt_window.resize(WIDTH, HEIGHT)
app.processEvents()

viewer.close()

# Diagnostic: verify window_size was saved to napari's YAML settings file.
# This prints to CI build logs for debugging screenshot sizing issues.
settings_path = Path(os.getenv('NAPARI_CONFIG', _DEFAULT_CONFIG_PATH)).expanduser()
if settings_path.exists():
    raw = settings_path.read_text()
    # YAML writes lists as multi-line by default
    if f'window_size:\n  - {WIDTH}\n  - {HEIGHT}' in raw:
        print(f'seed_napari_geometry: YAML settings OK — {WIDTH}x{HEIGHT} at {settings_path}')
    else:
        print(f'seed_napari_geometry: WARNING — unexpected window_size in {settings_path}')
        print(f'  content:\n{raw}')
else:
    print(f'seed_napari_geometry: WARNING — YAML not found at {settings_path}')
