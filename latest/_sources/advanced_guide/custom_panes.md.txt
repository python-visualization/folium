```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# Panes and CustomPane

Panes are used to control the ordering of layers on the map. You can customise
them using the `CustomPane` class.

For more info on the panes Leaflet has, see https://leafletjs.com/reference.html#map-pane.

First we'll load geojson data to use in the examples:

```{code-cell} ipython3
import requests

geo_json_data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()

style_function = lambda x: {"fillOpacity": 0.8}
```

## Map without custom pane

We'll make an example to show how the GeoJson we add hides any labels
underneath.

```{code-cell} ipython3
m = folium.Map([43, -100], zoom_start=4, tiles="stamentoner")

folium.GeoJson(geo_json_data, style_function=style_function).add_to(m)

m
```

## Map with custom pane

Now we'll create a custom pane and add a tile layer that contains only labels.
The labels will show on top off the geojson.

```{code-cell} ipython3
m = folium.Map([43, -100], zoom_start=4, tiles="stamentonerbackground")

folium.GeoJson(geo_json_data, style_function=style_function).add_to(m)

folium.map.CustomPane("labels").add_to(m)

# Final layer associated to custom pane via the appropriate kwarg
folium.TileLayer("stamentonerlabels", pane="labels").add_to(m)

m
```
