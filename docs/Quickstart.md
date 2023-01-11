---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

Quickstart
==========


Getting Started
---------------


To create a base map, simply pass your starting coordinates to Folium:

```{code-cell} ipython3
import folium


m = folium.Map(location=[45.5236, -122.6750])
```

To display it in a Jupyter notebook, simply ask for the object representation:

```{code-cell} ipython3
m
```

to save it in a file,

```{code-cell} ipython3
m.save("index.html")
```

The default tiles are set to `OpenStreetMap`, but `Stamen Terrain`, `Stamen Toner`, `Mapbox Bright`, and `Mapbox Control Room`, and many others tiles are built in.

```{code-cell} ipython3
folium.Map(location=[45.5236, -122.6750], zoom_start=13)
```

One can use `Cloudmade` or `Mapbox` custom tilesets--simply pass your key to the `API_key` keyword:

```python
folium.Map(location=[45.5236, -122.6750],
           tiles='Mapbox',
           API_key='your.API.key')
```

Lastly, Folium supports passing any `leaflet.js` compatible custom tileset:

```python
folium.Map(location=[45.372, -121.6972],
           zoom_start=12,
           tiles='http://{s}.tiles.yourtiles.com/{z}/{x}/{y}.png',
           attr='My Data Attribution')
```

+++

Markers
-------

There are numerous marker types, starting with a simple `Leaflet`
style location marker with a popup and tooltip `HTML`.

```{code-cell} ipython3
m = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles="Stamen Terrain")

tooltip = "Click me!"

folium.Marker(
    [45.3288, -121.6625], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
).add_to(m)
folium.Marker(
    [45.3311, -121.7113], popup="<b>Timberline Lodge</b>", tooltip=tooltip
).add_to(m)

m
```

There is built in support for colors and marker icon types from bootstrap.

```{code-cell} ipython3
m = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles="Stamen Terrain")

folium.Marker(
    location=[45.3288, -121.6625],
    popup="Mt. Hood Meadows",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[45.3311, -121.7113],
    popup="Timberline Lodge",
    icon=folium.Icon(color="green"),
).add_to(m)

folium.Marker(
    location=[45.3300, -121.6823],
    popup="Some Other Location",
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(m)


m
```

Leaflet's `Circle` and `CircleMarker`, implemented to reflect radii in units of meters and pixels respectively, are available as `features`. See the `features.py` for more options.

```{code-cell} ipython3
m = folium.Map(location=[45.5236, -122.6750], tiles="Stamen Toner", zoom_start=13)

folium.Circle(
    radius=100,
    location=[45.5244, -122.6699],
    popup="The Waterfront",
    color="crimson",
    fill=False,
).add_to(m)

folium.CircleMarker(
    location=[45.5215, -122.6261],
    radius=50,
    popup="Laurelhurst Park",
    color="#3186cc",
    fill=True,
    fill_color="#3186cc",
).add_to(m)


m
```

a convenience function to enable lat/lon popovers. This can help users to find a location by interactively browsing the map.

```{code-cell} ipython3
m = folium.Map(location=[46.1991, -122.1889], tiles="Stamen Terrain", zoom_start=13)

m.add_child(folium.LatLngPopup())

m
```

and click-for-marker functionality for on-the-fly placement of markers:

```{code-cell} ipython3
m = folium.Map(location=[46.8527, -121.7649], tiles="Stamen Terrain", zoom_start=13)

folium.Marker([46.8354, -121.7325], popup="Camp Muir").add_to(m)

m.add_child(folium.ClickForMarker(popup="Waypoint"))


m
```

## Polylines

`folium` can show linear elements on a map using `PolyLine`. This object can help put emphasis on a trail, a road, or a coastline.

```{code-cell} ipython3
m = folium.Map(location=[-71.38, -73.9], zoom_start=11)

trail_coordinates = [
    (-71.351871840295871, -73.655963711222626),
    (-71.374144382613707, -73.719861619751498),
    (-71.391042575973145, -73.784922248007007),
    (-71.400964450973134, -73.851042243124397),
    (-71.402411391077322, -74.050048183880477),
]


folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(m)

m
```

## Vincent/Vega and Altair/VegaLite Markers

