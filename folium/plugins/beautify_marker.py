# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import Figure, JavascriptLink, CssLink, MacroElement

from folium.utilities import _validate_location, get_bounds
from folium.map import Popup

from jinja2 import Template

from six import binary_type, text_type


class BeautifyMarker(MacroElement):
    """
    Create a BeautifyMarker marker on the map, with optional
    popup text.
    Parameters
    ----------
    location: tuple or list, default None
        Latitude and Longitude of Marker (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object.
    icon: string
        the Font-Awesome icon name to use to render the marker.
    icon_shape: string
        the icon shape of the marker.
    border_width: integer
        the border width of the marker.
    border_color: string with hexadecimal RGB
        the border color of the marker.
    text_color: string with hexadecimal RGB
        the text color of the marker.
    background_color: string with hexadecimal RGB
        the background color of the marker.
    inner_icon_style: string with css styles for the icon.
        the css styles for the icon of the marker.
    spin: boolean
        allow the icon of the marker to be spinning.
    number: integer
        the number of the marker.
    is_draggable: boolean
        allow the marker to be dragged.
    Returns
    -------
    Marker names and HTML in obj.template_vars
    Examples
    --------
    >>> BeautifyMarker(location=[45.5, -122.3], popup='Portland, OR')
    >>> BeautifyMarker(location=[45.5, -122.3], popup=folium.Popup('Portland, OR'))
    >>> BeautifyMarker(location=[45.5, -122.3], popup=folium.Popup('Portland, OR'),
                       text_color='#000', border_color='transparent',
                       background_color='#FFF').add_to(map)
    >>> BeautifyMarker(location=[45.5, -122.3], popup=folium.Popup('Portland, OR'),
                       text_color='#000', border_color='transparent',
                       background_color='#FFF', number=10,
                       inner_icon_style='font-size:12px;padding-top:-5px;').add_to(map)
    >>> BeautifyMarker(location=[45.5, -122.3], popup=folium.Popup('Portland, OR'),
                       icon='arrow-down', icon_shape='marker').add_to(map)
    """
    ICON_SHAPE_TYPES = ['circle', 'circle-dot', 'doughnut', 'rectangle-dot',
                        'marker', None]

    def __init__(self, location, icon=None, icon_shape=None,
                 border_width=3, border_color='#000', text_color='#000',
                 background_color='#FFF', inner_icon_style='', spin=False,
                 number=None, is_draggable=False, popup=None, tooltip=None):
        super(BeautifyMarker, self).__init__()
        self._name = 'BeautifyMarker'
        self.location = _validate_location(location)
        self.tooltip = tooltip
        self.icon = icon
        self.icon_shape = icon_shape
        self.number = number
        self.is_draggable = str(is_draggable).lower()

        self.border_width = border_width
        self.border_color = border_color
        self.text_color = text_color
        self.background_color = background_color
        self.inner_icon_style = inner_icon_style
        self.spin = str(spin).lower()

        if isinstance(popup, text_type) or isinstance(popup, binary_type):
            self.add_child(Popup(popup))
        elif popup is not None:
            self.add_child(popup)

        if self.icon_shape not in self.ICON_SHAPE_TYPES:
            raise ValueError('Icon Shape is not one of these: circle-dot, '
                             'doughnut, marker, rectangle-dot.')

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
            var options = {
                {% if this.icon %}
                icon: '{{ this.icon }}',
                {% endif %}
                {% if this.icon_shape %}
                iconShape: '{{ this.icon_shape }}',
                {% endif %}
                borderWidth: {{ this.border_width }},
                borderColor: '{{ this.border_color }}',
                textColor: '{{ this.text_color }}',
                backgroundColor: '{{ this.background_color }}',
                innerIconStyle: '{{ this.inner_icon_style }}',
                spin: {{ this.spin }},
                {% if this.has_number %}
                isAlphaNumericIcon: {{ this.is_alpha_numeric_icon }},
                text: {{ this.number }},
                {% endif %}
            };
            var {{this.get_name()}} = L.marker(
                [{{this.location[0]}}, {{this.location[1]}}],
                {
                    icon: new L.BeautifyIcon.icon(options),
                    draggable: {{ this.is_draggable }},
                    }
                )
                {% if this.tooltip %}.bindTooltip("{{this.tooltip.__str__()}}"){% endif %}
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    @property
    def has_number(self):
        return self.number is not None

    @property
    def is_alpha_numeric_icon(self):
        return 'true' if self.has_number else 'false'

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].
        """
        return get_bounds(self.location)

    def render(self, **kwargs):
        super(BeautifyMarker, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')
        figure.header.add_child(
            CssLink('https://cdn.rawgit.com/marslan390/BeautifyMarker/master/leaflet-beautify-marker-icon.css'),  # noqa
            name='beautify_marker_css')

        figure.header.add_child(
            JavascriptLink('https://cdn.rawgit.com/marslan390/BeautifyMarker/master/leaflet-beautify-marker-icon.js'),  # noqa
            name='beautify_marker_js')
