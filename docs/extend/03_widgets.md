---
label: extend-block3
title: "3. Custom Widgets & Interactions"
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

**Goal:** Add interactive GUI widgets, custom keybindings, layer event
callbacks, and mouse drag interactions to napari — turning analysis functions
into interactive tools.

# Setup

Let's load the spots and nuclei data from Block 2 and get a fresh viewer:

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from pathlib import Path
from skimage.io import imread

# Cross-environment path
data_dir = next(p for p in [Path('extend/data'), Path('data')] if p.exists())
nuclei = imread(data_dir / 'nuclei_cropped.tif')
spots = imread(data_dir / 'spots_cropped.tif')

viewer = napari.Viewer()
viewer.add_image(nuclei, name='nuclei', colormap='I Forest')
viewer.add_image(spots, name='spots', colormap='I Orange', blending='minimum')
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

# 1. Writing analysis functions (10 min)

First, let's write the analysis function we'll turn into a widget. The spots
image has some background autofluorescence — we can clean it up with a
**gaussian high-pass filter**: subtract a blurred version of the image from
the original, keeping only the sharp, spot-like features.

```{code-cell} ipython3
from scipy import ndimage as ndi

def gaussian_high_pass(image, sigma):
    """Remove broad background signal by subtracting a gaussian-blurred copy.

    Parameters
    ----------
    image : np.ndarray
        The image to filter.
    sigma : float
        Width of the gaussian — larger values remove broader features.

    Returns
    -------
    high_passed : np.ndarray
        The filtered image with background suppressed.
    """
    low_pass = ndi.gaussian_filter(image, sigma)
    high_passed = (image - low_pass).clip(0)
    return high_passed
```

Let's test it on our spots data with `sigma=2`:

```{code-cell} ipython3
high_passed_spots = gaussian_high_pass(spots, 2)

viewer.add_image(
    high_passed_spots,
    name='filtered spots',
    colormap='I Blue',
    blending='minimum'
)
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

The spots stand out much more clearly against the background! But what if we
want to try a different `sigma` value? We'd have to re-run the cell manually
each time — not exactly an interactive exploration.

# 2. Interactive filtering with magicgui (25 min)

In Block 2 we wrote a `gaussian_high_pass` function to clean up the spots
image — but changing the `sigma` parameter meant re-running a cell each time.
Let's make it interactive with **magicgui**.

The `@magicgui` decorator reads type annotations on your function parameters
and automatically generates corresponding GUI widgets:

```{code-cell} ipython3
from magicgui import magicgui
from napari.types import ImageData
from scipy import ndimage as ndi

@magicgui
def gaussian_high_pass(
    image: ImageData, sigma: float = 2.0
) -> ImageData:
    """Apply a gaussian high-pass filter to suppress background.

    Parameters
    ----------
    image : np.ndarray
        The image to filter.
    sigma : float
        Width of the gaussian — larger values remove broader features.
    """
    low_pass = ndi.gaussian_filter(image, sigma)
    return (image - low_pass).clip(0)
```

```{code-cell} ipython3
viewer.window.add_dock_widget(gaussian_high_pass)
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

Notice what just happened: `magicgui` read the `ImageData` type annotation
and automatically created a dropdown that lists only image layers. The
`sigma` parameter became a spin box. And because the return type is also
`ImageData`, the result is automatically added as a new image layer.

Press the **Run** button — the filtered result appears. Change the `sigma`
value and press Run again: the layer updates in place.

```{tip}
Hover over the labels `image` and `sigma` — you should see tooltips with
the docstring information. More *magic* from magicgui!
```

````{admonition} A note about type hints
:class: note
Type hints like `ImageData` are not enforced at runtime, but they **can**
raise `NameError` if the name isn't defined. We imported `ImageData` from
`napari.types` to avoid this. Alternatively, you can use a forward reference
in quotes (`"napari.types.ImageData"`) or add:

```python
from __future__ import annotations
```

This makes **all** annotations strings automatically, so you never need to
import types just for hinting.
````

The `gaussian_high_pass` object is both a widget **and** a callable function:

```{code-cell} ipython3
# Read the current sigma value from the widget
print(gaussian_high_pass.sigma.value)

# Call it as a plain function — still works!
test_output = gaussian_high_pass(spots, sigma=5)
print(f'Output shape: {test_output.shape}')
```

