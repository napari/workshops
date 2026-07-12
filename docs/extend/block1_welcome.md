---
label: extend-block1
title: "1. Welcome and GUI Walkthrough"
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

**Goal:** Set up your environment, get an overview of the workshop, and learn
your way around the napari viewer — from the GUI essentials to running example
scripts.

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
| **1** | Welcome and GUI Walkthrough — get oriented in the napari viewer |
| **2** | Python, Data, and Metadata — control napari from Python, set physical scales, work with xarray and Zarr |
| **3** | Custom Widgets and Interactions — build interactive GUIs with magicgui, keybindings, and mouse callbacks |
| **4** | From Script to Plugin — package your custom tools as pip-installable napari plugins |

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

# About napari (3 min)

[napari](https://napari.org) is a free, open-source, multi-dimensional image viewer for Python. It is:

- **Community-driven** — built by scientists, for scientists
- **Extensible** — hundreds of plugins on [napari-hub.org](https://napari-hub.org)
- **Interoperable** — works with NumPy, xarray, Zarr, TIFF, and more
- **Interactive** — explore and annotate your data with a GUI or from Python

# What Are Images? (3 min)

A quick conceptual grounding before we open our first image:

- **Images are arrays of numbers** — each pixel has an intensity value
- **n-dimensional** — images can have more dimensions than just height and width
- **Common convention**: TZYX — time, depth (z), height (y), width (x)
- **Labels** — images where pixel values are integer categories (0=background, 1=object1, etc.)
- **Scale and units** — each pixel corresponds to a real-world physical size

# Open Your First Image (5 min)

Let's get the viewer up and running with a sample dataset:

```bash
pixi run -e extend napari
```

1. In napari, select: **File > Open Sample > napari builtins > Cells (3D + 2Ch)**
2. Two layers appear in the layer list: `membrane` and `nuclei`
3. Use the **dimension slider** at the bottom to scroll through z-slices
4. Toggle each layer on/off with the **eye icon** next to its name

```{code-cell} python
:tags: [remove-cell]
import napari
from napari.utils import nbscreenshot
viewer = napari.Viewer()
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

# GUI Essentials Walkthrough (15 min)

Follow along as we walk through the major parts of the napari
interface.

```{hint} Something broken?
If you run into any issues, copy and paste the error message into the
**#napari-workshop-[DATE]** stream on [Zulip](https://napari.zulipchat.com)
so we can help — and improve the workshop for next time!
```

## The Viewer Layout

| Area | Purpose |
|------|---------|
| **Canvas** (center) | Where your image is displayed |
| **Dimension sliders** (bottom) | Scrub through z, t, or other axes beyond 2D |
| **Viewer buttons** (bottom-left) | 2D/3D toggle, home, grid, axes, scale bar |
| **Layer list** (left) | All open layers; click to select, eye to toggle visibility |
| **Layer controls** (top-left) | Adjust appearance of the selected layer |

## Key Interactions

- **Zoom:** right-click and drag or scroll wheel (two-finger scroll on trackpad)
- **Pan:** click and drag on the canvas — hold Shift to pan in 3D mode
- **Reset view:** click the **home button** in the viewer button row (bottom-left)

## Dimension Sliders

When a layer has more dimensions than the two displayed on the canvas, sliders
appear at the bottom. Drag a slider to move through z-slices, time points, or
channels.

```{code-cell} python
:tags: [remove-cell]
viewer.dims.ndisplay = 2
viewer.dims.current_step = (23, 100, 100)
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

You can rename the slider labels! Right-click the **roll dimensions button**
(bottom-left) and double-click an axis label to edit it.

![Dims ordering](https://napari.org/stable/_images/dims_roll_lock_widget.png)

```{tip} See that chevron?
If you see a button with a chevron mark » in the lower right corner, it means
you can **right-click** it to reveal more advanced options.

![Right-click chevron](https://napari.org/stable/_images/button-right-click-indicator.png)
```

## 2D ↔ 3D Toggle

Click the **2D/3D button** in the viewer button row to switch rendering modes.
In 3D mode, click-drag to rotate the volume. Give it a try!

![viewer buttons](https://napari.org/stable/_images/viewer-buttons.png)

```{code-cell} python
:tags: [remove-cell]
viewer.dims.axis_labels = ['Z', 'Y', 'X']
viewer.axes.visible = True
viewer.dims.ndisplay = 3
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

## Overlays

napari can display helpful overlays on the canvas. Here are the most useful ones:

- **Floating Axes**: **View > Axes > Floating Axes Visible** — shows axis labels in the corner of the canvas.
- **Scale bar**: **View > Scale Bar > Visible** — displays the physical scale in real-world units. We'll set units in Block 2.
- **Color bar**: Right-click a layer or use **Layers > Measure > Color Bar** — shows the colormap-to-intensity mapping for the selected layer.

```{tip} The Command Palette
Can't remember a menu location? Press `Ctrl+Shift+P` (Windows/Linux) or
`Cmd+Shift+P` (macOS) to open the **Command Palette**. Search for any napari
or plugin command by name — no menu navigation needed.
```

## Layer Controls

With a layer selected in the layer list, the layer controls panel (top-left)
lets you change how that layer appears. The most important controls:

- **Contrast limits** — the brightness range; drag the sliders or click "auto"
- **Colormap** — the colour used to map intensity values to pixels
- **Blending** — how overlapping layers are composited (try `additive`!)
- **Opacity** — layer transparency from 0 (invisible) to 1 (fully opaque)

```{code-cell} python
:tags: [remove-cell]
viewer.axes.visible = False
viewer.dims.ndisplay = 2
viewer.dims.current_step = (29, 100, 100)
nuclei = viewer.layers['nuclei']
nuclei.contrast_limits = (0, 40000)
nuclei.colormap = 'cyan'

membrane = viewer.layers['membrane']
membrane.contrast_limits = (0, 40000)
membrane.colormap = 'orange'
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

Try adjusting these controls yourself — change the colormap of `nuclei`, lower
the opacity of `membrane`, or switch the blending mode to `additive`. The
changes are immediate, which makes exploring your data fast and intuitive.

## Console Peek

napari has a built-in **Python console** — open it from **Window > Console**
or click the leftmost viewer button. It lets you interact with the viewer
programmatically while you explore:

```python
# Type this in the console and press Enter:
viewer.layers['nuclei'].colormap = 'viridis'
```

The console gives you access to the full napari Python API without leaving
the GUI. It's the bridge between point-and-click exploration and scripted
analysis.

# Opening Files from the Command Line

napari can also run Python scripts — it reads them and executes them
in the viewer. This is a great way to explore the napari gallery examples:

```bash
pixi run -e extend napari demos/everything.py
```

Drag-and-drop works too: download any `.py` file from the
[napari gallery](https://napari.org/stable/gallery) and drop it onto the
napari canvas. napari runs it automatically.

Speaking of which…

# Gallery Exploration Breakout (10 min)

```{admonition} Breakout
:class: tip
**Goal:** Try a napari gallery example and share what you found.

**Tasks:**

1. Open the [napari gallery](https://napari.org/stable/gallery) and find an example
   that looks interesting — see the [](#recommended-examples) list below for ideas.
2. Drag-and-drop the `.py` file Button onto the napari canvas.
3. Explore the result! Try adjusting colors, contrast, or the 3D view.

> **Note:** Some examples require extra packages and will show that with an
> adominition below the download buttons — just try another one.

**When you're done (or any time during the breakout):**
Take a screenshot and post it to the **#workshops** stream on
[Zulip](https://napari.zulipchat.com). 
Add a note: *what example did you try, and what surprised or interested you?*
```

(recommended-examples)=
## Recommended Examples

1. 3D Layer Bounding Box Overlay
2. Add points 3D
3. Anisotropic data with scale
4. Annotate segmentation with text
5. Colorbars and auto-tiling in grid mode
6. Displaying xarray data in napari
7. Heart with multiple annotations
8. Image points 3D
9. Labels 3D
10. Surface with texture and vertex colors
11. Tracks 3D

# Sharing Time (3 min)

- What did you find in the gallery? *(check the Zulip stream for screenshots!)*
- Any surprising layer types or visualizations?
- Questions about the interface before we dive into Python?

In **Block 2**, we'll switch from clicking to coding — controlling napari
entirely from Python, loading our own data, and setting physical scales
for real-world measurements.

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```
