# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "napari[all]>=0.8.0rc0",
#     "dynamical-catalog>=0.7.0",
#     "xarray>=2026.7.0",
#     "cartopy",            # state boundaries
#     "shapely",            # clip boundaries to region
#     "numpy",
# ]
# ///
"""Minneapolis weather in napari — 4D HRRR forecast volume from dynamical.org.

Shows five weather variables from the NOAA HRRR forecast model over the Upper
Midwest US. Each layer is a 4D volume (init_time, lead_time, y, x):

- The forecast **lead_time** (0–48 h) forms the depth axis — scroll hour by
  hour through the 3D volume to see weather patterns evolving forward in time.
- The **init_time** slider lets you flip between consecutive forecast runs
  to compare what the model predicted at different start times.

Data from dynamical.org / NOAA NWS NCEP HRRR at 3 km resolution over the
conterminous US (Lambert Conformal Conic projection).

    uv run demos/weather.py
"""

import dynamical_catalog
import napari
import numpy as np

# --- configuration ---------------------------------------------------------
# Minneapolis: 44.9778°N, 93.2650°W
LAT_CENTER, LON_CENTER = 44.98, -93.27
LAT_HALF, LON_HALF = 4.0, 5.0  # ~450 km × 400 km box

# How many recent initialization times to stack (→ 4th dimension slider)
NUM_INIT_TIMES = 2

# Layer definitions: variable name → napari display preset
LAYERS = {
    'temperature_2m': dict(cmap='turbo', clim=(5, 35), label='2 m temperature (°C)'),
    'wind_gust_surface': dict(cmap='plasma', clim=(0, 18), label='Wind gust (m/s)'),
    'total_cloud_cover_atmosphere': dict(
        cmap='gray', clim=(10, 100), label='Total cloud cover (%)'
    ),
    'relative_humidity_2m': dict(cmap='Blues', clim=(30, 100), label='2 m relative humidity (%)'),
}

# --- open dataset ----------------------------------------------------------
print('Opening HRRR forecast dataset from dynamical.org …')
ds = dynamical_catalog.open('noaa-hrrr-forecast-48-hour')

# The HRRR uses a Lambert Conformal Conic grid (x, y in metres).
# latitude / longitude are 2-D auxiliary arrays (y × x).
lat = ds['latitude'].load()
lon = ds['longitude'].load()

# Spatial subset around Minneapolis via bounding-box mask on lat/lon
mask = (
    (lat >= LAT_CENTER - LAT_HALF)
    & (lat <= LAT_CENTER + LAT_HALF)
    & (lon >= LON_CENTER - LON_HALF)
    & (lon <= LON_CENTER + LON_HALF)
)
y_inds, x_inds = np.where(mask)
y_slice = slice(int(y_inds.min()), int(y_inds.max()) + 1)
x_slice = slice(int(x_inds.min()), int(x_inds.max()) + 1)

# Select data — isel for all positional slicing
sel = ds.isel(
    init_time=slice(-NUM_INIT_TIMES, None),  # last N init times
    lead_time=slice(0, 49),  # hours 0..48
    y=y_slice,
    x=x_slice,
)
sel = sel.compute()
init_times = sel.init_time.values
n_init, n_lead, ny, nx = (
    sel.sizes['init_time'],
    sel.sizes['lead_time'],
    sel.sizes['y'],
    sel.sizes['x'],
)
print(f'Init times: {list(init_times)}', flush=True)
print(f'Selected shape: ({n_init}, {n_lead}, {ny}, {nx})  (init, lead, y, x)', flush=True)

# --- world scale -----------------------------------------------------------
# x, y are in metres (Lambert projection); resolution is ~3 km.
# Access dimension coordinates via the dimension name directly
y_vals = sel.y.values
x_vals = sel.x.values
print(f'y range: {y_vals.min():.0f} .. {y_vals.max():.0f}  (n={len(y_vals)})', flush=True)
print(f'x range: {x_vals.min():.0f} .. {x_vals.max():.0f}  (n={len(x_vals)})', flush=True)
scale_y = float(abs(np.diff(y_vals[:5]).mean())) / 1000  # km
scale_x = float(abs(np.diff(x_vals[:5]).mean())) / 1000  # km
if not np.isfinite(scale_y) or scale_y < 0.001:
    scale_y = 3.0
if not np.isfinite(scale_x) or scale_x < 0.001:
    scale_x = 3.0
# Exaggerate the lead_time (depth) axis so the 48-hour column is visible
Z_EXAG = 120.0  # km per forecast hour
# Scale tuple matches the data shape (init_time, lead_time, y, x):
# init_time is a slider dimension → scale=1
scale = (1, Z_EXAG, scale_y, scale_x)
print(f'Scale (km/px): lead_time={Z_EXAG}, y={scale_y:.1f}, x={scale_x:.1f}', flush=True)

# --- compute derived variables & handle NaN data ---------------------------
layers_data = {}

