Getting started
===============

Installation
------------

Folium can be installed using

```
$ pip install folium
```

If you are using the Conda package manager, the equivalent is

```
$ conda install folium -c conda-forge
```


### Dependencies

Folium has the following dependencies, all of which are installed automatically
with the above installation commands:

- branca
- Jinja2
- Numpy
- Requests

Additional packages may be necessary for some functionality. It will say so in
the documentation where that's the case.


Creating a map
---------------

Here's a basic example of creating a map:

```{code-cell} ipython3
import folium

m = folium.Map(location=(45.5236, -122.6750))
```

If you are in a Jupyter Notebook, you can display it by asking for the object representation:

```{code-cell} ipython3
m
```

Or you can save it as an HTML file:

```{code-cell} ipython3
m.save("index.html")
```


Choosing a tileset
------------------

The default tiles are set to `OpenStreetMap`, but a selection of tilesets are also built in.

```{code-cell} ipython3
folium.Map((45.5236, -122.6750), tiles="cartodb positron")
```

You can also pass any tileset as a url template. Choose one from https://leaflet-extras.github.io/leaflet-providers/preview/
and pass the url and attribution. For example:

```
folium.Map(tiles='https://{s}.tiles.example.com/{z}/{x}/{y}.png', attr='My Data Attribution')
```

Folium also accepts objects from the [xyzservices package](https://github.com/geopandas/xyzservices).


Adding markers
--------------

There are various marker types, here we start with a simple `Marker`. You can add a popup and
tooltip. You can also pick colors and icons.

```{code-cell} ipython3
m = folium.Map([45.35, -121.6972], zoom_start=12)

folium.Marker(
    location=[45.3288, -121.6625],
    tooltip="Click me!",
    popup="Mt. Hood Meadows",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.Marker(
    location=[45.3311, -121.7113],
    tooltip="Click me!",
    popup="Timberline Lodge",
    icon=folium.Icon(color="green"),
).add_to(m)

m
```


Vectors such as lines
---------------------

Folium has various vector elements. One example is `PolyLine`, which can show linear elements on a map.
This object can help put emphasis on a trail, a road, or a coastline.

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


Grouping and controlling
------------------------

You can group multiple elements such as markers together in a `FeatureGroup`. You can select
which you want to show by adding a `LayerControl` to the map.

```{code-cell} ipython3
m = folium.Map((0, 0), zoom_start=7)

group_1 = folium.FeatureGroup("first group").add_to(m)
folium.Marker((0, 0), icon=folium.Icon("red")).add_to(group_1)
folium.Marker((1, 0), icon=folium.Icon("red")).add_to(group_1)

group_2 = folium.FeatureGroup("second group").add_to(m)
folium.Marker((0, 1), icon=folium.Icon("green")).add_to(group_2)

folium.LayerControl().add_to(m)

m
```


GeoJSON/TopoJSON overlays
-------------------------

Folium supports both GeoJSON and TopoJSON data in various formats, such as urls,
file paths and dictionaries.

```{code-cell} ipython3
import requests

m = folium.Map(tiles="cartodbpositron")

geojson_data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
).json()

folium.GeoJson(geojson_data, name="hello world").add_to(m)

folium.LayerControl().add_to(m)

m
```


Choropleth maps
---------------

Choropleth can be created by binding the data between Pandas DataFrames/Series and Geo/TopoJSON geometries.

```{code-cell} ipython3
import pandas

state_geo = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()
state_data = pandas.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv"
)

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
