---
label: classification-and-3d
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
  - file: scripts/07_classify_features.py
    title: "Script 07 — Classify features"
  - file: scripts/08_going_3D.py
    title: "Script 08 — Going 3D"
---

# Adding interactive classification and going 3D

In this final module we add a small interactive classification step to our
pipeline, this time working on the Points layer. Finally, we test out our full
workflow on 3D data!

## 1. Classify objects based on their features

Let's finish up this workflow by adding a classification step. We calculate
some more object properties, and we add a new magic function that updates
the Points visualisation based on the `features` and our thresholds, and which
saves which objects should be marked as `good`.

You should recognize the magicgui pattern (with a new trick, `RangedSliders`!) and the
code for extracting object properties via `regionprops_table`. What's new is how we set
border and face colors on the `Points` layer based on properties and a colormap, as well
as their size based on the size of the underlying object. We also update the symbol
when a point satisfies our thresholds!

{button}`07_classify_features.py <./scripts/07_classify_features.py>`

```{code-cell} python
:tags: [remove-output]
:linenos:
:emphasize-lines: 43,46,58-60,65,69-100,109

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
    image: napari.layers.Image,
) -> list[napari.types.LayerDataTuple]:
    """Improve Labels using watershed and seeds from a Points layer."""
    if not markers or not labels or not image:
        return
    base_labels = labels.data != 0
    distance_field = ndi.distance_transform_edt(base_labels)

    # generate seeds for the watershed algorithm from point markers
    markers_array = np.zeros_like(base_labels, dtype=bool)
    markers_array[tuple(markers.data.astype(int).T)] = True
    markers = ndi.label(markers_array)[0]

    watershedded = segmentation.watershed(-distance_field, markers, mask=base_labels)

    props = measure.regionprops_table(watershedded, intensity_image=image.data, properties=['label', 'area', 'centroid', 'solidity', 'intensity_mean'])
    props['index'] = props.pop('label')
    centroids = np.array([props[f'centroid-{i}'] for i in range(markers.ndim)]).T

    return [
        (distance_field, {'name': 'distance field'}, 'image'),
        (watershedded, {'name': 'watershed', 'features': props}, 'labels'),
        (centroids, {'name': 'watershed centroids', 'features': props, 'blending': 'translucent_no_depth'}, 'points'),
    ]


def classify_features(
    centroids: napari.layers.Points,
    solidity: Annotated[tuple[float, float], {'widget_type': 'FloatRangeSlider', 'min': 0, 'max': 1, 'step': 0.05}] = (0, 1),
    intensity: Annotated[tuple[float, float], {'widget_type': 'FloatRangeSlider', 'min': 0, 'max': 1, 'step': 0.05}] = (0, 1),
) -> None:
    """Classify objects into good/bad based on their solidity and intensity features.

    Also updates the visualisation by altering colors and sizes based on values and thresholds.
    """
    if not centroids or 'solidity' not in centroids.features.columns:
        return

    area = centroids.features.area
    centroids.size = np.sqrt(area / area.max()) * 25

    centroids.border_width = 0.2
    centroids.border_color = 'solidity'
    centroids.border_colormap = 'orange'
    centroids.border_contrast_limits = solidity

    centroids.face_color = 'intensity_mean'
    centroids.face_colormap = 'cyan'
    i = centroids.features.intensity_mean
    # intensity is not between 0 and 1, so let's rescale the limits
    rescaled_int_limits = (np.array(intensity) * (i.max() - i.min())) + i.min()
    centroids.face_contrast_limits = rescaled_int_limits

    s = centroids.features.solidity
    good = (s >= solidity[0]) & (s <= solidity[1]) & (i >= rescaled_int_limits[0]) & (i <= rescaled_int_limits[1])
    centroids.features['good'] = good

    centroids.symbol = np.where(good, 'diamond', 'disc')


viewer = napari.Viewer()
image = data.cells3d()[30, 1]  # 2d
image_layer = viewer.add_image(image)

viewer.window.add_function_widget(threshold_and_label, magic_kwargs={'auto_call': True})
viewer.window.add_function_widget(watershed)
viewer.window.add_function_widget(classify_features, magic_kwargs={'auto_call': True})
```

