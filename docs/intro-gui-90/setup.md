---
label: intro-gui-90-setup
title: Setup and Installation
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

The easiest way to install napari is the **napari bundled app**. It packages
napari and everything it needs into a single installer, just like any other
desktop application. No Python knowledge or command-line setup required.

```{note}
If you already have napari installed through another method (conda, pip, etc.)
you are welcome to use that instead. However, we strongly encourage using a
new, clean environment containing the newest version of napari.
```

```{important}
Please install the bundled app **before the workshop** — the download is
large and can take a while on a slower connection. If you run into trouble,
ask for help on [Zulip](https://napari.zulipchat.com); instructors are also
available on-site to help.
```

# Download and install the bundled app

Follow the official napari documentation for step-by-step instructions:

**[napari bundled app installation guide](https://napari.org/stable/getting_started/installation.html#installation-bundle-conda)**

The guide covers:

- Downloading the installer for your operating system (Windows, macOS, Linux)
- Running the installer
- Launching napari for the first time

# Verify your installation

Once napari is open you should see the napari viewer — an empty window with a
layer list on the left and a canvas in the center. If it opens successfully,
you are ready for the workshop.

```{tip} Having trouble?
If you have problems installing or launching napari, reach out to the workshop
instructors or ask for help in the
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