This means you can use the same function in a script **or** as a widget in
napari — no code duplication.

### Adding sliders and auto-call

Let's make it even more interactive: replace the spin box with a slider
and have the function run automatically whenever we move it.

First, remove the old widget:

```{code-cell} ipython3
viewer.window.remove_dock_widget('all')
```

Now recreate it with widget configuration:

```{code-cell} ipython3
@magicgui(
    auto_call=True,
    sigma={"widget_type": "FloatSlider", "min": 0, "max": 20}
)
def gaussian_high_pass(
    image: ImageData, sigma: float = 2.0
) -> ImageData:
    """Apply a gaussian high-pass filter to suppress background."""
    low_pass = ndi.gaussian_filter(image, sigma)
    return (image - low_pass).clip(0)

viewer.window.add_dock_widget(gaussian_high_pass)
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

Now drag the slider — the filter updates instantly! `auto_call=True` means
the function runs whenever any parameter changes, no Run button needed.

You can also set widget values programmatically:

```{code-cell} ipython3
gaussian_high_pass.sigma.value = 8.0
```

### A more complete example: spot detection

Let's build a widget for the full spot detection workflow. We'll use
`skimage.feature.blob_log` to detect spots and return them as a Points
layer with custom styling.

When a function returns a `LayerDataTuple`, napari creates a new layer
using whatever data **and** visualization settings you provide:

- `(layer_data, layer_metadata, layer_type)` — data, display options, and type string
- `layer_metadata` can include `size`, `face_color`, `symbol`, and more

```{code-cell} ipython3
viewer.window.remove_dock_widget('all')

from skimage.feature import blob_log
from napari.types import LayerDataTuple

