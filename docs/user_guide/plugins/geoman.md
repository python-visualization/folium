# Geoman

The Geoman plugin provides an interactive drawing and editing interface for polygons, polylines, circles, and other geometric shapes on your Folium map. It's based on the [Leaflet-Geoman](https://github.com/geoman-io/leaflet-geoman/) library.

## Advantages over Draw Plugin

Geoman is a more recent and actively maintained alternative to the Draw plugin, offering several key advantages:

- **Advanced Shape Features**: Supports drawing shapes with holes inside them, which is not available in the Draw plugin
- **Enhanced Editing Capabilities**: Includes cutting, rotating, scaling, and snapping functionality for precise geometry editing
- **Professional Add-ons**: Offers [paid extensions](https://geoman.io/docs/leaflet/getting-started/pro-version) with advanced functionality for complex GIS applications

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

For more advanced usage and configuration options, refer to the [Leaflet-Geoman documentation](https://geoman.io/docs/leaflet).
