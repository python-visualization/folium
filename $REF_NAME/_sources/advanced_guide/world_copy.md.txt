# Scrolling beyond the world edge

What happens if you scroll beyond the longitudinal edge of the world? Leaflet has a setting
to determine the behavior, which we'll demonstrate here.

## Defaults

```{code-cell} ipython3
import folium

m = folium.Map(world_copy_jump=False)

folium.Marker(
    location=[0, 0], popup="I will disappear when moved outside the  map domain."
).add_to(m)

m
```

## World copy jump

```{code-cell} ipython3
m = folium.Map(world_copy_jump=True)

folium.Marker(
    location=[0, 0],
    popup="I will magically reappear when moved outside the map domain.",
).add_to(m)

m
```

## No wrap

```{code-cell} ipython3
m = folium.Map(
    tiles=folium.TileLayer(no_wrap=True)
)

folium.Marker(location=[0, 0], popup="The map domain here is not wrapped.").add_to(m)

m
```
