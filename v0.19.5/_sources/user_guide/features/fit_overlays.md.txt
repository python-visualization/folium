```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
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
