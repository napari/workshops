---
label: block4-analysis
title: "4. Interactive Analysis and Next Steps"
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

**Goal:** Run a complete filter → threshold → segment → measure workflow
using a plugin GUI, take a brief look at the napari console, and learn where
to go from here.

# napari-skimage Segmentation Demo (5 min + 20 min hands-on)

[napari-skimage](https://napari-hub.org/plugins/napari-skimage)
provides GUI access to common image-processing steps powered by scikit-image —
no code required.

**Install it:**
1. **Plugins > Install/Uninstall Plugins…** → search `napari-skimage` → Install
2. Restart napari

## Workflow 

Use **File > Open Sample > napari builtins > Cells (3D + 2Ch)** as your starting image.

| Step | What to do | Why |
|------|-----------|-----|
| 1. Load | Open Cells (3D + 2Ch) | Your raw data |
| 2. Filter | **Layers > Filter > Filtering > Gaussian filter** — apply to `nuclei` | Reduce noise |
| 3. Threshold | **Layers > Filter > Thresholding > Automated Threshold** — apply Otsu to the filtered layer. The threshold output is a binary Labels mask. | Separate foreground from background |
| 4. Label | **Layers > Segment > Label connected components** on the mask to generate a new Labels layer with a unique ID (and color) for each object.  | Each connected region gets a unique integer ID |
| 5. Measure | **Layers > Measure > Regionprops (labels)** — select the Labels and nuclei layers | Outputs a table of features e.g. area, intensity, eccentricity per cell |
| 6. Save | Click **Save Results** in the Regionprops widget | Export measurements for further analysis |

```{tip}
Make sure you look through all your z-slices when gauging whether a
particular filter or thresholding algorithm worked as expected!
```

```{code-cell} python
:tags: [remove-cell]
import napari
import numpy as np

from scipy import ndimage as ndi
from skimage import data, filters, morphology
from napari.utils import nbscreenshot


cells3d = data.cells3d()
viewer = napari.Viewer()
membranes_layer, nuclei_layer = viewer.add_image(
    cells3d, channel_axis=1, name=['membranes', 'nuclei']
)
membrane, nuclei = cells3d.transpose((1, 0, 2, 3)) / np.max(cells3d)
edges = filters.scharr(nuclei)
denoised = ndi.median_filter(nuclei, size=3)
thresholded = denoised > filters.threshold_li(denoised)
cleaned = morphology.remove_small_objects(
    morphology.remove_small_holes(thresholded, 20**3),
    20**3,
)

segmented = ndi.label(cleaned)[0]

labels_layer = viewer.add_labels(segmented)

# viewer.dims.current_step = (27, 0, 0)
viewer.dims.ndisplay=3
viewer.camera.angles = (-20, 35, -40)
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

# Sharing Time and Q&A (5 min)

- How many nuclei did your segmentation find?
- What measurements were in the regionprops table?
- Open questions about the workflow or napari in general?

# Where to Go From Here (5 min)

## Learning Resources

| Resource | Link |
|----------|------|
| napari documentation | [napari.org/stable](https://napari.org/stable/) |
| Gallery | [napari.org/stable/gallery](https://napari.org/stable/gallery) |
| Plugin search | [napari-hub.org](https://napari-hub.org) |

## Community & Getting Help

| Channel | Description |
|---------|------|
| [Image analysis forum](https://forum.image.sc/tag/napari) | Ask questions about using napari, how to perform different image analysis tasks, and get help from experienced image analysts. |
| [Zulip chat](https://napari.zulipchat.com) | Chat with the napari community - developers, users and contributors. Ask questions, share your analyses, or just lurk for info! |
| [napari GitHub](https://github.com/napari/napari) | Participate in development, report bugs and request new features. |

## Next Steps

- Try opening one of **your own images** in napari
- Browse [napari-hub.org](https://napari-hub.org) for plugins relevant to your field
- Add a new example or sample data to napari!

# Survey + Wrap-up (10 min)

Please fill in the post-workshop survey (link shared by instructors).

Your feedback helps improve these materials and future workshops —
thank you for participating!
