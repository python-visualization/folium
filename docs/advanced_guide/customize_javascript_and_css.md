# Customizing javascript or css resources

```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

## Adding javascript or css resources
Many leaflet resources require loading of custom css or javascript modules. This is handled in the `folium.elements.JSCSSMixin` class. Anything that inherits from this class can load custom resources.

You can use the methods `add_js_link` and `add_css_link` to ensure these resources are loaded into the map.

### Example 1: overriding the locations from where resources are loaded
One use case is to override the locations from where resources are loaded. This can be useful if you have to use a private CDN for your javascript and css resources, or if you want to use a different version.

```{code-cell}
m = folium.Map()
m.add_css_link(
    "bootstrap_css",
    "https://example.com/bootstrap/400.5.0/css/bootstrap.min.css"
)
```


### Example 2: loading additional javascript
A second use case is to load library modules that you can then use inside JsCode blocks. Continuing from the Realtime ISS example, see :doc:Realtime <user_guide/plugins/realtime>, we can modify this so that it uses the dayjs library to format the current date.

```{code-cell} ipython3
from folium.utilities import JsCode
from folium.plugins import Realtime

m = folium.Map()
on_each_feature = JsCode("""
function(f, l) {
    l.bindPopup(function() {
        return '<h5>' + dayjs.unix(f.properties.timestamp).format() + '</h5>';
    });
}
""")

source = JsCode("""
function(responseHandler, errorHandler) {
    var url = 'https://api.wheretheiss.at/v1/satellites/25544';

    fetch(url)
    .then((response) => {
        return response.json().then((data) => {
            var { id, timestamp, longitude, latitude } = data;

            return {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [longitude, latitude]
                    },
                    'properties': {
                        'id': id,
                        'timestamp': timestamp
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
              on_each_feature=on_each_feature,
              interval=1000)
rt.add_js_link("dayjs", "https://cdn.jsdelivr.net/npm/dayjs@1.11.10/dayjs.min.js")
rt.add_to(m)
m
```

## Referring to other map objects in JsCode
Inside a `JsCode` block you often need the Javascript variable of another folium object, such as a marker or a layer. You can write `%(name)s` placeholders in the code and pass the objects as keyword arguments. Folium objects are replaced by their Javascript variable name when the map is rendered, other `JsCode` objects by their code, and any other value is inserted as is.

When you pass parameters, write a literal `%` in the code as `%%`.

```{code-cell} ipython3
from folium.utilities import JsCode

m = folium.Map(location=[45, -30], zoom_start=4)
marker = folium.Marker([45, -30], popup="Hello!").add_to(m)

m.on(click=JsCode("""
function(e) {
    %(marker)s.setLatLng(e.latlng).openPopup();
}
""", marker=marker))
m
```
