```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# Using GeoPandas.GeoDataFrame in folium

GeoPandas is a project to add support for geographic data to [pandas](https://pandas.pydata.org) objects.
(See https://github.com/geopandas/geopandas)

It provides (among other cool things) a `GeoDataFrame` object that represents a Feature collection.
When you have one, you may be willing to use it on a folium map. Here's the simplest way to do so.

In this example, we'll use the same file as GeoPandas demo ; it's containing the boroughs of New York City.

```{code-cell} ipython3
import geopandas

boros = geopandas.read_file(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/new_york_boroughs.zip"
)

boros
```

To create a map with these features, simply put them in a `GeoJson`:

```{code-cell} ipython3
m = folium.Map([40.7, -74], zoom_start=10, tiles="cartodbpositron")

folium.GeoJson(boros).add_to(m)

m
```

Quite easy.

## Adding style

Well, you can also take advantage of your `GeoDataFrame` structure to set the style of the data. For this, just create a column `style` containing each feature's style in a dictionary.

```{code-cell} ipython3
boros["style"] = [
    {"fillColor": "#ff0000", "weight": 2, "color": "black"},
    {"fillColor": "#00ff00", "weight": 2, "color": "black"},
    {"fillColor": "#0000ff", "weight": 2, "color": "black"},
    {"fillColor": "#ffff00", "weight": 2, "color": "black"},
    {"fillColor": "#00ffff", "weight": 2, "color": "black"},
]

boros
```

```{code-cell} ipython3
m = folium.Map([40.7, -74], zoom_start=10, tiles="cartodbpositron")

folium.GeoJson(boros).add_to(m)

m
```

## Use any object with `__geo_interface__`

Folium should work with any object that implements the `__geo_interface__` but be aware that sometimes you may need to convert your data to `epsg='4326'` before sending it to `folium`.

```{code-cell} ipython3
import fiona
import shapely

url = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/route_farol.gpx"
with fiona.open(url, "r", layer="tracks") as records:
    tracks = [shapely.geometry.shape(record["geometry"]) for record in records]

track = tracks[0]

m = folium.Map(tiles="cartodbpositron")
folium.GeoJson(track).add_to(m)

m.fit_bounds(m.get_bounds())

m
```
