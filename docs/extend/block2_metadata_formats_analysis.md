---
label: extend-block2
title: "2. Python, Data, and Metadata"
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

**Goal:** Control napari entirely from Python — create viewers, add layers,
adjust properties, set physical scales and units, load data from files and
the cloud with xarray and Zarr, and write your first analysis function.

# 1. Create a viewer from Python (10 min)

In Block 1 we explored the napari GUI. Now let's do everything from code.
Launching `napari.Viewer()` from a Jupyter notebook or Python script opens
the napari GUI window — you can interact with it via the GUI **and**
programmatically at the same time.

```{code-cell} ipython3
import napari

# Create an empty viewer
viewer = napari.Viewer()
```

```{tip}
If you launch napari from a Python script (not a notebook), you need to call
`napari.run()` to start the event loop and show the GUI. In Jupyter notebooks,
this is handled automatically.
```

Let's load the **Cells (3D + 2Ch)** sample dataset and add it as layers —
the same data we explored in Block 1, but now we're doing it from Python.

```{code-cell} ipython3
from skimage.data import cells3d

image_data = cells3d()  # shape (60, 2, 256, 256) — (z, channels, y, x)
print(f'Data shape: {image_data.shape}')
```

Split the channels and add them with different colormaps:

```{code-cell} ipython3
membrane_data = image_data[:, 0, :, :]
nuclei_data = image_data[:, 1, :, :]

membrane = viewer.add_image(
    membrane_data,
    name='membranes',
    colormap='green',
)
nuclei = viewer.add_image(
    nuclei_data,
    name='nuclei',
    colormap='magenta',
    blending='additive',
)
```

```{code-cell} ipython3
:tags: [remove-input]

from napari.utils import nbscreenshot
nbscreenshot(viewer)
```

```{tip}
You can pass colormap, blending, opacity, contrast limits, and many other
parameters directly in `viewer.add_image()`. Check the
[docs](https://napari.org/stable/api/napari.Viewer.html#napari.Viewer.add_image)
for the full list.
```

# 2. Screenshots in your notebook (3 min)

Just like in the GUI, you can capture what's on screen — but from code:

```{code-cell} ipython3
from napari.utils import nbscreenshot
nbscreenshot(viewer)
# nbscreenshot(viewer, canvas_only=True)  # canvas only, no UI chrome
```

# 3. Exercise: Layer controls from Python (5 min)

Every property you adjusted with sliders and dropdowns in the GUI can be
set from Python. Try adjusting the nuclei layer:

```{code-cell} ipython3
nuclei_layer = viewer.layers['nuclei']
nuclei_layer.opacity = 0.7
nuclei_layer.contrast_limits = (0, 15000)
nuclei_layer.colormap = 'cyan'
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

```{code-cell} ipython3
# Reset for next section
nuclei_layer.colormap = 'magenta'
nuclei_layer.contrast_limits = (0, 65535)
nuclei_layer.opacity = 1.0
```

# 4. Physical scale, units, and axis labels (10 min)

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

### The napari-metadata plugin

The [napari-metadata](https://napari.org/napari-metadata/) plugin provides a
dock widget for viewing and editing all of this metadata in one place.
Install it via **Plugins > Install/Uninstall Plugins…** and open it from
**Plugins > napari-metadata: Layer metadata**.

```{image} https://napari.org/napari-metadata/en/latest/_images/screenshot.png
:width: 400px
:alt: napari-metadata widget showing axis labels, scale, translation, and units
:target: https://napari.org/napari-metadata/
```

The widget shows three sections:
1. **File metadata** — read-only properties (shape, dtype, file path)
2. **Axes metadata** — editable axis labels, scale, translation, and units
3. **Copy metadata** — propagate metadata from one layer to others

---

# 5. Loading data with Python (10 min)

napari's drag-and-drop and **File > Open** work well for many formats, but
when you need precise control over data loading, you can use Python libraries
directly.

Let's switch to a new dataset — we'll work with images of cell nuclei and
fluorescent spots from an in situ sequencing experiment. These files are
included in the workshop data.

```{code-cell} ipython3
from skimage.io import imread
from pathlib import Path

# Cross-environment path: works in both MyST (CWD=docs/) and JupyterLab
data_dir = next(p for p in [Path('extend/data'), Path('data')] if p.exists())

nuclei = imread(data_dir / 'nuclei_cropped.tif')
spots = imread(data_dir / 'spots_cropped.tif')

print(f'Nuclei shape: {nuclei.shape}')
print(f'Spots shape: {spots.shape}')
```

Let's clear the viewer and add this new data:

```{code-cell} ipython3
viewer.layers.clear()

viewer.add_image(nuclei, name='nuclei', colormap='I Forest')
viewer.add_image(spots, name='spots', colormap='I Orange', blending='additive')
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

### Other image reading libraries

For multi-page TIFF, OME-TIFF, and other complex TIFF variants, `tifffile`
provides more control:

```python
from tifffile import imread
nuclei = imread(data_dir / 'nuclei_cropped.tif')
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

# 6. A quick look at xarray: labeled arrays (5 min)

NumPy arrays are great, but they don't carry information about which axis is
which. **xarray** adds dimension names and coordinate labels to arrays, making
code more readable and robust.

```{code-cell} ipython3
import numpy as np
import xarray as xr

# Wrap our nuclei data in an xarray DataArray with named dimensions
labeled_nuclei = xr.DataArray(
    nuclei_slice,
    dims=['y', 'x'],
    coords={
        'y': np.arange(nuclei_slice.shape[0]) * 0.13,  # physical y (µm)
        'x': np.arange(nuclei_slice.shape[1]) * 0.13,  # physical x (µm)
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

# 7. Zarr and OME-Zarr: cloud-native image data (10 min)

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

# 8. Writing analysis functions (10 min)

Now let's write our first analysis function. The spots image has some
background autofluorescence — we can clean it up with a **gaussian high-pass
filter**: subtract a blurred version of the image from the original, keeping
only the sharp, spot-like features.

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

viewer.add_image(high_passed_spots, name='filtered spots', colormap='I Blue', blending='additive')
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

The spots stand out much more clearly against the background! But what if we
want to try a different `sigma` value? We'd have to re-run the cell manually
each time — not exactly an interactive exploration.

In **Block 3**, we'll turn this function into an interactive widget with
sliders, so we can tune parameters in real time — without writing any GUI code.

---

# Sharing Time (5 min)

- What was the largest or most interesting Zarr image you explored?
- Did adding scale and units change how you think about the data?
- What would you want to measure or analyze in the spots + nuclei dataset?

Share a screenshot on the **#workshops** stream on
[Zulip](https://napari.zulipchat.com): press `Alt+C` to copy the canvas,
then paste into Zulip.

```{code-cell} ipython3
:tags: [remove-cell]

viewer.close()
```
