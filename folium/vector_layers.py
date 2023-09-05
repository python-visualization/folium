"""
Wraps leaflet Polyline, Polygon, Rectangle, Circle, and CircleMarker

"""
from typing import List, Optional, Sequence, Union

from branca.element import MacroElement
from jinja2 import Template

from folium.map import Marker, Popup, Tooltip
from folium.utilities import (
    TypeLine,
    TypeMultiLine,
    TypePathOptions,
    camelize,
    get_bounds,
    validate_locations,
    validate_multi_locations,
)


def path_options(
    line: bool = False, radius: Optional[float] = None, **kwargs: TypePathOptions
):
    """
    Contains options and constants shared between vector overlays
    (Polygon, Polyline, Circle, CircleMarker, and Rectangle).

    Parameters
    ----------
    stroke: Bool, True
        Whether to draw stroke along the path.
        Set it to false to disable borders on polygons or circles.
    color: str, '#3388ff'
        Stroke color.
    weight: int, 3
        Stroke width in pixels.
    opacity: float, 1.0
        Stroke opacity.
    line_cap: str, 'round' (lineCap)
        A string that defines shape to be used at the end of the stroke.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linecap
    line_join: str, 'round' (lineJoin)
        A string that defines shape to be used at the corners of the stroke.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linejoin
    dash_array: str, None (dashArray)
        A string that defines the stroke dash pattern.
        Doesn't work on Canvas-powered layers in some old browsers.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dasharray
    dash_offset:, str, None (dashOffset)
        A string that defines the distance into the dash pattern to start the dash.
        Doesn't work on Canvas-powered layers in some old browsers.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dashoffset
    fill: Bool, False
        Whether to fill the path with color.
        Set it to false to disable filling on polygons or circles.
    fill_color: str, default to `color` (fillColor)
        Fill color. Defaults to the value of the color option.
    fill_opacity: float, 0.2 (fillOpacity)
        Fill opacity.
    fill_rule: str, 'evenodd' (fillRule)
        A string that defines how the inside of a shape is determined.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule
    bubbling_mouse_events: Bool, True (bubblingMouseEvents)
        When true a mouse event on this path will trigger the same event on the
        map (unless L.DomEvent.stopPropagation is used).
    gradient: bool, default None
        When a gradient on the stroke and fill is available,
        allows turning it on or off.

    Note that the presence of `fill_color` will override `fill=False`.

    This function accepts both snake_case and lowerCamelCase equivalents.

    See https://leafletjs.com/reference.html#path

    """

    kwargs = {camelize(key): value for key, value in kwargs.items()}

    extra_options = {}
    if line:
        extra_options = {
            "smoothFactor": kwargs.pop("smoothFactor", 1.0),
            "noClip": kwargs.pop("noClip", False),
        }
    if radius:
        extra_options.update({"radius": radius})

    color = kwargs.pop("color", "#3388ff")
    fill_color = kwargs.pop("fillColor", False)
    if fill_color:
        fill = True
    elif not fill_color:
        fill_color = color
        fill = kwargs.pop("fill", False)  # type: ignore

    gradient = kwargs.pop("gradient", None)
    if gradient is not None:
        extra_options.update({"gradient": gradient})

    if kwargs.get("tags"):
        extra_options["tags"] = kwargs.pop("tags")

    default = {
        "stroke": kwargs.pop("stroke", True),
        "color": color,
        "weight": kwargs.pop("weight", 3),
        "opacity": kwargs.pop("opacity", 1.0),
        "lineCap": kwargs.pop("lineCap", "round"),
        "lineJoin": kwargs.pop("lineJoin", "round"),
        "dashArray": kwargs.pop("dashArray", None),
        "dashOffset": kwargs.pop("dashOffset", None),
        "fill": fill,
        "fillColor": fill_color,
        "fillOpacity": kwargs.pop("fillOpacity", 0.2),
        "fillRule": kwargs.pop("fillRule", "evenodd"),
        "bubblingMouseEvents": kwargs.pop("bubblingMouseEvents", True),
    }
    default.update(extra_options)
    return default


class BaseMultiLocation(MacroElement):
    """Base class for vector classes with multiple coordinates.

    :meta private:

    """

    def __init__(
        self,
        locations: TypeMultiLine,
        popup: Union[Popup, str, None] = None,
        tooltip: Union[Tooltip, str, None] = None,
    ):
        super().__init__()
        self.locations = validate_multi_locations(locations)
        if popup is not None:
            self.add_child(popup if isinstance(popup, Popup) else Popup(str(popup)))
        if tooltip is not None:
            self.add_child(
                tooltip if isinstance(tooltip, Tooltip) else Tooltip(str(tooltip))
            )

    def _get_self_bounds(self) -> List[List[Optional[float]]]:
        """Compute the bounds of the object itself."""
        return get_bounds(self.locations)


