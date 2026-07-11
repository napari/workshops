---
label: extend-block3
title: "3. Custom Widgets & Interactions"
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

# Block 3: Custom Widgets & Interactions

**Goal:** Add interactive GUI widgets, custom keybindings, layer event
callbacks, and mouse drag interactions to napari — turning analysis functions
into interactive tools.

## 1. Interactive thresholding with magicgui (20 min)

In Block 1 we ran segmentation steps cell by cell. Let's make it interactive
by adding a slider that updates the threshold in real time — without writing
any GUI code.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from napari.types import ImageData, LabelsData
from magicgui import magicgui
from skimage.data import cells3d

# Load and prepare data
image_data = cells3d()
nuclei = image_data[:, 1, :, :]       # nuclei channel
nuclei_mip = nuclei.max(axis=0)

viewer = napari.Viewer()
viewer.add_image(nuclei_mip, name='nuclei_mip')
```

### A magicgui from a function

The `@magicgui` decorator reads type annotations on your function parameters
and automatically generates corresponding GUI widgets:

```{code-cell} ipython3
@magicgui(auto_call=True,
          percentile={"widget_type": "IntSlider", "min": 0, "max": 100})
def threshold(image: ImageData, percentile: int = 50) -> LabelsData:
    """Threshold an image at a given percentile of its intensity range."""
    data_min = np.min(image)
    data_max = np.max(image)
    return image > data_min + percentile / 100 * (data_max - data_min)
```

Now add it to the viewer as a dock widget:

```{code-cell} ipython3
viewer.window.add_dock_widget(threshold, area="right")
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

```{tip}
`auto_call=True` means the function runs automatically whenever any parameter
changes — no need to press a "Run" button! The `ImageData` annotation tells
magicgui to show a dropdown of available image layers, and `LabelsData` tells
it the return type is a labels layer.
```

Try moving the **percentile** slider — the threshold result updates instantly.

### Exercise: Add more controls

```{code-cell} ipython3
:tags: [remove-cell]

# Clean up before next section
viewer.layers.clear()
```

Let's build a more complete widget with multiple parameters:

```{code-cell} ipython3
from typing import Annotated

viewer.add_image(nuclei_mip, name='nuclei_mip')

@magicgui(auto_call=True,
          percentile={"widget_type": "IntSlider", "min": 0, "max": 100},
          min_hole={"widget_type": "IntSlider", "min": 0, "max": 200, "step": 10},
          min_obj={"widget_type": "IntSlider", "min": 0, "max": 200, "step": 10})
def segment(
    image: ImageData,
    percentile: int = 50,
    min_hole: int = 60,
    min_obj: int = 50,
) -> LabelsData:
    """Threshold + morphological cleaning."""
    from skimage import morphology

    data_min = np.min(image)
    data_max = np.max(image)
    foreground = image > data_min + percentile / 100 * (data_max - data_min)

    cleaned = morphology.remove_small_holes(foreground, min_hole)
    cleaned = morphology.remove_small_objects(cleaned, min_size=min_obj)
    return cleaned

viewer.window.add_dock_widget(segment, area="right")
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

---

## 2. Custom keybindings (15 min)

Keybindings let you trigger actions with keyboard shortcuts. napari makes this
remarkably easy.

### A keybinding for morphological cleanup

Let's bind `Shift-P` to clean up the threshold result:

```{code-cell} ipython3
from skimage import morphology

@viewer.bind_key('Shift-P')
def process_foreground(viewer):
    """Remove small holes and objects from the threshold result."""
    data = viewer.layers['segment result'].data
    cleaned = morphology.remove_small_holes(data.astype(bool), 60)
    cleaned = morphology.remove_small_objects(cleaned, min_size=50)
    viewer.layers['segment result'].data = cleaned
