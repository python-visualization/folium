# -*- coding: utf-8 -*-

"""
Features
--------

Extra features Elements.

"""

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import (CssLink, Element, Figure, JavascriptLink, MacroElement)  # noqa
from branca.utilities import (_locations_tolist, _parse_size, image_to_url, iter_points, none_max, none_min)  # noqa

from folium.map import Marker
from folium.utilities import _parse_path

from jinja2 import Template


class PolyLine(Marker):
    """
    Creates a PolyLine (array) or MultiPolyline (array of arrays) object to
    append into a map.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    color: string, default Leaflet's default ('#03f')
    weight: float, default Leaflet's default (5)
    opacity: float, default Leaflet's default (0.5)
    popup: string or folium.Popup, default None
        Input text or visualization for object.

    See http://leafletjs.com/reference-1.2.0.html#polyline for more options.

    """
    def __init__(self, locations, popup=None, tooltip=None, **kw):
        super(PolyLine, self).__init__(location=locations, popup=popup)
        self._name = 'PolyLine'
        self.tooltip = tooltip
        options = _parse_path(**kw)
        options.update(
            {
                'smoothFactor': kw.pop('smooth_factor', 1.0),
                'noClip': kw.pop('no_clip', False),
            }
        )

        self.options = json.dumps(options, sort_keys=True, indent=2)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.polyline(
                    {{this.location}},
                    {{ this.options }}
                    )
                    {% if this.tooltip %}.bindTooltip("{{this.tooltip.__str__()}}"){% endif %}
                    .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)  # noqa


class Polygon(Marker):
    """
    Creates a Polygon Marker object for plotting on a Map.

    Parameters
    ----------
    locations: tuple or list, default None
        Latitude and Longitude of Polygon
    color: string, default ('black')
        Edge color of a polygon.
    weight: float, default (1)
        Edge line width of a polygon.
    fill_color: string, default ('black')
        Fill color of a polygon.
    fill_opacity: float, default (0.6)
        Fill opacity of a polygon.
    popup: string or folium.Popup, default None
        Input text or visualization for object.

    See http://leafletjs.com/reference-1.2.0.html#path for more options.

    """
    def __init__(self, locations, popup=None, tooltip=None, **kwargs):
        super(Polygon, self).__init__(locations, popup=popup)
        self._name = 'Polygon'
        self.tooltip = tooltip

        options = _parse_path(**kwargs)
        self.options = json.dumps(options, sort_keys=True, indent=2)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.polygon(
                {{this.location}},
                {{ this.options }}
                )
                {% if this.tooltip %}.bindTooltip("{{this.tooltip.__str__()}}"){% endif %}
                .addTo({{this._parent.get_name()}});

            {% endmacro %}
            """)


class Rectangle(Marker):
    """
    Creates a Rectangle Marker object for plotting on a Map.

    Parameters
    ----------
    bounds: tuple or list, default None
        Latitude and Longitude of Marker (southWest and northEast)
    color: string, default ('black')
        Edge color of a rectangle.
    weight: float, default (1)
        Edge line width of a rectangle.
    fill_color: string, default ('black')
        Fill color of a rectangle.
    fill_opacity: float, default (0.6)
        Fill opacity of a rectangle.
    popup: string or folium.Popup, default None
        Input text or visualization for object.

    See http://leafletjs.com/reference-1.2.0.html#path for more options.

    """
    def __init__(self, bounds, popup=None, tooltip=None, **kwargs):
        super(Rectangle, self).__init__(location=bounds, popup=popup)
        self._name = 'rectangle'
        self.tooltip = tooltip

        options = _parse_path(**kwargs)
        self.options = json.dumps(options, sort_keys=True, indent=2)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.rectangle(
                {{this.location}},
                {{ this.options }}
                )
                {% if this.tooltip %}.bindTooltip("{{this.tooltip.__str__()}}"){% endif %}
                .addTo({{this._parent.get_name()}});

            {% endmacro %}
            """)


class Circle(Marker):
    """
    Creates a Circle object for plotting on a Map.

    Parameters
    ----------
    location: tuple or list
        Latitude and Longitude of Marker (Northing, Easting)
    radius: int
        The radius of the circle in meters.
        For setting the radius in pixel, use CircleMarker.
    color: str, default '#3388ff'
        The color of the marker's edge in a HTML-compatible format.
    fill: bool, default False
        If true the circle will be filled.
    fill_color: str, default to the same as color
        The fill color of the marker in a HTML-compatible format.
    fill_opacity: float, default 0.2
        The fill opacity of the marker, between 0. and 1.
    popup: string or folium.Popup, default None
        Input text or visualization for object.

    See http://leafletjs.com/reference-1.2.0.html#path for more options.

    """
    def __init__(self, location, radius=10, popup=None, tooltip=None, **kwargs):
        super(Circle, self).__init__(location=location, popup=popup)
        self._name = 'circle'
        self.tooltip = tooltip

        options = _parse_path(**kwargs)
        options.update({'radius': radius})
        self.options = json.dumps(options, sort_keys=True, indent=2)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.circle(
                [{{this.location[0]}}, {{this.location[1]}}],
                {{ this.options }}
                )
                {% if this.tooltip %}.bindTooltip("{{this.tooltip.__str__()}}"){% endif %}
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)


class CircleMarker(Marker):
    """
    Creates a CircleMarker object for plotting on a Map.

    Parameters
    ----------
    location: tuple or list
        Latitude and Longitude of Marker (Northing, Easting)
    radius: int
        The radius of the circle in pixels.
        For setting the radius in meter, use Circle.
    color: str, default '#3388ff'
        The color of the marker's edge in a HTML-compatible format.
    fill: bool, default False
        If true the circle will be filled.
    fill_color: str, default to the same as color
        The fill color of the marker in a HTML-compatible format.
    fill_opacity: float, default 0.2
        The fill opacity of the marker, between 0. and 1.
    popup: string or folium.Popup, default None
        Input text or visualization for object.

    See http://leafletjs.com/reference-1.2.0.html#path for more options.

    """
    def __init__(self, location, radius=10, popup=None, tooltip=None, **kw):
        super(CircleMarker, self).__init__(location=location, popup=popup)
        self._name = 'CircleMarker'
        self.tooltip = tooltip

        options = _parse_path(**kw)
        options.update({'radius': radius})
        self.options = json.dumps(options, sort_keys=True, indent=2)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.circleMarker(
                [{{this.location[0]}}, {{this.location[1]}}],
                {{ this.options }}
                )
                {% if this.tooltip %}.bindTooltip("{{this.tooltip.__str__()}}"){% endif %}
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)
