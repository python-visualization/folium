## MiniMap

```{code-cell} ipython3
import folium
from folium.plugins import MiniMap

m = folium.Map(location=(30, 20), zoom_start=4)

MiniMap().add_to(m)

m
```

### Make the minimap collapsible

```{code-cell} ipython3
m = folium.Map(location=(30, 20), zoom_start=4)
MiniMap(toggle_display=True).add_to(m)
m
```

### Change the minimap tile layer

```{code-cell} ipython3
m = folium.Map(location=(30, 20), zoom_start=4)
MiniMap(tile_layer="Stamen Toner").add_to(m)
m
```

### Change the minimap position

```{code-cell} ipython3
m = folium.Map(location=(30, 20), zoom_start=4)
MiniMap(position="topleft").add_to(m)
m
```

### Change the minimap size

```{code-cell} ipython3
m = folium.Map(location=(30, 20), zoom_start=4)
MiniMap(width=400, height=100).add_to(m)
m
```

### Change the zoom offset

```{code-cell} ipython3
m = folium.Map(location=(30, 20), zoom_start=8)
MiniMap(zoom_level_offset=-8).add_to(m)
m
```
