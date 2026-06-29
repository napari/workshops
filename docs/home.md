---
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# napari workshops

[napari](https://napari.org) is a powerful open-source, multi-dimensional image viewer
built for scientific data analysis in Python. Whether you're a biologist exploring
microscopy data, an imaging specialist working with large datasets, or a data scientist
curious about what napari can do — these workshops are designed to meet you where you are.

No prior napari experience required. Some workshops require Python familiarity; the
introductory workshop uses napari's graphical interface and is accessible to all.

Live workshops are available — see the [workshop events](#events) for upcoming
sessions and past events.

```{code-cell} python
:tags: [remove-cell]
from pathlib import Path
import napari
from napari.utils import nbscreenshot

viewer = napari.Viewer()
viewer.open(Path() / '_resources' / 'kiribati.jpg')
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```

## [Introduction to napari 🖱️](#intro-overview)

**Level:** Beginner | **Duration:** ~4 hours

Get started with napari's bundled application. Load and explore multi-dimensional images,
annotate data, run interactive analysis, and discover community plugins. No Python
experience required, everything is done through the graphical interface!

## [Extending napari with code ⌨️](#extend-overview)

**Level:** Intermediate (napari Beginner) | **Duration:** ~4 hours

Write Python scripts that control napari programmatically, create interactive widgets
with magicgui, connect functions to layer events, implement mouse callbacks, and define
custom colormaps. Requires basic Python familiarity.

## [napari Express 🚀](#express-overview)

**Level:** Intermediate | **Duration:** 90 minutes

A quickstart tour through napari's capabilities for interactive image analysis.
Build a complete cell segmentation workflow using magicgui widgets, annotated
sliders, quantitative features, and mouse callbacks — all from Python.

## Resources

- **napari documentation:** [napari.org](https://napari.org)
- **napari hub** (plugin directory): [napari-hub.org](https://napari-hub.org)
- **Community forum:** [forum.image.sc/tag/napari](https://forum.image.sc/tag/napari)
- **Zulip chat:** [napari.zulipchat.com](https://napari.zulipchat.com)

## Contributing

Found an issue or have suggestions? Contributions are welcome!
See [CONTRIBUTING.md](https://github.com/napari/workshops/blob/main/CONTRIBUTING.md) or open an issue on GitHub.
