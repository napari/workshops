# Downloading and launching this workshop's Jupyter notebooks

The complete, executed notebooks are hosted in the materials on this website. We encourage you
to follow along with the workshop in a fresh, blank notebook. However, if you
would like to be able to run the completed notebooks locally, you can download them
and launch the `jupyter lab` application using the instructions below.

## Downloading the notebooks

There are two ways to download the notebooks; follow the instructions below for
either downloading a .zip file (recommended for beginners) or cloning via git.

### Downloading a .zip file
To download the notebooks as a .zip file, do the following:

1. Click the GitHub logo at the top of this page or navigate your web browser to the workshop's GitHub repository (for this
   template, this is [https://github.com/napari/napari-workshop-template](https://github.com/napari/napari-workshop-template))
2. Click the green (or blue) "Code" button to open the download menu and then
   "Download ZIP" ![download code](./resources/download_code.png)
3. Choose the location you would like to download the .zip into.
4. Open your file browser and double click on the .zip file to uncompress it.
5. You have downloaded the notebooks! Proceed to the "Launching jupyter
   notebook" section.

### Cloning via git
To clone the repository containing the tutorial materials to your computer, open
your Terminal and navigate to the folder where you will download the course
materials into. We recommend cloning the materials into your Documents folder,
but you can choose another suitable location. 

 ```bash
 cd ~/Documents
 ```

Then, clone the repository. This will download all of the files necessary for
this tutorial.

 ```bash
 git clone https://github.com/napari/napari-workshop-template.git
 ```

## Ensuring notebook support is installed

Because the notebooks use MyST Markdown format (`.md` files with executable cells), you need
`jupytext` and `jupyterlab-myst` installed in your environment.

**If you set up your environment with pixi or uv** (by cloning the repo and running
`pixi install` or `uv sync --group dev`), these dependencies are already included — nothing
extra to do.

**If you used conda** to create a manual environment, install them now:

````{important}
Remember to activate the right environment first!

```bash
conda activate napari-workshop
```
````

```bash
conda install -c conda-forge jupytext jupyterlab-myst
```


## Launch the `jupyter lab` application

Navigate to the directory you just cloned or downloaded.

```bash
cd workshops   # or the path where you extracted the .zip
```

Activate your environment and start JupyterLab:

```bash
# pixi (no activation needed)
pixi run -- jupyter lab

# uv
uv run jupyter lab

# conda
conda activate napari-workshop
jupyter lab
```

The Jupyter interface will open in a browser window and you will see the notebooks
in the file browser on the left.

````{important}
To open these workshop notebooks in the Jupyter interface, right click the notebook name in the file navigation panel from the Jupyter interface, and click "Open with -> Notebook".

![Right click on "intro_bioimage_visualization.md" file, and select "Open with -> Notebook"](./resources/open_with_notebook.png)

Or, as an alternative you can first convert them to `.ipynb` files using:

```bash
jupytext --to ipynb <notebook_file>.md
```

````