```

### A keybinding for full segmentation

Now bind `Shift-S` to run the complete watershed pipeline:

```{code-cell} ipython3
from skimage import feature, measure, segmentation as sk_seg, util
from scipy import ndimage as ndi

@viewer.bind_key('Shift-S')
def complete_segmentation(viewer):
    """Run the full watershed segmentation pipeline."""
    foreground = viewer.layers['segment result'].data
    distance = ndi.distance_transform_edt(foreground)
    smoothed = ndi.gaussian_filter(distance, sigma=10)

    peaks = feature.peak_local_max(smoothed, min_distance=7, exclude_border=False)

    shape = viewer.layers['nuclei_mip'].data.shape
    markers = util.label_points(peaks, output_shape=shape)

    labels = sk_seg.watershed(-smoothed, markers, mask=foreground)

    # Add or update the labels layer
    if 'segmentation' in viewer.layers:
        viewer.layers['segmentation'].data = labels
    else:
        viewer.add_labels(labels, name='segmentation')
```

```{code-cell} ipython3
:tags: [remove-cell]

# Simulate the keybinding to create an initial result for screenshots
process_foreground(viewer)
complete_segmentation(viewer)
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

```{tip}
Keybindings can be attached to the viewer (`@viewer.bind_key`) or to
individual layers (`@layer.bind_key`). Layer-specific bindings only fire
when that layer type is active.
```

---

## 3. Layer events (15 min)

napari layers emit **events** when their properties change — data, colormap,
opacity, even individual point positions. You can connect custom functions
(callbacks) to these events.

Let's set up an example to demonstrate: we'll warp an image whenever a
control point is moved.

```{code-cell} ipython3
:tags: [remove-cell]

viewer.layers.clear()
```

```{code-cell} ipython3
import skimage as ski

# Create a checkerboard image with four control points
image = ski.data.checkerboard()
src = np.array([[66, 66], [133, 66], [66, 133], [133, 133]])

viewer.add_image(image, name='checkerboard')
viewer.add_points(src, name='source_points', symbol='+', face_color='red', size=5)
moving_points = viewer.add_points(src.copy(), name='moving_points')
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
from functools import partial
warp_checkerboard = partial(warp, viewer.layers['checkerboard'], src)
```

### Connecting to the data event

We want the warp to happen whenever a point moves. We connect a function to
the layer's `data` event:

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

# Reset image for next section
viewer.layers['checkerboard'].data = image
```

```{important}
Always disconnect callbacks when you're done:

```python
moving_points.events.data.disconnect(warp_on_point_changed)
```
```

---

## 4. Mouse callbacks (15 min)

Layer events fire when a change *completes*. But what if you want to react
while the user is dragging? That's where **mouse callbacks** come in.

Mouse callbacks use a **generator pattern** — they `yield` to separate the
logic for mouse press, drag, and release:

```{code-cell} ipython3
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

Let's replace the layer event callback with a mouse drag callback that warps
the image **as you drag** a point:

```{code-cell} ipython3
def warp_on_move(points_layer, event):
    """Warp the image as the user drags a control point."""
    # Nothing to do on mouse press
    yield

    # While dragging...
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
```

Attach the callback to the moving points layer:

```{code-cell} ipython3
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

---

## Recap

In this block you learned to:

| Technique | What it does | How to attach |
|-----------|-------------|---------------|
| **magicgui** | Auto-generate GUI widgets from functions | `@magicgui` + `viewer.window.add_dock_widget()` |
| **Custom keybindings** | Trigger actions with keyboard shortcuts | `@viewer.bind_key('Shift-P')` / `@layer.bind_key('key')` |
| **Layer events** | React to property changes | `layer.events.data.connect(callback)` |
| **Mouse callbacks** | React to mouse drag in real time | `layer.mouse_drag_callbacks.append(callback)` |

```{code-cell} ipython3
:tags: [remove-cell]

viewer.close()
```

In **Block 4**, we'll package these customizations into a pip-installable
napari plugin.
