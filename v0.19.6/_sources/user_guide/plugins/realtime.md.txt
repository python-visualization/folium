```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

# Realtime

Put realtime data on a Leaflet map: live tracking GPS units,
sensor data or just about anything.

Based on: https://github.com/perliedman/leaflet-realtime

This plugin functions much like an `L.GeoJson` layer, for
which the geojson data is periodically polled from a url.


## Simple example

In this example we use a static geojson, whereas normally you would have a
url that actually updates in real time.

```{code-cell} ipython3
from folium import JsCode
m = folium.Map(location=[40.73, -73.94], zoom_start=12)
rt = folium.plugins.Realtime(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/subway_stations.geojson",
    get_feature_id=JsCode("(f) => { return f.properties.objectid; }"),
    interval=10000,
)
rt.add_to(m)
m
```


## Javascript function as source

For more complicated scenarios, such as when the underlying data source does not return geojson, you can
write a javascript function for the `source` parameter. In this example we track the location of the
International Space Station using a public API.


```{code-cell} ipython3
import folium
from folium.plugins import Realtime

m = folium.Map()

source = folium.JsCode("""
    function(responseHandler, errorHandler) {
        var url = 'https://api.wheretheiss.at/v1/satellites/25544';

        fetch(url)
        .then((response) => {
            return response.json().then((data) => {
                var { id, longitude, latitude } = data;

                return {
                    'type': 'FeatureCollection',
                    'features': [{
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [longitude, latitude]
                        },
                        'properties': {
                            'id': id
                        }
                    }]
                };
            })
        })
        .then(responseHandler)
        .catch(errorHandler);
    }
""")

rt = Realtime(source, interval=10000)
rt.add_to(m)

m
```


## Customizing the layer

The leaflet-realtime plugin typically uses an `L.GeoJson` layer to show the data. This
means that you can also pass parameters which you would typically pass to an
`L.GeoJson` layer. With this knowledge we can change the first example to display
`L.CircleMarker` objects.

```{code-cell} ipython3
import folium
from folium import JsCode
from folium.plugins import Realtime

m = folium.Map(location=[40.73, -73.94], zoom_start=12)
source = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/subway_stations.geojson"

Realtime(
    source,
    get_feature_id=JsCode("(f) => { return f.properties.objectid }"),
    point_to_layer=JsCode("(f, latlng) => { return L.circleMarker(latlng, {radius: 8, fillOpacity: 0.2})}"),
    interval=10000,
).add_to(m)

m
```

## Using a MarkerCluster as a container

The subway stations in the previous example are not easy to distinguish at lower zoom levels.
It is possible to use a custom container for the GeoJson. In this example we use a MarkerCluster.
```{code-cell} ipython3
import folium
from folium import JsCode
from folium.plugins import Realtime, MarkerCluster

m = folium.Map(location=[40.73, -73.94], zoom_start=12)
source = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/subway_stations.geojson"

container = MarkerCluster().add_to(m)
Realtime(
    source,
    get_feature_id=JsCode("(f) => { return f.properties.objectid }"),
    point_to_layer=JsCode("(f, latlng) => { return L.circleMarker(latlng, {radius: 8, fillOpacity: 0.2})}"),
    container=container,
    interval=10000,
).add_to(m)

m
```
