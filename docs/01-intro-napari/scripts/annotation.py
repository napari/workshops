"""
Annotation Setup
================


"""

from skimage import data, feature, filters, morphology

import napari

# get sample 3D image data, threshold, and find maxima
cells3d = data.cells3d()
nuclei = cells3d[:, 1]
membrane = cells3d[:, 0]

nuclei_smoothed = filters.gaussian(nuclei, sigma=4)
nuclei_thresholded = nuclei_smoothed > filters.threshold_otsu(nuclei_smoothed)
nuclei_labels = morphology.label(nuclei_thresholded)
nuclei_points = feature.peak_local_max(nuclei_smoothed, min_distance=20)

viewer = napari.Viewer()
viewer.add_image(
    membrane,
    name='membrane',
    blending='translucent_no_depth',
    colormap='orange',
    contrast_limits=(5000, 65355),
)
viewer.add_image(
    nuclei,
    name='nuclei',
    blending='additive',
    colormap='cyan',
    contrast_limits=(5000, 60000)
)
viewer.add_labels(
    nuclei_labels,
    name='nuclei labels'
)
viewer.add_points(
    nuclei_points,
    name='nuclei maxima',
    blending='additive',
    opacity=0.5,
)

# set the view to 3D and rotate camera
viewer.dims.ndisplay = 3
viewer.camera.angles = (-27, 8, -58)

if __name__ == '__main__':
    napari.run()
