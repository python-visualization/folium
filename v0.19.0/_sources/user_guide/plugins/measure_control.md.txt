# MeasureControl

This plugin allows you to measure distances on the map.

```{code-cell} ipython3
import folium
from folium.plugins import MeasureControl

m = folium.Map([-27.5717, -48.6256], zoom_start=10)

m.add_child(MeasureControl())

m
```
