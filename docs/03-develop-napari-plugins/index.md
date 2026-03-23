(develop-napari-plugins)=

# Workshop 3: Developing napari Plugins

**Level:** Advanced (but beginner-friendly!)  
**Duration:** 4-5 hours

## Overview

This workshop teaches you how to package your custom napari functionality as plugins that can be shared with the broader scientific community. You'll learn about the napari plugin ecosystem (npe2), how to structure plugins, contribute different types of functionality, test your code, and publish to PyPI and the napari hub. While this is an "advanced" workshop, it's designed to be accessible to developers who have completed the previous workshops or have equivalent experience.

## Learning Objectives

By completing this workshop, you will be able to:

- ✅ Understand the napari plugin ecosystem and npe2 architecture
- ✅ Use the napari plugin template to create well-structured plugins
- ✅ Implement different plugin contribution types (widgets, readers, writers, sample data)
- ✅ Convert magicgui widgets from Workshop 2 into plugin widgets
- ✅ Write tests for your plugin functionality
- ✅ Debug common plugin issues
- ✅ Publish plugins to PyPI and the napari hub
- ✅ Maintain and update plugins over time

## Prerequisites

- Completion of [Workshop 2: Extending napari with Scripts](../02-extend-napari/index.md) or equivalent experience with magicgui and napari scripting
- Comfortable with Python package structure and imports
- Basic familiarity with git and GitHub (helpful for publishing)
- Understanding of virtual environments and pip installation

## Workshop Structure

This workshop guides you through the complete plugin development lifecycle:

### 1. Plugin Overview & npe2 Architecture
Understand what plugins are and how they integrate with napari.

**Topics covered:**
- What is a napari plugin?
- The npe2 (napari plugin engine v2) architecture
- Plugin manifest files (napari.yaml)
- Contribution types and their use cases
- Browsing existing plugins for inspiration
- The plugin development lifecycle

### 2. Choosing Plugin Contributions
Decide what type of contribution(s) your plugin should provide.

**Topics covered:**
- Reader contributions for custom file formats
- Writer contributions for saving data
- Widget contributions for analysis tools
- Sample data contributions
- Theme contributions
- Combining multiple contributions in one plugin

### 3. Using the Plugin Template
Bootstrap your plugin with best practices baked in.

**Topics covered:**
- Using cookiecutter/copier with the napari plugin template
- Understanding the generated file structure
- Configuration files (pyproject.toml, napari.yaml)
- Setting up development environments
- Testing infrastructure

### 4. Building a Widget Plugin
Turn your magicgui widgets into a distributable plugin.

**Topics covered:**
- Converting Workshop 2 spot detection widget to a plugin
- Registering widget contributions in napari.yaml
- Handling layer inputs and outputs
- Plugin-specific best practices
- Making widgets user-friendly

### 5. Reader & Writer Plugins
Extend napari's file format support.

**Topics covered:**
- Implementing reader functions
- Supporting multiple file formats
- Implementing writer functions
- Testing readers and writers
- Handling metadata
- Best practices for I/O plugins

### 6. Testing & Debugging
Ensure your plugin is robust and maintainable.

**Topics covered:**
- Writing unit tests with pytest
- Testing with pytest-napari
- Using fixtures for napari viewer testing
- Debugging plugin loading issues
- Common pitfalls and solutions
- Continuous integration with GitHub Actions

### 7. Publishing & Maintaining Plugins
Share your plugin with the community and keep it updated.

**Topics covered:**
- Preparing for release (version, changelog, docs)
- Publishing to PyPI
- Submitting to the napari hub
- Setting up GitHub releases
- Versioning strategies
- Maintaining compatibility with napari updates
- Responding to user issues and PRs
- Deprecation and migration strategies

## Key Concepts

### Plugin Manifest (napari.yaml)

The `napari.yaml` file is the heart of your plugin. It declares what your plugin provides:

```yaml
name: napari-my-plugin
contributions:
  commands:
    - id: napari-my-plugin.spot_detection
      python_name: napari_my_plugin._widget:SpotDetector
      title: Detect Spots
  widgets:
    - command: napari-my-plugin.spot_detection
      display_name: Spot Detector
```

### Contribution Types

napari plugins can provide:

- **Readers**: Load data from custom file formats
- **Writers**: Save layers to custom file formats
- **Widgets**: Add analysis tools and GUI elements
- **Sample data**: Provide example datasets
- **Themes**: Customize napari's appearance

### Plugin Development Workflow

1. **Develop** functionality as scripts (Workshop 2)
2. **Package** using the plugin template
3. **Test** with pytest and pytest-napari
4. **Document** usage and API
5. **Publish** to PyPI
6. **Register** on napari hub
7. **Maintain** over time

## From Widget to Plugin: A Case Study

This workshop includes a complete case study of converting the spot detection widget from Workshop 2 into a published plugin, including:

- Repository structure
- Test suite
- Documentation
- CI/CD setup
- Release process

## Practical Considerations

### When to Build a Plugin

Build a plugin when you want to:

- Share tools with collaborators or the community
- Provide a well-tested, versioned analysis tool
- Contribute to the napari ecosystem
- Extend napari's file format support
- Create lab-specific analysis infrastructure

### Plugin Maintenance

Good plugins require ongoing maintenance:

- Keep compatible with napari updates
- Fix bugs reported by users
- Add features based on community needs
- Update dependencies
- Maintain documentation

We'll discuss strategies to make maintenance manageable!

## Resources

- **Plugin template:** [github.com/napari/napari-plugin-template](https://github.com/napari/napari-plugin-template)
- **npe2 documentation:** [napari.org/npe2](https://github.com/napari/npe2)
- **Plugin development guide:** [napari.org/plugins](https://napari.org/stable/plugins/index.html)
- **napari hub:** [napari-hub.org](https://napari-hub.org)
- **Community forum:** `forum.image.sc/tag/napari`

## Getting Help

- **Zulip #plugin-dev channel:** [napari.zulipchat.com](https://napari.zulipchat.com)
- **GitHub discussions:** [github.com/napari/napari](https://github.com/napari/napari)
- **Office hours:** Check the napari community calendar

## Next Steps

After completing this workshop:

- Build and publish your first plugin!
- Contribute to existing napari plugins
- Join the napari developer community
- Help others with plugin development questions
- Explore advanced topics like custom layer types

---

```{tableofcontents}
```
