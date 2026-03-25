---
label: intro-block1
title: "1. Welcome and First Images"
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

**Goal:** Get napari installed and open your first images.

# Welcome (10 min)

- Introduce instructors and helpers
- Share the [Code of Conduct](https://napari.org/stable/community/code_of_conduct.html)
- Ask about accessibility needs (private DMs ok)
- Share the Etherpad shared-notes link; invite participants to add an
  icebreaker answer: *"What field are you from, and what kind of images do
  you work with?"*
- Zoom etiquette
  - Cameras tend to improve the experience, but it's ok to keep off
  - 👍 reaction = ready to continue; ✋ = stuck/question
  - If asking questions in chat, please send them to everyone unless it needs to be private

# Download napari

napari comes as a **bundled application** — a single installer, just like any
other desktop app. No Python or command line required.

1. **Download:** Go to [napari.org](https://napari.org/stable/getting_started/installation.html#installation-bundle-conda) and download the installer for your OS (Windows, macOS, or Linux).
2. **Install:** Run the installer and follow the on-screen prompts.
3. **Launch:** Open napari from your Applications folder / Start Menu / desktop shortcut.

# About napari (10 min)

napari is a free, open-source, multi-dimensional image viewer for Python and
scientific image analysis. It is:

- **Community-driven** — built by scientists, for scientists
- **Extensible** — hundreds of plugins on [napari-hub.org](https://napari-hub.org)
- **Interoperable** — works with NumPy arrays, tiff files, zarr, and more
- **Interactive** — explore and annotate your data with a handy GUI

# Install the downloaded bundle

# napari Demo (10 min)

# Installation Check-in (5 min)

```{tip}
The first launch can take up to a minute. Subsequent launches are much faster.
```

Everyone should now have napari open. You should see:

- An empty **canvas** in the centre
- A **layer list** panel on the left
- A **layer controls** panel on the top-left
- **Viewer buttons** at the bottom of the canvas

If napari is open, give a 👍 as a Zoom reaction.

```{code-cell} python
:tags: [remove-cell]
import napari
from napari.utils import nbscreenshot

viewer = napari.Viewer()
```
```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

# What Are Images? (10 min)

Before diving into napari, a quick conceptual grounding:

- **Images are arrays of numbers** — each pixel has a value (brightness, intensity)
- **n-dimensional images** — beyond rows and columns in an array, images can have more array indexes
- **zero-based indexing** — the first element/pixel is at position 0, not 1
- A not-so standard **convention** TZYX ordering for time, depth, height, and width dimensions
- **multi-channel images**  — can be just another dimension in the array (e.g. RGB(A) is shape height, width, 3 (or 4))
- **labels** — images where pixel values are integers representing categories (e.g. 0=background, 1=cell1, 2=cell2, etc.)

napari can display all of these — the dimension sliders let you navigate indexes
beyond the 2D canvas.

# Open Your First Image (5 min)

1. In napari, select: **File > Open Sample > napari builtins > Cells (3D + 2Ch)**
2. Two layers appear in the layer list: `membrane` and `nuclei`
3. Use the **dimension slider** at the bottom to scroll through z-slices
4. Toggle each layer on/off with the **eye icon** next to its name

```{tip}
Shortcut: open the command palette with `Ctrl+Shift+P` (Windows/Linux) or
`Cmd+Shift+P` (macOS) and search for *"Cells 3D"*.
```

> **What you're looking at:** Confocal microscopy images of cells in 3D.
> The `nuclei` channel (channel 1) shows cell nuclei stained with a dye.
> The `membrane` channel (channel 0) shows cell membranes.

```{code-cell} python
:tags: [remove-cell]
viewer.open_sample('napari', 'cells3d')
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

# Screenshots (5 min)

Save what you see in napari at any time:

- **File > Save Screenshot...** — saves the canvas as an image file
- **File > Save Screenshot with Viewer** — saves the canvas plus the entire GUI
- **File > Copy Screenshot to Clipboard** — paste it directly into a document or chat

Keyboard shortcut: `Alt+S` (saves to file) or `Alt+C` (copies to clipboard). Add Shift to include the viewer UI: `Alt+Shift+S` or `Alt+Shift+C`.

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer=viewer,canvas_only=True)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```
