## Heatmap

```{code-cell} ipython3
import numpy as np

data = (
    np.random.normal(size=(100, 3)) * np.array([[1, 1, 1]]) + np.array([[48, 5, 1]])
).tolist()
```

```{code-cell} ipython3
import folium
from folium.plugins import HeatMap

m = folium.Map([48.0, 5.0], tiles="stamentoner", zoom_start=6)

HeatMap(data).add_to(m)

m
```
