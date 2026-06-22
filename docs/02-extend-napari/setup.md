---
title: Setup and Installation
---

# Setup and Installation

This guide walks you through setting up your environment for the "Extending napari"
workshop. Unlike [Workshop 1](../01-intro-napari/setup.md), which uses the napari
bundled app, this workshop uses a Python environment and `pixi`.

## Prerequisites

- [**Git**](https://git-scm.com/) for cloning the repository (can also use a git GUI like [Github Desktop](https://desktop.github.com/download/))
- [**pixi**](https://pixi.sh/latest/#installation) for managing environments
- **Basic familiarity** with the terminal/command line

## Setup

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

> Under the hood, pixi features are `[dependency-groups]` in `pyproject.toml`.
> If you use uv instead, run `uv sync --group dev` for the full dependency set.
