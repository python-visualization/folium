```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## FeatureGroupSubGroup

### Sub categories

Disable all markers in the category, or just one of the subgroup.

```{code-cell} ipython3
m = folium.Map(location=[0, 0], zoom_start=6)

fg = folium.FeatureGroup(name="groups")
m.add_child(fg)

g1 = folium.plugins.FeatureGroupSubGroup(fg, "group1")
m.add_child(g1)

g2 = folium.plugins.FeatureGroupSubGroup(fg, "group2")
m.add_child(g2)

folium.Marker([-1, -1]).add_to(g1)
folium.Marker([1, 1]).add_to(g1)

folium.Marker([-1, 1]).add_to(g2)
folium.Marker([1, -1]).add_to(g2)

folium.LayerControl(collapsed=False).add_to(m)

m
```

### Marker clusters across groups

Create two subgroups, but cluster markers together.

```{code-cell} ipython3
m = folium.Map(location=[0, 0], zoom_start=6)

mcg = folium.plugins.MarkerCluster(control=False)
m.add_child(mcg)

g1 = folium.plugins.FeatureGroupSubGroup(mcg, "group1")
m.add_child(g1)

g2 = folium.plugins.FeatureGroupSubGroup(mcg, "group2")
m.add_child(g2)

folium.Marker([-1, -1]).add_to(g1)
folium.Marker([1, 1]).add_to(g1)

folium.Marker([-1, 1]).add_to(g2)
folium.Marker([1, -1]).add_to(g2)

folium.LayerControl(collapsed=False).add_to(m)

m
```
