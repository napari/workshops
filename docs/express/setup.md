---
label: express-setup
title: Setup and Installation
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

This guide walks you through setting up your environment for the "napari Express"
workshop. This workshop uses a Python environment with `uv` or `pixi`.

# Prerequisites

- [**Git**](https://git-scm.com/) for cloning the repository (can also use a git GUI
  like [GitHub Desktop](https://desktop.github.com/download/))
- [**uv**](https://docs.astral.sh/uv/#installation) or [**pixi**](https://pixi.sh/latest/#installation)
  for environment management and running scripts. 

# Setup

[Install uv](https://docs.astral.sh/uv/#installation) with a single command, then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
uv sync --group express
uv run napari
```

A napari GUI window should open. If it does, your environment is ready for the workshop!

Or if you prefer pixi, [install pixi](https://pixi.sh/latest/#installation) with a single command, then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
pixi run -e express napari
```

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
