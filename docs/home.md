---
label: home
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

All materials here are self-guided and modular: each workshop is offered in more than
one session length, so you can pick the format that fits your time. Live,
instructor-led sessions are listed in the [workshop schedule](#events).

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

## Workshop catalogue

Each workshop is a family of modules taught at different session lengths. Pick a
workshop, then pick the length that fits your time.

| Workshop | What you'll learn | Level | Code experience |
|---|---|---|---|
| [Introduction to napari: the viewer](#intro-gui-90-overview) | Load, explore, and annotate multi-dimensional images; find and use community plugins — all in the napari bundled app | Beginner | None |
| [Introduction to napari: with Python](#extend-90-overview) | Control napari from Python: correct scales and units, and your own interactive widgets with magicgui | Beginner–intermediate | Some scripting (Python for the half-day session) |
| [napari express](#express-overview) | A fast tour for Pythonistas: build segmentation and classification workflows without leaving napari | Intermediate | Python |

## Running a workshop

Want to attend, host, or sponsor a workshop? Announcements and registration links appear
in the [workshop schedule](#events); for anything else, send us an e-mail at 
info@napari.org or reach out on our [Zulip](https://napari.zulipchat.com).

If you are teaching or organizing a session, start with the
[organizer guide](#organizer-guide) and the [instructor guide](#instructor-guide).

## Resources

- **napari documentation:** [napari.org](https://napari.org)
- **napari hub** (plugin directory): [napari-hub.org](https://napari-hub.org)
- **Community forum:** [forum.image.sc/tag/napari](https://forum.image.sc/tag/napari)
- **Zulip chat:** [napari.zulipchat.com](https://napari.zulipchat.com)

## Contributing

Found an issue or have suggestions? Contributions are welcome!
See [CONTRIBUTING.md](https://github.com/napari/workshops/blob/main/CONTRIBUTING.md) or open an issue on GitHub.
