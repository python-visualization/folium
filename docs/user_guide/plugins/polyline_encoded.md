```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

# PolyLineFromEncoded

```{code-cell} ipython3

m = folium.Map(location=[40, -120], zoom_start=5)

encoded =  r"_p~iF~cn~U_ulLn{vA_mqNvxq`@"
plugins.PolyLineFromEncoded(encoded=encoded).add_to(m)

m
```
