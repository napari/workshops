#!/usr/bin/env python3
"""
Quick introduction presentation to the napari GUI.

Use the dimension slider at the bottom or the arrow keys to move
to the next slides.

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

Open some sample data (via menu or palette) and play around!
"""

from pathlib import Path

import napari
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
            [0, 0, 100],
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
            '',
        ],
        'anchor': 'lower_left',
        'size': 2,
        'color': 'white',
        'scaling': True,
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
    Path('./docs/_resources/logo-dark.png'),
    scale=[0.015, 0.015],
    translate=[7, 75],
    interpolation2d='spline36',
    units='m',
)

viewer.dims.axis_labels = 'slides', 'y', 'x'
viewer.dims.point = (0, 0, 0)
viewer.reset_view()
napari.run()
