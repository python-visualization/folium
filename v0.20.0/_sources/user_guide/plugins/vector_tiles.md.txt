# Vector tiles using VectorGridProtobuf

```{code-cell} ipython3
from folium.plugins import VectorGridProtobuf
import folium
```

```{code-cell} ipython3
styles = {
    "water": {
        "fill": True,
        "weight": 1,
        "fillColor": "#06cccc",
        "color": "#06cccc",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "admin": {
        "weight": 1,
        "fillColor": "pink",
        "color": "pink",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "waterway": {
        "weight": 1,
        "fillColor": "#2375e0",
        "color": "#2375e0",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "landcover": {
        "fill": True,
        "weight": 1,
        "fillColor": "#53e033",
        "color": "#53e033",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "landuse": {
        "fill": True,
        "weight": 1,
        "fillColor": "#e5b404",
        "color": "#e5b404",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "park": {
        "fill": True,
        "weight": 1,
        "fillColor": "#84ea5b",
        "color": "#84ea5b",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "boundary": {
        "weight": 1,
        "fillColor": "#c545d3",
        "color": "#c545d3",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "aeroway": {
        "weight": 1,
        "fillColor": "#51aeb5",
        "color": "#51aeb5",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "building": {
        "fill": True,
        "weight": 1,
        "fillColor": "#2b2b2b",
        "color": "#2b2b2b",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "water_name": {
        "weight": 1,
        "fillColor": "#022c5b",
        "color": "#022c5b",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "transportation_name": {
        "weight": 1,
        "fillColor": "#bc6b38",
        "color": "#bc6b38",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "place": {
        "weight": 1,
        "fillColor": "#f20e93",
        "color": "#f20e93",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "housenumber": {
        "weight": 1,
        "fillColor": "#ef4c8b",
        "color": "#ef4c8b",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "poi": {
        "weight": 1,
        "fillColor": "#3bb50a",
        "color": "#3bb50a",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
    "road": {
        "weight": 1,
        "fillColor": "#f2b648",
        "color": "#f2b648",
        "fillOpacity": 0.2,
        "opacity": 0.4
    },
}
```

```{code-cell} ipython3
vectorTileLayerStyles = {}
vectorTileLayerStyles["aerodrome_label"] = []
vectorTileLayerStyles["aeroway"] = []
vectorTileLayerStyles["area_name"] = []
vectorTileLayerStyles["boundary"] = styles["admin"]
vectorTileLayerStyles["building"] = []
vectorTileLayerStyles["building_ln"] = []
vectorTileLayerStyles["construct"] = []
vectorTileLayerStyles["contour_line"] = []
vectorTileLayerStyles["landcover"] = styles["landcover"]
vectorTileLayerStyles["landuse"] = styles["landuse"]
vectorTileLayerStyles["mountain_peak"] = []
vectorTileLayerStyles["park"] = styles["park"]
vectorTileLayerStyles["place"] = []
vectorTileLayerStyles["poi"] = []
vectorTileLayerStyles["spot_elevation"] = []
vectorTileLayerStyles["transportation"] = styles["road"]
vectorTileLayerStyles["transportation_name"] = []
vectorTileLayerStyles["water"] = styles["water"]
vectorTileLayerStyles["waterway"] = styles["water"]
vectorTileLayerStyles["water_name"] = []
```

```{code-cell} ipython3
url = "https://vectortiles3.geo.admin.ch/tiles/ch.swisstopo.leichte-basiskarte.vt/v1.0.0/{z}/{x}/{y}.pbf"
m = folium.Map(tiles=None, location=[46.8, 8.2], zoom_start=14)

options = {
    "vectorTileLayerStyles": vectorTileLayerStyles
}

VectorGridProtobuf(url, "folium_layer_name", options).add_to(m)

m
```
