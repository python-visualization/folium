```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import branca
```

## Subplots

### Two maps in one figure

A `Map` automatically creates a `Figure` to put itself in. You can also do this
manually, or in this example, create subplots to have two maps in one figure.

```{code-cell} ipython3
fig = branca.element.Figure()

subplot1 = fig.add_subplot(1, 2, 1)
subplot2 = fig.add_subplot(1, 2, 2)

subplot1.add_child(
    folium.Map([0, 0], tiles="stamenwatercolor", zoom_start=1)
)
subplot2.add_child(
    folium.Map([46, 3], tiles="OpenStreetMap", zoom_start=5)
)

fig
```


### Vega div and a Map

Here we create a single figure in which we'll embed two maps and two Vega charts.
Note that this also works with `VegaLite`.

```{code-cell} ipython3
import json

import numpy as np
import vincent


multi_iter2 = {
    "x": np.random.uniform(size=(100,)),
    "y": np.random.uniform(size=(100,)),
}
scatter = vincent.Scatter(multi_iter2, iter_idx="x", height=250, width=420)
data = json.loads(scatter.to_json())

f = branca.element.Figure()

# Create two maps.
m = folium.Map(
    location=[0, 0],
    tiles="stamenwatercolor",
    zoom_start=1,
    position="absolute",
    left="0%",
    width="50%",
    height="50%",
)

m2 = folium.Map(
    location=[46, 3],
    tiles="OpenStreetMap",
    zoom_start=4,
    position="absolute",
    left="50%",
    width="50%",
    height="50%",
    top="50%",
)

# Create two Vega charts
v = folium.Vega(data, position="absolute", left="50%", width="50%", height="50%")

v2 = folium.Vega(
    data, position="absolute", left="0%", width="50%", height="50%", top="50%"
)

f.add_child(m)
f.add_child(m2)
f.add_child(v)
f.add_child(v2)

f
```
