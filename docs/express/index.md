---
label: express-overview
title: Overview
---

**Level:** Intermediate | **Duration:** 90 minutes | **Python required**

This workshop is a fast-paced tour through what napari can do for interactive
image and data analysis. Starting from pure-Python functions, you will
progressively integrate it with napari using `magicgui` widgets, customize
parameters with annotated sliders, compute quantitative features and do some
interactive classification — all without leaving napari's GUI.

By the end, you will have built complete interactive segmentation and
classification workflows, and know how to turn them into a reusable plugins.

```{tip} Drag'n'drop scripts for maximum speed
All standalone scripts from this workshop are available in the
[scripts directory](https://github.com/napari/workshops/tree/main/docs/express/scripts), from the download button at the top right on each page, and in buttons above the script code.

To quickly run one, you can also simply drag and drop the button/link onto the napari canvas!
```

## Workshop modules

1. [**From pure Python to interactive napari widget**](01_python_to_widget) —
   Start with a pure Python threshold function, convert it to a `magicgui`
   widget, and add interactive sliders with real-time updates.

2. [**Building a segmentation pipeline**](02_segmentation_pipeline) —
   Add morphological cleaning, connected-component labeling, quantitative
   features (area, centroid), Points layer visualization, and watershed
   refinement.

3. [**Adding interactive classification and going 3D**](03_classification_and_3d) —
   Make a new widget for interactively classifying objects based on their features,
   and then run the entire pipeline on 3D data with zero code changes.

## Prerequisites

- Completing the [installation instructions](#express-setup)
- Comfortable writing Python functions
- Basic familiarity with NumPy and scientific Python libraries
- Familiarity with the command line
