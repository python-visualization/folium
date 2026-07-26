```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

## Rectangle

```{code-cell} ipython3
m = folium.Map(location=[35.685, 139.76], zoom_start=15)

kw = {
    "color": "blue",
    "line_cap": "round",
    "fill": True,
    "fill_color": "red",
    "weight": 5,
    "popup": "Tokyo, Japan",
    "tooltip": "<strong>Click me!</strong>",
}

folium.Rectangle(
    bounds=[[35.681, 139.766], [35.691, 139.776]],
    line_join="round",
    dash_array="5, 5",
    **kw,
).add_to(m)

dx = 0.012
folium.Rectangle(
    bounds=[[35.681, 139.766 - dx], [35.691, 139.776 - dx]],
    line_join="mitter",
    dash_array="5, 10",
    **kw,
).add_to(m)

folium.Rectangle(
    bounds=[[35.681, 139.766 - 2 * dx], [35.691, 139.7762 - 2 * dx]],
    line_join="bevel",
    dash_array="15, 10, 5, 10, 15",
    **kw,
).add_to(m)

m
```