class PolyLine(BaseMultiLocation):
    """Draw polyline overlays on a map.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
        Pass multiple sequences of coordinates for a multi-polyline.
    popup: str or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    smooth_factor: float, default 1.0
        How much to simplify the polyline on each zoom level.
        More means better performance and smoother look,
        and less means more accurate representation.
    no_clip: Bool, default False
        Disable polyline clipping.
    **kwargs
        Other valid (possibly inherited) options. See:
        https://leafletjs.com/reference.html#polyline

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.polyline(
                {{ this.locations|tojson }},
                {{ this.options|tojson }}
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """
    )

    def __init__(self, locations, popup=None, tooltip=None, **kwargs):
        super().__init__(locations, popup=popup, tooltip=tooltip)
        self._name = "PolyLine"
        self.options = path_options(line=True, **kwargs)


class Polygon(BaseMultiLocation):
    """Draw polygon overlays on a map.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        - One list of coordinate pairs to define a polygon. You don't have to
          add a last point equal to the first point.
        - If you pass a list with multiple of those it will make a multi-
          polygon.
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    **kwargs
        Other valid (possibly inherited) options. See:
        https://leafletjs.com/reference.html#polygon

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.polygon(
                {{ this.locations|tojson }},
                {{ this.options|tojson }}
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """
    )

    def __init__(
        self,
        locations: TypeMultiLine,
        popup: Union[Popup, str, None] = None,
        tooltip: Union[Tooltip, str, None] = None,
        **kwargs: TypePathOptions
    ):
        super().__init__(locations, popup=popup, tooltip=tooltip)
        self._name = "Polygon"
        self.options = path_options(line=True, radius=None, **kwargs)


class Rectangle(MacroElement):
    """Draw rectangle overlays on a map.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    bounds: [(lat1, lon1), (lat2, lon2)]
        Two lat lon pairs marking the two corners of the rectangle.
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    **kwargs
        Other valid (possibly inherited) options. See:
        https://leafletjs.com/reference.html#rectangle

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.rectangle(
                {{ this.locations|tojson }},
                {{ this.options|tojson }}
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """
    )

    def __init__(
        self,
        bounds: TypeLine,
        popup: Union[Popup, str, None] = None,
        tooltip: Union[Tooltip, str, None] = None,
        **kwargs: TypePathOptions
    ):
        super().__init__()
        self._name = "rectangle"
        self.options = path_options(line=True, radius=None, **kwargs)
        self.locations = validate_locations(bounds)
        assert len(self.locations) == 2, "Need two lat/lon pairs"
        if popup is not None:
            self.add_child(popup if isinstance(popup, Popup) else Popup(str(popup)))
        if tooltip is not None:
            self.add_child(
                tooltip if isinstance(tooltip, Tooltip) else Tooltip(str(tooltip))
            )

    def _get_self_bounds(self) -> List[List[Optional[float]]]:
        """Compute the bounds of the object itself."""
        return get_bounds(self.locations)


class Circle(Marker):
    """
    Class for drawing circle overlays on a map.

    It's an approximation and starts to diverge from a real circle closer to
    the poles (due to projection distortion).

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    location: tuple[float, float]
        Latitude and Longitude pair (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    radius: float
        Radius of the circle, in meters.
    **kwargs
        Other valid (possibly inherited) options. See:
        https://leafletjs.com/reference.html#circle

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.circle(
                {{ this.location|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """
    )

    def __init__(
        self,
        location: Optional[Sequence[float]] = None,
        radius: float = 50,
        popup: Union[Popup, str, None] = None,
        tooltip: Union[Tooltip, str, None] = None,
        **kwargs: TypePathOptions
    ):
        super().__init__(location, popup=popup, tooltip=tooltip)
        self._name = "circle"
        self.options = path_options(line=False, radius=radius, **kwargs)


class CircleMarker(Marker):
    """
    A circle of a fixed size with radius specified in pixels.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    location: tuple[float, float]
        Latitude and Longitude pair (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    radius: float, default 10
        Radius of the circle marker, in pixels.
    **kwargs
        Other valid (possibly inherited) options. See:
        https://leafletjs.com/reference.html#circlemarker

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.circleMarker(
                {{ this.location|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """
    )

    def __init__(
        self,
        location: Optional[Sequence[float]] = None,
        radius: float = 10,
        popup: Union[Popup, str, None] = None,
        tooltip: Union[Tooltip, str, None] = None,
        **kwargs: TypePathOptions
    ):
        super().__init__(location, popup=popup, tooltip=tooltip)
        self._name = "CircleMarker"
        self.options = path_options(line=False, radius=radius, **kwargs)
