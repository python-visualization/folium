```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# Icons

## Rotate icons

```{code-cell} ipython3
m = folium.Map(location=[41, -71], zoom_start=4)

kw = {"prefix": "fa", "color": "green", "icon": "arrow-up"}

angle = 180
icon = folium.Icon(angle=angle, **kw)
folium.Marker(location=[41, -72], icon=icon, tooltip=str(angle)).add_to(m)

angle = 45
icon = folium.Icon(angle=angle, **kw)
folium.Marker(location=[41, -75], icon=icon, tooltip=str(angle)).add_to(m)

angle = 90
icon = folium.Icon(angle=angle, **kw)
folium.Marker([41, -78], icon=icon, tooltip=str(angle)).add_to(m)

m
```

## Custom icon

```{code-cell} ipython3
m = folium.Map(location=[45.3288, -121.6625], zoom_start=12, tiles="Stamen Terrain")

url = "https://leafletjs.com/examples/custom-icons/{}".format
icon_image = url("leaf-red.png")
shadow_image = url("leaf-shadow.png")

icon = folium.CustomIcon(
    icon_image,
    icon_size=(38, 95),
    icon_anchor=(22, 94),
    shadow_image=shadow_image,
    shadow_size=(50, 64),
    shadow_anchor=(4, 62),
    popup_anchor=(-3, -76),
)

folium.Marker(
    location=[45.3288, -121.6625], icon=icon, popup="Mt. Hood Meadows"
).add_to(m)

m
```
