# OverlappingMarkerSpiderfier

The `OverlappingMarkerSpiderfier` is a plugin for Folium that helps manage overlapping markers by "spiderfying" them when clicked, making it easier to select individual markers.

```{code-cell} ipython3
import folium
from folium.plugins import OverlappingMarkerSpiderfier

# Create a map
m = folium.Map(location=[45.05, 3.05], zoom_start=13)

# Add markers to the map
for i in range(20):
    folium.Marker(
        location=[45.05 + i * 0.0001, 3.05 + i * 0.0001],
        popup=f"Marker {i}"
    ).add_to(m)

# Add the OverlappingMarkerSpiderfier plugin
oms = OverlappingMarkerSpiderfier(options={
    "keepSpiderfied": True,  # Markers remain spiderfied after clicking
    "nearbyDistance": 20,    # Distance for clustering markers in pixel
    "circleSpiralSwitchover": 10,  # Threshold for switching between circle and spiral
    "legWeight": 2.0         # Line thickness for spider legs
})
oms.add_to(m)

m
```
