```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## SemiCircle

This can be used to display a semicircle or sector on a map. Whilst called SemiCircle it is not limited to 180 degree angles and can be used to display a sector of any angle.

The semicircle is defined with a location (the central point, if it was a full circle), a radius and will either have a direction and an arc **or** a start angle and a stop angle.

```{code-cell} ipython3
m = folium.Map([45, 3], zoom_start=5)

folium.plugins.SemiCircle(
    (45, 3),
    radius=400000,
    start_angle=50,
    stop_angle=200,
    color="green",
    fill_color="green",
    opacity=0,
    popup="start angle - 50 degrees, stop angle - 200 degrees",
).add_to(m)

folium.plugins.SemiCircle(
    (46.5, 9.5),
    radius=200000,
    direction=360,
    arc=90,
    color="red",
    fill_color="red",
    opacity=0,
    popup="Direction - 0 degrees, arc 90 degrees",
).add_to(m)

m
```
