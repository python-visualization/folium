## Features

### ColorLine

```{code-cell} ipython3
import numpy as np

x = np.linspace(0, 2 * np.pi, 300)

lats = 20 * np.cos(x)
lons = 20 * np.sin(x)
colors = np.sin(5 * x)
```

```{code-cell} ipython3
import folium
from folium import features


m = folium.Map([0, 0], zoom_start=3)

color_line = features.ColorLine(
    positions=list(zip(lats, lons)),
    colors=colors,
    colormap=["y", "orange", "r"],
    weight=10,
)

color_line.add_to(m)

m
```

### Marker, Icon, Popup

```{code-cell} ipython3
m = folium.Map([0, 0], zoom_start=1)
mk = features.Marker([0, 0])
pp = folium.Popup("hello")
ic = features.Icon(color="red")

mk.add_child(ic)
mk.add_child(pp)
m.add_child(mk)

m
```

### Vega popup

```{code-cell} ipython3
import json

import vincent

N = 100

multi_iter2 = {
    "x": np.random.uniform(size=(N,)),
    "y": np.random.uniform(size=(N,)),
}

scatter = vincent.Scatter(multi_iter2, iter_idx="x", height=100, width=200)
data = json.loads(scatter.to_json())

m = folium.Map([0, 0], zoom_start=1)
mk = features.Marker([0, 0])
p = folium.Popup("Hello")
v = features.Vega(data, width="100%", height="100%")

mk.add_child(p)
p.add_child(v)
m.add_child(mk)

m
```

### Vega-Lite popup

```{code-cell} ipython3
from altair import Chart

import vega_datasets

# load built-in dataset as a pandas DataFrame
cars = vega_datasets.data.cars()

scatter = (
    Chart(cars)
    .mark_circle()
    .encode(
        x="Horsepower",
        y="Miles_per_Gallon",
        color="Origin",
    )
)

vega = folium.features.VegaLite(
    scatter,
    width="100%",
    height="100%",
)

m = folium.Map(location=[-27.5717, -48.6256])

marker = folium.features.Marker([-27.57, -48.62])

popup = folium.Popup()

vega.add_to(popup)
popup.add_to(marker)

marker.add_to(m)

m
```

### Vega div and a Map

```{code-cell} ipython3
import branca

N = 100

multi_iter2 = {
    "x": np.random.uniform(size=(N,)),
    "y": np.random.uniform(size=(N,)),
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

# Create two Vega.
v = features.Vega(data, position="absolute", left="50%", width="50%", height="50%")

v2 = features.Vega(
    data, position="absolute", left="0%", width="50%", height="50%", top="50%"
)

f.add_child(m)
f.add_child(m2)
f.add_child(v)
f.add_child(v2)

f
```

### Vega-Lite div and a Map

```{code-cell} ipython3
import pandas as pd

N = 100

multi_iter2 = pd.DataFrame(
    {
        "x": np.random.uniform(size=(N,)),
        "y": np.random.uniform(size=(N,)),
    }
)

scatter = Chart(multi_iter2).mark_circle().encode(x="x", y="y")
scatter.width = 420
scatter.height = 250
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


# Create two Vega.
v = features.VegaLite(data, position="absolute", left="50%", width="50%", height="50%")

v2 = features.VegaLite(
    data, position="absolute", left="0%", width="50%", height="50%", top="50%"
)

f.add_child(m)
f.add_child(m2)
f.add_child(v)
f.add_child(v2)

f
```

### GeoJson

```{code-cell} ipython3
N = 1000

lons = +5 - np.random.normal(size=N)
lats = 48 - np.random.normal(size=N)

data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": [[lon, lat] for (lat, lon) in zip(lats, lons)],
            },
            "properties": {"prop0": "value0"},
        },
    ],
}

m = folium.Map([48, 5], zoom_start=6)
m.add_child(features.GeoJson(data))

m
```

### Div

```{code-cell} ipython3
N = 100

multi_iter2 = {
    "x": np.random.uniform(size=(N,)),
    "y": np.random.uniform(size=(N,)),
}

scatter = vincent.Scatter(multi_iter2, iter_idx="x", height=250, width=420)
data = json.loads(scatter.to_json())

f = branca.element.Figure()

d1 = f.add_subplot(1, 2, 1)
d2 = f.add_subplot(1, 2, 2)

d1.add_child(folium.Map([0, 0], tiles="stamenwatercolor", zoom_start=1))
d2.add_child(folium.Map([46, 3], tiles="OpenStreetMap", zoom_start=5))

f
```

### LayerControl

```{code-cell} ipython3
m = folium.Map(tiles=None)

folium.raster_layers.TileLayer("OpenStreetMap").add_to(m)
folium.raster_layers.TileLayer("stamentoner", show=False).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

m
```
