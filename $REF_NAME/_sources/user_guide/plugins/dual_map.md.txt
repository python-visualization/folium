```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

# DualMap plugin

This plugin is using the Leaflet plugin Sync by Jieter:
https://github.com/jieter/Leaflet.Sync

The goal is to have two maps side by side. When you pan or zoom on one map, the other will move as well.

The `DualMap` class accepts the same arguments as the normal `Map` class. Except for these: 'width', 'height', 'left', 'top', 'position'.

In the following example we create a `DualMap`, add layer controls and then show the map. Try panning and zooming to check that both maps are synchronized.

```{code-cell} ipython3
folium.plugins.DualMap(location=(52.1, 5.1), zoom_start=8)
```

You can access the two submaps with attributes `m1` and `m2`. You can add objects to each map specifically.

Here we add different tile layers to each map. This way you can see two different tile sets at the same time.

```{code-cell} ipython3
m = folium.plugins.DualMap(location=(52.1, 5.1), tiles=None, zoom_start=8)

folium.TileLayer("openstreetmap").add_to(m.m1)
folium.TileLayer("cartodbpositron").add_to(m.m2)

folium.LayerControl(collapsed=False).add_to(m)
m
```

Now we're going to add feature groups and markers to both maps and to each map individually. We'll color the shared icon red.

```{code-cell} ipython3
m = folium.plugins.DualMap(location=(52.1, 5.1), tiles="cartodbpositron", zoom_start=8)

fg_both = folium.FeatureGroup(name="markers_both").add_to(m)
fg_1 = folium.FeatureGroup(name="markers_1").add_to(m.m1)
fg_2 = folium.FeatureGroup(name="markers_2").add_to(m.m2)

icon_red = folium.Icon(color="red")
folium.Marker((52.0, 5.0), tooltip="both", icon=icon_red).add_to(fg_both)
folium.Marker((52.4, 5.0), tooltip="1").add_to(fg_1)
folium.Marker((52.0, 5.4), tooltip="2").add_to(fg_2)

folium.LayerControl(collapsed=False).add_to(m)
m
```

Finally, you can use the `layout` argument to change the layout to vertical:

```{code-cell} ipython3
m = folium.plugins.DualMap(layout="vertical")
m
```
