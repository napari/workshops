---
label: intro-block3
title: "3. Plugins and Annotation"
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

**Goal:** Install a plugin from the napari hub, open images with it, and
manually annotate images using Points, Shapes, and Labels layers.

# Plugins and the napari Hub (5 min)

napari's functionality can be extended with **plugins** — Python packages
contributed by the community.

Plugins can add:

| Type | What it enables |
|------|----------------|
| **Readers** | Open file formats napari doesn't know by default |
| **Writers** | Save layers to custom formats |
| **Widgets** | New GUI panels for analysis, measurement, etc. |
| **Sample data** | Built-in example datasets |

Browse and search for plugins at [napari-hub.org](https://napari-hub.org).

**Installing a plugin from within napari:**

1. **Plugins > Install/Uninstall Plugins…**
2. Search by name in the top search bar
3. Click **Install** next to the plugin you want
4. (Restart napari when prompted)

```{admonition} Plugin maintenance
:class: warning
Plugins are contributed by the community and maintained independently.
If a plugin doesn't work as expected, check its GitHub page or ask on
[forum.image.sc](https://forum.image.sc/tag/napari).
```

# Opening Images with ndevio (10 min)

[ndevio](https://napari-hub.org/plugins/ndevio) is a plugin that
adds enhanced reading support for a wide range of file formats,
including OME-TIFF and BigTIFF.

Today we'll be using it to look at an example TIFF file from the [QuPath
documentation](https://qupath.readthedocs.io/en/stable/docs/intro/acknowledgements.html).

**Download your TIFF:**
1. [Click this link](https://downloads.openmicroscopy.org/images/Vectra-QPTIFF/perkinelmer/PKI_fields/LuCa-7color_%5B13860%2C52919%5D_1x1component_data.tif)
to download your image so it's available on your device.


**Install `ndevio`:**
1. **Plugins > Install/Uninstall Plugins…** → search `ndevio` → Install
2. You will see a warning about installing the plugin from PyPI. The napari bundle
typically uses `conda` to manage packages and plugins. A plugin installed from
PyPI **may** interact with other installed packages so we encourage using `conda`
when available. In this case, we know this plugin will work fine.

![Image displaying warning pop-up when installing a PyPI plugin in the napari bundle.](resources/pypi_install_warning.png)

3. Click OK.
4. Once the plugin is installed, close the plugin manager and restart napari, as advised.

**Open an image:**
- **File > Open File(s)** to open any `.tif` or `.tiff` file, or drag-and-drop onto the canvas
- You will be asked which plugin you want to use to open the file. Choose `ndevio`.
- You **may** see an error (and no image open) when first trying to open a 
`.tiff` file with `ndevio`. If you see this error, try opening the file again.
- If opening the file was successful, you may see a new GUI element on the right side of the viewer.
This is because some TIFF files have multiple different scenes bundled into
the same file e.g. one scene for each imaged region of interest (e.g. well, slide, sample).
Click on one of the detected scenes. You'll see the images added as layers to the viewer.

![Screenshot of the napari viewer with ndevio's scene selection widget open, and a white arrow pointing to the widget.](resources/ndevio-with-widget.png)

If you'd like to read other different file types with `ndevio`, check out [its documentation](https://napari-hub.org/plugins/ndevio).

```{note} Try some other TIFF files
There are a number of TIFF files on the [QuPath acknowledgements page](https://qupath.readthedocs.io/en/stable/docs/intro/acknowledgements.html)
and on the [OME-TIFF sample data page](https://docs.openmicroscopy.org/ome-model/5.6.3/ome-tiff/data.html).

Try downloading some other files and opening them in napari with builtins and/or with `ndevio`.

Does the image display as you expected? Do both plugins open the images in the same way? Do some
TIFF files not open at all and you get an error?
```

# napari-ome-zarr and the IDR (10 min)

napari-ome-zarr lets you
stream images directly from the web — no download required. The
[Image Data Resource (IDR)](https://idr.openmicroscopy.org/) hosts thousands
of public bioimages in OME-Zarr format. You will first need to install `napari-ome-zarr`

```{admonition} Asynchronous Rendering
However, for the best experience, you should turn on the "experimental" `Asynchronous Rendering`
option in napari's settings (**File > Preferences > Experimental**) and check
the box for "Render Images Asynchronously". This allows napari to load and render
large datasets in pieces without freezing the interface.
```

To open a remote image, you can drag-drop a URL onto the canvas, or on some platforms,
use **File > Open File(s)** and paste the URL there.
While you can try any image on the IDR, we suggest starting with any from the
[OME-NGFF Samples collection](https://idr.github.io/ome-ngff-samples/).

**After it loads, open napari-metadata** (**Plugins > napari-metadata: Metadata Widget**)
and examine the axis names and pixel scales the images come with.

```{note}
Streaming large remote datasets requires a network connection. If the connection
is slow during the workshop, we recommend 
`https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.5/idr0062A/6001240_labels.zarr`.
```

# Sharing Time (5 min)

- What did you open?
- What did the metadata widget show for axis scales and units?
- Any plugins you found interesting while browsing napari-hub?

# What Is Annotation? (5 min)

**Manual annotation** means marking up images by hand. Common reasons:

- **Training data** for machine learning segmentation models
- **Quality control** of automated results
- **Counting** cells, events, or structures of interest
- **Region-of-interest selection** for downstream analysis

Two fundamental approaches:

| Approach | napari layer | When to use |
|----------|-------------|-------------|
| **Vector** | Points, Shapes | Marking locations, outlines |
| **Raster** | Labels | Pixel-wise segmentation masks |

# Annotation with Points and Shapes (10 min)

Use the **Cells (3D + 2Ch)** sample for this exercise.

## Points layer — marking cell centers

1. In the layer list, click **Add Points layer** (the points icon in the top-left)
   — or go to **Layer > New Points Layer**
2. In layer controls, ensure the **Add points** tool is active (circle icon with a + inside)
3. Click on cell centers in the `nuclei` layer to add a point at each location
4. Each click drops a point; Use the Backspace/Delete key to remove the last added point (or the x icon)
5. Switch to the **Select** tool to move existing points

```{code-cell} python
:tags: [remove-cell]
import napari
import numpy as np
from skimage import data, feature, filters, morphology
from napari.utils import nbscreenshot

cells3d = data.cells3d()
nuclei = cells3d[:, 1]

nuclei_smoothed = filters.gaussian(nuclei, sigma=5)
nuclei_thresholded = nuclei_smoothed > filters.threshold_otsu(nuclei_smoothed)
nuclei_labels = morphology.label(nuclei_thresholded)
nuclei_points = feature.peak_local_max(nuclei_smoothed, min_distance=20)

viewer = napari.Viewer()
viewer.add_image(nuclei, name='nuclei', contrast_limits = (10000, 65355))
viewer.add_labels(nuclei_labels, name='nuclei labels')
viewer.add_points(
    nuclei_points, name='nuclei maxima', blending='additive', opacity=0.5
)
viewer.dims.ndisplay = 3
viewer.camera.angles = (-27, 8, -58)
viewer.fit_to_view()
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

Compare visualization in 2D with checking `out_of_slice_display` in layer controls — it shows points that are outside the current z-slice.

## Shapes layer — outlining a region

1. Add a shapes layer: **Layer > New Shapes Layer**
2. Choose a shape tool from layer controls (rectangle, ellipse, polygon, etc.)
3. Draw an outline around a region of interest
4. Use the **Select** tool to resize or move shapes

## Labels layer — painting a cell

1. Add a labels layer: **Layer > New Labels Layer** (choose the size to match your image)
2. Select the **Paint** tool from layer controls and pick a brush size
3. Paint over one cell to label it — each label value is a different integer (colour)
4. Use **Fill** to flood-fill an enclosed region

```{tip}
You can save any annotation layer via **File > Save Selected Layer(s)** as a
tiff (labels) or csv/shapefile (shapes/points).
```
