---
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
    colormap='yellow',
)
nuclei = viewer.add_image(
    nuclei_data,
    name='nuclei',
    colormap='cyan',
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
nbscreenshot(viewer, canvas_only=True)
```

# 3. Exercise: Layer controls from Python (5 min)

Every property you adjusted with sliders and dropdowns in the GUI can be
set from Python. Try adjusting the nuclei layer:

```{code-cell} ipython3
nuclei_layer = viewer.layers['nuclei']
nuclei_layer.opacity = 0.7
nuclei_layer.contrast_limits = (0, 30000)
nuclei_layer.colormap = 'magenta'
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

```{code-cell} ipython3
# Reset for next section
nuclei_layer.colormap = 'cyan'
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
    layer.scale = [0.13, 0.13, 0.13]
    layer.units = ('µm', 'µm', 'µm')

# viewer.fit_to_view()
```

Now enable the scale bar to see the physical scale:

```{code-cell} ipython3
viewer.scale_bar.visible = True
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

### Axis labels

The dimension sliders at the bottom of the viewer show generic index labels
by default. We can rename them to reflect the actual axes and show the floating
axes overlay:

```{code-cell} ipython3
viewer.dims.axis_labels = ['Z', 'Y', 'X']
viewer.floating_axes.visible = True
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

viewer.add_image(
    nuclei,
    colormap='I Forest'
)
viewer.add_image(
    spots,
    colormap='I Orange',
    blending='minimum'
)
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

# 6. Zarr and OME-Zarr: cloud-native image data (10 min)

**Zarr** is a chunked, compressed, n-dimensional array format designed for
cloud storage. Instead of downloading the whole file, you can stream only
the parts you need.

**OME-Zarr** is a standardized specification for bioimaging data built on top
of Zarr — it's what the 
uses to host thousands of public microscopy images.

### Opening a remote OME-Zarr image

```{admonition} Readers and plugins
:class: tip
napari uses a **plugin-based reader system**. Different file formats are
handled by different reader plugins:
- **Built-in**: PNG, JPEG, TIFF (basic), CSV
- **[napari-ome-zarr](https://napari-hub.org/plugins/napari-ome-zarr)**: OME-Zarr,
  streaming from cloud URLs
- **[ndevio](https://napari-hub.org/plugins/ndevio)**: OME-TIFF, Zarr, major microscopy formats, and bioformats support
- **Other plugins**: Search [napari-hub.org](https://napari-hub.org) for your format

When you attempt to open a file onto the canvas, napari asks which reader to use.
In addition to Pythonic dependency management, you can also install them from the
napari plugin manager (**Plugins > Install/Uninstall Plugins…**).
```

We will first use the specialized [napari-ome-zarr](https://github.com/ome/napari-ome-zarr)
plugin to open public OME-Zarr datasets directly from the
[Image Data Resource (IDR)](https://idr.openmicroscopy.org/). This plugin is
not included in the default napari installation, but the `extend` feature includes
napari-ome-zarr.

```{important}
The experimental Asynchronous Rendering feature in napari is especially useful for 
remote datasets because the viewer is not "blocked" while data is being downloaded.
Enable it in **File > Preferences > Experimental > Render Images Asynchronously**.
```

Now let's stream a public image from the [IDR Catalog of OME-NGFF samples](https://idr.github.io/ome-ngff-samples/).

```{code-cell} ipython3
:tags: [remove-output]

# plants: https://livingobjects.ebi.ac.uk/idr/zarr/v0.5/idr0157/Asterella%20gracilis%20SWE/IMG_1033-1112%20Asterella%20gracilis%20(Mannia%20gracilis)%20stature.ome.zarr
# brain slice: https://livingobjects.ebi.ac.uk/idr/zarr/v0.4/idr0048A/9846152.zarr/
# cells: https://livingobjects.ebi.ac.uk/idr/zarr/v0.4/idr0047A/4496763.zarr

# If the connection is slow, try this fallback URL:
# https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.5/idr0062A/6001240_labels.zarr

zarr_url = "https://livingobjects.ebi.ac.uk/idr/zarr/v0.4/idr0048A/9846152.zarr/"

viewer_zarr = napari.Viewer()
viewer_zarr.open(zarr_url, plugin='napari-ome-zarr')
```

```{tip}
You can copy an image link and "paste" it into the napari GUI to open it!
Use the "Ctrl+N" shortcut (New Image) when the link is copied to your clipboard.
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer_zarr)
```

### Explore more OME-Zarr datasets

- [OME-NGFF Samples collection](https://idr.github.io/ome-ngff-samples/)
- [2024 NGFF Challenge](https://ome.github.io/ome2024-ngff-challenge/) — filter by
  organism, modality, or dimension count

```{code-cell} ipython3
:tags: [remove-cell]

viewer_zarr.close()
```

# 7. Full-circle: from plugin to code to napari (10 min)

To wrap this all up, let's now use [bioio](https://bioio-devs.github.io/bioio/OVERVIEW.html)
to see how we can programmatically interact with a broad number of bioimaging formats.
By default, the `extend` environment install bioio-ome-zarr and bioio-ome-tiff, but
there are many other bioio plugins available. 

Then, we'll use [ndevio](https://github.com/ndev-kit/ndevio) as a flexible napari plugin
that uses bioio and its metadata system to make napari-ready data, in addition to 
its general use as a napari reader plugin.

Under the hood, bioio uses **xarray** to represent image data with named
dimensions — that's what gives us meaningful axis labels like `T`, `C`, `Z`,
`Y`, `X` instead of opaque index numbers.

We're going to look at a multiscale chicken embryo:

```{code-cell} ipython3
from bioio import BioImage
import bioio

# note the trailing forward slash must be absent
img = BioImage("https://livingobjects.ebi.ac.uk/idr/zarr/v0.5/idr0066/ExpD_chicken_embryo_MIP.ome.zarr")

print(img.dims)
print(img.shape)
img.xarray_dask_data
```

```{code-cell} ipython3
from ndevio import nImage

nimg = nImage("https://livingobjects.ebi.ac.uk/idr/zarr/v0.5/idr0066/ExpD_chicken_embryo_MIP.ome.zarr")
# sublcasses BioImage, so it contains all properties:
print(nimg.dims)
# and ndevio logic for "reasonable" defaults
nimg.reference_xarray
```

```{code-cell} ipython3
# the 0th data is the highest resolution, while the -1th data is the coursest
nimg.layer_data[-1]
```

```{code-cell} ipython3
ldt = nimg.get_layer_data_tuples()
print(type(ldt))
ldt[0]
```

```{code-cell} ipython3
for data, kwargs, layer_type in nimg.get_layer_data_tuples():
    add_method = getattr(viewer, f'add_{layer_type}')
    add_method(data, **kwargs)
```

In **Block 3**, we'll take our programmatic understanding of napari to the
next step by creating an interactive widget with sliders,
so we can tune parameters in real time — without writing any GUI code.

# Sharing Time (5 min)

- What was the most interesting image you explored? Why?
- Did managing and visualizing metadata improve your understanding of the data?

Share a screenshot on the **#workshops** stream on
[Zulip](https://napari.zulipchat.com): press `Alt+C` to copy the canvas,
then paste into Zulip.

```{code-cell} ipython3
:tags: [remove-cell]

viewer.close()
```
