from typing import Annotated

import napari
import numpy as np
from scipy import ndimage as ndi
from skimage import data, filters, measure, morphology, segmentation


def threshold_and_label(
    layer: napari.layers.Image,
    sigma: Annotated[float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 2, 'step': 0.1}] = 0.5,
    threshold: Annotated[
        float, {'widget_type': 'FloatSlider', 'min': 0, 'max': 1, 'step': 0.05}
    ] = 0.3,
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

    props = measure.regionprops_table(
        watershedded,
        intensity_image=image.data,
        properties=['label', 'area', 'centroid', 'solidity', 'intensity_mean'],
    )
    props['index'] = props.pop('label')
    centroids = np.array([props[f'centroid-{i}'] for i in range(markers.ndim)]).T

    return [
        (distance_field, {'name': 'distance field'}, 'image'),
        (watershedded, {'name': 'watershed', 'features': props}, 'labels'),
        (
            centroids,
            {'name': 'watershed centroids', 'features': props, 'blending': 'translucent_no_depth'},
            'points',
        ),
    ]


def classify_features(
    centroids: napari.layers.Points,
    solidity: Annotated[
        tuple[float, float], {'widget_type': 'FloatRangeSlider', 'min': 0, 'max': 1, 'step': 0.05}
    ] = (0, 1),
    intensity: Annotated[
        tuple[float, float], {'widget_type': 'FloatRangeSlider', 'min': 0, 'max': 1, 'step': 0.05}
    ] = (0, 1),
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
    good = (
        (s >= solidity[0])
        & (s <= solidity[1])
        & (i >= rescaled_int_limits[0])
        & (i <= rescaled_int_limits[1])
    )
    centroids.features['good'] = good

    centroids.symbol = np.where(good, 'diamond', 'disc')


if __name__ == '__main__':
    viewer = napari.Viewer()
    image = data.cells3d()[30, 1]  # 2d
    image_layer = viewer.add_image(image)

    viewer.window.add_function_widget(threshold_and_label, magic_kwargs={'auto_call': True})
    viewer.window.add_function_widget(watershed)
    viewer.window.add_function_widget(classify_features, magic_kwargs={'auto_call': True})

    napari.run()
