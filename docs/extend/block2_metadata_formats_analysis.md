---
label: extend-block2
title: "2. Metadata, Formats, and Interactive Analysis"
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

**Goal:** Set physical scales and units on image layers, load data with Python
libraries, explore xarray for labeled arrays and Zarr for cloud-native data,
and run an interactive segmentation workflow.

## 1. Physical scale, units, and axis labels (10 min)

Images from microscopes and other instruments have physical meaning — pixels
correspond to real-world distances. napari can represent this with **scale**,
**units**, and **axis labels**.

```{important}
Setting physical scales and units is essential for making real-world
measurements. The scale bar, axis overlays, and measurement tools all
depend on this metadata.
```

### Setting layer scale

The `cells3d` data has voxel dimensions of approximately 0.29 µm in z and
0.13 µm in xy. Let's set them:

```{code-cell} ipython3
for layer in viewer.layers:
    layer.scale = [0.29, 0.13, 0.13]
    layer.units = ('µm', 'µm', 'µm')
```

Now enable the scale bar to see the physical scale:

```{code-cell} ipython3
viewer.scale_bar.visible = True
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

```{code-cell} ipython3
:tags: [remove-cell]

viewer.scale_bar.visible = False
```

### Axis labels

The dimension sliders at the bottom of the viewer show generic index labels
by default. We can rename them to reflect the actual axes:

```{code-cell} ipython3
viewer.dims.axis_labels = ['Z', 'Y', 'X']
```

```{tip}
You can also edit axis labels by right-clicking the roll-dimensions button
and double-clicking the label in the popup.
```

### The napari-metadata plugin

The [napari-metadata](https://napari.org/napari-metadata/) plugin provides a
dock widget for viewing and editing metadata. Install it via
**Plugins > Install/Uninstall Plugins…** and open it from
**Plugins > napari-metadata: Layer metadata**.

![napari-metadata widget](https://napari.org/napari-metadata/_images/screenshot.png)

The widget shows three sections:
1. **File metadata** — read-only properties (shape, dtype, file path)
2. **Axes metadata** — editable axis labels, scale, translation, and units
3. **Copy metadata** — propagate metadata from one layer to others

---

## 2. Loading data with Python (10 min)

napari's drag-and-drop and **File > Open** work well for many formats, but
when you need precise control over data loading, you can use Python libraries
directly.

### Using skimage.io.imread

For common image formats (TIFF, PNG, JPEG):

```{code-cell} ipython3
from skimage.io import imread

# Load a cropped nuclei image from the workshop data
# Path works both in MyST (CWD=docs/) and JupyterLab (CWD=notebook dir)
from pathlib import Path
data_dir = next(p for p in [Path('extend/data'), Path('data')] if p.exists())

nuclei_slice = imread(data_dir / 'nuclei_cropped.tif')
print(f'Shape: {nuclei_slice.shape}')
```

### Using tifffile for advanced TIFF support

For multi-page TIFF, OME-TIFF, and other complex TIFF variants:

```python
from tifffile import imread
nuclei = imread('extend/data/nuclei_cropped.tif')
```

```{admonition} Why so many libraries?
:class: note
Different Python libraries support different file formats and feature sets.
`skimage.io.imread` is convenient for common formats, `tifffile` handles
complex TIFF metadata, and reader plugins (like `ndevio` for proprietary
microscope formats) provide support for everything else. Check the
[napari hub](https://napari-hub.org) for format-specific reader plugins.
```

---

## 3. A quick look at xarray: labeled arrays (5 min)

NumPy arrays are great, but they don't carry information about which axis is
which. **xarray** adds dimension names and coordinate labels to arrays, making
code more readable and robust.

```{code-cell} ipython3
import xarray as xr

# Wrap our nuclei data in an xarray DataArray with named dimensions
labeled_nuclei = xr.DataArray(
    nuclei,
    dims=['z', 'y', 'x'],
    coords={
        'z': np.arange(nuclei.shape[0]) * 0.29,  # physical z coordinate (µm)
        'y': np.arange(nuclei.shape[1]) * 0.13,   # physical y coordinate (µm)
        'x': np.arange(nuclei.shape[2]) * 0.13,   # physical x coordinate (µm)
    },
    name='nuclei',
)
print(labeled_nuclei)
```

When you pass an xarray DataArray to napari's `add_image()`, napari
automatically reads the dimension names and coordinate values:

```{code-cell} ipython3
viewer2 = napari.Viewer()
viewer2.add_image(labeled_nuclei)
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer2)
```

```{code-cell} ipython3
:tags: [remove-cell]

viewer2.close()
```

Notice how the dimension sliders already have the correct axis labels and
the scale is set from the coordinate values. The [napari docs on xarray
support](https://napari.org/stable/gallery/display_xarray_data.html) has more
details.

---

## 4. Zarr and OME-Zarr: cloud-native image data (10 min)

**Zarr** is a chunked, compressed, n-dimensional array format designed for
cloud storage. Instead of downloading the whole file, you can stream only
the parts you need.

**OME-Zarr** is a standardized specification for bioimaging data built on top
of Zarr — it's what the [Image Data Resource (IDR)](https://idr.openmicroscopy.org/)
uses to host thousands of public microscopy images.

### Opening a remote OME-Zarr image

First, we need the `napari-ome-zarr` reader plugin:

```python
# In the napari GUI:
# Plugins > Install/Uninstall Plugins… > search "napari-ome-zarr" > Install > Restart
```

Or from the terminal:
```bash
pixi run -e extend pip install napari-ome-zarr
```

Now let's stream a public image from the IDR:

```{code-cell} ipython3
:tags: [remove-output]

