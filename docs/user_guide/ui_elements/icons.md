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
m = folium.Map(location=[45.3288, -121.6625], zoom_start=12)

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

## Text labels with DivIcon

`DivIcon` allows you to add text directly on the map using an HTML `div` element.
This is useful when you want a visible label at a specific location, without
relying on tooltips or popups that only appear on interaction.

```{code-cell} ipython3
m = folium.Map(location=[41, -71], zoom_start=6)

folium.Marker(
    location=[41, -71],
    icon=folium.DivIcon(
        html='<div style="font-size: 14px; color: black; font-weight: bold;">New York</div>',
        icon_size=(100, 36),
        icon_anchor=(50, 18),
    ),
).add_to(m)

folium.Marker(
    location=[42.36, -71.06],
    icon=folium.DivIcon(
        html='<div style="font-size: 12px; color: navy;">Boston</div>',
        icon_size=(80, 30),
        icon_anchor=(40, 15),
    ),
).add_to(m)

m
```