```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# WmsTileLayer

`transparent=True` requests a transparent background from the WMS server.
It does not make black (or other colored) pixels in the returned imagery transparent.
Use an image format that supports transparency, such as `image/png`, and check
that the server supports transparency for the requested layer.

```{code-cell} ipython3
m = folium.Map(location=[41, -70], zoom_start=5, tiles="cartodb positron")

folium.WmsTileLayer(
    url="https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
    name="test",
    fmt="image/png",
    layers="nexrad-n0r-900913",
    attr=u"Weather data © 2012 IEM Nexrad",
    transparent=True,
    overlay=True,
    control=True,
).add_to(m)

folium.LayerControl().add_to(m)

m
```
