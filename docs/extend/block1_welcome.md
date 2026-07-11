---
label: extend-block1
title: "1. Welcome and First Images"
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

**Goal:** Set up your environment, get an overview of the workshop, create a
napari viewer from Python, and add layers programmatically.

# Welcome (10 min)

- Introduce instructors and helpers
- Share the [Code of Conduct](https://napari.org/stable/community/code_of_conduct.html)
- Share the Zulip **#napari-workshop-[DATE]** thread
  - post an introduction: *"What field are you from, and what kind of images do
  you work with?"*
- Ask about accessibility needs (private DMs on Zulip will be monitored)

# Workshop Overview (5 min)

This workshop has **four blocks**:

| Block | Topic |
|-------|-------|
| **1** | Welcome and GUI walkthrough — set up, create a viewer from Python |
| **2** | Metadata, formats, and interactive analysis — scale, units, xarray, Zarr, segmentation |
| **3** | Custom widgets and interactions — magicgui, keybindings, events, mouse callbacks |
| **4** | From script to plugin — package your tools as pip-installable napari plugins |

The workshop blurb says it best:

```{admonition} 
With everything from microscopes to telescopes to satellites, scientists
produce image data in countless formats, shapes, sizes, and dimensions.
napari is a Python library for multidimensional image visualization, but it
does double duty as a standalone application that can be easily extended
with GUI tools for analysis, visualization, and annotation.

In this tutorial, we'll start with the basics of image visualization and
analysis in napari, then show how to extend the napari user interface to
make analysis workflows as easy as pushing a button, and finally show how
to share these extensions as *plugins*, which can be easily installed by
users and collaborators.
```

# About napari (5 min)

[napari](https://napari.org) is a free, open-source, multi-dimensional image viewer for Python. It is:

- **Community-driven** — built by scientists, for scientists
- **Extensible** — hundreds of plugins on [napari-hub.org](https://napari-hub.org)
- **Interoperable** — works with NumPy, xarray, Zarr, TIFF, and more
- **Interactive** — explore and annotate your data with a GUI or from Python

# What Are Images? (5 min)

A quick conceptual grounding before we code:

- **Images are arrays of numbers** — each pixel has an intensity value
- **n-dimensional** — images can have more dimensions than just height and width
- **Common convention**: TZYX — time, depth (z), height (y), width (x)
- **Labels** — images where pixel values are integer categories (0=background, 1=object1, etc.)
- **Scale and units** — each pixel corresponds to a real-world physical size

# Open Your First Image and take Screenshots (5 min)

```bash
pixi run -e extend napari
```

1. In napari, select: **File > Open Sample > napari builtins > Cells (3D + 2Ch)**
2. Two layers appear in the layer list: `membrane` and `nuclei`
3. Use the **dimension slider** at the bottom to scroll through z-slices
4. Toggle each layer on/off with the **eye icon** next to its name

```{code-cell} python
:tags: [remove-cell]
viewer.open_sample('napari', 'cells3d')
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

> **What you're looking at:** Confocal microscopy images of cells in 3D.
> The `nuclei` channel (channel 1) shows cell nuclei stained with a dye.
> The `membrane` channel (channel 0) shows cell membranes.

## Screenshots

Save what you see in napari at any time:

- **File > Save Screenshot...** — saves the canvas as an image file
- **File > Save Screenshot with Viewer** — saves the canvas plus the entire GUI
- **File > Copy Screenshot to Clipboard** — paste it directly into a document or chat

Keyboard shortcut: `Alt+S` (saves to file) or `Alt+C` (copies to clipboard).
Add Shift to include the viewer UI: `Alt+Shift+S` or `Alt+Shift+C`.

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer=viewer,canvas_only=True)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## Opening Files from the Command Line

Now, try and see how the command line can also read files (images and scripts!):

```bash
pixi run -e extend napari demos/everything.py
```

# Create a viewer from Python (15 min)

Unlike the intro workshop (which uses the bundled app), we're working from
Python. Let's create our first viewer programmatically from launching this jupyter notebook.

Launching `napari.Viewer()` from a Jupyter notebook or Python script opens
the napari GUI window. You can interact with it via the GUI and
programmatically at the same time.

```{code-cell} ipython3
import napari

# Create an empty viewer
viewer = napari.Viewer()

# If in a script, call to start the event loop and show the GUI
# napari.run()  
```

```{tip}
If you launch napari from a Python script, you need to call `napari.run()` to
start the event loop and show the GUI.
In a Jupyter notebook, this is not necessary as Jupyter handles its own event loop.
```

# Screenshots in your notebook (5 min)

You can capture what's displayed in the viewer at any time:

```{code-cell} ipython3
from napari.utils import nbscreenshot
nbscreenshot(viewer)
# nbscreenshot(viewer, canvas_only=True)
```

### Add layers programmatically

Let's load the the common **Cells (3D + 2Ch)** dataset and add it as layers.

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
  blending='additive'
)
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

```{tip}
You can pass colormap, blending, opacity, contrast limits, and many other
parameters directly in `viewer.add_image()`. Check the
[docs](https://napari.org/stable/api/napari.Viewer.html#napari.Viewer.add_image)
for the full list.
```

### Exercise: Layer controls from Python

Try adjusting properties programmatically:

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
# Reset for next block
nuclei_layer.colormap = 'magenta'
nuclei_layer.contrast_limits = (0, np.max(nuclei))
nuclei_layer.opacity = 1.0
```

# Sharing Time (5 min)

- What did you notice about controlling layers from Python vs. the GUI?
- Any questions about the viewer or layer types?

Share a screenshot on the **#workshops** stream on
[Zulip](https://napari.zulipchat.com).

```{code-cell} ipython3
:tags: [remove-cell]
viewer.close()
```
