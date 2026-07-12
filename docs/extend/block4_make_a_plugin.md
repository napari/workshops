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

**Goal:** Package the interactive spot detection widget from Block 3 into a
pip-installable napari plugin, then install and test it.

The primary steps in making a napari plugin are:

1. **Choose** which manifest contribution(s) your plugin requires
2. **Create** your repository using the [napari-plugin-template](https://github.com/napari/napari-plugin-template)
3. **Implement** your contributions
4. **Share** your plugin with the community

A functional napari plugin only needs **4 files** to be shared:
`napari.yaml`, some Python module, `pyproject.toml`, and `README.md`. The
napari-plugin-template generates all of these — plus testing, CI, and
documentation scaffolding — so you can focus on the code.

## 1. What is a napari plugin? (5 min)

A napari plugin is a Python package that declares **contributions** in a
`napari.yaml` manifest file. napari reads this manifest to discover what your
plugin provides without importing your code at startup. The manifest itself
is registered as an **entry point** in `pyproject.toml`.
To learn about the minimal requirements of a napari plugin, you can read through
the [Your first plugin tutorial](https://napari.org/stable/plugins/building_a_plugin/first_plugin.html).
However, for this workshop we will use the [napari-plugin-template](https://github.com/napari/napari-plugin-template).

napari plugins can be found on [napari-hub.org](https://napari-hub.org).
The hub is automatically updated when a plugin is published to [PyPI](https://pypi.org/),
though many plugins are also available on [conda-forge](https://conda-forge.org/).
While we won't deploy our plugin in this workshop, you can learn more by
reading the [plugin deploy instructions](https://napari.org/dev/plugins/building_a_plugin/index.html#[plugin-test-deploy])

### Contribution types

A contribution is a construct in `napari.yaml` (the manifest file), that napari
uses for each specific type of plugin. Each contribution conforms to a function
signature, i.e. the function linked to the contribution defines what napari
provides to the plugin (e.g., data and parameters) and what the plugin returns
to napari. napari is then able to use the functions pointed to in `napari.yaml`
to carry out the plugin tasks. Please see the
[contributions guide](https://napari.org/dev/plugins/building_a_plugin/guides.html) for more details.
(And technical references for the
[manifest](https://napari.org/dev/plugins/technical_references/manifest.html) and
[contributions](https://napari.org/dev/plugins/technical_references/contributions.html).
Many plugins will declare multiple contributions to provide all of the desired
functionality.

| Type | What it enables |
|------|----------------|
| **Reader** | Open file formats napari doesn't know |
| **Writer** | Save layers to custom formats |
| **Widget** | Add GUI panels for analysis, measurement, etc. |
| **Sample data** | Provide built-in example datasets |
| **Theme** | Customize the viewer's appearance |

Today we'll make a **widget** plugin — the `detect_spots` function from
Block 3, packaged so anyone can install it and use it in napari.

## 2. Scaffolding with napari-plugin-template (15 min)

The [napari-plugin-template](https://github.com/napari/napari-plugin-template)
uses [Copier](https://copier.readthedocs.io/) to generate a complete plugin
project structure from a few prompts.

### Run the template

Open a terminal and navigate to where you want your plugin; the following commands
do not require the environments from this workshop, and are fully self-contained.
Then run the pixi command, replacing `<new-plugin-name>` with your desired plugin name
(e.g. `napari-spot-detector`):

```bash
pixi exec -w npe2 -w jinja2-time -w python=3.13 copier copy --trust https://github.com/napari/napari-plugin-template <new-plugin-name>
```

Alternatively, uv:

```bash
uvx -w jinja2-time -w npe2 -p 3.13 copier copy --trust https://github.com/napari/napari-plugin-template <new-plugin-name>
```

### Template prompts

You'll be asked a series of questions. When prompted for which plugins
to include, you only need to answer `Yes` to `Include widget plugin?`,
but you may be interested in exploring the other contributions as well.
To read more about the prompts, you can refer to the `napari-plugin-template`
[Prompts Reference](https://github.com/napari/napari-plugin-template/blob/main/PROMPTS.md)

| Prompt | Answer |
|--------|--------|
| `plugin_name` | `napari-spot-detector` |
| `display_name` | anything |
| `module_name` | `napari_spot_detector` |
| `short_description` | anything |
| project info | as appropriate |
| `include_reader_plugin` | optional |
| `include_writer_plugin` | optional |
| `include_sample_data_plugin` | optional |
| `include_widget_plugin` | **Yes** |
| Other defaults | Press Enter to accept |

After completing all of the questions, a directory will be created containing
your new napari plugin. You will be given instructions on how to upload the
initialized git repository to GitHub. By default, we will not be covering this
aspect in the tutorial, but please feel free to ask the teaching team if you
would like to give it a try.

### Structure and first steps

Now, we'll explore the generated project structure. An up-to-date reference
is available in the [napari-plugin-template README](https://github.com/napari/napari-plugin-template).

See below for explanations about some of the most notable files, but do not
hesitate to reach out to the teaching team if you have questions about any of
the other files.

- `.github/workflows/test_and_deploy.yml`: This is a
  [github actions](https://github.com/features/actions) workflow that will
  automatically run the tests and upload your plugin to pypi (thus making it
  available through the built-in napari plugin browser). Please ask the teaching
  team if you would like to learn how to set up your github repository to
  support this workflow.
- `pyproject.toml`: This file allows your plugin to be built as
  a package and installed by pip. The `napari-plugin-template` has set everything
  up in these files, so you are good to go!
- The `src/` folder contains all the Python code for your plugin.
- `src/napari_spot_detector/_widget.py`: This file contains example
  implementations for different widget contributions. This is where you will add
  your `detect_spots()` function.
- The `src/napari_spot_detector/napari.yaml` file declares commands and
  contributions for each example widget in the `_widget.py` file. Look at these
  carefully and match up which command & contribution belong to what Python code
  in the `_widget.py` file.

## 3. Understanding napari.yaml (10 min)

Open `src/napari_spot_detector/napari.yaml`. This is the **manifest** — the
heart of your plugin:

```yaml
name: napari-spot-detector
display_name: napari-spot-detector
contributions:
  commands:
    - id: napari-spot-detector.make_function_widget
      python_name: napari_spot_detector._widget:threshold_autogenerate_widget
      title: Make threshold widget
  widgets:
    - command: napari-spot-detector.make_function_widget
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
napari.manifest = "napari_spot_detector:napari.yaml"
```

```{tip}
When napari starts, it scans all installed packages for `napari.manifest`
entry points. This is how it discovers plugins without importing them.
```

Note that `src` doesn't appear in the path `napari_spot_detector:napari.yaml`, but
`napari.yaml` is definitely inside the `src/` folder. Python knows to look
there because `pyproject.toml` declares:

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

## 4. Implementing the widget (20 min)

Now let's add our spot detection logic. Open `src/napari_spot_detector/_widget.py`.

The template populates `_widget.py` with **four example widget approaches**:

1. **Autogenerated function** — a plain function with type annotations;
   napari uses magicgui to auto-generate GUI widgets from the annotations.
2. **`@magic_factory` decorator** — gives you control over individual widget
   parameters (slider ranges, step sizes, etc.) while keeping things simple.
3. **`magicgui.widgets.Container` subclass** — more flexibility while still
   using magicgui's type-annotation-based widget creation.
4. **`QWidget` subclass** — full control over layout, callbacks, and events.

We'll use **option 2 (`@magic_factory`)** — the sweet spot of control and
simplicity for our spot detection function.

### Step 1: Add imports

```python
import numpy as np
from scipy import ndimage as ndi
from skimage.feature import blob_log
from napari.types import ImageData, LayerDataTuple
```

### Step 2: Add the spot detection function

Add our `detect_spots` function from Block 3, switching from `@magicgui` to
`@magic_factory` so napari can call it from the manifest:

```python
@magic_factory(
    auto_call=True,
    high_pass_sigma={"widget_type": "FloatSlider", "min": 0, "max": 20},
    spot_threshold={"widget_type": "FloatSlider", "min": 0.01, "max": 1.0, "step": 0.01},
    blob_sigma={"widget_type": "FloatSlider", "min": 1, "max": 20},
)
def detect_spots(
    image: ImageData,
    high_pass_sigma: float = 2.0,
    spot_threshold: float = 0.1,
    blob_sigma: float = 5.0,
) -> LayerDataTuple:
    """Detect spots in an image using Laplacian of Gaussian.

    Parameters
    ----------
    image : np.ndarray
        The image in which to detect spots.
    high_pass_sigma : float
        Sigma for the background-suppressing high-pass filter.
    spot_threshold : float
        Relative threshold for spot detection (lower = more spots).
    blob_sigma : float
        Expected spot size — passed as max_sigma to the detector.
    """
    # Suppress background with gaussian high-pass
    low_pass = ndi.gaussian_filter(image, high_pass_sigma)
    filtered = (image - low_pass).clip(0)

    # Detect spots with Laplacian of Gaussian
    blobs = blob_log(
        filtered,
        max_sigma=blob_sigma,
        threshold=None,
        threshold_rel=spot_threshold,
    )

    # Convert to points: first two columns are y, x coordinates
    coords = blobs[:, :2]
    # Third column is the detected sigma — convert to diameters for sizing
    sizes = 2 * np.sqrt(2) * blobs[:, 2]

    return (coords, {"size": sizes, "face_color": "red"}, "Points")
```

```{tip}
The `@magic_factory` decorator is a mostly drop-in replacement for `@magicgui`,
except this one *does not return a widget instance immediately*. Instead, it
turns our function into a "widget factory function" that can be called to
*create a widget instance*. This can be more convenient in many cases, if you
are writing a library or package where someone else will be instantiating your
widget. One additional important—and useful—distinction is that
`@magic_factory` gains the `widget_init` keyword argument, which will be called
with the new widget each time the factory function is called.
For more details on the two `magicgui` decorators, see
[the magicgui documentation](https://pyapp-kit.github.io/magicgui/decorators/).
```

### Step 3: Update napari.yaml

Add a new command and widget entry for our function:

```yaml
contributions:
  commands:
    - id: napari-spot-detector.make_detect_spots_widget
      python_name: napari_spot_detector._widget:detect_spots
      title: Make spot detection widget
  widgets:
    - command: napari-spot-detector.make_detect_spots_widget
      display_name: Detect Spots
  menus:
    napari/layers/analyze:
      - command: napari-spot-detector.make_detect_spots_widget
```

```{note}
The `menus` section adds the widget to napari's **Layers > Analyze** menu,
making it easy for users to find.
```

## 5. Install and test (15 min)

### Install the plugin

A single command will get you started from the root of the plugin.
`uv run` will install the plugin in editable mode with the
`dev` dependency-group:

```bash
cd napari-spot-detector
uv run napari
```

For a more classical approach, you could personally create a virtual
environment, activate it, and install the plugin in editable mode with:

```bash
cd napari-spot-detector
uv venv -p 3.13
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

uv pip install -e . --group dev
```

The `-e` flag installs in **editable mode** — any changes you make to the
source code take effect immediately after restarting napari. To launch:

```bash
napari
```

### Test in napari

From the menu: **Plugins > napari-spot-detector > Detect Spots**

Or find it at: **Layers > Analyze > Detect Spots**

```{image} https://napari.org/stable/_images/plugin-widget.png
:width: 400px
:alt: napari viewer with plugin widget dock panel
```

### Test with pytest

The template already includes a test file. Run it with pytest:

```bash
cd napari-spot-detector
uv run pytest
```

```{tip}
See the `_tests/test_widget.py` file — it uses `napari`'s `make_test_viewer`
fixture to test widgets without opening a GUI window.
```

## 6. Publishing overview (5 min)

To share your plugin with the world:

### 1. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/napari-spot-detector.git
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

## Bonus exercises

Finished early? Here are some ways to extend your plugin:

- **Add the filtered image as an output** — modify `detect_spots()` to also
  return the high-pass filtered image as an Image layer in the `LayerDataTuple`.
- **Add sample data** — implement the
  [sample data contribution](https://napari.org/dev/plugins/building_a_plugin/guides.html#sample-data)
  so users can try your plugin with built-in example images.
- **Write more tests** — expand `_tests/test_widget.py` with additional
  test cases using `make_test_viewer`.
- **Add a reader** — if your work involves a custom file format, implement
  a [reader contribution](https://napari.org/dev/plugins/building_a_plugin/guides.html#reader).
- **Push to GitHub** — follow the instructions copier printed after
  scaffolding to push your repo and enable CI (also available in the napari-plugin-template
  [README](https://github.com/napari/napari-plugin-template/blob/main/README.md)).

## Recap

In this block you:

| Step | What you did |
|------|-------------|
| 1 | Learned about plugin contribution types |
| 2 | Scaffolded a plugin project with copier |
| 3 | Understood `napari.yaml` manifest structure |
| 4 | Added your spot detection function to `_widget.py` |
| 5 | Installed in editable mode and tested |
| 6 | Learned how to publish to PyPI and the napari hub |

## Want to contribute?

Have you enjoyed your experience using pixi or uv?
We'd love to update the napari-plugin-template to first class these tools!