for var_key, cfg in LAYERS.items():
    arr = sel[var_key].values
    # Replace NaN with 0 to avoid thumbnail computation issues
    arr = np.nan_to_num(arr, nan=0.0)
    layers_data[cfg['label']] = (arr, cfg)

# 10 m wind speed from u and v components
u10 = sel['wind_u_10m'].values
v10 = sel['wind_v_10m'].values
ws = np.nan_to_num(np.hypot(u10, v10), nan=0.0)
layers_data['10 m wind speed (m/s)'] = (
    ws,
    dict(cmap='inferno', clim=(0, 12), label='10 m wind speed (m/s)'),
)

# Quick sanity check
for name, (arr, _) in layers_data.items():
    print(f'  {name}: shape={arr.shape}, range=[{arr.min():.1f}, {arr.max():.1f}]', flush=True)


def _nearest_grid_idx(lat_q, lon_q):
    """Return (row, col) of the nearest grid point for a query lat/lon."""
    # lat_subset, lon_subset: 2-D arrays of the selected region
    dist = np.hypot(lat_grid - lat_q, lon_grid - lon_q)
    flat_idx = np.argmin(dist)
    return np.unravel_index(flat_idx, lat_grid.shape)


# Cache the lat/lon grid for the selected subset
lat_grid = lat[y_slice, x_slice].values
lon_grid = lon[y_slice, x_slice].values


def city_markers():
    """Return (coords, labels) for reference cities in the region.

    Each coordinate is (init_time, lead_time, row, col) — pinned to
    the first init_time and first lead_time so labels sit on the
    front face of the 4D volume.
    """
    cities = [
        ('Minneapolis', 44.98, -93.27),
        ('St. Paul', 44.95, -93.09),
        ('Duluth', 46.79, -92.10),
        ('Rochester, MN', 44.02, -92.47),
        ('Des Moines', 41.59, -93.62),
        ('Sioux Falls', 43.54, -96.73),
        ('Fargo', 46.88, -96.80),
        ('Green Bay', 44.51, -88.00),
        ('Madison', 43.07, -89.40),
    ]
    coords = []
    labels = []
    for name, lat_q, lon_q in cities:
        try:
            r, c = _nearest_grid_idx(lat_q, lon_q)
        except ValueError:
            continue  # outside the selected region — skip
        coords.append((0, 0, r, c))  # front face: first init, first lead
        labels.append(name)
    return np.array(coords), labels


# --- build the viewer ------------------------------------------------------
viewer = napari.Viewer(ndisplay=3)

for name, (data_values, cfg) in layers_data.items():
    viewer.add_image(
        data_values,
        name=name,
        colormap=cfg['cmap'],
        contrast_limits=list(cfg['clim']),
        rendering='attenuated_mip',
        scale=scale,
        units='km',
    )

# Reference city markers (white points on the front face)
try:
    pts, labels = city_markers()
    viewer.add_points(
        pts,
        size=4,
        face_color='white',
        border_color='white',
        scale=scale,
        units='km',
        name='cities',
        opacity=0.8,
        text=labels,
    )
    print(f'cities: {len(pts)} markers')
except Exception as e:
    print(f'skipping city markers ({type(e).__name__}: {e})')

# State boundary overlay (projected via lat/lon nearest-neighbor lookup)
try:
    import cartopy.feature as cfeature
    from shapely.geometry import box

    clip = box(
        LON_CENTER - LON_HALF, LAT_CENTER - LAT_HALF, LON_CENTER + LON_HALF, LAT_CENTER + LAT_HALF
    )
    feature = cfeature.NaturalEarthFeature(
        'cultural',
        'admin_1_states_provinces_lines',
        '50m',
    )
    boundary_paths = []
    for geom in feature.geometries():
        clipped = geom.intersection(clip)
        if clipped.is_empty:
            continue
        lines = clipped.geoms if clipped.geom_type.startswith('Multi') else [clipped]
        for line in lines:
            if line.geom_type != 'LineString':
                continue
            lons, lats = np.asarray(line.coords).T
            pts = []
            for plon, plat in zip(lons, lats):
                r, c = _nearest_grid_idx(plat, plon)
                pts.append((0, 0, r, c))  # (init, lead, y, x)
            boundary_paths.append(np.array(pts))
    if boundary_paths:
        viewer.add_shapes(
            boundary_paths,
            shape_type='path',
            edge_color='white',
            edge_width=0.5,
            scale=scale,
            units='km',
            name='state boundaries',
            opacity=0.7,
        )
        print(f'state boundaries: {len(boundary_paths)} segments')
except Exception as e:
    print(f'skipping state boundaries ({type(e).__name__}: {e})')

# --- labeled axes + scale bar ----------------------------------------------
viewer.dims.axis_labels = ('init_time', 'lead_time', 'y', 'x')
viewer.dims.set_current_step(0, 0)  # start on the first init_time

viewer.axes.visible = True
viewer.axes.labels = True
viewer.scale_bar.visible = True
viewer.title = f'Minneapolis HRRR forecast — {str(init_times[0])[:16]} + 0–48 h'

if __name__ == '__main__':
    napari.run()