`folium` enables passing any HTML object as a popup,
including [`bokeh`](https://docs.bokeh.org/en/latest/) plots,
but there is a built-in support for [vincent](https://github.com/wrobstory/vincent) and [altair](https://altair-viz.github.io) visualizations to any marker type, with the visualization as the popover.

```{code-cell} ipython3
import json

import requests

url = (
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
)
vis1 = json.loads(requests.get(f"{url}/vis1.json").text)
vis2 = json.loads(requests.get(f"{url}/vis2.json").text)
vis3 = json.loads(requests.get(f"{url}/vis3.json").text)
```

```{code-cell} ipython3
m = folium.Map(location=[46.3014, -123.7390], zoom_start=7, tiles="Stamen Terrain")

folium.Marker(
    location=[47.3489, -124.708],
    popup=folium.Popup(max_width=450).add_child(
        folium.Vega(vis1, width=450, height=250)
    ),
).add_to(m)

folium.Marker(
    location=[44.639, -124.5339],
    popup=folium.Popup(max_width=450).add_child(
        folium.Vega(vis2, width=450, height=250)
    ),
).add_to(m)

folium.Marker(
    location=[46.216, -124.1280],
    popup=folium.Popup(max_width=450).add_child(
        folium.Vega(vis3, width=450, height=250)
    ),
).add_to(m)


m
```

For more information about popups, please visit [Popups.ipynb](https://nbviewer.org/github/python-visualization/folium/blob/main/examples/Popups.ipynb)

+++

## GeoJSON/TopoJSON Overlays

Both GeoJSON and TopoJSON layers can be passed to the map as an overlay, and multiple layers can be visualized on the same map:

```{code-cell} ipython3
url = (
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
)
antarctic_ice_edge = f"{url}/antarctic_ice_edge.json"
antarctic_ice_shelf_topo = f"{url}/antarctic_ice_shelf_topo.json"


m = folium.Map(
    location=[-59.1759, -11.6016],
    tiles="cartodbpositron",
    zoom_start=2,
)

folium.GeoJson(antarctic_ice_edge, name="geojson").add_to(m)

folium.TopoJson(
    json.loads(requests.get(antarctic_ice_shelf_topo).text),
    "objects.antarctic_ice_shelf",
    name="topojson",
).add_to(m)

folium.LayerControl().add_to(m)


m
```

## Choropleth maps

Choropleth can be easily created by binding the data between Pandas DataFrames/Series and Geo/TopoJSON geometries. [Color Brewer](https://colorbrewer2.org/) sequential color schemes are built-in to the library, and can be passed to quickly visualize different combinations.

```{code-cell} ipython3
import pandas as pd

url = (
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
)
state_geo = f"{url}/us-states.json"
state_unemployment = f"{url}/US_Unemployment_Oct2012.csv"
state_data = pd.read_csv(state_unemployment)

m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
).add_to(m)

folium.LayerControl().add_to(m)

m
```

The legend on the upper right is automatically generated for your values using 6 same sized bins.
Passing your own bins (number or list) is simple:

```{code-cell} ipython3
bins = list(state_data["Unemployment"].quantile([0, 0.25, 0.5, 0.75, 1]))

m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="BuPu",
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="Unemployment Rate (%)",
    bins=bins,
    reset=True,
).add_to(m)

m
```

By binding data via the Pandas DataFrame, different datasets can be quickly visualized.

+++

## Styling function

`GeoJson` and `TopoJson` features accepts `style_function` to allow for further custimization of the map.
Take a look at the use examples below.

```{code-cell} ipython3
import branca

url = (
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
)
county_data = f"{url}/us_county_data.csv"
county_geo = f"{url}/us_counties_20m_topo.json"


df = pd.read_csv(county_data, na_values=[" "])

colorscale = branca.colormap.linear.YlOrRd_09.scale(0, 50e3)
employed_series = df.set_index("FIPS_Code")["Employed_2011"]


def style_function(feature):
    employed = employed_series.get(int(feature["id"][-5:]), None)
    return {
        "fillOpacity": 0.5,
        "weight": 0,
        "fillColor": "#black" if employed is None else colorscale(employed),
    }


m = folium.Map(location=[48, -102], tiles="cartodbpositron", zoom_start=3)

folium.TopoJson(
    json.loads(requests.get(county_geo).text),
    "objects.us_counties_20m",
    style_function=style_function,
).add_to(m)


m
```

```{code-cell} ipython3
colorscale = branca.colormap.linear.YlGnBu_09.scale(0, 30)

employed_series = df.set_index("FIPS_Code")["Unemployment_rate_2011"]


def style_function(feature):
    employed = employed_series.get(int(feature["id"][-5:]), None)
    return {
        "fillOpacity": 0.5,
        "weight": 0,
        "fillColor": "#black" if employed is None else colorscale(employed),
    }


m = folium.Map(location=[48, -102], tiles="cartodbpositron", zoom_start=3)

folium.TopoJson(
    json.loads(requests.get(county_geo).text),
    "objects.us_counties_20m",
    style_function=style_function,
).add_to(m)


m
```

```{code-cell} ipython3
colorscale = branca.colormap.linear.PuRd_09.scale(0, 100000)

employed_series = df.set_index("FIPS_Code")["Median_Household_Income_2011"].dropna()


def style_function(feature):
    employed = employed_series.get(int(feature["id"][-5:]), None)
    return {
        "fillOpacity": 0.5,
        "weight": 0,
        "fillColor": "#black" if employed is None else colorscale(employed),
    }


m = folium.Map(location=[48, -102], tiles="cartodbpositron", zoom_start=3)

folium.TopoJson(
    json.loads(requests.get(county_geo).text),
    "objects.us_counties_20m",
    style_function=style_function,
).add_to(m)


m
```

For more examples and use cases please take a look at the gallery:

https://nbviewer.org/github/python-visualization/folium_contrib/tree/main/notebooks/