# NOTE: This cell requires an internet connection
# If the connection is slow, try this fallback URL:
# https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.5/idr0062A/6001240_labels.zarr

zarr_url = "https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.5/idr0062A/6001240_labels.zarr"

viewer_zarr = napari.Viewer()
viewer_zarr.open(zarr_url, plugin='napari-ome-zarr')
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer_zarr)
```

```{tip}
For the best experience with large remote datasets, enable **Asynchronous
Rendering** in napari's settings (**File > Preferences > Experimental >
Render Images Asynchronously**). This lets napari load data in pieces
without freezing the interface.
```

### Explore more OME-Zarr datasets

- [OME-NGFF Samples collection](https://idr.github.io/ome-ngff-samples/)
- [2024 NGFF Challenge](https://ome.github.io/ome2024-ngff-challenge/) — filter by
  organism, modality, or dimension count

```{code-cell} ipython3
:tags: [remove-cell]

viewer_zarr.close()
```

```{admonition} Readers and plugins
:class: tip
napari uses a **plugin-based reader system**. Different file formats are
handled by different reader plugins:
- **Built-in**: PNG, JPEG, TIFF (basic), CSV
- **[ndevio](https://napari-hub.org/plugins/ndevio)**: OME-TIFF, BigTIFF, and
  many proprietary microscope formats
- **[napari-ome-zarr](https://napari-hub.org/plugins/napari-ome-zarr)**: OME-Zarr,
  streaming from cloud URLs
- **Other plugins**: Search [napari-hub.org](https://napari-hub.org) for your format

When you drag a file onto the canvas, napari asks which reader to use. If no
reader matches, you can install one from the plugin manager.
```

---

## 5. Interactive segmentation workflow (30 min)

Now let's put everything together and build an interactive segmentation workflow
using the napari viewer connected to a Jupyter notebook.

### Load the data

We'll use the `cells3d` dataset — no external files needed.

```{code-cell} ipython3
from skimage import filters, feature, morphology, measure, segmentation, util
from scipy import ndimage as ndi

image_data = cells3d()
membranes = image_data[:, 0, :, :]
nuclei = image_data[:, 1, :, :]

# Compute a maximum intensity projection for 2D analysis
nuclei_mip = nuclei.max(axis=0)

viewer.layers.clear()
viewer.add_image(nuclei_mip, name='nuclei_mip')
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

### Thresholding

Let's separate nuclei from background using automatic thresholding:

```{code-cell} ipython3
foreground = nuclei_mip >= filters.threshold_li(nuclei_mip)
viewer.add_labels(foreground, name='foreground')
```

We can clean up small holes and debris:

```{code-cell} ipython3
foreground_processed = morphology.remove_small_holes(foreground, 60)
foreground_processed = morphology.remove_small_objects(foreground_processed, min_size=50)

viewer.layers['foreground'].data = foreground_processed
```

### Marker-controlled watershed

Now we convert the binary mask into an instance segmentation (each nucleus
gets a unique label). The approach: distance transform → find peaks →
watershed.

```{code-cell} ipython3
distance = ndi.distance_transform_edt(foreground_processed)
smoothed = filters.gaussian(distance, sigma=10)

viewer.add_image(smoothed, name='distance')
```

```{code-cell} ipython3
peak_local_max = feature.peak_local_max(
    smoothed, min_distance=7, exclude_border=False
)

viewer.add_points(peak_local_max, name='peaks', size=5, face_color='red')
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

Now seed the watershed from those peaks:

```{code-cell} ipython3
markers = util.label_points(
    viewer.layers['peaks'].data,
    output_shape=viewer.layers['nuclei_mip'].data.shape,
)

nuclei_segmentation = segmentation.watershed(
    -smoothed, markers, mask=foreground_processed
)

viewer.add_labels(nuclei_segmentation, name='segmentation')
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

### Measure and save

```{code-cell} ipython3
props = measure.regionprops_table(
    nuclei_segmentation,
    intensity_image=nuclei_mip,
    properties=('label', 'area', 'centroid', 'intensity_mean'),
)

print(f'Found {len(props["label"])} nuclei')
print(f'Average area: {np.mean(props["area"]):.0f} pixels')
```

```python
# Save the segmentation
viewer.layers['segmentation'].save('nuclei-automated-segmentation.tif', plugin='builtins')
```

---

## Sharing Time (5 min)

- What was the largest or most interesting Zarr image you explored?
- Did adding scale and units change how you think about the data?
- How many nuclei did your segmentation find?

Share a screenshot on the **#workshops** stream on
[Zulip](https://napari.zulipchat.com): press `Alt+C` to copy the canvas,
then paste into Zulip.

```{code-cell} ipython3
:tags: [remove-cell]

viewer.layers.clear()
viewer.close()
```
