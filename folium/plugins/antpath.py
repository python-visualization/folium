from folium.elements import JSCSSMixin
from folium.vector_layers import path_options, BaseMultiLocation

from jinja2 import Template


class AntPath(JSCSSMixin, BaseMultiLocation):
    """
    Class for drawing AntPath polyline overlays on a map.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: str or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, optional
        Display a text when hovering over the object.
    **kwargs:
        Polyline and AntPath options. See their Github page for the
        available parameters.

    https://github.com/rubenspgcavalcante/leaflet-ant-path/

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            {{ this.get_name() }} = L.polyline.antPath(
              {{ this.locations|tojson }},
              {{ this.options|tojson }}
        ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)

    default_js = [
        ('antpath',
         'https://cdn.jsdelivr.net/npm/leaflet-ant-path@1.1.2/dist/leaflet-ant-path.min.js')
    ]

    def __init__(self, locations, popup=None, tooltip=None, **kwargs):
        super(AntPath, self).__init__(
            locations,
            popup=popup,
            tooltip=tooltip,
        )

        self._name = 'AntPath'
        # Polyline + AntPath defaults.
        self.options = path_options(line=True, **kwargs)
        self.options.update({
            'paused': kwargs.pop('paused', False),
            'reverse': kwargs.pop('reverse', False),
            'hardwareAcceleration': kwargs.pop('hardware_acceleration', False),
            'delay': kwargs.pop('delay', 400),
            'dashArray': kwargs.pop('dash_array', [10, 20]),
            'weight': kwargs.pop('weight', 5),
            'opacity': kwargs.pop('opacity', 0.5),
            'color': kwargs.pop('color', '#0000FF'),
            'pulseColor': kwargs.pop('pulse_color', '#FFFFFF'),
        })
