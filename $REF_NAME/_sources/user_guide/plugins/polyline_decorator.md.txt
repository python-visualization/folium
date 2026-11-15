```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## PolyLineDecorator

Draw arrowheads, dashes or markers along a line, for example to show the direction of travel.

```{code-cell} ipython3
m = folium.Map([46.5, 6.6], zoom_start=9)

route = folium.PolyLine(
    [[46.2, 6.15], [46.52, 6.63], [46.95, 7.45]], color="#3388ff", weight=4
).add_to(m)

folium.plugins.PolyLineDecorator(
    route,
    [
        {
            "offset": 25,
            "repeat": 50,
            "symbol": {
                "type": "arrowHead",
                "pixel_size": 12,
                "path_options": {"color": "#3388ff", "fill_opacity": 1, "weight": 0},
            },
        }
    ],
).add_to(m)

border = folium.PolyLine([[46.0, 6.0], [46.3, 7.2]], color="black", weight=1).add_to(m)

folium.plugins.PolyLineDecorator(
    border,
    [
        {
            "offset": 0,
            "repeat": 10,
            "symbol": {"type": "dash", "pixel_size": 5, "path_options": {"color": "red"}},
        }
    ],
).add_to(m)

m
```