```{admonition} How to use the classification widget
1. Run the `threshold and label` widget, followed up by the manual steps of the `watershed` widget 
2. In the `classify features` widget in the UI, choose your Points layer as
   `markers` and the `result` labels layer as `labels`, then click **Run**.
4. A new `watershed` labels layer will appear with separated objects.
```

```{code-cell} python
:tags: [remove-input]
from napari.utils import nbscreenshot

t = viewer.window.dock_widgets['threshold and label']
t.sigma.value = 1
t.threshold.value = 0.15
t.min_hole_size.value = 471
t.min_obj_size.value = 79
t()

# done this manually so we can show what it looks like in the screenshot
manual_seeds = np.array(
    [
        [ 13.96171682,  26.20149842],
        [ 30.29515511,  80.64629274],
        [ 10.33206386, 155.05417831],
        [ 41.18411398, 178.64692252],
        [ 39.3692875 , 222.20275798],
        [ 70.22133761, 111.49834286],
        [ 75.66581705,  58.86837501],
        [ 93.81408182, 160.49865775],
        [ 95.6289083 , 249.42515514],
        [144.62922319, 242.16584923],
        [144.62922319, 193.16553434],
        [150.07370262, 115.12799581],
        [173.66644682,  49.79424263],
        [220.85193524,  84.2759457 ],
        [242.62985296, 142.35039297],
        [246.25950592, 211.31379911],
        [219.03710876, 245.79550218],
        [200.57463293, 171.9494017 ],
        [137.28352217,  33.42546117]
    ]
)

l = viewer.add_points(manual_seeds)
w = viewer.window.dock_widgets['watershed']
w.markers.value = l
w()

c = viewer.window.dock_widgets['classify features']
c.centroids.value = viewer.layers['watershed centroids']
c.solidity.value = (0.63, 1)
c.intensity.value = (0.23, 0.62)
c()

nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## 2. Going 3D

Everything we've built so far works on a 2D slice of `cells3d`. But napari is
**n-dimensional** — let's load the full 3D volume and see our pipeline in
action across all slices.

The best part? **No code changes needed**, other than loading the data.
napari's widgets automatically operate on whatever data the selected
layer contains, whether it's 2D or 3D.

{button}`08_going_3D.py <./scripts/08_going_3D.py>`

```{code-cell} python
:tags: [remove-output]
:linenos:
:emphasize-lines: 104

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
    image: napari.layers.Image,
) -> list[napari.types.LayerDataTuple]:
    """Improve Labels using watershed and seeds from a Points layer."""
    if not markers or not labels or not image:
        return
    base_labels = labels.data != 0
    distance_field = ndi.distance_transform_edt(base_labels)

    # generate seeds for the watershed algorithm from point markers
    markers_array = np.zeros_like(base_labels, dtype=bool)
    markers_array[tuple(markers.data.astype(int).T)] = True
    markers = ndi.label(markers_array)[0]

    watershedded = segmentation.watershed(-distance_field, markers, mask=base_labels)

    props = measure.regionprops_table(watershedded, intensity_image=image.data, properties=['label', 'area', 'centroid', 'solidity', 'intensity_mean'])
    props['index'] = props.pop('label')
    centroids = np.array([props[f'centroid-{i}'] for i in range(markers.ndim)]).T

    return [
        (distance_field, {'name': 'distance field'}, 'image'),
        (watershedded, {'name': 'watershed', 'features': props}, 'labels'),
        (centroids, {'name': 'watershed centroids', 'features': props, 'blending': 'translucent_no_depth'}, 'points'),
    ]


