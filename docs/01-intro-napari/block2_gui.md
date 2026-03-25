---
label: block2-gui
title: "2. Exploring the napari GUI"
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Block 2 — Exploring the napari GUI

**Goal:** Navigate the viewer confidently, adjust how images look, try the
napari gallery, and understand image metadata.

## 11. Instructor-guided GUI Walkthrough (25 min)

Follow along as the instructor walks through the major parts of the napari
interface using the **Cells (3D + 2Ch)** sample image.

Check out the [napari viewer documentation](https://napari.org/stable/tutorials/fundamentals/viewer.html) for a full walkthrough.

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

### The Viewer Layout

| Area | Purpose |
|------|---------|
| **Canvas** (center) | Where your image is displayed |
| **Viewer buttons** (bottom) | 2D/3D toggle, home, grid, axes, scale bar |
| **Layer list** (left) | All open layers; click to select, eye to toggle visibility |
| **Dimension sliders** (bottom) | Scrub through z, t, or other axes |
| **Layer controls** (top-left) | Adjust appearance of the selected layer |

### Key Interactions

- **Zoom:** scroll wheel (or two-finger scroll on trackpad)
- **Pan:** click and drag on the canvas, hold Shift to pan in 3D mode
- **Reset view:** click the **home button** (bottom-right row of viewer buttons)

### 2D ↔ 3D Toggle

Click the **2D/3D button** in the viewer button row to switch rendering modes.
In 3D mode you can click-drag to rotate the volume.

![viewer buttons](https://napari.org/dev/_images/viewer-buttons.png)

```{code-cell} python
:tags: [remove-cell]
viewer.dims.ndisplay = 3
viewer.camera.angles = (-27, 8, -58)
```
```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

### Dimension Sliders

When a layer has more dimensions than the viewer can display, sliders appear at the bottom of the
canvas. Drag a slider to move through z-slices, time points, or channels.

```{code-cell} python
:tags: [remove-cell]
viewer.dims.ndisplay = 2
viewer.dims.current_step = (23, 100, 100)
```
```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

You can rename the slider labels! Right click on the roll dimensions button and
double-click on the axis label to edit it. 

![Dims ordering](https://napari.org/stable/_images/dims_roll_lock_widget.png)

```{tip} See that indicator?
If you see a button with a chevron mark in the lower right corner,
it means you can click it with the right mouse button to bring up more advanced options!

![Right-click chevron](https://napari.org/stable/_images/button-right-click-indicator.png)
```

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

### Overlays

There are [viewer overlays](https://napari.org/stable/getting_started/viewer.html#viewer-overlays)
that can be added to the canvas. In this case we will add the Axes overlay to show 
the Axis Labels attached to the data. Go to **View > Axes > Axes Visible** to turn it on.

Try also to visualize the Color Bar (LUT) overlay for each layer by right clicking on the layer(s) that you want to visualize or toggle the color bar from the navbar menu **Layers > Measure > Color Bar**.

```{tip} Still haven't find what you're looking for?
The [Command Palette](https://napari.org/stable/getting_started/features.html#command-palette)
can be launched via **View > Command Palette** or with 
`Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).
This allows you to search for (almost all) napari commands by name and run them
with needing to remember menu location or keyboard shortcuts.
```

### Layer Controls

With a layer selected, [layer controls](https://napari.org/stable/getting_started/layers.html) at the top-left let you change:

- **Contrast limits** — adjust brightness/darkness and auto-contrast
- **Colormap** — the colour used to display intensity values
- **Blending** — how layers are composited
- **Opacity** — layer transparency

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

```{code-cell} python
:tags: [remove-cell]
viewer.dims.ndisplay = 3
membrane.rendering = 'attenuated_mip'
membrane.visible = False
nuclei.rendering = 'attenuated_mip'
```
```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

### Grid View

Grid Mode allows you to view multiple layers in separate panels at the same time.
This is especially useful for comparing channels in a multi-channel image.
You can enable it with the **grid button** in the viewer buttons (bottom row, second from the right).
You can right-click the grid button to adjust the number of rows and columns in the grid.

```{code-cell} python
:tags: [remove-cell]
viewer = napari.Viewer()
viewer.open_sample('napari', 'lily')
viewer.grid.enabled = True
```
```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

### Scale Bar

Enable the scale bar with **View > Scale Bar > Visible** navbar.
If all layers have consistent units, then the scalebar displays the physical scale.
If not, it defaults to pixels.

```{code-cell} python
:tags: [remove-cell]
viewer.grid.stride = 2
for l in viewer.layers:
    l.colorbar.visible = True
viewer.scale_bar.visible = True
```
```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

### Console Peek

napari has a built-in **Python console** that allows you to interact
with the viewer programmatically. Some features that
are not yet exposed through the GUI can be used via the console.

Open it from the menu with **Window > Console**, or click the leftmost
viewer button.

As an example, here we change the viewer scale bar units (you can't do
this through the GUI yet):

```{code-cell} python
viewer.scale_bar.unit = 'micrometer'
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

The console lets you access the `viewer` directly to programmatically
change different properties. You can also access individual
layers using `viewer.layers` — the starting point for scripting napari in
your own workflows.

## 12. Layer Metadata with napari-metadata  (5 min)

The [**napari-metadata**](https://napari.org/napari-metadata/)
plugin lets you view and edit layer metadata, including 
axis labels, scale, units physical scale and
axis labels of your layers — essential for making measurements in real units.

Open the widget: **Plugins > Layer metadata: Layer metadata**

There are three parts to the widget:
1. **File metadata** — read-only metadata from the file
2. **Axes metadata** — axis labels, physical scale, units, and more
3. **Copy metadata** — copy metadata from one layer to another

## 13. Gallery Exploration Breakout (15 min)

The [napari gallery](https://napari.org/stable/gallery) contains dozens of
example visualizations covering various layer types and use cases.

**To try a gallery example without any code:**

1. Open a gallery page that looks interesting: https://napari.org/stable/gallery
2. Scroll to the bottom of the example page and click **Download Python source**
3. Drag-and-drop the downloaded `.py` file onto the napari canvas
4. napari will run it automatically, adding the results to the viewer

```{note} Some examples require extra packages
Some examples require packages that are not in the bundle and will show an
error — just try another one. Most built-in examples work fine.
```

## 14. Sharing Time (5 min)

- What did you find in the gallery?
- Any surprising layer types or visualizations?
- Questions about the interface?
