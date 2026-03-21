---
label: intro-schedule
title: Session Schedule
---

# Session Schedule

**Total time:** ~4 hours | **Format:** 50 minutes instruction → 10 minutes break × 4

## Block 1 — Welcome and First Images (50 min)

**By the end of this block you will:** have napari installed, open an image,
and see your data in 2D and 3D.

| # | Segment | Time |
|---|---------|------|
| 1 | Welcome + introductions | 10 min |
| 2 | Download the napari bundle | 5 min |
| 3 | About napari: community, open source, plugins | 10 min |
| 4 | Install the bundle | 5 min |
| 5 | **Demo first** — instructor opens a large image, toggles 3D | 10 min |
| 6 | Installation check-in — everyone confirms napari opens | 5 min |
| 7 | What is an image? Pixels, arrays, dimensionality | 5 min |

**Welcome format:**
- Introduce instructors and helpers
- Share the [Code of Conduct](https://napari.org/stable/community/code_of_conduct.html)
- Ask about accessibility needs (private DMs ok)
- Share the HackMD shared-notes link; invite participants to add an
  icebreaker answer: *"What field are you from, and what kind of images do
  you work with?"*
- Zoom etiquette
  - Cameras tend to improve the experience, but it's ok to keep off
  - 👍 reaction = ready to continue; ✋ = stuck/question
  - If asking questions in chat, please send them to everyone unless it needs to be private

## Break (10 min)

## Block 2 — Exploring the napari GUI (50 min)

**By the end of this block you will:** navigate the napari interface
confidently, adjust visualizations, open and save files, and take screenshots.

| # | Segment | Time |
|---|---------|------|
| 8 | Open first sample image — RGB (skin) and multichannel (Cells 3D) | 10 min |
| 9 | **"I" demo:** Instructor-guided GUI walkthrough | 20 min |
| 10 | **"You" exercise:** Personal exploration + breakout rooms | 12 min |
| 11 | **Sharing time:** What did you discover? | 5 min |
| 12 | Load and save images; take screenshots | 3 min |

**Instructor GUI walkthrough covers** ([full lesson](01_napari_gui.md)):
- Layer controls, layer list, viewer buttons
- 2D ↔ 3D toggle; rotate and zoom
- Dimension sliders; merging/splitting stack channels
- Contrast limits, colormap, blending modes
- Scale bar; adding a Labels layer; save / screenshot

**"You" exercise — Gallery exploration:**

Open the [napari gallery](https://napari.org/dev/gallery) in a browser tab.
You can drag any gallery `.py` script file 
(from the links at the bottom of each example) directly
onto the napari canvas and it will run immediately — no terminal needed!
This is possible because napari has a (.py) reader, and works just like dragging and dropping an image. 
You can also download the script and drag it in.
Pick any example that looks interesting and try it.
Some examples will not be able to run because they have dependencies
that are not in the bundle, but most will work!

## Break (10 min)

## Block 3 — Plugins and Annotation (50 min)

**By the end of this block you will:** install plugins from the napari hub,
use napari-metadata to understand image scales and units, and annotate images
with Points, Shapes, and Labels layers.

| # | Segment | Time |
|---|---------|------|
| 13 | Introduction to the napari hub | 5 min |
| 14 | Install napari-metadata and napari-skimage | 5 min |
| 15 | **"I" demo:** napari-metadata — inspecting and setting scale, units, axis labels | 10 min |
| 16 | What is annotation? Raster vs vector; when and why to annotate | 5 min |
| 17 | **"We":** Annotate together — Points to mark nuclei, Shapes to outline a region | 10 min |
| 18 | **"You" exercise:** Annotation in breakout rooms | 10 min |
| 19 | Sharing time | 5 min |

**napari hub intro covers** ([full lesson](05_using_plugins.md)):
- What plugins are and what they can do (readers, writers, widgets, sample data)
- How to find plugins on [napari-hub.org](https://napari-hub.org)
- How to install from within napari: **Plugins > Install/Uninstall Plugins**

**napari-metadata demo covers:**
- Opening the metadata dock widget (**Plugins > napari-metadata: Metadata Widget**)
- Reading the current scale and axis names
- Setting physical scale (e.g. microns per pixel) and units
- How scale affects the scale bar display

**Annotation "You" exercise:**
- Use the nuclei image from Block 2
- Mark at least 3 cell centres with the Points layer
- Outline any region of interest with a Shapes layer
- Use the Labels paintbrush to paint one cell

## Break (10 min)

## Block 4 — Interactive Analysis and Next Steps (50 min)

**By the end of this block you will:** run image filtering and segmentation
through plugin menus, measure region properties from a Labels layer, and know
where to go from here.

| # | Segment | Time |
|---|---------|------|
| 20 | **"I" demo:** napari-skimage — filter, threshold, segment | 15 min |
| 21 | **"We":** End-to-end workflow together | 10 min |
| 22 | Console peek: a brief look at programmatic access | 5 min |
| 23 | Where to go from here: resources, community, next workshops | 10 min |
| 24 | Survey + wrap-up | 10 min |

**napari-skimage end-to-end workflow covers** ([full lesson](05_using_plugins.md)):
1. Open or reload the nuclei layer (Cells 3D sample)
2. **Layers > Filter > Filtering > Gaussian filter** — reduce noise
3. **Layers > Filter > Thresholding** — threshold to binary
4. **Layers > Measure > Regionprops (labels)** — measure the Labels layer
5. Save results to CSV from the measurement table widget

**Console peek** (brief — not the focus for this workshop):
```python
# How many nuclei did we find?
import numpy as np
labels = viewer.layers['nuclei labels'].data
print(f"Number of labelled nuclei: {np.max(labels)}")
```

**Resources to share:**
- napari documentation: [napari.org/stable](https://napari.org/stable/)
- napari tutorials: [napari.org/stable/tutorials](https://napari.org/stable/tutorials/)
- napari hub (plugin search): [napari-hub.org](https://napari-hub.org)
- Community forum: [forum.image.sc/tag/napari](https://forum.image.sc/tag/napari)
- Zulip chat: [napari.zulipchat.com](https://napari.zulipchat.com)
- napari gallery: [napari.org/stable/gallery](https://napari.org/stable/gallery)
- These workshop materials (self-guided): [napari.org/workshops](https://napari.org/workshops/)
- **Next workshop:** see [schedule](../schedule.md)

**Survey:** Share the link in Zoom chat and the HackMD in the final 10 minutes.
