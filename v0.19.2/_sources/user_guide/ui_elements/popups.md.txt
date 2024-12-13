# Popups

## Simple popups

You can define your popup at the feature creation, but you can also overwrite them afterwards:

```{code-cell} ipython3
import folium


m = folium.Map([45, 0], zoom_start=4)

folium.Marker([45, -30], popup="inline implicit popup").add_to(m)

folium.CircleMarker(
    location=[45, -10],
    radius=25,
    fill=True,
    popup=folium.Popup("inline explicit Popup"),
).add_to(m)

ls = folium.PolyLine(
    locations=[[43, 7], [43, 13], [47, 13], [47, 7], [43, 7]], color="red"
)

ls.add_child(folium.Popup("outline Popup on Polyline"))
ls.add_to(m)

gj = folium.GeoJson(
    data={"type": "Polygon", "coordinates": [[[27, 43], [33, 43], [33, 47], [27, 47]]]}
)

gj.add_child(folium.Popup("outline Popup on GeoJSON"))
gj.add_to(m)

m
```

```{code-cell} ipython3
m = folium.Map([45, 0], zoom_start=2)

folium.Marker(
    location=[45, -10],
    popup=folium.Popup("Let's try quotes", parse_html=True, max_width=100),
).add_to(m)

folium.Marker(
    location=[45, -30],
    popup=folium.Popup(u"Ça c'est chouette", parse_html=True, max_width="100%"),
).add_to(m)

m
```

## HTML in popup

```{code-cell} ipython3
import branca

m = folium.Map([43, -100], zoom_start=4)

html = """
    <h1> This is a big popup</h1><br>
    With a few lines of code...
    <p>
    <code>
        from numpy import *<br>
        exp(-2*pi)
    </code>
    </p>
    """


folium.Marker([30, -100], popup=html).add_to(m)

m
```

## Iframe in popup

You can also put any HTML code inside a Popup, thaks to the `IFrame` object.

```{code-cell} ipython3
m = folium.Map([43, -100], zoom_start=4)

html = """
    <h1> This popup is an Iframe</h1><br>
    With a few lines of code...
    <p>
    <code>
        from numpy import *<br>
        exp(-2*pi)
    </code>
    </p>
    """

iframe = branca.element.IFrame(html=html, width=500, height=300)
popup = folium.Popup(iframe, max_width=500)

folium.Marker([30, -100], popup=popup).add_to(m)

m
```

```{code-cell} ipython3
import pandas as pd

df = pd.DataFrame(
    data=[["apple", "oranges"], ["other", "stuff"]], columns=["cats", "dogs"]
)

m = folium.Map([43, -100], zoom_start=4)

html = df.to_html(
    classes="table table-striped table-hover table-condensed table-responsive"
)

popup = folium.Popup(html)

folium.Marker([30, -100], popup=popup).add_to(m)

m
```

Note that you can put another `Figure` into an `IFrame` ; this should let you do strange things...

```{code-cell} ipython3
# Let's create a Figure, with a map inside.
f = branca.element.Figure()
folium.Map([-25, 150], zoom_start=3).add_to(f)

# Let's put the figure into an IFrame.
iframe = branca.element.IFrame(width=500, height=300)
f.add_to(iframe)

# Let's put the IFrame in a Popup
popup = folium.Popup(iframe, max_width=2650)

# Let's create another map.
m = folium.Map([43, -100], zoom_start=4)

# Let's put the Popup on a marker, in the second map.
folium.Marker([30, -100], popup=popup).add_to(m)

# We get a map in a Popup. Not really useful, but powerful.
m
```


## Vega chart in popup

[Vega](https://vega.github.io/vega/) is a way to describe charts. You can embed
a Vega chart in a popup using the `Vega` class.

```{code-cell} ipython3
import json

import numpy as np
import vincent

multi_iter2 = {
    "x": np.random.uniform(size=(100,)),
    "y": np.random.uniform(size=(100,)),
}
scatter = vincent.Scatter(multi_iter2, iter_idx="x", height=100, width=200)
data = json.loads(scatter.to_json())

m = folium.Map([0, 0], zoom_start=1)
marker = folium.Marker([0, 0]).add_to(m)
popup = folium.Popup("Hello").add_to(marker)
folium.Vega(data, width="100%", height="100%").add_to(popup)

m
```

## Vega-Lite chart in popup

[Vega-lite](https://vega.github.io/vega-lite/) is a higher-level version of Vega.
Folium supports it as well in the `VegaLite` class.

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

vega_lite = folium.VegaLite(
    scatter,
    width="100%",
    height="100%",
)

m = folium.Map(location=[-27.5717, -48.6256])

marker = folium.Marker([-27.57, -48.62])

popup = folium.Popup()

vega_lite.add_to(popup)
popup.add_to(marker)

marker.add_to(m)

m
```

## Lazy loading

If whatever you are showing in the popup is slow or heavy to load and you have many popups, you may not want to render the popup contents immediately. There's an argument to prevent loading until the popup is opened.

```{code-cell} ipython3
m = folium.Map([43, -100], zoom_start=4)

html = "{a resource that is heavy to load, such as an image}"

folium.Marker([30, -100], popup=html, lazy=True).add_to(m)

m
```
