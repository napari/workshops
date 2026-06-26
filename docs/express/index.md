---
label: express-overview
title: Overview
---

**Level:** Intermediate | **Duration:** 90 minutes | **Python required**

This workshop is a fast-paced tour through what napari can do for interactive
image analysis. Starting from a pure-Python segmentation function, you will
progressively integrate it with napari using `magicgui` widgets, customize
parameters with annotated sliders, compute quantitative features, add
interactive mouse callbacks, and see how everything works in 3D — all without
leaving napari's GUI.

By the end, you will have built a complete interactive cell segmentation
workflow and know how to turn it into a reusable plugin.

```{tip}
All standalone scripts from this workshop are available in the
[scripts directory](https://github.com/napari/workshops/tree/main/docs/express/scripts)
or from the download button on each page.
```

## Workshop modules

1. [**From Python to interactive napari widget**](01_python_to_widget) —
   Start with a pure Python threshold function, convert it to a `magicgui`
   widget, and add interactive sliders with real-time updates.

2. [**Building a segmentation pipeline**](02_segmentation_pipeline) —
   Add morphological cleaning, connected-component labeling, quantitative
   features (area, centroid), Points layer visualization, and watershed
   refinement.

3. [**Interactivity and 3D**](03_interactivity_and_3d) —
   Add a mouse callback for Shift+Click label inspection and run the entire
   pipeline on 3D data with zero code changes.

## Prerequisites

- Completing the [installation instructions](#express-setup)
- Comfortable writing Python functions
- Basic familiarity with NumPy and scientific Python libraries
- Familiarity with the command line
