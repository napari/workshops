# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "napari[all]>=0.8.0rc0",
#     "arraylake>=1.2.0",
#     "xarray>=2026.7.0",
#     "zarr>=3",
#     "numcodecs[pcodec]",  # ERA5 chunks are pcodec-compressed
#     "cartopy",            # coastline geometries
#     "shapely",            # clip coastlines to the region box
#     "dask",
#     "numpy",
# ]
# ///
"""ERA5 as a 3D atmospheric volume in napari, from Arraylake (public, read-only).

The public `earthmover-public/era5` repo carries pressure-level fields on 13
levels (1000 -> 50 hPa). At a single time we pull a regional (level, lat, lon)
block and show it as a true 3D volume: x = longitude, y = latitude, and
z = pressure level (height). A coastline outline sits on the surface (1000 hPa)
face for geographic reference.

The default variable is relative humidity: high RH aloft is essentially where
the clouds are, so the volume renders as a 3D cloud/moisture field. Swap `VAR`
for `t` (temperature) or `q` (specific humidity) using the presets below.

This file carries its own dependencies (PEP 723), so it runs standalone:

    uv run era5_napari.py
"""

import napari
import numpy as np
import xarray as xr
from arraylake import Client

# --- what to show ----------------------------------------------------------
TIME = '2025-07-01T00:00'  # single time snapshot
VAR = 'r'  # "r" clouds/moisture | "t" temperature | "q" humidity

# per-variable display presets: colormap, contrast limits, 3D render mode
PRESETS = {
    'r': dict(
        cmap='gray',
        clim=(50, 100),
        rendering='attenuated_mip',
        label='relative humidity (%) — high RH aloft ~ clouds',
    ),
    't': dict(cmap='turbo', clim=(-70, 40), rendering='mip', label='temperature (degC)'),
    'q': dict(
        cmap='viridis',
        clim=(0.0, 0.015),
        rendering='attenuated_mip',
        label='specific humidity (kg/kg)',
    ),
}
preset = PRESETS[VAR]

# Region as standard geographic bounds (-180..180 lon). North America:
LON_W, LON_E = -130, -60  # 130W .. 60W
LAT_S, LAT_N = 20, 60  # 20N .. 60N
RES = 0.25  # ERA5 grid spacing (degrees)

# --- open the public ERA5 repo, read-only ---------------------------------
client = Client()
repo = client.get_repo('earthmover-public/era5')
session = repo.readonly_session('main')
ds = xr.open_zarr(session.store, zarr_format=3, group='pressure/spatial')

# ERA5 longitude is 0-360 ascending; latitude runs 90 -> -90 (descending),
# so the latitude slice is (high, low). `% 360` maps -130..-60 -> 230..300.
da = (
    ds[VAR]
    .sel(valid_time=TIME, method='nearest')
    .sel(longitude=slice(LON_W % 360, LON_E % 360), latitude=slice(LAT_N, LAT_S))
    .transpose('pressure_level', 'latitude', 'longitude')
)
if VAR == 't':
    da = da - 273.15  # K -> degC

vol = da.load()  # (level, lat, lon); ~13 levels, a few seconds from S3
levels = vol.pressure_level.values
print(f'{VAR} volume (level, lat, lon): {vol.shape}  levels(hPa): {levels.tolist()}')

# --- world scale -----------------------------------------------------------
# lat/lon in kilometres so the scale bar means something (0.25 deg ~ 27.8 km;
# lon shrinks by cos(latitude)). pressure_level index 0 = 1000 hPa (surface) up
# to index 12 = 50 hPa. The 13 levels are NOT evenly spaced in true altitude;
# we draw them at uniform, vertically-exaggerated spacing so the column is
# tall enough to see (the real atmosphere is a very thin shell vs its width).
DEG_KM = 111.32
cos_lat = float(np.cos(np.deg2rad(vol.latitude.mean().item())))
scale_lat = RES * DEG_KM  # km per pixel along latitude
scale_lon = RES * DEG_KM * cos_lat  # km per pixel along longitude
Z_KM = 180.0  # exaggerated height per pressure level
scale = (Z_KM, scale_lat, scale_lon)  # (level, lat, lon)


def coastline_paths():
    """Coastline segments as napari 'path' arrays in (level, row, col) coords,
    clipped to the region box and pinned to the surface level (index 0)."""
    import cartopy.feature as cfeature
    from shapely.geometry import box

    clip = box(LON_W, LAT_S, LON_E, LAT_N)
    feature = cfeature.NaturalEarthFeature('physical', 'coastline', '50m')
    paths = []
    for geom in feature.geometries():
        clipped = geom.intersection(clip)
        if clipped.is_empty:
            continue
        lines = clipped.geoms if clipped.geom_type.startswith('Multi') else [clipped]
        for line in lines:
            if line.geom_type != 'LineString':
                continue
            lon, lat = np.asarray(line.coords).T
            row = (LAT_N - lat) / RES  # lat 60 -> row 0 (top)
            col = (lon - LON_W) / RES  # lon -130 -> col 0 (left)
            z0 = np.zeros_like(row)  # surface (1000 hPa) face
            paths.append(np.column_stack([z0, row, col]))
    return paths


# --- build the viewer ------------------------------------------------------
viewer = napari.Viewer(ndisplay=3)  # default to 3D
viewer.add_image(
    vol.data,
    name=f'ERA5 {VAR}',
    colormap=preset['cmap'],
    contrast_limits=list(preset['clim']),
    rendering=preset['rendering'],
    scale=scale,
)

try:
    paths = coastline_paths()
    viewer.add_shapes(
        paths,
        shape_type='path',
        edge_color='#ff5555',
        edge_width=0.8,
        scale=scale,
        name='coastline',
        opacity=0.9,
    )
    print(f'coastline: {len(paths)} segments')
except Exception as e:  # cartopy data download failed, etc. — still show data
    print(f'skipping coastlines ({type(e).__name__}: {e})')

# --- labeled, visible axes + scale bar with units --------------------------
viewer.dims.axis_labels = ('pressure_level', 'latitude', 'longitude')
viewer.axes.visible = True
viewer.axes.labels = True
viewer.scale_bar.visible = True
viewer.scale_bar.unit = 'km'  # horizontal (lat/lon) axes are in km
viewer.title = f'ERA5 {TIME} — {preset["label"]}'

if __name__ == '__main__':
    napari.run()
