---
label: interactivity-and-3d
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
  - file: scripts/07_mouse_callback.py
    title: "Script 07 — Mouse callback"
  - file: scripts/08_going_3D.py
    title: "Script 08 — Going 3D"
---

# Interactivity and 3D

In this final module we add two more interactive features:
1. A mouse callback that lets you **Shift+Click** on a label to see its area.
2. Running the entire pipeline on **3D data** — napari handles the extra
   dimension natively.

## Step 1: Interactive mouse callback

Let's add a mouse drag callback that prints the area of the label under the
cursor when you **Shift+Click**.

```{code-cell} python
from skimage import data, filters, morphology, measure, segmentation
import napari
import numpy as np
from typing import Annotated
from scipy import ndimage as ndi


def threshold_and_label(
    layer: napari.layers.Image,
    sigma: Annotated[float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 2, 'step': 0.1}] = 0.5,
    threshold: Annotated[float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 1, 'step': 0.05}] = 0.3,
    min_hole_size: Annotated[int, {'widget_type': 'Slider', 'min': 0, 'max': 1000, 'step': 50}] = 0,
    min_obj_size: Annotated[int, {'widget_type': 'Slider', 'min': 0, 'max': 1000, 'step': 50}] = 0,
) -> list[napari.types.LayerDataTuple]:
    """Apply a gaussian filter, threshold, and compute labels on a napari Image.

    When added to napari as a function widget, expose parameters as sliders.
    Label properties (area and centroid) are also computed and exposed via layer
    `features`. Centroids are also shown in a Points layer.
    """
    if not layer:
        return
    norm = (layer.data - np.min(layer.data)) / np.max(layer.data)
    blur = filters.gaussian(norm, sigma=sigma)
    blobs = blur >= threshold

    filled = morphology.remove_small_holes(blobs, min_hole_size)
    cleaned = morphology.remove_small_objects(filled, min_obj_size)
    labels = measure.label(cleaned)

    props = measure.regionprops_table(labels, properties=['label', 'area', 'centroid'])
    props['index'] = props.pop('label')
    centroids = np.array([props[f'centroid-{i}'] for i in range(layer.ndim)]).T

    return [
        (blur, {'name': 'blur'}, 'image'),
        (blobs, {'name': 'blobs'}, 'image'),
        (filled, {'name': 'filled'}, 'image'),
        (cleaned, {'name': 'cleaned'}, 'image'),
        (labels, {'name': 'result', 'features': props}, 'labels'),
        (centroids, {'name': 'centroids', 'features': props}, 'points'),
    ]


def watershed(
    markers: napari.layers.Points,
    labels: napari.layers.Labels,
) -> list[napari.types.LayerDataTuple]:
    """Improve Labels using watershed and seeds from a Points layer."""
    if not markers or not labels:
        return
    base_labels = labels.data != 0
    distance_field = ndi.distance_transform_edt(base_labels)

    markers_array = np.zeros_like(base_labels, dtype=bool)
    markers_array[tuple(markers.data.astype(int).T)] = True
    markers = ndi.label(markers_array)[0]

    watershedded = segmentation.watershed(-distance_field, markers, mask=base_labels)

    return [
        (distance_field, {'name': 'distance field'}, 'image'),
        (watershedded, {'name': 'watershed'}, 'labels'),
    ]


def print_props(viewer, event):
    """Mouse callback to print hovered label information on Shift+Click."""
    if event.type != 'mouse_press' or 'Shift' not in event.modifiers:
        return

    try:
        labels = viewer.layers['result']
    except KeyError:
        return

    label_id = labels.get_value(
        viewer.cursor.position,
        view_direction=viewer.cursor._view_direction,
        dims_displayed=list(viewer.dims.displayed),
        world=True,
    )

    if label_id == 0:
        napari.utils.notifications.show_info('Background!')
    else:
        area = labels.features.loc[label_id, 'area']
        napari.utils.notifications.show_info(f'Area of label {label_id}: {area} px.')


viewer = napari.Viewer()
image = data.cells3d()[30, 1]  # 2d
image_layer = viewer.add_image(image)

viewer.window.add_function_widget(threshold_and_label, magic_kwargs={'auto_call': True})
viewer.window.add_function_widget(watershed)
viewer.mouse_drag_callbacks.append(print_props)
```

```{code-cell} python
from napari.utils import nbscreenshot

nbscreenshot(viewer)
```

```{tip}
Hold **Shift** and click on any object in the `result` labels layer to see
its area displayed in napari's status bar!
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## Step 2: Going 3D

Everything we've built so far works on a 2D slice of `cells3d`. But napari is
**n-dimensional** — let's load the full 3D volume and see our pipeline in
action across all slices.

The best part? **No code changes needed.** napari's widgets automatically
operate on whatever data the selected layer contains, whether it's 2D or 3D.

```{code-cell} python
from skimage import data, filters, morphology, measure, segmentation
import napari
import numpy as np
from typing import Annotated
from scipy import ndimage as ndi


