# OverlappingMarkerSpiderfier

```{code-cell} ipython3
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
