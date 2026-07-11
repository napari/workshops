---
label: extend-block4
title: "4. From Script to Plugin"
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Block 4: From Script to Plugin

**Goal:** Package the interactive segmentation workflow from Block 2 into a
pip-installable napari plugin, then install and test it.

## 1. What is a napari plugin? (5 min)

A napari plugin is a Python package that declares **contributions** in a
`napari.yaml` manifest file. napari reads this manifest to discover what your
plugin provides without importing your code at startup. The manifest itself
is registered as an **entry point** in `pyproject.toml`.

### Contribution types

| Type | What it enables |
|------|----------------|
| **Reader** | Open file formats napari doesn't know |
| **Writer** | Save layers to custom formats |
| **Widget** | Add GUI panels for analysis, measurement, etc. |
| **Sample data** | Provide built-in example datasets |
| **Theme** | Customize the viewer's appearance |

Today we'll make a **widget** plugin — the threshold-and-segment function from
Block 2, packaged so anyone can install it with `pip` and use it in napari.

## 2. Scaffolding with napari-plugin-template (15 min)

The [napari-plugin-template](https://github.com/napari/napari-plugin-template)
uses [Copier](https://copier.readthedocs.io/) to generate a complete plugin
project structure from a few prompts.

### Run the template

Open a terminal and navigate to where you want your plugin. Then run the
pixi command, replacing `<new-plugin-name>` with your desired plugin name
(e.g. `napari-segment`):

```bash
pixi run -e extend copier copy --trust https://github.com/napari/napari-plugin-template <new-plugin-name>
```

Alternatively, you could follow the instructions in the template's README to use uv:

```bash
uv tool run --with jinja2-time --with npe2 --python=3.13 copier copy --trust https://github.com/napari/napari-plugin-template <new-plugin-name>
```

### Template prompts

You'll be asked a series of questions. For this workshop, answer:

| Prompt | Answer |
|--------|--------|
| `module_name` | `napari_segment` |
| `display_name` | `napari-segment` |
| `short_description` | `A napari widget for interactive thresholding and segmentation` |
| `include_reader_plugin` | optional |
| `include_writer_plugin` | optional |
| `include_sample_data_plugin` | optional |
| `include_widget_plugin` | **Yes** |
| Other defaults | Press Enter to accept |

### Structure and first steps

Now, we'll explore the generated project structure. An up-to-date reference
is available in the [napari-plugin-template README](https://github.com/napari/napari-plugin-template).

## 3. Understanding napari.yaml (10 min)

Open `src/napari_segment/napari.yaml`. This is the **manifest** — the
heart of your plugin:

```yaml
name: napari-segment
display_name: napari-segment
contributions:
  commands:
    - id: napari-segment.make_func_widget
      python_name: napari_segment._widget:threshold_autogenerate_widget
      title: Make threshold widget
  widgets:
    - command: napari-segment.make_func_widget
      autogenerate: true
      display_name: Threshold
```

Key concepts:
- **`commands`** — declare which Python functions napari can call, with a
  unique `id` and the full Python path to the function
- **`widgets`** — register a command as a GUI widget; `autogenerate: true`
  tells napari to use magicgui to auto-generate the UI from type annotations

The `pyproject.toml` has an entry point that tells napari where to find the
manifest:

```toml
[project.entry-points."napari.manifest"]
napari.manifest = "napari_segment:napari.yaml"
```

```{tip}
When napari starts, it scans all installed packages for `napari.manifest`
entry points. This is how it discovers plugins without importing them.
```

## 4. Implementing the widget (20 min)

Now let's add our segmentation logic. Open `src/napari_segment/_widget.py`.

### Step 1: Add imports

```python
import numpy as np
from skimage import morphology
from napari.types import ImageData, LabelsData
```

### Step 2: Add the threshold function

Replace or complement the existing `threshold_autogenerate_widget` function
with our segmentation function from Block 2:

```python
def threshold_widget(
    image: ImageData,
    percentile: int = 50,
    min_hole: int = 60,
    min_obj: int = 50,
) -> LabelsData:
    """Interactive thresholding with morphological cleaning."""
    data_min = np.min(image)
    data_max = np.max(image)
    foreground = image > data_min + percentile / 100 * (data_max - data_min)

    cleaned = morphology.remove_small_holes(foreground, min_hole)
    cleaned = morphology.remove_small_objects(cleaned, min_size=min_obj)
    return cleaned
```

### Step 3: Update napari.yaml

Add a new command and widget entry for our function:

```yaml
commands:
  - id: napari-segment.make_func_widget
    python_name: napari_segment._widget:threshold_autogenerate_widget
    title: Make threshold widget
  - id: napari-segment.make_segment_widget
    python_name: napari_segment._widget:threshold_widget
    title: Make segmentation widget
widgets:
  - command: napari-segment.make_func_widget
    autogenerate: true
    display_name: Threshold
  - command: napari-segment.make_segment_widget
    autogenerate: true
    display_name: Segmentation
menus:
  napari/layers/segment:
    - command: napari-segment.make_segment_widget
```

```{note}
The `menus` section adds the widget to napari's **Layers > Segment** menu,
making it easy for users to find.
```

### Step 4: Update __init__.py

Open `src/napari_segment/__init__.py` and ensure it imports the widget
function so it's accessible:

```python
from ._widget import threshold_widget
```

## 5. Install and test (15 min)

### Install the plugin

```bash
cd napari-segment
pip install -e .

# Or with uv:
uv pip install -e .
```

The `-e` flag installs in **editable mode** — any changes you make to the
source code take effect immediately after restarting napari.

### Test in napari

Launch napari:

```bash
napari
```

From the menu: **Plugins > napari-segment > Segmentation**

Or find it at: **Layers > Segment > Make segmentation widget**

```{figure} https://napari.org/stable/_images/plugin-widget.png
:width: 400px

Your widget should appear as a dock panel in the viewer.
```

### Test with pytest

The template already includes a test file. Run it:

```bash
cd napari-segment
pytest
```

```{tip}
See the `_tests/test_widget.py` file — it uses `napari`'s `make_test_viewer`
fixture to test widgets without opening a GUI window.
```

## 6. Publishing overview (5 min)

To share your plugin with the world:

### 1. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/napari-segment.git
git push -u origin main
```

### 2. Publish to PyPI

The template includes a GitHub Actions workflow (`.github/workflows/test_and_deploy.yml`)
that automatically publishes to PyPI when you push a version tag. 
The actual version number of the published package is derived from git tags via
[setuptools_scm](https://github.com/pypa/setuptools_scm/).

```bash
git tag v0.1.0
git push --tags
```

Or **create a GitHub Release** with a new tag:
   - Go to [Releases](https://github.com/napari/napari-metadata/releases) →
     "Draft a new release".
   - Choose a tag matching the new version (e.g. `v0.4.0`).
   - Target `main`.
   - Click "Generate release notes" to auto-populate the changelog from merged
     PRs.

### 3. Appear on napari hub

Once published on PyPI, your plugin will automatically appear on
[napari-hub.org](https://napari-hub.org) after a short delay.

## Recap

In this block you:

| Step | What you did |
|------|-------------|
| 1 | Learned about plugin contribution types |
| 2 | Scaffolded a plugin project with copier |
| 3 | Understood `napari.yaml` manifest structure |
| 4 | Added your segmentation function to `_widget.py` |
| 5 | Installed in editable mode and tested |
| 6 | Learned how to publish to PyPI and the napari hub |
