## Circle and CircleMarker

`CircleMarker` has a radius specified in pixels, while `Circle` is specified in meters.
That means a `CircleMarker` will not change size on your screen when you zoom,
while `Circle` will have a fixed position on the map.

```{code-cell} ipython3
import folium

m = folium.Map(location=[-27.5717, -48.6256], zoom_start=9)

radius = 50
folium.CircleMarker(
    location=[-27.55, -48.8],
    radius=radius,
    color="cornflowerblue",
    stroke=False,
    fill=True,
    fill_opacity=0.6,
    opacity=1,
    popup="{} pixels".format(radius),
    tooltip="I am in pixels",
).add_to(m)

radius = 25
folium.CircleMarker(
    location=[-27.35, -48.8],
    radius=radius,
    color="black",
    weight=3,
    fill=False,
    fill_opacity=0.6,
    opacity=1,
).add_to(m)

radius = 10000
folium.Circle(
    location=[-27.551667, -48.478889],
    radius=radius,
    color="black",
    weight=1,
    fill_opacity=0.6,
    opacity=1,
    fill_color="green",
    fill=False,  # gets overridden by fill_color
    popup="{} meters".format(radius),
    tooltip="I am in meters",
).add_to(m)

m
```
