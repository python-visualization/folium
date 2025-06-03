```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

## LayerControl

Add a control to the map to show or hide layers.

```{code-cell} ipython3
m = folium.Map(tiles=None)

folium.TileLayer("OpenStreetMap", overlay=True).add_to(m)

folium.LayerControl().add_to(m)

m
```

### Common layer arguments

Every layer element in Folium has a couple common arguments:

- `name`: how the layer will be named in the layer control.
- `overlay`: True if the layer is an overlay, False if the layer is a base layer.
  - base layer: only one can be active at a time. Tile layers are base layers by default.
  - overlay: multiple can be active at the same time. `FeatureGroup`s and most non-tile layers are overlays by default.
- `control`: Whether the layer can be controlled in the layer control.
- `show`: Whether the layer will be shown when opening the map.

Next we'll give some examples using a `FeatureGroup`.

### Remove from control

```{code-cell} ipython3
m = folium.Map()

fg = folium.FeatureGroup(name="Icon collection", control=False).add_to(m)
folium.Marker(location=(0, 0)).add_to(fg)

folium.LayerControl().add_to(m)

m
```

### Show manually

```{code-cell} ipython3
m = folium.Map()

fg = folium.FeatureGroup(name="Icon collection", show=False).add_to(m)
folium.Marker(location=(0, 0)).add_to(fg)

folium.LayerControl().add_to(m)

m
```
