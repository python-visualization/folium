# UI elements

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

folium.TileLayer("OpenStreetMap").add_to(m)
folium.TileLayer("stamentoner", show=False).add_to(m)

folium.LayerControl().add_to(m)

m
```

## Common layer arguments

Every layer element in Folium has a couple common arguments:

- `name`: how the layer will be named in the layer control.
- `overlay`: True if the layer is an overlay, False if the layer is a base layer.
  - base layer: only one of them can be active at a time. Mostly used for tile layers.
  - overlay: multiple can be active at the same time. Used for anything else than tile layers.
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

## Marker, Icon, Popup

```{code-cell} ipython3
m = folium.Map([0, 0], zoom_start=1)
mk = folium.Marker([0, 0])
pp = folium.Popup("hello")
ic = folium.Icon(color="red")

mk.add_child(ic)
mk.add_child(pp)
m.add_child(mk)

m
```


## FitOverlays

When you add this class to your map, the map will pan and zoom to fit the enabled overlays.

By default, the map won't necessarily show all elements that were added. You may have to pan or zoom out to find them.

If we add the `FitOverlays` class, it will automatically pan and zoom to show the enabled overlays.
In this example we show only the first marker by default. If you enable the second marker, the view changes to include it.

```{code-cell} ipython3
m = folium.Map((52, 0), tiles='cartodbpositron', zoom_start=8)

fg1 = folium.FeatureGroup().add_to(m)
folium.Marker((52, 5)).add_to(fg1)

fg2 = folium.FeatureGroup(show=False).add_to(m)
folium.Marker((52, 5.1)).add_to(fg2)

folium.FitOverlays().add_to(m)

folium.LayerControl().add_to(m)

m
```

`FitOverlays` has a couple options:

- `padding` adds pixels around the bounds.
- `max_zoom` can be used to prevent zooming in too far.
- `fly` enables a smoother, longer animation, so you can see how the view changes.
- `fit_on_map_load` can be used to disable the fitting that happens when the map loads.

Note that `padding` and `max_zoom` can achieve the same effect.
