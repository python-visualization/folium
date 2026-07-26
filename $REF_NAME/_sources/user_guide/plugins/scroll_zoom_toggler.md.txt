```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## ScrollZoomToggler

Add a button to enable/disable zoom scrolling.

```{code-cell} ipython3
m = folium.Map([45, 3], zoom_start=4)

folium.plugins.ScrollZoomToggler().add_to(m)

m
```
