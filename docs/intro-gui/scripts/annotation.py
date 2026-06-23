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

shape = [
    [ 29.       , 124.29706  ,  58.10305  ],
    [ 29.       , 120.45354  ,  16.251354 ],
    [ 29.       , 100.80886  ,   6.429018 ],
    [ 29.       ,  80.310074 ,   6.8560762],
    [ 29.       ,  50.416004 ,  24.792517 ],
    [ 29.       ,  42.72896  ,  39.312492 ],
    [ 29.       ,  46.145424 ,  54.68659  ],
    [ 29.       ,  56.394817 ,  70.48774  ],
    [ 29.       ,  74.33126  ,  83.72654  ],
    [ 29.       ,  90.55947  ,  90.13241  ],
    [ 29.       , 105.079445 ,  88.42418  ],
    [ 29.       , 116.610016 ,  79.455956 ]
]

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
viewer.add_shapes(
    shape,
    name='dividing cell',
    shape_type='polygon',
    blending='translucent',
    edge_color='yellow',
    face_color='#FFA50080',
)

viewer.dims.ndisplay = 3
viewer.camera.angles = (-30, 15, -35)

if __name__ == '__main__':
    napari.run()
