import warnings

from folium.elements import JSCSSMixin
from folium.map import Layer
from folium.utilities import (
    none_max,
    none_min,
    parse_options,
    if_pandas_df_convert_to_numpy,
    validate_location,
)

from jinja2 import Template

import numpy as np


class HeatMap(JSCSSMixin, Layer):
    """
    Create a Heatmap layer

    Parameters
    ----------
    data : list of points of the form [lat, lng] or [lat, lng, weight]
        The points you want to plot.
        You can also provide a numpy.array of shape (n,2) or (n,3).
    name : string, default None
        The name of the Layer, as it will appear in LayerControls.
    min_opacity  : default 1.
        The minimum opacity the heat will start at.
    max_zoom : default 18
        Zoom level where the points reach maximum intensity (as intensity
        scales with zoom), equals maxZoom of the map by default
    radius : int, default 25
        Radius of each "point" of the heatmap
    blur : int, default 15
        Amount of blur
    gradient : dict, default None
        Color gradient config. e.g. {0.4: 'blue', 0.65: 'lime', 1: 'red'}
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.heatLayer(
                {{ this.data|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)

    default_js = [
        ('leaflet-heat.js',
         'https://cdn.jsdelivr.net/gh/python-visualization/folium@main/folium/templates/leaflet_heat.min.js'),
    ]

    def __init__(self, data, name=None, min_opacity=0.5, max_zoom=18,
                 radius=25, blur=15, gradient=None,
                 overlay=True, control=True, show=True, **kwargs):
        super(HeatMap, self).__init__(name=name, overlay=overlay,
                                      control=control, show=show)
        self._name = 'HeatMap'
        data = if_pandas_df_convert_to_numpy(data)
        self.data = [[*validate_location(line[:2]), *line[2:]]  # noqa: E999
                     for line in data]
        if np.any(np.isnan(self.data)):
            raise ValueError('data may not contain NaNs.')
        if kwargs.pop('max_val', None):
            warnings.warn('The `max_val` parameter is no longer necessary. '
                          'The largest intensity is calculated automatically.',
                          stacklevel=2)
        self.options = parse_options(
            min_opacity=min_opacity,
            max_zoom=max_zoom,
            radius=radius,
            blur=blur,
            gradient=gradient,
            **kwargs
        )

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """

        bounds = [[None, None], [None, None]]
        for point in self.data:
            bounds = [
                [
                    none_min(bounds[0][0], point[0]),
                    none_min(bounds[0][1], point[1]),
                ],
                [
                    none_max(bounds[1][0], point[0]),
                    none_max(bounds[1][1], point[1]),
                ],
            ]
        return bounds
