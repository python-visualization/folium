# OverlappingMarkerSpiderfier

The `OverlappingMarkerSpiderfier` is a plugin for Folium that helps manage overlapping markers by "spiderfying" them when clicked, making it easier to select individual markers.

## Using with Markers

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
oms = OverlappingMarkerSpiderfier(
    keep_spiderfied=True,  # Markers remain spiderfied after clicking
    nearby_distance=20,  # Distance for clustering markers in pixel
    circle_spiral_switchover=10,  # Threshold for switching between circle and spiral
    leg_weight=2.0  # Line thickness for spider legs
    )
oms.add_to(m)

m
```

## Using with FeatureGroups

```{code-cell} ipython3
import folium
from folium.plugins import OverlappingMarkerSpiderfier

# Create a map
m = folium.Map(location=[45.05, 3.05], zoom_start=13)

# Create a FeatureGroup
feature_group = folium.FeatureGroup(name='Feature Group')

# Add markers to the FeatureGroup
for i in range(10):
    folium.Marker(
        location=[45.05 + i * 0.0001, 3.05 + i * 0.0001],
        popup=f"Feature Group Marker {i}"
    ).add_to(feature_group)

# Add the FeatureGroup to the map
feature_group.add_to(m)

# Initialize OverlappingMarkerSpiderfier
oms = OverlappingMarkerSpiderfier()
oms.add_to(m)

m
```

## Using with FeatureGroupSubGroups

```{code-cell} ipython3
import folium
from folium.plugins import OverlappingMarkerSpiderfier, FeatureGroupSubGroup

# Create a map
m = folium.Map(location=[45.05, 3.05], zoom_start=13)

# Create a main FeatureGroup
main_group = folium.FeatureGroup(name='Main Group')

# Create sub-groups
sub_group1 = FeatureGroupSubGroup(main_group, name='Sub Group 1')
sub_group2 = FeatureGroupSubGroup(main_group, name='Sub Group 2')

# Add markers to the first sub-group
for i in range(10):
    folium.Marker(
        location=[45.05 + i * 0.0001, 3.05 + i * 0.0001],
        popup=f"Sub Group 1 Marker {i}"
    ).add_to(sub_group1)

# Add markers to the second sub-group
for i in range(10, 20):
    folium.Marker(
        location=[45.06 + (i - 10) * 0.0001, 3.06 + (i - 10) * 0.0001],
        popup=f"Sub Group 2 Marker {i}"
    ).add_to(sub_group2)

# Add the main group to the map
main_group.add_to(m)

# Add sub-groups to the map
sub_group1.add_to(m)
sub_group2.add_to(m)

# Initialize OverlappingMarkerSpiderfier
oms = OverlappingMarkerSpiderfier()
oms.add_to(m)

# Add the LayerControl plugin
folium.LayerControl().add_to(m)

m
```
