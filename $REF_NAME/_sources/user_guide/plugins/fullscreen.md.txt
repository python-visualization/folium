```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## Fullscreen

Add a button to toggle a fullscreen view of the map.

```{code-cell} ipython3
m = folium.Map(location=[41.9, -97.3], zoom_start=4)

folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
).add_to(m)

m
```
