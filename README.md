# napari Workshops

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Welcome to the napari workshops repository! This collection provides comprehensive, hands-on training materials for learning napari - from basic visualization to plugin development.

##  Workshop Series

This repository contains three progressive workshops:

### [Workshop 1: Introduction to napari](https://napari.org/workshops/01-intro-napari/index.html)

**Level:** Beginner | **Duration:** 3-4 hours

Learn napari's GUI for bioimage visualization, manual annotation, and interactive analysis. Perfect for microscopists and biologists who want to explore their data interactively.

### [Workshop 2: Extending napari with Scripts](https://napari.org/workshops/02-extend-napari/index.html)

**Level:** Intermediate | **Duration:** 3-4 hours

Build custom analysis tools using magicgui widgets, event callbacks, and mouse interactions. Ideal for Python users who want to customize napari for their workflows.

### [Workshop 3: Developing napari Plugins](https://napari.org/workshops/03-develop-napari-plugins/index.html)

**Level:** Intermediate - Advanced | **Duration:** 3-4 hours

Package and share your tools as napari plugins. Learn about plugin architecture, testing, publishing, and maintenance.

##  Getting Started

### Installation

Clone the repository and install the environment with your preferred tool:

**pixi (recommended)** — installs napari, Qt, and all workshop deps from conda-forge:
```bash
git clone https://github.com/napari/workshops.git
cd workshops
pixi install          # resolves + installs everything
pixi run -- napari    # test the napari viewer
pixi run -- jupyter lab
```

**uv** — pure PyPI install, no conda required:
```bash
git clone https://github.com/napari/workshops.git
cd workshops
uv sync --group dev
uv run napari
uv run jupyter lab
```

**conda** — traditional approach, see the full [installation guide](shared/installation.md):
```bash
conda create -n napari-workshops -c conda-forge python=3.12 napari pyqt \
    napari-animation matplotlib jupyterlab jupytext jupyterlab-myst
conda activate napari-workshops
```

### Cloud Options

Can't install locally? You can run these workshops in the cloud:

- **Nebari** (recommended): See [cloud setup guide](shared/cloud_setup.md)
- **Binder** (free, but limited): Click the badge at the top of any notebook

##  Workshop Materials

All workshops include:

-  Detailed narrative explanations
-  Executable Jupyter notebooks (MyST Markdown format)
-  Sample data and images
-  Hands-on exercises
-  Learning objectives and prerequisites

##  Contributing

We welcome contributions! Whether it's fixing typos, improving explanations, or adding new content:

1. Fork this repository
2. Create a branch for your changes
3. Submit a pull request

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Building the Documentation

```bash
# pixi (recommended)
pixi install
pixi run build   # executes notebooks + builds static site

# uv
uv sync --group dev
uv run python scripts/copy_theme_css.py   # generate CSS
uv run jupyter-book build --html --execute --strict
```

The built site will be in `_build/html/`.

##  Resources

- **napari documentation:** [napari.org](https://napari.org)
- **napari hub:** [napari-hub.org](https://napari-hub.org)
- **Community forum:** [image.sc/tag/napari](https://forum.image.sc/tag/napari)
- **Zulip chat:** [napari.zulipchat.com](https://napari.zulipchat.com)
- **GitHub:** [github.com/napari/napari](https://github.com/napari/napari)

##  License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

These workshops are developed and maintained by the napari community. Special thanks to:

- The napari core development team
- All workshop contributors and instructors
- The Chan Zuckerberg Initiative for supporting napari development
- The broader scientific Python community

---

**Ready to start?** Head to [Workshop 1](https://napari.org/workshops/01-intro-napari/index.html) to begin your napari journey!
