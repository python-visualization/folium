```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
from folium import plugins
```

# PolygonFromEncoded

```{code-cell} ipython3

m = folium.Map(location=[40, -80], zoom_start=5)

encoded =  r"w`j~FpxivO}jz@qnnCd}~Bsa{@~f`C`lkH"
plugins.PolygonFromEncoded(encoded=encoded).add_to(m)

m
```
