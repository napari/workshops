# Contributing to the napari workshops

## Environment setup

### Option A: pixi (recommended)

[Install pixi](https://pixi.sh/latest/#installation) (one command), then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
pixi install
```

This installs napari, jupyter-book, and all other dependencies from conda-forge + PyPI
into a managed environment. No `conda activate` or `pip install` needed.

### Option B: uv

[Install uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
uv sync --group dev
```

All dependencies are resolved from PyPI into `.venv/`.

## Build and serve

```bash
# pixi
pixi run start   # live-preview server (runs copy-css then jupyter-book start)
pixi run build   # full build with notebook execution (requires a display server)
pixi run clean   # remove _build/

# uv
uv run jupyter-book start --execute
uv run jupyter-book build --html --execute --strict
```

## Docs Configuration

### File Paths in Notebooks

#### The Problem

JupyterBook/MyST sets each kernel's working directory to the **directory
containing the notebook file** at execution time. A notebook in `notebooks/`
runs with `CWD = .../napari-jupyterbook/notebooks/`. However, when opening
notebooks directly in JupyterLab via `pixi run start`, the kernel starts from
the **JupyterLab server root** (the repo root).

This produces a cross-environment CWD mismatch:

| Environment | `Path().resolve()` | `Path('data').exists()` | `Path('notebooks/data').exists()` |
|---|---|---|---|
| `pixi run build` locally | repo root | ✗ | ✓ |
| `pixi run build` on CI | `notebooks/` | ✓ | ✗ |
| JupyterLab (`pixi run start`) | repo root | ✗ | ✓ |

Actual output from `notebooks/files.md` in `timmonko/napari-jupyterbook`, where `data/` is a sibling of `notebooks/`:

```
# Locally (pixi run start --execute or build)
Current working directory:  C:\Users\...\napari-jupyterbook
Does notebooks/data exist?  True
Does data exist?  False

# On CI (pixi run build)
Current working directory:  /home/runner/work/napari-jupyterbook/napari-jupyterbook/notebooks
Does notebooks/data exist?  False
Does data exist?  True
```

#### Recommendation

Use a robust fallback at the top of any notebook that accesses data files,
so the path resolves correctly regardless of CWD:

```python
from pathlib import Path

# Works whether CWD is the repo root or the notebooks/ subdirectory
data_dir = next(p for p in [Path('data'), Path('notebooks/data')] if p.exists())
```

### CSS and napari-sphinx theme

The `start` and `build` tasks automatically run `copy-css`
first, which merges `napari-sphinx-theme`'s CSS with `resources/_custom.css`
to produce `resources/napari-theme.css`. This generated file is gitignored.
uv users need to run `uv run python scripts/copy_theme_css.py` once before building.

### Window management, sizing, and CI reproducibility

The `start` and `build` tasks also execute `scripts/seed_napari_geometry.py` to write a known window geometry to QSettings before launching notebooks. This ensures that all napari windows start with the same size, which is critical for reproducibility in CI. If you want to test different window sizes, modify the constants in that script.
