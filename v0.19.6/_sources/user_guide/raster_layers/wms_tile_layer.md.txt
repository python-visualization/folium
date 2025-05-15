```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# WmsTileLayer

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
