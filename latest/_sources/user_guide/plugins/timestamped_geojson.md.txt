```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

##  TimestampedGeoJson

### Example 1

```{code-cell} ipython3
m = folium.Map(location=[35.68159659061569, 139.76451516151428], zoom_start=16)

# Lon, Lat order.
lines = [
    {
        "coordinates": [
            [139.76451516151428, 35.68159659061569],
            [139.75964426994324, 35.682590062684206],
        ],
        "dates": ["2017-06-02T00:00:00", "2017-06-02T00:10:00"],
        "color": "red",
    },
    {
        "coordinates": [
            [139.75964426994324, 35.682590062684206],
            [139.7575843334198, 35.679505030038506],
        ],
        "dates": ["2017-06-02T00:10:00", "2017-06-02T00:20:00"],
        "color": "blue",
    },
    {
        "coordinates": [
            [139.7575843334198, 35.679505030038506],
            [139.76337790489197, 35.678040905014065],
        ],
        "dates": ["2017-06-02T00:20:00", "2017-06-02T00:30:00"],
        "color": "green",
        "weight": 15,
    },
    {
        "coordinates": [
            [139.76337790489197, 35.678040905014065],
            [139.76451516151428, 35.68159659061569],
        ],
        "dates": ["2017-06-02T00:30:00", "2017-06-02T00:40:00"],
        "color": "#FFFFFF",
    },
]

features = [
    {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": line["coordinates"],
        },
        "properties": {
            "times": line["dates"],
            "style": {
                "color": line["color"],
                "weight": line["weight"] if "weight" in line else 5,
            },
        },
    }
    for line in lines
]

folium.plugins.TimestampedGeoJson(
    {
        "type": "FeatureCollection",
        "features": features,
    },
    period="PT1M",
    add_last_point=True,
).add_to(m)

m
```

### Example 2

```{code-cell} ipython3
table = """\
<table style=\'width:100%\'>
  <tr>
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
</table>
"""

points = [
    {
        "time": "2017-06-02",
        "popup": "<h1>address1</h1>",
        "coordinates": [-2.548828, 51.467697],
    },
    {
        "time": "2017-07-02",
        "popup": "<h2 style='color:blue;'>address2<h2>",
        "coordinates": [-0.087891, 51.536086],
    },
    {
        "time": "2017-08-02",
        "popup": "<h2 style='color:orange;'>address3<h2>",
        "coordinates": [-6.240234, 53.383328],
    },
    {
        "time": "2017-09-02",
        "popup": "<h2 style='color:green;'>address4<h2>",
        "coordinates": [-1.40625, 60.261617],
    },
    {"time": "2017-10-02", "popup": table, "coordinates": [-1.516113, 53.800651]},
]

features = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": point["coordinates"],
        },
        "properties": {
            "time": point["time"],
            "popup": point["popup"],
            "id": "house",
            "icon": "marker",
            "iconstyle": {
                "iconUrl": "https://leafletjs.com/examples/geojson/baseball-marker.png",
                "iconSize": [20, 20],
            },
        },
    }
    for point in points
]

features.append(
    {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [-2.548828, 51.467697],
                [-0.087891, 51.536086],
                [-6.240234, 53.383328],
                [-1.40625, 60.261617],
                [-1.516113, 53.800651],
            ],
        },
        "properties": {
            "popup": "Current address",
            "times": [
                "2017-06-02",
                "2017-07-02",
                "2017-08-02",
                "2017-09-02",
                "2017-10-02",
            ],
            "icon": "circle",
            "iconstyle": {
                "fillColor": "green",
                "fillOpacity": 0.6,
                "stroke": "false",
                "radius": 13,
            },
            "style": {"weight": 0},
            "id": "man",
        },
    }
)

m = folium.Map(
    location=[56.096555, -3.64746],
    tiles="cartodbpositron",
    zoom_start=5,
)

folium.plugins.TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="P1M",
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options="YYYY/MM/DD",
    time_slider_drag_update=True,
    duration="P2M",
).add_to(m)

m
```
