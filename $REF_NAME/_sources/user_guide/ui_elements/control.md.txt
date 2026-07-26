```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
from folium.features import Control
```

# Controls

Leaflet controls are UI elements anchored to the corners of a map (zoom, scale,
custom buttons, etc.). Folium exposes a generic `Control` class that can render
any `L.Control.<Name>` class. This is useful when you want to wire up a Leaflet
plugin directly in user code without creating a new `folium.plugins` class.

## Built-in controls

```{code-cell} ipython3
m = folium.Map(location=[45, 0], zoom_start=4, zoom_control=False)

Control("Zoom", position="topleft").add_to(m)
Control("Scale", position="bottomleft").add_to(m)

m
```

## Leaflet plugin controls

If a Leaflet plugin exposes a `L.Control.<Name>` class, you can wire it up
directly and attach its JS/CSS assets to the map.

```{code-cell} ipython3
import folium
from folium.features import Control

m = folium.Map(location=[45, 0], zoom_start=4)

control = Control(
    "fullscreen",
    position="topright",
    # Any plugin options become JS options.
    title="View Fullscreen",
    titleCancel="Exit Fullscreen",
)

# Add the plugin's JS/CSS assets.
control.add_js_link(
    "leaflet-fullscreen",
    "https://unpkg.com/leaflet-fullscreen@1.6.0/dist/leaflet.fullscreen.umd.js",
)
control.add_css_link(
    "leaflet-fullscreen",
    "https://unpkg.com/leaflet.fullscreen@1.6.0/Control.FullScreen.css",
)

control.add_to(m)
m
```

For reusable plugins, consider creating a dedicated `folium.plugins` class. For
one-off integrations, `Control` keeps the wiring minimal.
