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
instructor-led sessions are listed on the [Events](#events) page.

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
| [Introduction to napari: with the App](#intro-overview) | Load, explore, and annotate multi-dimensional images; find and use community plugins — all in the napari bundled app | Beginner | None |
| [Introduction to napari: with Python](#extend-overview) | Control napari from Python: correct scales and units, and your own interactive widgets with magicgui | Beginner–intermediate | Some scripting (Python knowledge needed for the half-day schedule) |
| [napari express](#express-overview) | A fast tour for Pythonistas: build segmentation and classification workflows without leaving napari | Intermediate | Python |

## About this site

This site is the home for workshops about napari:

- **Workshop catalogue** (the workshops in the sidebar): self-guided workshop
  materials, maintained by the napari team and free for anyone to learn from
  or teach with.
- **[Events](#events)**: upcoming and past live workshops, both those taught
  by the napari team and those organized by the community.
- **[Past workshops](#past-workshops)**: a record of workshops and tutorials
  about napari that community members have developed and taught over the
  years.
- **Instructors**: the [organizer guide](#organizer-guide) and
  [instructor guide](#instructor-guide), for anyone running a session.

## Running a workshop

Want to attend, host, or sponsor a workshop taught by the napari team?
Announcements and registration links appear on the [Events](#events) page;
for anything else, send us an e-mail at info@napari.org or reach out on our
[Zulip](https://napari.zulipchat.com).

Want to run your own workshop about napari? You are welcome to teach with
the catalogue materials as they are, adapt them, or build your own. Either
way, the [organizer guide](#organizer-guide) and the
[instructor guide](#instructor-guide) are a good place to start. Let us know
about your workshop and we will list it on the [Events](#events-community)
page, and afterwards on [Past workshops](#past-workshops).

## Resources

- **napari documentation:** [napari.org](https://napari.org)
- **napari hub** (plugin directory): [napari-hub.org](https://napari-hub.org)
- **Community forum:** [forum.image.sc/tag/napari](https://forum.image.sc/tag/napari)
- **Zulip chat:** [napari.zulipchat.com](https://napari.zulipchat.com)

## Contributing

Found an issue or have suggestions? Contributions are welcome!
See [CONTRIBUTING.md](https://github.com/napari/workshops/blob/main/CONTRIBUTING.md) or open an issue on GitHub.
