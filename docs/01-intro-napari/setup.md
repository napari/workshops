---
label: intro-setup
title: Setup and Installation
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

The easiest way to install napari is the **napari bundled app**. It packages napari and
everything it needs into a single installer, just like any other desktop application. No
Python knowledge or command-line setup required.

```{note}
If you already have napari installed through another method (conda, pip, etc.) you are
welcome to use that instead. Version 0.6.6 or newer is fine for this workshop.
```

## Download and install the bundled app

Follow the official napari documentation for step-by-step instructions:

**[napari bundled app installation guide](https://napari.org/dev/getting_started/installation.html#installation-bundle-conda)**

The guide covers:

- Downloading the installer for your operating system (Windows, macOS, Linux)
- Running the installer
- Launching napari for the first time

## Verify your installation

Once napari is open you should see the napari viewer - an empty window with a layer list on
the left and a canvas in the centre. If it opens successfully, you are ready for the
workshop.

```{admonition} Problems installing?
:class: tip
Reach out to the workshop instructors or ask for help in the
[napari Zulip chat](https://napari.zulipchat.com/#narrow/stream/212875-general).
```

```{code-cell} python
:tags: [remove-cell]
import napari
from napari.utils import nbscreenshot
viewer = napari.Viewer()
```

```{code-cell} python
:tags: [remove-input]
nbscreenshot(viewer)
```

```{code-cell} python
:tags: [remove-cell]
viewer.close()
```
