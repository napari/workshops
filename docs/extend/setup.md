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

- [**pixi**](https://pixi.sh/latest/#installation) for running the workshop tasks and environment management
- [**Git**](https://git-scm.com/) if you prefer cloning over downloading a ZIP

# Setup

```{important}
Please complete this setup **before the workshop** - the first run downloads
napari and its dependencies and can take a few minutes.
```

1. Install [pixi](https://pixi.sh/latest/#installation).
2. Get the workshop files using either method:

   - Clone with git:

     ```bash
     git clone --depth 1 https://github.com/napari/workshops.git napari-workshops
     cd napari-workshops
     ```

   - Or download as ZIP:

     [Download workshops as a ZIP](https://github.com/napari/workshops/archive/refs/heads/main.zip),
     unpack it, and open a terminal in the extracted folder.

3. Run the extend environment:

```bash
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
Reach out to the workshop instructors or ask for help in the
[napari Zulip chat](https://napari.zulipchat.com/#narrow/stream/212875-general).

If you previously set up your environment and the instructor updated the
configuration, first try `pixi update`. If that does not resolve issues,
the easiest reset is:

`pixi clean -e extend`

and then re-run `pixi run -e extend napari`.
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
