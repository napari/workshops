---
label: sprints
title: napari sprint guide
---

A sprint is a quick and low-stakes group coding meetup where new and old contributors (and usually some core team members) meet to help each other with contributing to open source projects.

If you're joining one of our sprints, this page will give you a kickstart with finding something to work on, setting up your environment, and making the most out of your time with us!

## What to do

The napari project is organized over several repos:

- [napari/napari](https://github.com/napari/napari): main napari application/library development. Code, docstrings and gallery examples live here.
- [napari/docs](https://github.com/napari/docs): napari documentation, served on napari.org. 
- [napari/npe2](https://github.com/napari/npe2): Version 2 of the napari plugin engine.
- [napari/napari-plugin-manager](https://github.com/napari/napari-plugin-manager): napari plugin manager to provide a graphical user interface for installing napari plugins.
- [napari/napari-plugin-template](https://github.com/napari/napari-plugin-template): a copier-based template repo used to make new napari plugins
- [napari/hub-lite](https://github.com/napari/hub-lite): napari plugin hub served at https://napari.org/hub-lite/. Includes code for backend and frontend.
- [napari/workshops](https://github.com/napari/workshops): workshop materials.
- [napari/island-dispatch](https://github.com/napari/island-dispatch) Our blog!

<details>
  <summary>Expand to see other secondary repos</summary>

- [napari/npe2api](https://github.com/napari/npe2api): The rest API used by napari to query plugins
- [napari/bermuda](https://github.com/napari/bermuda): Rust implementation of spatial algorithms for napari, compiled for performance.
- [napari/napari-svg](https://github.com/napari/napari-svg): A plugin for writing svg files from napari
- [napari/napari-animation](https://github.com/napari/napari-animation): A napari plugin for making animations
- [napari/napari-metadata](https://github.com/napari/napari-metadata): A napari plugin for viewing and editing layer and viewer metadata.

</details>

[Issues labelled `contribute:sprint`](https://github.com/napari/napari/issues?q=state%3Aopen%20label%3Acontribute%3Asprint) or [`contribute:good-first-issue`](https://github.com/napari/napari/issues?q=state%3Aopen%20label%3A%22contribute%3Agood%20first%20issue%22) are a mix of code and documentation issues selected for newcomers.

If you do not see a suitable issue or you are interested in a particular napari repo, please look at the relevant repo labels or ask a mentor for a suggestion.

## How to do it

We have excellent guides helping (any) person get started with contributing to napari. If you find something difficult about contributing, whether practical or documentation, please work with us to improve these guides! 😁
-  [napari contributing guides](https://napari.org/stable/developers/index.html)
-  [Contributing documentation](https://napari.org/stable/developers/contributing/documentation/index.html)

The following documentation will help you set up and build a local development environment:
- [Setting up a development installation](https://napari.org/stable/developers/contributing/dev_install.html)

- As an alternative, you can use GitHub codespaces _(this works without having to install anything, get to coding straight away in the browser!)_. However, napari is not fully functional in codespaces (the data in the canvas cannot be seen, but the napari viewer can be interacted with), so consider if this is appropriate for working on your contribution.

![Screenshot 2025-07-08 at 1.25.53 PM](https://hackmd.io/_uploads/HJGaI6qrxe.png)

## Doing it!

* Please comment on the issue that you are working on to avoid multiple people taking on the same issue. We do not assign issues. Alternatively, team up with others (intentionally)!

* There are plenty of issues 😅! The selections labelled `contribute:sprint` and `contribute:good-first-issue` are focused on beginner-to-intermediate-friendly issues that are actionable and should be doable today. If you want to take on something a little more challenging, there are a lot of issues in the repo to choose from. If you search for an issue not labelled `contribute:sprint` or `contribute:good-first-issue`, try to choose issues that (from the title or labels) seem to be bugs, and don't have more than 5 comments - those are most likely to be actionable (old issues are often difficult to solve or unresolvable which is why they still remain.)

* First sprint? Welcome :wave: and relax :relaxed:. We encourage questions. Questions are how we learn something new and build skills; so, ask away. Your getting started steps for success (ask questions as needed :smile:):
    * Pick a repo. 
    * Set up a development environment.
    * Try to run the tests.
    * Work with a sprint mentor to find an issue.

---

## Tips and resources

#### Documentation issues

If you are working on documentation, remember to check against https://napari.org/dev/index.html. This is the version of the documentation corresponding to the latest development version (aka what is merged on the main branch on GitHub).

#### How to co-author commits

If you worked in a pair/group and would like to acknowledge multiple authors on the PR, find some helpful documentation [here.](https://gist.github.com/lisawolderiksen/f9747a3ae1e58e9daa7d176ab98f1bad)

#### Recommended resources about contributing to open source

- Talk *Sphinx for Python documentation* by Melissa Weber Mendonça: https://youtu.be/tXWscUSYdBs
- Talk *Intro to git* by Reshama Shaikh: https://github.com/reshamas/git-intro-workshop
- Guide to making open source contributions, for first-timers and veterans: https://opensource.guide/how-to-contribute/
- Guide to pair programming: https://medium.com/@weblab_tech/pair-programming-guide-a76ca43ff389
- Mentored Sprints community handbook: https://mentored-sprints.netlify.app/
- Talk *Contributing to Core Python* by Carol Willing: https://youtu.be/Pkg-DKkObKs
