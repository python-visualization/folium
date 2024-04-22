# TimestampedWmsTileLayers

Add a time dimension to a WMS tile layer.

### Exploring the WMS with OWSLib

```{code-cell} ipython3
from owslib.wms import WebMapService


url = "https://pae-paha.pacioos.hawaii.edu/thredds/wms/dhw_5km?service=WMS"

web_map_services = WebMapService(url)

print("\n".join(web_map_services.contents.keys()))
```

### Layer metadata

```{code-cell} ipython3
layer = "CRW_SST"
wms = web_map_services.contents[layer]

name = wms.title

lon = (wms.boundingBox[0] + wms.boundingBox[2]) / 2.0
lat = (wms.boundingBox[1] + wms.boundingBox[3]) / 2.0
center = lat, lon

time_interval = "{0}/{1}".format(
    wms.timepositions[0].strip(), wms.timepositions[-1].strip()
)
style = "boxfill/sst_36"

if style not in wms.styles:
    style = None
```

### Map with WmsTileLayer and TimestampedWmsTileLayers

```{code-cell} ipython3
import folium
import folium.plugins

m = folium.Map(location=[-40, -50], zoom_start=5)

wms_tile_layer = folium.WmsTileLayer(
    url=url,
    name=name,
    styles=style,
    fmt="image/png",
    transparent=True,
    layers=layer,
    overlay=True,
    COLORSCALERANGE="1.2,28",
).add_to(m)

folium.plugins.TimestampedWmsTileLayers(
    wms_tile_layer,
    period="PT1H",
    time_interval=time_interval,
).add_to(m)

folium.LayerControl().add_to(m)

m
```
