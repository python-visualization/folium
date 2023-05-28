# GroupedLayerControl

We can create a GroupedLayerControl and define what layers we want to group together. Those layers won't show up in the regular layer control.

`GroupedLayerControl` takes the same arguments as `LayerControl`.

By default, groups are exclusive, meaning only one layer in a group can be active at a time.

```{code-cell} ipython3
import folium
from folium.plugins import GroupedLayerControl

m = folium.Map([40., 70.], zoom_start=6)

fg1 = folium.FeatureGroup(name='g1')
fg2 = folium.FeatureGroup(name='g2')
fg3 = folium.FeatureGroup(name='g3')
folium.Marker([40, 74]).add_to(fg1)
folium.Marker([38, 72]).add_to(fg2)
folium.Marker([40, 72]).add_to(fg3)
m.add_child(fg1)
m.add_child(fg2)
m.add_child(fg3)

folium.LayerControl(collapsed=False).add_to(m)

GroupedLayerControl(
    groups={'groups1': [fg1, fg2]},
    collapsed=False,
).add_to(m)

m
```

It's also possible to have check boxes instead of radio buttons, so multiple layers within a group can be active.

In this example the layers are not shown by default, but can all be activated.

```{code-cell} ipython3
m = folium.Map([40., 70.], zoom_start=6)

fg1 = folium.FeatureGroup(name='g1', show=False)
fg2 = folium.FeatureGroup(name='g2', show=False)
fg3 = folium.FeatureGroup(name='g3')
folium.Marker([40, 74]).add_to(fg1)
folium.Marker([38, 72]).add_to(fg2)
folium.Marker([40, 72]).add_to(fg3)
m.add_child(fg1)
m.add_child(fg2)
m.add_child(fg3)

folium.LayerControl(collapsed=False).add_to(m)

GroupedLayerControl(
    groups={'groups1': [fg1, fg2]},
    exclusive_groups=False,
    collapsed=False,
).add_to(m)

m
```
