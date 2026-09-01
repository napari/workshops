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
"""Hurricane Milton as a 3D wind-speed volume in napari (Arraylake, read-only).

Milton was one of the most intense Atlantic hurricanes on record. Here we take a
single time snapshot near its Florida landfall (2024-10-10 00Z, centre ~27.5N
83.2W) from the public `earthmover-public/era5` pressure-level fields, compute
wind speed sqrt(u^2 + v^2) on all 13 levels (1000 -> 50 hPa), and show it as a
true 3D volume: x = longitude, y = latitude, z = pressure level (height).

You can see the deep cyclonic column at low/mid levels and the separate
upper-level outflow jet aloft. (ERA5's 0.25deg grid smooths the eyewall, so peak
speeds read ~50-60 m/s rather than the real ~80 m/s, but the vortex is clear.)
The Florida/Gulf coastline sits on the surface (1000 hPa) face for reference.

    uv run era5_storm_napari.py
"""

import napari
import numpy as np
import xarray as xr
from arraylake import Client

# --- the storm -------------------------------------------------------------
TIME = '2024-10-10T00:00'  # Milton just offshore SW Florida
# Region as standard geographic bounds (-180..180 lon), centred on the storm
# (~27.5N 83.5W) with enough margin that the full circulation is contained.
LON_W, LON_E = -95, -71  # 95W .. 71W
LAT_S, LAT_N = 16, 39  # 16N .. 39N
RES = 0.25  # ERA5 grid spacing (degrees)
# Keep only the lower/mid troposphere. Above ~400 hPa the broad upper-level jet
# stream is faster than the storm and washes out the volume; capping here leaves
# just the hurricane's cyclonic column. Levels: 1000,925,850,700,600,500,400.
LEVEL_MIN_HPA = 400

# --- open the public ERA5 repo, read-only ---------------------------------
client = Client()
repo = client.get_repo('earthmover-public/era5')
session = repo.readonly_session('main')
ds = xr.open_zarr(session.store, zarr_format=3, group='pressure/spatial')

# ERA5 longitude is 0-360 ascending; latitude runs 90 -> -90 (descending).
# `% 360` maps -95..-75 -> 265..285.
sel = (
    ds[['u', 'v']]
    .sel(valid_time=TIME, method='nearest')
    .sel(
        longitude=slice(LON_W % 360, LON_E % 360),
        latitude=slice(LAT_N, LAT_S),
        pressure_level=slice(1000, LEVEL_MIN_HPA),
    )
    .transpose('pressure_level', 'latitude', 'longitude')
)
spd = np.hypot(sel['u'], sel['v'])  # wind speed (m/s), lazy
vol = spd.load()  # (level, lat, lon)
print(f'wind-speed volume (level, lat, lon): {vol.shape}  max {float(vol.max()):.1f} m/s')

# --- world scale -----------------------------------------------------------
# lat/lon in kilometres (0.25 deg ~ 27.8 km; lon shrinks by cos(latitude)).
# pressure_level index 0 = 1000 hPa (surface) .. index 12 = 50 hPa. The 13
# levels are drawn at uniform, vertically-exaggerated spacing so the column is
# tall enough to see (the real atmosphere is a thin shell vs its width).
DEG_KM = 111.32
cos_lat = float(np.cos(np.deg2rad(vol.latitude.mean().item())))
scale_lat = RES * DEG_KM  # km per pixel along latitude
scale_lon = RES * DEG_KM * cos_lat  # km per pixel along longitude
Z_KM = 200.0  # exaggerated height per pressure level
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
            row = (LAT_N - lat) / RES  # lat 39 -> row 0 (top)
            col = (lon - LON_W) / RES  # lon -95 -> col 0 (left)
            z0 = np.zeros_like(row)  # surface (1000 hPa) face
            paths.append(np.column_stack([z0, row, col]))
    return paths


# --- build the viewer ------------------------------------------------------
viewer = napari.Viewer(ndisplay=3)  # default to 3D
viewer.add_image(
    vol.data,
    name='Milton wind speed (m/s)',
    colormap='inferno',
    contrast_limits=[10, 50],
    rendering='attenuated_mip',
    scale=scale,
)

try:
    paths = coastline_paths()
    viewer.add_shapes(
        paths,
        shape_type='path',
        edge_color='cyan',
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
viewer.title = f'ERA5 Hurricane Milton wind speed — {TIME}Z'

if __name__ == '__main__':
    napari.run()
