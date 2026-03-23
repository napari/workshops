(extend-napari)=

# Workshop 2: Extending napari with Scripts

**Level:** Intermediate  
**Duration:** 3-4 hours

## Overview

This workshop teaches you how to extend napari's functionality through scripting and custom code. You'll learn to create interactive widgets using magicgui, respond to layer events, handle mouse interactions, and customize napari's appearance. This workshop bridges the gap between using napari as a GUI application and developing custom analysis tools, providing the foundation needed for plugin development.

## Learning Objectives

By completing this workshop, you will be able to:

- ✅ Write Python scripts that control the napari viewer programmatically
- ✅ Create interactive widgets from Python functions using magicgui
- ✅ Connect functions to layer events for dynamic analysis
- ✅ Implement custom mouse callbacks for interactive editing
- ✅ Define and apply custom colormaps
- ✅ Build reproducible analysis workflows that combine napari with the scientific Python ecosystem
- ✅ Turn exploratory analysis into reusable, GUI-accessible tools

## Prerequisites

- Completion of [Workshop 1: Introduction to napari](../01-intro-napari/index.md) or equivalent napari experience
- Comfortable writing Python functions
- Basic familiarity with NumPy and scientific Python libraries
- Understanding of Jupyter notebooks

## Workshop Structure

This workshop is organized into six main modules that progressively build your skills:

### 1. Scripting Basics with napari
Transition from GUI-based interaction to programmatic control of napari.

**Topics covered:**
- Creating and manipulating viewers from Python
- Adding and removing layers programmatically
- Accessing and modifying layer properties
- Working with the bidirectional viewer-kernel connection

### 2. Exploratory Analysis: Spot Detection
Develop an exploratory analysis workflow for detecting spots in microscopy data.

**Topics covered:**
- Loading and visualizing data
- Testing image processing functions interactively
- Using scipy and scikit-image with napari
- Visualizing intermediate results as layers
- Iterative parameter exploration

### 3. From Functions to Widgets
Transform your analysis functions into interactive widgets using magicgui.

**Topics covered:**
- Understanding the magicgui decorator
- Type hints and automatic widget generation
- Connecting widgets to napari layers
- Creating compound widgets
- Widget styling and layout
- Making analysis reproducible and user-friendly

### 4. Mouse Callbacks & Layer Events
Create interactive tools that respond to user actions and layer changes.

**Topics covered:**
- Understanding napari's event system
- Connecting callbacks to layer events
- Implementing custom mouse interactions
- Image warping and transformation examples
- Building tools for manual annotation refinement

### 5. Custom Colormaps
Customize napari's appearance and improve data visualization.

**Topics covered:**
- Defining custom colormaps with matplotlib
- Applying colormaps to Image layers
- Creating perceptually uniform colormaps
- Using colormaps for scientific visualization
- Best practices for color selection

### 6. Keybindings (Coming Soon)
Add custom keyboard shortcuts to streamline your workflows.

**Topics covered:**
- Registering custom keybindings
- Creating keyboard-driven workflows
- Combining keybindings with functions
- Best practices for keybinding design

## Key Concepts

### magicgui: Function-to-GUI Magic

`magicgui` is the secret sauce that makes creating napari widgets easy. It automatically generates GUI elements from Python function signatures:

```python
from magicgui import magicgui

@magicgui
def threshold_image(image: "napari.layers.Image", threshold: float = 0.5):
    return image.data > threshold
```

This creates a widget with an image layer dropdown and a threshold slider!

### Event-Driven Architecture

napari uses an event-driven architecture via the `psygnal` library. Layers emit events when their properties change:

```python
def update_on_data_change(event):
    print(f"Data changed for layer: {event.source.name}")

layer.events.data.connect(update_on_data_change)
```

### Bridging GUI and Code

The power of napari comes from seamless integration between interactive GUI manipulation and programmatic control. Changes in code update the GUI, and GUI interactions are accessible from code.

## Practical Applications

Skills from this workshop enable you to:

- Build custom analysis workflows with interactive parameter tuning
- Create tools for manual annotation and quality control
- Develop lab-specific utilities without full plugin infrastructure
- Prototype plugin functionality before formal development
- Share analysis workflows with collaborators

## Getting Help

- **magicgui documentation:** [pyapp-kit.github.io/magicgui](https://pyapp-kit.github.io/magicgui)
- **napari events guide:** [napari.org/guides/events](https://napari.org/stable/guides)
- **Community forum:** `forum.image.sc/tag/napari`
- **Zulip chat:** [napari.zulipchat.com](https://napari.zulipchat.com)

## Next Steps

After completing this workshop:

- **Continue to [Workshop 3: Developing napari Plugins](../03-develop-napari-plugins/index.md)** to learn how to package your custom functionality as installable plugins
- Explore the [napari how-to guides](https://napari.org/stable/howtos/index.html) for advanced techniques
- Share your custom tools with the community!

---

```{tableofcontents}
```
