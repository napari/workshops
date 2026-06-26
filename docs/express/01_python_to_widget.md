---
label: python-to-widget
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
downloads:
  - file: scripts/01_pure_python.py
    title: "Script 01 — Pure Python threshold"
  - file: scripts/02_magicgui.py
    title: "Script 02 — magicgui widget"
  - file: scripts/03_sliders.py
    title: "Script 03 — Annotated sliders"
---

# From Python to interactive napari widget

In this module, we start with a pure Python segmentation function and
progressively integrate it with napari using `magicgui` widgets and
customizable sliders. By the end, you will have an interactive thresholding
widget inside napari that updates in real time.

```{tip}
All standalone scripts for this module are available for download using the
download button above.
```

## 1. A pure Python threshold function

We begin with a pure Python function that takes a numpy array, applies a Gaussian
blur and a threshold, and returns a binary mask.

{button}`01_pure_python.py <./scripts/01_pure_python.py>`

```{code-cell} python
:lineno-start: 1

from skimage import data, filters
import napari
import numpy as np


def threshold(
    data: np.ndarray,
    sigma: float = 0.5,
    threshold: float = 0.3,
) -> np.ndarray:
    """Apply a gaussian filter and threshold to image data."""
    norm = (data - np.min(data)) / np.max(data)
    blur = filters.gaussian(norm, sigma=sigma)
    blobs = blur >= threshold
    return blobs
```

Let's test it outside napari first.

```{code-cell} python
image = data.cells3d()[30, 1]  # 2d slice
blobs = threshold(image, sigma=1, threshold=0.5)

print(f"Input shape: {image.shape}, Output shape: {blobs.shape}")
print(f"Number of foreground pixels: {blobs.sum()}")
```

This works, but every time we want to try different parameters we have to
re-run the function. Wouldn't it be nice to tweak `sigma` and `threshold`
interactively inside napari?

## 2. napari + magicgui — a widget from a function

napari has built-in support for
[magicgui](https://pyapp-kit.github.io/magicgui/), a library that
automatically generates GUIs from Python function type annotations.

Let's rewrite our function so it takes a napari `Image` layer instead of a raw
array, and returns `LayerDataTuple` — a format napari understands for creating
new layers.

{button}`02_magicgui.py <./scripts/02_magicgui.py>`

```{code-cell} python:
:lineno-start: 1
:emphasize-lines: 7,10,12-13,18-21

from skimage import data, filters
import napari
import numpy as np


def threshold(
    layer: napari.layers.Image,
    sigma: float = 0.5,
    threshold: float = 0.3,
) -> list[napari.types.LayerDataTuple]:
    """Apply a gaussian filter and threshold to a napari Image."""
    if not layer:
        return
    norm = (layer.data - np.min(layer.data)) / np.max(layer.data)
    blur = filters.gaussian(norm, sigma=sigma)
    blobs = blur >= threshold

    return [
        (blur, {'name': 'blur'}, 'image'),
        (blobs, {'name': 'blobs'}, 'image'),
    ]
```

Notice the changes:
- The first parameter is now `layer: napari.layers.Image` — magicgui will read
  the type annotation and create a dropdown to select an Image layer. 
- The return type `list[napari.types.LayerDataTuple]` tells magicgui to create
  new layers from the returned data.
- We had to add a `if not layer` guard, to prevent errors when no Image layer
  is present in the viewer.

Now let's launch napari and add this function as a dock widget.
```{code-cell} python
:tags: [remove-output]
viewer = napari.Viewer()
image = data.cells3d()[30, 1]  # 2d
image_layer = viewer.add_image(image)

viewer.window.add_function_widget(threshold)
```

You should see a widget panel with dropdowns for `layer`, and spin boxes
for `sigma` and `threshold`. Click **Run** to apply the function. Try different
values!

```{code-cell} python
:tags: [remove-input]
from napari.utils import nbscreenshot

viewer.window.dock_widgets['threshold']()
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

This is already more interactive than the pure function, but the controls are still
a bit clunky, and we have to press `Run` every time we change the parameters...

## 3. Annotated sliders with auto_call

Let's replace the spin boxes with sliders, and autorun the function every time the
parameters are changed. We use `typing.Annotated` to attach widget metadata to each
parameter, and use the `magic_kwargs={'auto_call': True}` argument when adding the
function widget to napari.

Now move the sliders and watch the magic happen!

{button}`03_sliders.py <./scripts/03_sliders.py>`

```{code-cell} python
:tags: [remove-output]
:lineno-start: 1
:emphasize-lines: 9,10,32

from skimage import data, filters
import napari
import numpy as np
from typing import Annotated


def threshold(
    layer: napari.layers.Image,
    sigma: Annotated[float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 2, 'step': 0.1}] = 0.5,
    threshold: Annotated[float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 1, 'step': 0.05}] = 0.3,
) -> list[napari.types.LayerDataTuple]:
    """Apply a gaussian filter and threshold to a napari Image.

    When added to napari as a function widget, expose parameters as sliders.
    """
    if not layer:
        return
    norm = (layer.data - np.min(layer.data)) / np.max(layer.data)
    blur = filters.gaussian(norm, sigma=sigma)
    blobs = blur >= threshold

    return [
        (blur, {'name': 'blur'}, 'image'),
        (blobs, {'name': 'blobs'}, 'image'),
    ]


viewer = napari.Viewer()
image = data.cells3d()[30, 1]  # 2d
image_layer = viewer.add_image(image)

viewer.window.add_function_widget(threshold, magic_kwargs={'auto_call': True})
```

```{code-cell} python
:tags: [remove-input]

viewer.window.dock_widgets['threshold']()
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## Recap

- **1.** Pure Python function on numpy arrays — works but requires
  manual re-runs.
- **2.** Magicgui widget from a function with napari type annotations —
  interactive GUI inside napari, but still needs a "Run" click.
- **3.** Annotated type hints for sliders + `auto_call` — fully
  interactive, real-time updates.

Next up: we'll turn this thresholding into a full segmentation pipeline with
label cleaning, region properties, and watershed refinement.
