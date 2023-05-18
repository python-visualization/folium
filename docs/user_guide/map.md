# Map

```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

## Scale

Show a scale on the bottom of the map.

```{code-cell} ipython3
folium.Map(
    location=(-38.625, -12.875),
    control_scale=True,
)
```

## Zoom control

The map shows zoom buttons by default, but you can disable them.

```{code-cell} ipython3
folium.Map(
    location=(-38.625, -12.875),
    zoom_control=False,
)
```
