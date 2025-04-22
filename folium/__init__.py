import branca
from branca.colormap import ColorMap, LinearColormap, StepColormap
from branca.element import (
    CssLink,
    Div,
    Element,
    Figure,
    Html,
    IFrame,
    JavascriptLink,
    Link,
    MacroElement,
)

from folium.features import (
    Choropleth,
    ClickForLatLng,
    ClickForMarker,
    ColorLine,
    Control,
    CustomIcon,
    DivIcon,
    GeoJson,
    GeoJsonPopup,
    GeoJsonTooltip,
    LatLngPopup,
    RegularPolygonMarker,
    TopoJson,
    Vega,
    VegaLite,
)
from folium.folium import Map
from folium.map import (
    FeatureGroup,
    FitBounds,
    FitOverlays,
    Icon,
    LayerControl,
    Marker,
    Popup,
    Tooltip,
)
from folium.raster_layers import TileLayer, WmsTileLayer
from folium.utilities import JsCode
from folium.vector_layers import Circle, CircleMarker, Polygon, PolyLine, Rectangle

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"


if branca.__version__ != "unknown" and tuple(
    int(x) for x in branca.__version__.split(".")[:2]
) < (0, 3):
    raise ImportError(
        "branca version 0.3.0 or higher is required. "
        "Update branca with e.g. `pip install branca --upgrade`."
    )


__all__ = [
    "Choropleth",
    "ClickForMarker",
    "ClickForLatLng",
    "ColorLine",
    "ColorMap",
    "Control",
    "CssLink",
    "CustomIcon",
    "Div",
    "DivIcon",
    "Element",
    "FeatureGroup",
    "Figure",
    "FitBounds",
    "FitOverlays",
    "GeoJson",
    "GeoJsonPopup",
    "GeoJsonTooltip",
    "Html",
    "IFrame",
    "Icon",
    "JavascriptLink",
    "JsCode",
    "LatLngPopup",
    "LayerControl",
    "LinearColormap",
    "Link",
    "MacroElement",
    "Map",
    "Marker",
    "Popup",
    "RegularPolygonMarker",
    "StepColormap",
    "TileLayer",
    "Tooltip",
    "TopoJson",
    "Vega",
    "VegaLite",
    "WmsTileLayer",
    # vector_layers
    "Circle",
    "CircleMarker",
    "PolyLine",
    "Polygon",
    "Rectangle",
]
