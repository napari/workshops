# Contributing to the napari workshops

## Environment setup

## Environment setup

[Install pixi](https://pixi.sh/latest/#installation) (one command), then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
pixi run
```

> The pixi features are specified as `[dependency-groups]` in `pyproject.toml`.
> If you prefer using uv, run `uv sync --group dev` for the full set of deps.

## Common commands

```bash
pixi run docs-live                       # live preview server (dev env)
pixi run _docs-build                     # full site build (dev env)
```

## Docs Configuration

### Getting `nbscreenshot` to actual display screenshots.

At least in mystmd, `nbscreenshot()` needs to live in its own code cells.
If you put it in the same cell as other code, it will execute before the napari viewer window is fully initialized and not manager to capture an image. Additionally, closing viewers should be done it's own cell block. For example:

```{code-cell} python
:tags: [remove-cell]
import napari
from napari.utils import nbscreenshot

viewer = napari.Viewer()
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

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
first, which merges `napari-sphinx-theme`'s CSS with `docs/_resources/_custom.css`
to produce `docs/_resources/napari-theme.css`. This generated file is gitignored.
uv users need to run `uv run python docs/_scripts/copy_theme_css.py` once before building.

### Window management, sizing, and CI reproducibility

The `start` and `build` tasks also execute `docs/_scripts/seed_napari_geometry.py` to write a known window geometry to QSettings before launching notebooks. This ensures that all napari windows start with the same size, which is critical for reproducibility in CI. If you want to test different window sizes, modify the constants in that script.
