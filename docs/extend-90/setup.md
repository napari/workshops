---
label: extend-90-setup
title: Setup and Installation
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

This workshop uses a Python environment managed with **pixi**, and Jupyter
notebooks. Unlike the [GUI workshop](#intro-gui-90-overview), which uses the
napari bundled app, here you run napari from a Python environment you set up
on your own machine.

# Setup

```{important}
Please complete this setup **before the workshop** — the first run 
downloads napari and its dependencies and takes a few minutes. If you
previously set up your environment and the instructor updated the
configuration, the easiest fix is `pixi clean -e extend` followed by
re-running the command above. Running into trouble? Ask on
[Zulip](https://napari.zulipchat.com).
```

1. **Install pixi** for running the workshop environment with a single command;
   see the [pixi installation page](https://pixi.sh/latest/#installation).
2. [Download the workshop files as a ZIP](https://github.com/napari/workshops/archive/refs/heads/main.zip)
   and unpack them, or
   [clone the repository](https://github.com/napari/workshops) with git.
   All data files used in this workshop are included in the workshop files
   you downloaded — you do not need to download anything separately.
3. **Open a terminal in that folder** and run:

```bash
pixi run -e extend napari
```

A napari window should open. If it does, your environment is ready for the
workshop.

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
