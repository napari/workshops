"""Merge napari-sphinx-theme CSS variables with custom mystmd overrides.

Run via: python scripts/copy_theme_css.py
Called automatically by: pixi run copy-css (as a dependency of build/start).

Output: resources/napari-theme.css  (gitignored, regenerated each build)
Source: resources/_custom.css       (maintained in version control)
"""

import pathlib

import napari_sphinx_theme

pkg = pathlib.Path(napari_sphinx_theme.__file__).parent
theme_css_path = pkg / "static" / "css" / "napari-sphinx-theme.css"

if not theme_css_path.exists():
    raise FileNotFoundError(f"napari-sphinx-theme CSS not found: {theme_css_path}")

theme_css = theme_css_path.read_text(encoding="utf-8")
custom_css = pathlib.Path("resources/_custom.css").read_text(encoding="utf-8")

output = (
    "/* napari brand colors — auto-generated from napari-sphinx-theme.\n"
    " * DO NOT EDIT: regenerate with `pixi run copy-css`. */\n\n"
    + theme_css
    + "\n\n/* Custom overrides for the mystmd book-theme */\n\n"
    + custom_css
)

out_path = pathlib.Path("resources/napari-theme.css")
out_path.write_text(output, encoding="utf-8")
print(f"Generated {out_path} ({out_path.stat().st_size} bytes)")
