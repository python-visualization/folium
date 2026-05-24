```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

# WebGL Earth

Render a 3D interactive globe instead of a flat map, using the
WebGL Earth v2 library.

Based on: https://www.webglearth.com/

The flat Leaflet map is replaced by a 3D globe. Markers, tile
layers, and live data updates are all supported.

## Simple example

```{code-cell} ipython3
import folium
from folium.plugins import WebGLEarth, WebGLEarthMarker

m = folium.Map()

globe = WebGLEarth(center=[20, 0], zoom=2)
globe.add_to(m)

WebGLEarthMarker(location=[48.8566, 2.3522], popup="Paris").add_to(globe)
WebGLEarthMarker(location=[35.6762, 139.6503], popup="Tokyo").add_to(globe)
WebGLEarthMarker(location=[40.7128, -74.0060], popup="New York").add_to(globe)

m
```

## Custom tile layer

Add an additional tile overlay on top of the default OpenStreetMap tiles.

```{code-cell} ipython3
import folium
from folium.plugins import WebGLEarth, WebGLEarthTileLayer

m = folium.Map()

globe = WebGLEarth(center=[20, 0], zoom=2)
globe.add_to(m)

WebGLEarthTileLayer(
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution="© OpenStreetMap contributors",
    opacity=0.5,
).add_to(globe)

m
```

## Live ISS tracker

Use `WebGLEarthRealtime` to show live-updating data on the globe.
In this example we track the International Space Station using a
public API — the 3D equivalent of the Realtime plugin demo.

```{code-cell} ipython3
import folium
from folium import JsCode
from folium.plugins import WebGLEarth, WebGLEarthRealtime

m = folium.Map()

globe = WebGLEarth(center=[0, 0], zoom=1.8)
globe.add_to(m)

WebGLEarthRealtime(
    source_url="https://api.wheretheiss.at/v1/satellites/25544",
    interval=3000,
    on_update=JsCode("""
        function(data, earth) {
            if (window._issMarker) window._issMarker.removeFrom(earth);
            window._issMarker = WE.marker(
                [data.latitude, data.longitude]
            ).addTo(earth);
            window._issMarker.bindPopup(
                '<b>ISS</b><br>'
                + 'Lat: ' + data.latitude.toFixed(2)
                + '<br>Lng: ' + data.longitude.toFixed(2)
                + '<br>Alt: ' + data.altitude.toFixed(1) + ' km'
            );
        }
    """),
).add_to(globe)

m
```