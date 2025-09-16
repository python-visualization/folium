```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# Advanced GeoJSON Customization with on_each_feature

The `on_each_feature` parameter in `folium.GeoJson` provides powerful customization capabilities by allowing you to execute JavaScript code for each feature in your GeoJSON data. This is particularly useful for:

- Custom tooltip and popup handling for complex geometries like MultiPoint
- Adding custom event listeners
- Implementing advanced styling logic
- Working with geometry types that need special handling

## Understanding on_each_feature

The `on_each_feature` parameter accepts a `folium.utilities.JsCode` object containing JavaScript code that will be executed for each feature. The JavaScript function receives two parameters:
- `feature`: The GeoJSON feature object
- `layer`: The Leaflet layer object representing the feature

## Basic Example

```{code-cell} ipython3
import folium
from folium.utilities import JsCode
import json

# Simple point data
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Location 1", "value": 100},
            "geometry": {"type": "Point", "coordinates": [77.5946, 12.9716]}  # Central Bangalore
        },
        {
            "type": "Feature",
            "properties": {"name": "Location 2", "value": 200},
            "geometry": {"type": "Point", "coordinates": [77.6200, 12.9800]}  # Northeast Bangalore
        }
    ]
}

# Custom JavaScript to add popups
on_each_feature = JsCode("""
function(feature, layer) {
    layer.bindTooltip(
        '<b>' + feature.properties.name + '</b><br>' +
        'Value: ' + feature.properties.value
    );

    layer.bindPopup(
        '<b>' + ' This is popup ' + '</b><br>' +
        '<b>' + feature.properties.name + '</b><br>' +
        'Value: ' + feature.properties.value
    );
}
""")

m = folium.Map(location=[12.9716, 77.5946], zoom_start=10)

folium.GeoJson(
    geojson_data,
    on_each_feature=on_each_feature
).add_to(m)

m
```

The `on_each_feature` parameter provides the flexibility needed to handle complex GeoJSON scenarios that the standard tooltip and popup classes cannot address, particularly for MultiPoint geometries and advanced interactive features.

## References

- [Leaflet GeoJSON Tutorial](https://leafletjs.com/examples/geojson/) - Comprehensive guide to using GeoJSON with Leaflet, including the `onEachFeature` option that inspired folium's `on_each_feature` parameter.
