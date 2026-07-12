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

[Install pixi](https://pixi.sh/latest/#installation) with a single command,
then make a shallow clone of the napari workshops repository and use pixi to
run the `extend` environment with the `napari` task:

```bash
git clone --depth 1 https://github.com/napari/workshops.git napari-workshops
cd napari-workshops
pixi run -e extend napari
```

A napari GUI window should open. If it does, your environment is ready for the workshop!

```{admonition} Workshop data
:class: note
All data files used in this workshop are included in the repository under
`docs/extend/data/`. You do not need to download anything separately.
```

```{admonition} Problems?
:class: tip
Reach out to the workshop instructors on the slack channel or ask for help in the
[napari Zulip chat](https://napari.zulipchat.com/#narrow/stream/212875-general).

If you previously set up your environment and the instructor updated the config,
Then you may need to run `pixi update` to get the latest environment, and in the
worst case scenario may have binary dependency conflicts. The easiest way to
resolve this is `pixi clean -e extend` to remove the environment, and then
re-run `pixi run -e extend napari` to get a fresh environment.
```

```{code-cell} ipython3
:tags: [remove-cell]

import napari
from napari.utils import nbscreenshot
viewer = napari.Viewer()
```

```{code-cell} ipython3
:tags: [remove-input]

nbscreenshot(viewer)
```

```{code-cell} ipython3
:tags: [remove-cell]

viewer.close()
```
