```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## BoatMarker

```{code-cell} ipython3
m = folium.Map([30, 0], zoom_start=3)

folium.plugins.BoatMarker(
    location=(34, -43), heading=45, wind_heading=150, wind_speed=45, color="#8f8"
).add_to(m)

folium.plugins.BoatMarker(
    location=(46, -30), heading=-20, wind_heading=46, wind_speed=25, color="#88f"
).add_to(m)

m
```
