```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## BeautifyIcon

```{code-cell} ipython3
m = folium.Map([45.5, -122], zoom_start=3)

icon_plane = folium.plugins.BeautifyIcon(
    icon="plane", border_color="#b3334f", text_color="#b3334f", icon_shape="triangle"
)

icon_number = folium.plugins.BeautifyIcon(
    border_color="#00ABDC",
    text_color="#00ABDC",
    number=10,
    inner_icon_style="margin-top:0;",
)

folium.Marker(location=[46, -122], popup="Portland, OR", icon=icon_plane).add_to(m)

folium.Marker(location=[50, -122], popup="Portland, OR", icon=icon_number).add_to(m)

m
```