@magicgui(
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
    # Suppress background
    filtered = gaussian_high_pass(image, high_pass_sigma)

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

```{code-cell} ipython3
viewer.window.add_dock_widget(detect_spots, area="right")
```

```{code-cell} ipython3
:tags: [remove-cell]

# Trigger the widget for the screenshot
detect_spots.image.value = viewer.layers['spots']
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

Try adjusting the sliders. The spots update in real time — change
`spot_threshold` to detect more or fewer spots, adjust `blob_sigma` to
match the spot size in your image.

# 3. Custom keybindings (15 min)

Keybindings let you trigger actions with keyboard shortcuts. napari makes
this remarkably easy with the `bind_key` decorator.

Let's bind `Shift-D` to report how many spots were detected in the current
Points layer. We'll attach it to the Points layer type so it only fires
when a Points layer is active:

```{code-cell} ipython3
from napari.layers import Points
from napari.utils.notifications import show_info

@Points.bind_key("Shift-D")
def report_spot_count(points_layer: Points):
    """Print the number of detected spots in the active Points layer."""
    count = len(points_layer.data)
    show_info(f"Detected {count} spots")
```

Now select the Points layer created by `detect_spots` and press `Shift-D`.
You should see a notification pop up in the viewer!

```{code-cell} ipython3
:tags: [remove-cell]

# Simulate for the notebook
report_spot_count(viewer.layers['Points'])
```

```{tip}
We used `show_info()` instead of `print()` — this displays a notification
right in the napari viewer, which is much more visible than looking for
output in a notebook or terminal. Check out
[`napari.utils.notifications`](https://napari.org/dev/api/napari.utils.notifications.html)
for `show_warning()` and `show_error()` too.
```

```{important}
At the moment, `bind_key` shortcuts cannot overwrite napari's built-in
shortcuts. If a built-in shortcut uses the same key combination, the
built-in one wins — silently. Check **File > Preferences > Shortcuts**
to see which keys are already taken.
```

Keybindings can also be attached to the viewer (fires regardless of which
layer is active):

```python
@viewer.bind_key('Shift-R')
def run_detector(viewer):
    """Re-run spot detection with current settings."""
    detect_spots(viewer.layers['spots'].data)
```

# 4. Layer events (15 min)

napari layers emit **events** when their properties change — data, colormap,
opacity, even individual point positions. You can connect custom functions
(callbacks) to these events.

Let's demonstrate with a cool example: warping an image when control
points are moved.

```{code-cell} ipython3
:tags: [remove-cell]

# Clean up from the previous section
viewer.layers.clear()
```

```{code-cell} ipython3
import skimage as ski
from functools import partial

# Create a checkerboard image with four control points
image = ski.data.checkerboard()
src = np.array([[66, 66], [133, 66], [66, 133], [133, 133]])

viewer.add_image(image, name='checkerboard')
viewer.add_points(src, name='source_points', symbol='+', face_color='red', size=5)
moving_points = viewer.add_points(src.copy(), name='moving_points')
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

### The warp function

We'll use thin-plate splines to warp the image based on point positions:

```{code-cell} ipython3
def warp(im_layer, src, dst):
    """Warp an image from source to destination points using TPS."""
    tps = ski.transform.ThinPlateSplineTransform()
    tps.estimate(dst, src)
    warped = ski.transform.warp(image, tps)
    im_layer.data = (warped * 255).astype(image.dtype)

# Pre-bind the image layer and source points
warp_checkerboard = partial(warp, viewer.layers['checkerboard'], src)
```

### Connecting to the data event

We want the warp to happen whenever a point moves. We connect a callback
to the layer's `data` event:

```{code-cell} ipython3
def warp_on_point_changed(event):
    """Callback: warp the image when a point is moved."""
    if event.action == 'changed':
        warp_checkerboard(event.value)

moving_points.events.data.connect(warp_on_point_changed)
```

Now select the **moving_points** layer, switch to the **Select points** tool,
and drag a point. The image warps when you release the mouse.

```{code-cell} ipython3
:tags: [remove-cell]

# Reset for next section
viewer.layers['checkerboard'].data = image
```

```{important}
Always disconnect callbacks when you're done:

```python
moving_points.events.data.disconnect(warp_on_point_changed)
```

# 5. Mouse callbacks (15 min)

Layer events fire when a change *completes*. But what if you want to react
while the user is dragging? That's where **mouse callbacks** come in.

Mouse callbacks use a **generator pattern** — they `yield` to separate the
logic for mouse press, drag, and release:

```python
def some_mouse_callback(layer, event):
    # --- Mouse press ---
    print("Mouse pressed")
    yield  # ← this pauses; execution resumes on drag

    # --- Mouse drag ---
    while event.type == 'mouse_move':
        print("Dragging...")
        yield  # ← yields control each frame

    # --- Mouse release ---
    print("Mouse released")
```

```{code-cell} ipython3
:tags: [remove-cell]

viewer.layers['checkerboard'].data = image
```

### Warping on drag

Let's replace the layer event callback with a mouse drag callback that
warps the image **as you drag** a point:

```{code-cell} ipython3
def warp_on_move(points_layer, event):
    """Warp the image as the user drags a control point."""
    # --- Mouse press ---
    yield

    # --- Mouse drag ---
    while event.type == 'mouse_move':
        # Find which point is being dragged
        idx = list(points_layer.selected_data)[-1]

        # Copy and update the dragged point's position
        dst = points_layer.data.copy()
        dst[idx] = event.position

        # Warp the image
        warp_checkerboard(dst)
        yield

    # Nothing to do on mouse release

# Attach the callback to the moving points layer
moving_points.mouse_drag_callbacks.append(warp_on_move)
```

Now select the **moving_points** layer and drag a point — the image warps in
real time as you move the mouse!

```{code-cell} ipython3
:tags: [remove-cell]

# Cleanup
moving_points.mouse_drag_callbacks.remove(warp_on_move)
moving_points.events.data.disconnect(warp_on_point_changed)
```

```{important}
Clean up mouse callbacks when you're done:

```python
moving_points.mouse_drag_callbacks.remove(warp_on_move)
```
```

# Recap

In this block you learned to:

| Technique | What it does | How to attach |
|-----------|-------------|---------------|
| **magicgui** | Auto-generate GUI widgets from functions | `@magicgui` + `viewer.window.add_dock_widget()` |
| **Custom keybindings** | Trigger actions with keyboard shortcuts | `@Points.bind_key('Shift-D')` / `@viewer.bind_key('key')` |
| **Layer events** | React to property changes | `layer.events.data.connect(callback)` |
| **Mouse callbacks** | React to mouse drag in real time | `layer.mouse_drag_callbacks.append(callback)` |

In **Block 4**, we'll package our `detect_spots` widget into a
pip-installable napari plugin that anyone can use.

```{code-cell} ipython3
:tags: [remove-cell]

viewer.close()
```
