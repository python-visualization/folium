```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## Terminator

This plugin overlays the current day and night regions on the map. It updates
continuously. Zoom in in the example below to see the regions move.

```{code-cell} ipython3
m = folium.Map([45, 3], zoom_start=1)

folium.plugins.Terminator().add_to(m)

m
```