def threshold_and_label(
    layer: napari.layers.Image,
    sigma: Annotated[float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 2, 'step': 0.1}] = 0.5,
    threshold: Annotated[float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 1, 'step': 0.05}] = 0.3,
    min_hole_size: Annotated[int, {'widget_type': 'Slider', 'min': 0, 'max': 1000, 'step': 50}] = 0,
    min_obj_size: Annotated[int, {'widget_type': 'Slider', 'min': 0, 'max': 1000, 'step': 50}] = 0,
) -> list[napari.types.LayerDataTuple]:
    """Apply a gaussian filter, threshold, and compute labels on a napari Image."""
    if not layer:
        return
    norm = (layer.data - np.min(layer.data)) / np.max(layer.data)
    blur = filters.gaussian(norm, sigma=sigma)
    blobs = blur >= threshold

    filled = morphology.remove_small_holes(blobs, min_hole_size)
    cleaned = morphology.remove_small_objects(filled, min_obj_size)
    labels = measure.label(cleaned)

    props = measure.regionprops_table(labels, properties=['label', 'area', 'centroid'])
    props['index'] = props.pop('label')
    centroids = np.array([props[f'centroid-{i}'] for i in range(layer.ndim)]).T

    return [
        (blur, {'name': 'blur'}, 'image'),
        (blobs, {'name': 'blobs'}, 'image'),
        (filled, {'name': 'filled'}, 'image'),
        (cleaned, {'name': 'cleaned'}, 'image'),
        (labels, {'name': 'result', 'features': props}, 'labels'),
        (centroids, {'name': 'centroids', 'features': props}, 'points'),
    ]


def watershed(
    markers: napari.layers.Points,
    labels: napari.layers.Labels,
) -> list[napari.types.LayerDataTuple]:
    """Improve Labels using watershed and seeds from a Points layer."""
    if not markers or not labels:
        return
    base_labels = labels.data != 0
    distance_field = ndi.distance_transform_edt(base_labels)

    markers_array = np.zeros_like(base_labels, dtype=bool)
    markers_array[tuple(markers.data.astype(int).T)] = True
    markers = ndi.label(markers_array)[0]

    watershedded = segmentation.watershed(-distance_field, markers, mask=base_labels)

    return [
        (distance_field, {'name': 'distance field'}, 'image'),
        (watershedded, {'name': 'watershed'}, 'labels'),
    ]


def print_props(viewer, event):
    """Mouse callback to print hovered label information on Shift+Click."""
    if event.type != 'mouse_press' or 'Shift' not in event.modifiers:
        return

    try:
        labels = viewer.layers['result']
    except KeyError:
        return

    label_id = labels.get_value(
        viewer.cursor.position,
        view_direction=viewer.cursor._view_direction,
        dims_displayed=list(viewer.dims.displayed),
        world=True,
    )

    if label_id == 0:
        napari.utils.notifications.show_info('Background!')
    else:
        area = labels.features.loc[label_id, 'area']
        napari.utils.notifications.show_info(f'Area of label {label_id}: {area} px.')


viewer = napari.Viewer()
image = data.cells3d()[:, 1]  # 3d — two spatial dims + time/stack dim
image_layer = viewer.add_image(image)

viewer.window.add_function_widget(threshold_and_label, magic_kwargs={'auto_call': True})
viewer.window.add_function_widget(watershed)
viewer.mouse_drag_callbacks.append(print_props)
```

```{code-cell} python
nbscreenshot(viewer)
```

The only difference from the 2D version is the data source:
```python
# 2D (single slice)
image = data.cells3d()[30, 1]

# 3D (full stack)
image = data.cells3d()[:, 1]
```

Everything else — the widgets, the mouse callback, the feature computation —
**works identically** in 3D. Napari's slider at the bottom lets you scroll
through the z/t dimension, and the widgets operate on whichever slice (or the
full volume) the layer provides.

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## Recap

- **Mouse callbacks:** Attach arbitrary Python functions to mouse events for
  interactive label inspection.
- **3D support:** napari is n-dimensional — your widgets and callbacks work
  on 2D, 3D, and even higher-dimensional data without modification.

## Next steps: Turning this into a plugin

Now that you have a complete interactive segmentation workflow, you can package
it as a reusable napari plugin using the
[napari plugin template](https://github.com/napari/napari-plugin-template).

```bash
copier copy https://github.com/napari/napari-plugin-template.git my-plugin
```

See the [napari plugin documentation](https://napari.org/stable/plugins/index.html)
for more details. The napari hub ([napari-hub.org](https://napari-hub.org)) is
where you can share your plugin with the community!
