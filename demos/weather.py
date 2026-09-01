# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "napari[all]>=0.8.0rc0",
#     "dynamical-catalog>=0.7.0",
#     "xarray>=2026.7.0",
#     "cartopy",
#     "shapely",
#     "numpy",
# ]
# ///
"""Minneapolis weather in napari — 5 weather variables in a grid.

Five weather variables from the NOAA HRRR model over the Upper Midwest US.
Each is a 3D volume (lead_time, y, x) — scroll the time slider to see the
forecast evolve.  Layers are arranged in repeating stride-3 groups so the
napari grid viewer shows one variable per cell:

    Cell 0:  [boundaries, cities, temperature]
    Cell 1:  [boundaries, cities, wind gust]
    Cell 2:  [boundaries, cities, cloud cover]
    ...

Data from dynamical.org / NOAA NWS NCEP HRRR at 3 km resolution over the
CONUS (Lambert Conformal Conic projection).

    uv run demos/weather.py
"""

import cartopy.feature as cfeature
import dynamical_catalog
import napari
import numpy as np
from shapely.geometry import box

# --- configuration ---------------------------------------------------------
LAT_CENTER, LON_CENTER = 44.98, -93.27  # Minneapolis
LAT_HALF, LON_HALF = 5.0, 5.0  # ~ 10° × 10° box
Z_DEG = 1.0  # 1 hour per lead_time step (actual)

# Each entry → one grid cell: (variable_name, colormap, clim, display_label)
VARIABLES = [
    ('temperature_2m', 'coolwarm', (10, 38), '2 m temperature (°C)'),
    ('total_cloud_cover_atmosphere', 'Greys', (0, 100), 'Total cloud cover (%)'),
    ('pressure_surface', 'inferno', (94500, 100500), 'Surface pressure (kg m⁻² s⁻¹)'),
    ('relative_humidity_2m', 'viridis', (0, 100), '2 m relative humidity (%)'),
    ('wind_speed_10m', 'magma', (0, 18), '10 m wind speed (m/s)'),
    ('wind_gust_surface', 'magma', (0, 18), 'Wind gust (m/s)'),
]

CITIES = [
    ('Minneapolis', 44.98, -93.27),
    ('Duluth', 46.79, -92.10),
    ('Rochester, MN', 44.02, -92.47),
    ('Des Moines', 41.59, -93.62),
    ('Sioux Falls', 43.54, -96.73),
    ('Fargo', 46.88, -96.80),
    ('Green Bay', 44.51, -88.00),
    ('Madison', 43.07, -89.40),
]

# --- open dataset ----------------------------------------------------------
print('Opening HRRR forecast dataset from dynamical.org …')
ds = dynamical_catalog.open('noaa-hrrr-forecast-48-hour')

lat = ds['latitude'].load()
lon = ds['longitude'].load()

mask = (
    (lat >= LAT_CENTER - LAT_HALF)
    & (lat <= LAT_CENTER + LAT_HALF)
    & (lon >= LON_CENTER - LON_HALF)
    & (lon <= LON_CENTER + LON_HALF)
)
y_inds, x_inds = np.where(mask)
y_slice = slice(int(y_inds.min()), int(y_inds.max()) + 1)
x_slice = slice(int(x_inds.min()), int(x_inds.max()) + 1)

sel = ds.isel(init_time=-1, lead_time=slice(0, 49), y=y_slice, x=x_slice).compute()
n_lead, ny, nx = sel.sizes['lead_time'], sel.sizes['y'], sel.sizes['x']
lead_hours = sel.lead_time.values.astype('timedelta64[h]').astype(int)
print(f'Selected: ({n_lead}, {ny}, {nx})  (lead, y, x)', flush=True)
print(
    f'Lead times: {lead_hours[0]}h .. {lead_hours[-1]}h  '
    f'(step={lead_hours[1] - lead_hours[0]}h, n={n_lead})',
    flush=True,
)


# --- derive data arrays ----------------------------------------------------
def _prep(arr):
    return np.nan_to_num(arr, nan=0.0).astype(np.float32)


data_arrays = {}
for key, *_ in VARIABLES:
    if key == 'wind_speed_10m':
        data_arrays[key] = _prep(np.hypot(sel['wind_u_10m'].values, sel['wind_v_10m'].values))
    else:
        data_arrays[key] = _prep(sel[key].values)

# --- world scale -----------------------------------------------------------
lat_grid = lat[y_slice, x_slice].values
lon_grid = lon[y_slice, x_slice].values
lat_deg = float(np.abs(np.diff(lat_grid[:, 0])).mean())
lon_deg = float(np.abs(np.diff(lon_grid[0, :])).mean())
scale_3d = (Z_DEG, lat_deg, lon_deg)
units_3d = ('hour', 'degree', 'degree')
print(f'Scale (deg/px): lead={Z_DEG}, y={lat_deg:.5f}, x={lon_deg:.5f}', flush=True)


# --- nearest-grid lookup ---------------------------------------------------
def _nearest_grid_idx(lat_q, lon_q):
    dist = np.hypot(lat_grid - lat_q, lon_grid - lon_q)
    return np.unravel_index(np.argmin(dist), lat_grid.shape)


# --- reference overlays (3D: tiled across all lead_times) ------------------
# Cities — each city repeated at every lead_time
city_coords = []
city_labels = []
for name, lat_q, lon_q in CITIES:
    r, c = _nearest_grid_idx(lat_q, lon_q)
    for t in range(n_lead):
        city_coords.append((t, r, c))
        city_labels.append(name)

# State boundaries — each segment repeated at every lead_time

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
        base = []
        for plon, plat in zip(lons, lats):
            r, c = _nearest_grid_idx(plat, plon)
            base.append((r, c))
        for t in range(n_lead):
            boundary_paths.append(np.array([(t, r, c) for (r, c) in base]))

# --- build the viewer: repeating stride-3 groups ---------------------------
viewer = napari.Viewer()

for var_key, cmap, clim, label in VARIABLES:
    # Each grid cell gets: boundaries + cities + weather variable
    viewer.add_shapes(
        boundary_paths,
        shape_type='path',
        edge_color='white',
        edge_width=0.5,
        scale=scale_3d,
        units=units_3d,
        name=f'boundaries — {label}',
        opacity=0.7,
    )
    viewer.add_image(
        data_arrays[var_key],
        colormap=cmap,
        contrast_limits=list(clim),
        rendering='attenuated_mip',
        scale=scale_3d,
        units=units_3d,
        name=label,
        blending='additive',
    )
    viewer.add_points(
        np.array(city_coords),
        size=4,
        face_color='white',
        border_color='white',
        scale=scale_3d,
        units=units_3d,
        name=f'cities — {label}',
        opacity=0.8,
        text=city_labels,
    )

# --- grid + axes -----------------------------------------------------------
for lyr in viewer.layers:
    if hasattr(lyr, 'colorbar'):
        lyr.colorbar.visible = True
        lyr.name_overlay.visible = True
viewer._overlays['current_slice'].visible = True
viewer._overlays['current_slice'].gridded = True
viewer.grid.enabled = True
viewer.grid.stride = 3
viewer.grid.spacing = 0.05
viewer.dims.axis_labels = ('time (hours)', 'latitude', 'longitude')
viewer.scale_bar.visible = True
viewer.scale_bar.gridded = True
viewer.title = f'Minneapolis HRRR — {str(sel.init_time.values)[:16]}'

if __name__ == '__main__':
    napari.run()
