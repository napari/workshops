---
label: segmentation-pipeline
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
  - file: scripts/04_labels.py
    title: "Script 04 — Labels and morphology"
  - file: scripts/05_features_and_points.py
    title: "Script 05 — Features and Points"
  - file: scripts/06_watershed.py
    title: "Script 06 — Watershed refinement"
---

# Building a segmentation pipeline

In this module we extend our thresholding widget into a full segmentation
pipeline: we add morphological cleaning, label connected components, compute
quantitative features (area, centroid), display them on a Points layer, and
finally refine the result with a watershed step seeded by manual point
annotations.

## 1. Thresholding + morphology + labels

Let's build on the previous widget. We add two new parameters —
`min_hole_size` and `min_obj_size` — and return intermediate layers so you can
see each processing step.

{button}`04_labels.py <./scripts/04_labels.py>`

```{code-cell} python
:tags: [remove-output]
:lineno-start: 1
:emphasize-lines: 1,11-12,21-23,28-30

from skimage import data, filters, morphology, measure
import napari
import numpy as np
from typing import Annotated


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

    filled = morphology.remove_small_holes(blobs, max_size=min_hole_size)
    cleaned = morphology.remove_small_objects(filled, max_size=min_obj_size)
    labels = measure.label(cleaned)

    return [
        (blur, {'name': 'blur'}, 'image'),
        (blobs, {'name': 'blobs'}, 'image'),
        (filled, {'name': 'filled'}, 'image'),
        (cleaned, {'name': 'cleaned'}, 'image'),
        (labels, {'name': 'result'}, 'labels'),
    ]


viewer = napari.Viewer()
image = data.cells3d()[30, 1]  # 2d
image_layer = viewer.add_image(image)

viewer.window.add_function_widget(threshold_and_label, magic_kwargs={'auto_call': True})
```

Play with `min_hole_size` and `min_obj_size` to clean up the binary mask
before labeling. You can toggle visibility (eye icon in the layerlist) of the
intermediate layers to see what each step does.

```{code-cell} python
:tags: [remove-input]
from napari.utils import nbscreenshot

viewer.window.dock_widgets['threshold and label']()
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## 2. Quantitative features + Points layer

Let's compute region properties (area, centroid) for each detected object and
display them. We use `skimage.measure.regionprops_table` and attach the
results as layer `features`, then add a `Points` layer with the centroids.

```{code-cell} python
:tags: [remove-output]
:lineno-start: 1
:emphasize-lines: 27-29,36-37

from skimage import data, filters, morphology, measure
import napari
import numpy as np
from typing import Annotated


def threshold_and_label(
    layer: napari.layers.Image,
    sigma: Annotated[float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 2, 'step': 0.1}] = 0.5,
    threshold: Annotated[float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 1, 'step': 0.05}] = 0.3,
    min_hole_size: Annotated[int, {'widget_type': 'Slider', 'min': 0, 'max': 1000, 'step': 50}] = 0,
    min_obj_size: Annotated[int, {'widget_type': 'Slider', 'min': 0, 'max': 1000, 'step': 50}] = 0,
) -> list[napari.types.LayerDataTuple]:
    """Apply a gaussian filter, threshold, and compute labels on a napari Image.

    Label properties (area and centroid) are also computed and exposed via layer
    `features`. Centroids are also shown in a Points layer.
    """
    norm = (layer.data - np.min(layer.data)) / np.max(layer.data)
    blur = filters.gaussian(norm, sigma=sigma)
    blobs = blur >= threshold

    filled = morphology.remove_small_holes(blobs, max_size=min_hole_size)
    cleaned = morphology.remove_small_objects(filled, max_size=min_obj_size)
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


viewer = napari.Viewer()
image = data.cells3d()[30, 1]  # 2d
image_layer = viewer.add_image(image)

viewer.window.add_function_widget(threshold_and_label, magic_kwargs={'auto_call': True})
```

```{code-cell} python
:tags: [remove-input]

viewer.window.dock_widgets['threshold and label']()
nbscreenshot(viewer)
```

The number of layers is starting to be high and knowing exactly which parameter
to adjust can be tricky without an overview of all the steps. Let's enable the
grid view to spread out each individual layer into its own viewbox. We can also
enable the layer name overlay on each layer, to make it easier to know what's what.

```{code-cell} python
:tags: [remove-output]
viewer.grid.enabled = True
for layer in viewer.layers:
    layer.name_overlay.visible = True
viewer.reset_view()
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## 3. Watershed refinement

Sometimes the label boundaries are not perfect — especially when objects touch.
We can refine them using a watershed segmentation, seeded by points we place
manually.

For this, let's implement a separate function, since this requires manual intervention
and is also too computationally expensive to run continuously.

```{code-cell} python
:tags: [remove-output]
:lineno-start: 1
:emphasize-lines: 1,5,40-60,68

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

    filled = morphology.remove_small_holes(blobs, max_size=min_hole_size)
    cleaned = morphology.remove_small_objects(filled, max_size=min_obj_size)
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

    # generate seeds for the watershed algorithm from point markers
    markers_array = np.zeros_like(base_labels, dtype=bool)
    markers_array[tuple(markers.data.astype(int).T)] = True
    markers = ndi.label(markers_array)[0]

    watershedded = segmentation.watershed(-distance_field, markers, mask=base_labels)

    return [
        (distance_field, {'name': 'distance field'}, 'image'),
        (watershedded, {'name': 'watershed'}, 'labels'),
    ]


viewer = napari.Viewer()
image = data.cells3d()[30, 1]  # 2d
image_layer = viewer.add_image(image)

viewer.window.add_function_widget(threshold_and_label, magic_kwargs={'auto_call': True})
viewer.window.add_function_widget(watershed)
```

```{admonition} How to use the watershed widget
1. Run the `threshold_and_label` widget to get a `result` labels layer.
2. Create a new **Points layer** (`New > Points` or use the button above the layerlist),
   select the add mode (+ button at the top left) and place point markers inside the
   objects you want to separate — one marker per object.
3. Select the `watershed` widget in the UI, choose your Points layer as
   `markers` and the `result` labels layer as `labels`, then click **Run**.
4. A new `watershed` labels layer will appear with separated objects.
```

```{code-cell} python
:tags: [remove-input]

l = viewer.add_points()
l.mode = 'add'
viewer.layers.selected = {l}
viewer.window.dock_widgets['threshold and label']()
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## Recap

- **1.** Added morphological cleaning (`remove_small_holes`,
  `remove_small_objects`) and connected-component labeling.
- **2.** Computed region properties (area, centroid) and displayed them
  as layer features and a Points layer.
- **3.** Added a watershed refinement widget that uses manual point
  markers to split touching objects.

Next up: mouse callbacks for interactive label inspection, and taking our
pipeline into 3D!
