```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## SideBySideLayers

This plugin can be used to compare two layers on the same map using a vertical separator managed by the user.

The SideBySideLayers class must be instantiated with left and right layers, then added to the map along with layers.

If you want to add a layer control to your map, you can permanently enable the tile layers used for this plugin with `control=False`.

```{code-cell} ipython3
m = folium.Map(location=(30, 20), zoom_start=4)

layer_right = folium.TileLayer('openstreetmap')
layer_left = folium.TileLayer('cartodbpositron')

sbs = folium.plugins.SideBySideLayers(layer_left=layer_left, layer_right=layer_right)

layer_left.add_to(m)
layer_right.add_to(m)
sbs.add_to(m)

m
```
