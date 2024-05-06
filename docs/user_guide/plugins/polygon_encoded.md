```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
from folium import plugins
```

# PolygonFromEncoded

Create a Polygon directly from an encoded polyline string. To understand the encoding algorithm
refer to [this](https://developers.google.com/maps/documentation/utilities/polylinealgorithm) link.

```{code-cell} ipython3

m = folium.Map(location=[40, -80], zoom_start=5)

encoded =  r"w`j~FpxivO}jz@qnnCd}~Bsa{@~f`C`lkH"
plugins.PolygonFromEncoded(encoded=encoded).add_to(m)

m
```
