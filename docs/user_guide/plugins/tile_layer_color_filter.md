```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## Tile Layer Color Filter

Apply a [CSS filter](https://developer.mozilla.org/en-US/docs/Web/CSS/filter) to the tiles of a map, for example to turn a light basemap into a dark or grayscale background. This wraps the [Leaflet.TileLayer.ColorFilter](https://github.com/xtk93x/Leaflet.TileLayer.ColorFilter) plugin.

Filters are written as `"<name>:<number><unit>"`. The supported filters are `blur` (px), `brightness` (%), `contrast` (%), `grayscale` (%), `hue-rotate` (deg), `invert` (%), `opacity` (%), `saturate` (%) and `sepia` (%). The unit can be left out; the ones above are added for you.

### Dark basemap

Inverting the tiles and rotating the hue turns the light OpenStreetMap tiles into a dark basemap:

```{code-cell} ipython3
m = folium.Map([52.1, 5.1], zoom_start=6, tiles=None)

folium.plugins.TileLayerColorFilter(
    ["invert:100%", "hue-rotate:180deg", "brightness:95%", "contrast:90%"],
    name="dark",
    control=False,
).add_to(m)

m
```

### Grayscale background

A grayscale basemap keeps the attention on the data drawn on top of it. The filter applies to the tiles only, not to markers or other layers:

```{code-cell} ipython3
m = folium.Map([52.1, 5.1], zoom_start=6, tiles=None)

folium.plugins.TileLayerColorFilter(
    "grayscale:100%", name="grayscale", control=False
).add_to(m)

for lat, lon in [(52.37, 4.89), (51.92, 4.48), (52.09, 5.12)]:
    folium.CircleMarker([lat, lon], radius=8, color="red", fill=True).add_to(m)

m
```

Multiple filtered layers can be combined with a `LayerControl` to let the user switch between them.
