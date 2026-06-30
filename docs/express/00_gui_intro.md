---
label: lightning-gui-intro
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
  - file: scripts/00_lightning_gui_intro.py
    title: "Script 00 — Quick introduction to the napari GUI"
---

# Lightning introduction to the napari GUI

Before we start working with python, image processing and creating a workflow,
let's take a moment to familiarize with the napari graphical user interface (GUI).

Run the first script to start a quick tour of the GUI:

{button}`00_lightning_gui_intro.py <./scripts/00_lightning_gui_intro.py>`

```{tip} Rememeber
All scripts mentioned in a page are available on the download button at the top right,
as well as in button such as the one above. Drag and drop it into napari!.
```

```{warning}
This quick intro is mostly designed as a support for interactive teaching.

While this is neat, napari is not designed as a presentation tool, so you may
have to play around with the viewer size and resetting the view in order to
see all the various parts 😉
```

```{code-cell} python
:tags: [remove-input]

from pathlib import Path

import napari
from napari.utils import nbscreenshot
import numpy as np

print(__doc__)

viewer = napari.Viewer()

labels = viewer.add_points(
    data=np.array(
        [
            [0, 20, 70],
            [1, 50, 45],
            [2, 55, 15],
            [3, 35, 15],
            [4, 10, 15],
            [5, 10, 50],
            [6, 50, 70],
        ]
    ),
    size=2,
    face_color='transparent',
    border_width=0,
    text={
        'values': [
            'napari\nfundamentals',
            'dims sliders',
            'viewer buttons',
            'new layer buttons\nand layerlist',
            'layer controls',
            'menus',
            'Ctrl+Shift+p:\ncommand palette',
        ],
        'anchor': 'lower_left',
        'size': 20,
        'color': 'white',
    },
    units='m',
)

arrows = viewer.add_vectors(
    data=np.array(
        [
            [[1, 55, 55], [0, 8, 0]],
            [[2, 60, 14], [0, 5, -5]],
            [[3, 38, 14], [0, 0, -8]],
            [[4, 13, 14], [0, 0, -8]],
            [[5, 10, 49], [0, -5, -5]],
        ]
    ),
    edge_color='white',
    edge_width=1,
    vector_style='arrow',
    units='m',
)


logo = viewer.open(
    Path('../../docs/_resources/logo-dark.png'),
    scale=[0.015, 0.015],
    translate=[7, 75],
    interpolation2d='spline36',
    units='m',
)

viewer.dims.axis_labels = 'slides', 'y', 'x'
viewer.dims.point = (0, 0, 0)
viewer.reset_view()

nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

Key elements of the GUI:

1. Dims sliders:
    - allows scrolling through nondisplayed dimensions (in this case the "slides" dimension)
    - you can use arrow keys or ctrl+scroll to move the slider
    - right click on the slider handle to adjust slicing thickness (lets you see across multiple slices)
2. Viewer buttons:
    - general controls that are used often
    - ipython console (2-way interactivity between code and viewer)
    - 3d/2d toggle (try it, and see how this presentation is just a 3D image!)
    - dimension order controls
    - grid mode (useful for side-by-side when multiple layers are present)
    - home button (reset view)
3. New layer buttons and layerlist:
    - create new layers based on existing layers for annotation
    - points / shapes / labels
    - select, reorder and enable layers via the layerlist
4. Layer controls:
    - show current layer controls, depending on the selected layer
    - simple common things like opacity
    - more complex things like modes and layer-specific parameters (e.g: image colormap)
    - the rest they can play with afterwards
5. Menus:
    - many options (some are empty, extensible by plugins)
    - some typically used are scale bar and axes (in View, tried them out!)
6. Command palette:
    - many actions (present in menus or not) can be accessed easily with this

## Play around!

To better familiarize yourself with all the GUI components above, try opening some sample data
(e.g: `File -> Open Sample -> napari builtins -> Cells (3D+2Ch)`, or by searching it through the command palette via `Ctrl+Shift+p`). Take some time to play around!
