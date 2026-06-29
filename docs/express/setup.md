---
label: express-setup
title: Setup and Installation
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

This page walks you through setting up your environment for the **napari express 🚀**
workshop. We recommend using a Python environment managed with `uv` or `pixi`.

# Prerequisites

- [**Git**](https://git-scm.com/) for cloning the repository (can also use a git GUI
  like [GitHub Desktop](https://desktop.github.com/download/))
- either [**uv**](https://docs.astral.sh/uv/#installation) or [**pixi**](https://pixi.sh/latest/#installation)
  for environment management and running scripts. 

# Setup

Choose your preferred method (`uv` or `pixi`):

::::{tab-set}
:::{tab-item} uv
[Install uv](https://docs.astral.sh/uv/#installation) with a single command, then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
uv sync --group express
uv run napari
```
:::
:::{tab-item} pixi
[Install pixi](https://pixi.sh/latest/#installation) with a single command, then:

```bash
git clone https://github.com/napari/workshops.git
cd workshops
pixi run -e express napari
```
:::
::::

A napari window similar to the one below should open. If it does, your environment is ready for the workshop!

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


```{seealso} Problems?
:class: tip
Reach out to the workshop instructors or ask for help in the
[napari Zulip chat](https://napari.zulipchat.com/#narrow/stream/212875-general).
```
