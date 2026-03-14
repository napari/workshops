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
uv run jupyter-book start
uv run jupyter-book build --html --execute --strict
```

> **Note on CSS:** The `start` and `build` tasks automatically run `copy-css`
> first, which merges `napari-sphinx-theme`'s CSS with `resources/_custom.css`
> to produce `resources/napari-theme.css`. This generated file is gitignored.
> uv users need to run `uv run python scripts/copy_theme_css.py` once before building.
