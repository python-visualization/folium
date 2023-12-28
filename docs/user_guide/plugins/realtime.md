```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

# Realtime plugin

Put realtime data on a Leaflet map: live tracking GPS units,
sensor data or just about anything.

Based on: https://github.com/perliedman/leaflet-realtime

This plugin functions much like an `L.GeoJson` layer, for
which the geojson data is periodically polled from a url.

Parameters
----------
source :
  The source can be one of:
  * a string with the URL to get data from
  * a dict that is passed to javascript's `fetch` function
    for fetching the data
  * a folium.utilities.JsCode object in case you need more freedom.

start : bool, default True
  Should automatic updates be enabled when layer is added
  on the map and stopped when layer is removed from the map

interval : int, default 60000
  Automatic update interval, in milliseconds

get_feature_id : folium.utilities.JsCode
  A function with a geojson `feature` as parameter
  default returns `feature.properties.id`
  Function to get an identifier uniquely identify a feature over time

update_feature : folium.utilities.JsCode
  A function with a geojson `feature` as parameter
  Used to update an existing feature's layer;
  by default, points (markers) are updated, other layers are discarded
  and replaced with a new, updated layer.
  Allows to create more complex transitions,
  for example, when a feature is updated

remove_missing : bool, default False
  Should missing features between updates been automatically
          removed from the layer

Other parameters are passed to the `L.GeoJson` object, so you can pass
      `style`, `point_to_layer` and/or `on_each_feature`.


```{code-cell} ipython3
from folium.utilities import JsCode
m = folium.Map(location=[40.73, -73.94], zoom_start=12)
rt = folium.plugins.Realtime(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/subway_stations.geojson",
    get_feature_id=JsCode("(f) => { return f.properties.objectid; }"),
    interval=10000,
)
rt.add_to(m)
m
```

For more complicated scenarios, such as when the underlying data source does not return geojson, you can
write a javascript function for the `source` parameter. In this example we track the location of the
International Space Station.


```{code-cell} ipython3
import folium
from folium.utilities import JsCode
from folium.plugins import Realtime

m = folium.Map()

source = JsCode("""
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

rt = Realtime(source,
              interval=10000)
rt.add_to(m)
m
```

The leaflet-realtime plugin typically uses an `L.GeoJson` layer to show the data. This
means that you can also pass parameters which you would typically pass to an
`L.GeoJson` layer. With this knowledge we can change the first example to display
`L.CircleMarker` objects.

```{code-cell} ipython3
import folium
from folium.utilities import JsCode
from folium.plugins import Realtime

m = folium.Map(location=[40.73, -73.94], zoom_start=12)
source = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/subway_stations.geojson"

rt = Realtime(source,
              get_feature_id=JsCode("(f) => { return f.properties.objectid }"),
              point_to_layer=JsCode("(f, latlng) => { return L.circleMarker(latlng, {radius: 8, fillOpacity: 0.2})}"),
              interval=10000)
rt.add_to(m)
m
```
