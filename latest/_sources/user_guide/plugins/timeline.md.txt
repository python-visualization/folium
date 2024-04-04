```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

##  Timeline and TimelineSlider
Show changing geospatial data over time.

### Comparison to TimestampedGeoJson
This is a plugin with a similar purpose to `TimestampedGeoJson`. They both
show geospatial information that changes over time.

The main difference between the two is the input format.

In the `Timeline` plugin each `Feature` has its own `start` and `end` time among its properties.
In the `TimestampedGeojson` each `Feature` has an array of start times. Each start time in
the array corresponds to a part of the `Geometry` of that `Feature`.

`TimestampedGeojson` also does not have `end` times for each `Feature`. Instead you can
specify a global `duration` property that is valid for all features.

Depending on your input geojson, one plugin may be more convenient than the other.

### Comparison to Realtime
The `Timeline` plugin can only show data from the past. If you want live updates,
you need the `Realtime` plugin.

```{code-cell} ipython3
import folium
from folium.utilities import JsCode
from folium.features import GeoJsonPopup
from folium.plugins.timeline import Timeline, TimelineSlider
import requests

m = folium.Map()

data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/historical_country_borders.json"
).json()

timeline = Timeline(
    data,
    style=JsCode("""
        function (data) {
            function getColorFor(str) {
                var hash = 0;
                for (var i = 0; i < str.length; i++) {
                    hash = str.charCodeAt(i) + ((hash << 5) - hash);
                }
                var red = (hash >> 24) & 0xff;
                var grn = (hash >> 16) & 0xff;
                var blu = (hash >> 8) & 0xff;
                return "rgb(" + red + "," + grn + "," + blu + ")";
            }
            return {
                stroke: false,
                color: getColorFor(data.properties.name),
                fillOpacity: 0.5,
            };
        }
    """)
).add_to(m)
GeoJsonPopup(fields=['name'], labels=True).add_to(timeline)
TimelineSlider(
    auto_play=False,
    show_ticks=True,
    enable_keyboard_controls=True,
    playback_duration=30000,
).add_timelines(timeline).add_to(m)
m
```
