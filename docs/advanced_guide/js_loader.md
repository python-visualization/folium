# Loading event handlers from a CommonJS module

```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

## Loading Event handlers from javascript
Folium supports event handlers via the `JsCode` class. However, for more than a few lines of code, it becomes unwieldy to write javascript inside python using
only strings. For more complex code, it is much nicer to write javascript inside js files. This allows editor support, such as syntax highlighting, code completion
and linting.

Suppose we have the following javascript file:

```
/* located in js/handlers.js */
on_each_feature = function(f, l) {
    l.bindPopup(function() {
        return '<h5>' + dayjs.unix(f.properties.timestamp).format() + '</h5>';
    });
}

source = function(responseHandler, errorHandler) {
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

module.exports = {
    source,
    on_each_feature
}
```

Now we can load it as follows inside our python code:

```{code-cell} ipython3
from js_loader import install_js_loader
from folium.plugins import Realtime
install_js_loader()

from js import handlers

m = folium.Map()

rt = Realtime(handlers.source,
              on_each_feature=handlers.on_each_feature,
              interval=1000)
rt.add_js_link("dayjs", "https://cdn.jsdelivr.net/npm/dayjs@1.11.10/dayjs.min.js")
rt.add_to(m)
m
```
