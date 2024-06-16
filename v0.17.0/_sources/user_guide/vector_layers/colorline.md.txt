### ColorLine

```{code-cell} ipython3
import numpy as np

x = np.linspace(0, 2 * np.pi, 300)

lats = 20 * np.cos(x)
lons = 20 * np.sin(x)
colors = np.sin(5 * x)
```

```{code-cell} ipython3
import folium

m = folium.Map([0, 0], zoom_start=3)

color_line = folium.ColorLine(
    positions=list(zip(lats, lons)),
    colors=colors,
    colormap=["y", "orange", "r"],
    weight=10,
).add_to(m)

m
```
