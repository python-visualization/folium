# Geoman

The Geoman plugin provides an interactive drawing and editing interface for polygons, polylines, circles, and other geometric shapes on your Folium map. It's based on the [Leaflet-Geoman](https://github.com/geoman-io/leaflet-geoman/) library.

## Basic Usage

```{code-cell} ipython3
import folium
from folium.plugins import GeoMan

# Create a map
m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

# Add Geoman plugin
GeoMan().add_to(m)

m
```

## Customizing Controls

You can customize which drawing controls are available and their position:

```{code-cell} ipython3
import folium
from folium.plugins import GeoMan

m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

# Add Geoman with custom options
GeoMan(
    position='topright',
    drawMarker=True,
    drawCircleMarker=True,
    drawPolyline=True,
    drawRectangle=True,
    drawPolygon=True,
    drawCircle=True,
    drawText=False,
    editMode=True,
    dragMode=True,
    cutPolygon=True,
    removalMode=True,
    rotateMode=False
).add_to(m)

m
```

## Available Methods

The GeoMan plugin provides several methods for programmatic control:

### Drawing Controls
- `enable_draw(shape, **kwargs)`: Enable drawing mode for a specific shape
- `disable_draw()`: Disable drawing mode
- `set_path_options(**options)`: Set default styling options for drawn shapes

### Edit Controls
- `enable_global_edit_mode(**options)`: Enable edit mode for all shapes
- `disable_global_edit_mode()`: Disable edit mode
- `enable_global_drag_mode()`: Enable drag mode for all shapes
- `disable_global_drag_mode()`: Disable drag mode

### Other Controls
- `enable_global_removal_mode()`: Enable removal mode
- `disable_global_removal_mode()`: Disable removal mode
- `enable_global_cut_mode()`: Enable polygon cutting mode
- `disable_global_cut_mode()`: Disable polygon cutting mode
- `enable_global_rotation_mode()`: Enable rotation mode
- `disable_global_rotation_mode()`: Disable rotation mode

## Configuration Options

The GeoMan plugin accepts the following parameters:

- `position` (str): Position of the toolbar ('topleft', 'topright', 'bottomleft', 'bottomright')
- `feature_group` (FeatureGroup): Feature group to store drawn items
- `on` (dict): Event handlers for drawing events
- `drawMarker` (bool): Enable/disable marker drawing
- `drawCircleMarker` (bool): Enable/disable circle marker drawing
- `drawPolyline` (bool): Enable/disable polyline drawing
- `drawRectangle` (bool): Enable/disable rectangle drawing
- `drawPolygon` (bool): Enable/disable polygon drawing
- `drawCircle` (bool): Enable/disable circle drawing
- `drawText` (bool): Enable/disable text drawing
- `editMode` (bool): Enable/disable edit mode
- `dragMode` (bool): Enable/disable drag mode
- `cutPolygon` (bool): Enable/disable polygon cutting
- `removalMode` (bool): Enable/disable removal mode
- `rotateMode` (bool): Enable/disable rotation mode

For more advanced usage and configuration options, refer to the [Leaflet-Geoman documentation](https://geoman.io/docs/leaflet).
