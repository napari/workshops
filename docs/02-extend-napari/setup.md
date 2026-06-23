---
label: extend-setup
title: Setup and Installation
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

This guide walks you through setting up your environment for the "Extending napari"
workshop. Unlike [Workshop 1](#intro-setup), which uses the napari
bundled app, this workshop uses a Python environment and `pixi`.

# Prerequisites

- [**Git**](https://git-scm.com/) for cloning the repository (can also use a git GUI like [Github Desktop](https://desktop.github.com/download/))
- [**pixi**](https://pixi.sh/latest/#installation) for running the workshop tasks and environment management

# Setup

[Install pixi](https://pixi.sh/latest/#installation) with a single command, then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
pixi run -e extend napari
```

A napari GUI window should open. If it does, your environment is ready for the workshop!

```{admonition} Problems?
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
