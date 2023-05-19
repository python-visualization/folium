```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# Map

## Scale

Show a scale on the bottom of the map.

```{code-cell} ipython3
folium.Map(
    location=(-38.625, -12.875),
    control_scale=True,
)
```

## Zoom control

The map shows zoom buttons by default, but you can disable them.

```{code-cell} ipython3
folium.Map(
    location=(-38.625, -12.875),
    zoom_control=False,
)
```

## Limits

You can set limits, so the map won't scroll outside those limits.

```{code-cell} ipython3
import folium

min_lon, max_lon = -45, -35
min_lat, max_lat = -25, -15

m = folium.Map(
    max_bounds=True,
    location=[-20, -40],
    zoom_start=6,
    min_lat=min_lat,
    max_lat=max_lat,
    min_lon=min_lon,
    max_lon=max_lon,
)

folium.CircleMarker([max_lat, min_lon], tooltip="Upper Left Corner").add_to(m)
folium.CircleMarker([min_lat, min_lon], tooltip="Lower Left Corner").add_to(m)
folium.CircleMarker([min_lat, max_lon], tooltip="Lower Right Corner").add_to(m)
folium.CircleMarker([max_lat, max_lon], tooltip="Upper Right Corner").add_to(m)

m
```
