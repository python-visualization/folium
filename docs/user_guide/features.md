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


### Click-related classes

#### ClickForMarker

`ClickForMarker` lets you create markers on each click.

```{code-cell} ipython3
folium.Map().add_child(
    folium.ClickForMarker()
)
```

*Click on the map to see the effects*

You can customize the popup by providing a string, an IFrame object or an Html object. You can include the latitude and longitude of the marker by using `${lat}` and `${lng}`.

```{code-cell} ipython3
folium.Map().add_child(
    folium.ClickForMarker("<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}")
)
```

*Click on the map to see the effects*


#### LatLngPopup

`LatLngPopup` lets you create a simple popup at each click.

```{code-cell} ipython3
folium.Map().add_child(
    folium.LatLngPopup()
)
```

*Click on the map to see the effects*

+++

#### ClickForLatLng

`ClickForLatLng` lets you copy coordinates to your browser clipboard.

```{code-cell} ipython3
folium.Map().add_child(
    folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=True)
)
```

*Click on the map to see the effects*

If you want to collect back the information in python, you may (install and) import the [clipboard](https://github.com/terryyin/clipboard) library:

```
>>> import clipboard
>>> clipboard.paste()
[-43.580391,-123.824467]
```

### Custom icon

```{code-cell} ipython3
m = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles="Stamen Terrain")

url = "https://leafletjs.com/examples/custom-icons/{}".format
icon_image = url("leaf-red.png")
shadow_image = url("leaf-shadow.png")

icon = folium.features.CustomIcon(
    icon_image,
    icon_size=(38, 95),
    icon_anchor=(22, 94),
    shadow_image=shadow_image,
    shadow_size=(50, 64),
    shadow_anchor=(4, 62),
    popup_anchor=(-3, -76),
)

folium.Marker(
    location=[45.3288, -121.6625], icon=icon, popup="Mt. Hood Meadows"
).add_to(m)

m
```
