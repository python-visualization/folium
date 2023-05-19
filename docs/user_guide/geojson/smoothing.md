# Smoothing

The level of smoothing of the geometry can be determined by passing `smooth_factor` as an argument when initialising GeoJson, TopoJson and Choropleth objects. There are no upper or lower bounds to the smoothing level; Leaflet's default is 1.

```{code-cell} ipython3
import json

import folium
import requests


m = folium.Map(location=[-59.1759, -11.6016], tiles="cartodbpositron", zoom_start=2)


url = (
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
)
fname = f"{url}/antarctic_ice_shelf_topo.json"
topo = json.loads(requests.get(fname).text)


folium.TopoJson(
    data=topo,
    object_path="objects.antarctic_ice_shelf",
    name="default_smoothing",
    smooth_factor=1,
    style_function=lambda x: {"color": "#004c00", "opacity": "0.7"},
).add_to(m)


folium.TopoJson(
    data=topo,
    object_path="objects.antarctic_ice_shelf",
    name="default_smoothing",
    smooth_factor=10,
    style_function=lambda x: {"color": "#1d3060", "opacity": "0.7"},
).add_to(m)

folium.LayerControl().add_to(m)

m
```
