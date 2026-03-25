---
label: block4-analysis
title: "4. Interactive Analysis and Next Steps"
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Block 4 — Interactive Analysis and Next Steps

**Duration:** ~50 min  
**Goal:** Run a complete filter → threshold → segment → measure workflow
using a plugin GUI, take a brief look at the napari console, and learn where
to go from here.

---

## 23. napari-skimage Segmentation Demo (5 min + 20 min hands-on)

[napari-skimage-regionprops](https://napari-hub.org/plugins/napari-skimage-regionprops)
provides GUI access to common image-processing steps powered by scikit-image —
no code required.

**Install it:**
1. **Plugins > Install/Uninstall Plugins…** → search `napari-skimage-regionprops` → Install
2. Restart napari

### Workflow (segments 23 + 25)

Use **File > Open Sample > napari builtins > Cells (3D + 2Ch)** as your starting image.

| Step | What to do | Why |
|------|-----------|-----|
| 1. Load | Open Cells (3D + 2Ch) | Your raw data |
| 2. Filter | **Plugins > napari-skimage-regionprops > Filtering > Gaussian** — apply to `nuclei` | Reduce noise |
| 3. Threshold | **Plugins > napari-skimage-regionprops > Thresholding** — apply Otsu to the filtered layer | Separate foreground from background |
| 4. Label | The threshold output is a binary layer — run **Label** to convert it to a Labels layer | Each connected region gets a unique integer ID |
| 5. Measure | **Plugins > napari-skimage-regionprops > Measure > Regionprops (labels)** — select the Labels and nuclei layers | Outputs a table of area, intensity, centroid per cell |
| 6. Save | Click **Save as CSV** in the measurement table widget | Export measurements for further analysis |

```{tip}
Work on a single z-slice first: set the dimension slider to slice 30, then
apply the workflow to the 2D image that appears. The full 3D workflow is the
same but takes longer to process.
```

````{note} Instructor screenshot — segmented nuclei
```python
import napari
import numpy as np
from skimage.data import cells3d
from skimage.filters import gaussian
from skimage.filters import threshold_otsu
from skimage.measure import label

viewer = napari.current_viewer()
data = cells3d()
nuclei = data[30, 1, :, :]  # single z-slice

smoothed = gaussian(nuclei, sigma=2)
thresh = threshold_otsu(smoothed)
binary = smoothed > thresh
labels = label(binary)

viewer.add_image(nuclei, name="nuclei", colormap="magenta", blending="additive")
viewer.add_labels(labels, name="nuclei labels")
```
````

---

## 24. Console Peek (5 min)

napari has a built-in **Python console** that advanced users and developers
use to interact with the viewer programmatically.

Open it with: **Window > Console**

```{note}
Code in the console is for **instructors and developers** — you won't need to
use it during this workshop. This is just a quick peek to show it exists.
```

Example you can paste to see a quick result:

```python
# How many cells did we find?
import numpy as np
labels = viewer.layers['nuclei labels'].data
print(f"Number of labelled regions: {np.max(labels)}")
```

The console also lets you access `viewer` directly to change colours,
positions, and layer properties — the starting point for scripting napari in
your own workflows.

---

## 26. Sharing Time and Q&A (5 min)

- How many nuclei did your segmentation find?
- What measurements were in the regionprops table?
- Open questions about the workflow or napari in general?

---

## 27. Where to Go From Here (5 min)

### Learning Resources

| Resource | Link |
|----------|------|
| napari documentation | [napari.org/stable](https://napari.org/stable/) |
| Tutorials | [napari.org/stable/tutorials](https://napari.org/stable/tutorials/) |
| Gallery | [napari.org/stable/gallery](https://napari.org/stable/gallery) |
| Plugin search | [napari-hub.org](https://napari-hub.org) |
| These workshop materials | [napari.org/workshops](https://napari.org/workshops/) |

### Community

| Channel | Link |
|---------|------|
| Image analysis forum | [forum.image.sc/tag/napari](https://forum.image.sc/tag/napari) |
| Zulip chat | [napari.zulipchat.com](https://napari.zulipchat.com) |
| GitHub | [github.com/napari/napari](https://github.com/napari/napari) |
| Twitter / X | [napari_imaging](https://twitter.com/napari_imaging) |

### Next Steps

- Try opening one of **your own images** in napari
- Browse [napari-hub.org](https://napari-hub.org) for plugins relevant to your field
- Work through the [self-guided lessons](index.md) at your own pace
- Attend the next workshop — see [Events](../events.md)

---

## 28. Survey + Wrap-up (10 min)

Please fill in the post-workshop survey (link shared by instructors).

Your feedback helps improve these materials and future workshops —
thank you for participating!
