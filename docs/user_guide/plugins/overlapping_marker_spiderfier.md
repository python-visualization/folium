# OverlappingMarkerSpiderfier

The `OverlappingMarkerSpiderfier` plugin for Folium is designed to handle overlapping markers on a map. When multiple markers are located at the same or nearby coordinates, they can overlap, making it difficult to interact with individual markers. This plugin "spiderfies" the markers, spreading them out in a spider-like pattern, allowing users to easily click and view each marker.

## Features

- **Spiderfying**: Automatically spreads out overlapping markers into a spider-like pattern when clicked, making them individually accessible.
- **Customizable Options**: Offers options to customize the behavior and appearance of the spiderfied markers, such as `keepSpiderfied`, `nearbyDistance`, and `legWeight`.
- **Popup Integration**: Supports popups for each marker, which can be customized to display additional information.
- **Layer Control**: Can be added as a layer to the map, allowing users to toggle its visibility.

## Usage

To use the `OverlappingMarkerSpiderfier`, you need to create a list of `folium.Marker` objects and pass them to the plugin. You can also customize the options to suit your needs.

### Example

```python
import folium
from folium import plugins

# Create a map
m = folium.Map(location=[45.05, 3.05], zoom_start=14)

# Generate some markers
markers = [folium.Marker(location=[45.05 + i * 0.0001, 3.05 + i * 0.0001], options={'desc': f'Marker {i}'}) for i in range(10)]


# Add markers to the map
for marker in markers:
    marker.add_to(m)

# Add OverlappingMarkerSpiderfier
oms = plugins.OverlappingMarkerSpiderfier(
    markers=markers,
    options={'keepSpiderfied': True, 'nearbyDistance': 20}
).add_to(m)

# Display the map
m
```

## Options

- **keepSpiderfied**: (bool) Whether to keep the markers spiderfied after clicking.
- **nearbyDistance**: (int) The distance in pixels within which markers are considered overlapping.
- **legWeight**: (float) The weight of the spider legs connecting the markers.

## Installation

Ensure you have Folium installed in your Python environment. You can install it using pip:

```bash
pip install folium
```

## Conclusion

The `OverlappingMarkerSpiderfier` plugin is a powerful tool for managing overlapping markers on a map, enhancing the user experience by making it easier to interact with individual markers. Customize it to fit your application's needs and improve the clarity of your map visualizations.
