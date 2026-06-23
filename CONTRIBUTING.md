# Contributing to the napari workshops

## Environment setup

[Install pixi](https://pixi.sh/latest/#installation) (one command), then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
pixi run
```

If you prefer using uv, run `uv sync --group dev` for the full set of deps.

## Project environments

This project uses [pixi](https://pixi.sh/latest/) for environment management,
with dependencies, tasks, and environments defined in `pyproject.toml`.

### How pixi environments are structured

Dependencies are organized into **dependency groups** in `[dependency-groups]`,
which pixi maps directly to **features**. Each feature can also define its own
[tasks](https://pixi.sh/latest/features/tasks/) and any dependency overrides. 
Features are then composed into named **environments** under `[tool.pixi.environments]`.

```text
[dependency-groups]  ──►  pixi features  ──►  [tool.pixi.environments]
   extend                                      default  (catch-all solve group)
   dev                                         extend   (extend feature)
                                                dev      (dev feature → includes extend)
```

- **`default`** — a catch-all solve group with no features. Skips installing
  workshop-specific dependencies for contributors who only need the base
  environment.
- **`extend`** — the "Extending napari" workshop environment. Run with
  `pixi run -e extend <task>`.
- **`dev`** — full development environment (includes everything in `extend`
  plus build tools like `jupyter-book`, `mystmd`, etc.).

> Environments **must** be explicitly listed under `[tool.pixi.environments]`
> to be usable. Pixi will not auto-create environments from dependency groups
> alone. See [pixi environments docs](https://pixi.sh/latest/features/environment/).

### Tasks

Tasks are defined per feature. Tasks prefixed with `_` are hidden from
`pixi run` (which lists all tasks across all environments), keeping the
output focused on user-facing commands. Use `pixi run -e <env>` to scope
the task list to a specific environment.

| Command | Environment | Description |
|---|---|---|
| `pixi run docs-live` | dev | Live preview server (starts jupyter-book with `--execute`) |
| `pixi run _docs-build` | dev | Full site build with notebook execution |
| `pixi run -e extend napari` | extend | Launch napari to verify the extend environment |
| `pixi run -e extend jupyter-lab` | extend | Launch JupyterLab inside the `docs/02-extend-napari/` directory |

For a complete list of available tasks, see `[tool.pixi.tasks]` and
`[tool.pixi.feature.*.tasks]` in `pyproject.toml`, or refer to the
[pixi tasks documentation](https://pixi.sh/latest/features/tasks/).

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
containing the notebook file** at execution time. A notebook in `docs/01-intro-napari/`
runs with `CWD = .../workshops/docs/01-intro-napari/`. However, when opening
notebooks directly in JupyterLab via `pixi run docs-live`, the
kernel starts from the **JupyterLab server root** (the repo root).

This produces a cross-environment CWD mismatch when notebooks reference data
files by relative path.

#### Recommendation

Use a robust fallback at the top of any notebook that accesses data files,
so the path resolves correctly regardless of CWD:

```python
from pathlib import Path

# Works whether CWD is the repo root or the notebooks/ subdirectory
data_dir = next(p for p in [Path('data'), Path('notebooks/data')] if p.exists())
```

### CSS and napari-sphinx theme

The `docs-live` and `_docs-build` tasks automatically run `_copy-css`
first, which merges `napari-sphinx-theme`'s CSS with `docs/_resources/_custom.css`
to produce `docs/_resources/napari-theme.css`. This generated file is gitignored.
uv users need to run `uv run python docs/_scripts/copy_theme_css.py` once before building.

### Window management, sizing, and CI reproducibility

The `start` and `build` tasks also execute `docs/_scripts/seed_napari_geometry.py` to write a known window geometry to QSettings before launching notebooks. This ensures that all napari windows start with the same size, which is critical for reproducibility in CI. If you want to test different window sizes, modify the constants in that script.
