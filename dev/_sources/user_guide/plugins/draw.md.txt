# Draw

```{code-cell} ipython3
import folium
from folium.plugins import Draw

m = folium.Map()

Draw(export=True).add_to(m)

m
```
