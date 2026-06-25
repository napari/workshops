# Contributing to the napari workshops

## Environment setup

[Install pixi](https://pixi.sh/latest/#installation) (one command), then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
pixi run
```

If you prefer using uv, run `uv sync --group dev` for the full set of deps.

### Pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) hooks to format and
lint code automatically prior to each commit. The hooks are configured in
`.pre-commit-config.yaml`.

We recommend using [`prek`](https://github.com/j178/prek), a fast drop-in
replacement for `pre-commit` written in Rust (included in the dev dependencies).
Register the git hooks with:

```bash
pixi run prek install
```

Upon committing, your code will be checked for common issues, Python files
will be linted and formatted via `ruff`, and the `pixi.lock` file will be
validated against `pyproject.toml` to ensure it's up to date.

You can run all hooks against the entire codebase at any time:

```bash
pixi run prek -a
```

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
| `pixi run -e extend jupyter-lab` | extend | Launch JupyterLab inside the `docs/extend/` directory |

For a complete list of available tasks, see `[tool.pixi.tasks]` and
`[tool.pixi.feature.*.tasks]` in `pyproject.toml`, or refer to the
[pixi tasks documentation](https://pixi.sh/latest/features/tasks/).

## Docs Configuration

### Getting `nbscreenshot` to actual display screenshots.

**Window size on CI.** The CI workflow (`pages.yml`) runs `seed_napari_geometry.py`
before building docs, which creates a napari viewer, resizes it to 1200×680, and
saves the size to napari's YAML settings. Subsequent notebooks inherit the size.

The CI virtual display (Xvfb) defaults to 1024×768, which clamps Qt `resize()`.
The workflow restarts Xvfb at 1920×1080 to accommodate the requested size.
If the screenshots are the wrong size on CI, check the `seed_napari_geometry`
step output in the build logs — it prints the actual saved `window_size`.

**Cell layout.** `nbscreenshot()` needs to live in its own code cells.
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

**MyST (Jupyter Book v2)** executes notebooks with the working directory set to
the **project root** (`docs/`), not the notebook's directory. However, **JupyterLab**
sets the kernel's working directory to the **notebook's own directory**
(e.g., `docs/extend/`).

This produces a cross-environment CWD mismatch when notebooks reference nearby
data files by relative path.

For example, with a notebook at `docs/extend/02_notebook.md` referencing
`extend/data/nuclei.tif`:
- In MyST (`pixi run docs-live` or `pixi run _docs-build`): CWD = `docs/`,
  so `Path('data')` resolves to `docs/data/` — **wrong**.
- In JupyterLab (`pixi run -e extend jupyter-lab`): CWD = `docs/extend/`,
  so `Path('data')` resolves to `docs/extend/data/` — **correct**.

> Note: This behavior is specific to MyST (Jupyter Book v2, `jupyter-book>=2`).
> The older Jupyter Book v1 set CWD to the notebook's directory.
> `pixi run docs-live` runs `jupyter-book start`, *not* JupyterLab.

#### Recommendation

Use a `next()` fallback at the top of any notebook that accesses data files.
Check the project-root-relative path first (for MyST), then the notebook-relative
path (for JupyterLab):

```python
from pathlib import Path

# CWD is docs/ in MyST, notebook dir in JupyterLab
# For a notebook at docs/extend/02_notebook.md loading docs/extend/data/*:
data_dir = next(p for p in [Path('extend/data'), Path('data')] if p.exists())
```

### CSS and napari-sphinx theme

The `docs-live` and `_docs-build` tasks automatically run `_copy-css`
first, which merges `napari-sphinx-theme`'s CSS with `docs/_resources/_custom.css`
to produce `docs/_resources/napari-theme.css`. This generated file is gitignored.
uv users need to run `uv run python docs/_scripts/copy_theme_css.py` once before building.

### Window management, sizing, and CI reproducibility

The `start` and `build` tasks also execute `docs/_scripts/seed_napari_geometry.py` to write a known window geometry to QSettings before launching notebooks. This ensures that all napari windows start with the same size, which is critical for reproducibility in CI. If you want to test different window sizes, modify the constants in that script.