def classify_features(
    centroids: napari.layers.Points,
    solidity: Annotated[tuple[float, float], {'widget_type': 'FloatRangeSlider', 'min': 0, 'max': 1, 'step': 0.05}] = (0, 1),
    intensity: Annotated[tuple[float, float], {'widget_type': 'FloatRangeSlider', 'min': 0, 'max': 1, 'step': 0.05}] = (0, 1),
) -> None:
    """Classify features into good/bad based on solidity and mean intensity.

    Also updates the visualisation by altering colors and sizes based on values and thresholds.
    """
    if not centroids or 'solidity' not in centroids.features.columns:
        return

    area = centroids.features.area
    centroids.size = np.sqrt(area / area.max()) * 25

    centroids.border_width = 0.2
    centroids.border_color = 'solidity'
    centroids.border_colormap = 'orange'
    centroids.border_contrast_limits = solidity

    centroids.face_color = 'intensity_mean'
    centroids.face_colormap = 'cyan'
    i = centroids.features.intensity_mean
    # intensity is not between 0 and 1, so let's rescale the limits
    rescaled_int_limits = (np.array(intensity) * (i.max() - i.min())) + i.min()
    centroids.face_contrast_limits = rescaled_int_limits

    s = centroids.features.solidity
    good = (s >= solidity[0]) & (s <= solidity[1]) & (i >= rescaled_int_limits[0]) & (i <= rescaled_int_limits[1])
    centroids.features['good'] = good

    centroids.symbol = np.where(good, 'diamond', 'disc')


viewer = napari.Viewer()
image = data.cells3d()[:, 1]  # 3d
image_layer = viewer.add_image(image)

viewer.window.add_function_widget(threshold_and_label, magic_kwargs={'auto_call': True})
viewer.window.add_function_widget(watershed)
viewer.window.add_function_widget(classify_features, magic_kwargs={'auto_call': True})
```

Using the slider at the bottom of the viewer to scroll through the third dimension,
you can observe the effects of the pipeline on individual 2D slices.
However, you can also switch to 3D using the 2D/3D button at the bottom left of the viewer.

Each view has its advantages and disadvantages: for example, in 3D you can more easily see
object connectivity and general segmentation effectiveness, while in 2D you can see internal
holes that would be otherwise invisible, as well as add point annotations as seed for
the watershed step.

Try using both modes to do a final segmentation and classification of this data.
Just watch out: the processing speed will be much slower than before!

```{code-cell} python
:tags: [remove-input]

viewer.dims.ndisplay = 3
viewer.camera.angles = -30, 0, -45

t = viewer.window.dock_widgets['threshold and label']
t.sigma.value = 0.84
t.threshold.value = 0.17
t.min_hole_size.value = 1000
t.min_obj_size.value = 1000
t()

# done this manually so we can show what it looks like in the screenshot
manual_seeds = np.array(
    [
        [30.0,  13.96171682,  26.20149842],
        [30.0,  30.29515511,  80.64629274],
        [30.0,  10.33206386, 155.05417831],
        [30.0,  41.18411398, 178.64692252],
        [30.0,  39.3692875 , 222.20275798],
        [30.0,  70.22133761, 111.49834286],
        [30.0,  75.66581705,  58.86837501],
        [30.0,  93.81408182, 160.49865775],
        [30.0,  95.6289083 , 249.42515514],
        [30.0, 144.62922319, 242.16584923],
        [30.0, 144.62922319, 193.16553434],
        [30.0, 150.07370262, 115.12799581],
        [30.0, 173.66644682,  49.79424263],
        [30.0, 220.85193524,  84.2759457 ],
        [30.0, 242.62985296, 142.35039297],
        [30.0, 246.25950592, 211.31379911],
        [30.0, 219.03710876, 245.79550218],
        [30.0, 200.57463293, 171.9494017 ],
        [30.0, 137.28352217,  33.42546117]
    ]
)

l = viewer.add_points(manual_seeds)
w = viewer.window.dock_widgets['watershed']
w.markers.value = l
w()

c = viewer.window.dock_widgets['classify features']
c.centroids.value = viewer.layers['watershed centroids']
c.solidity.value = (0.63, 1)
c.intensity.value = (0.23, 0.62)
c()
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## Recap

- **1.** Added an interactive classification step using the Points layer features.
- **2.** Get 3D support for free! napari is n-dimensional — your widgets and callbacks work
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
