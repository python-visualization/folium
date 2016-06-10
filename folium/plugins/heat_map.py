# -*- coding: utf-8 -*-
"""
Heat map
--------

Create a HeatMap layer

"""
import json
from jinja2 import Template

from branca.element import JavascriptLink, Figure
from branca.utilities import none_min, none_max

from folium.map import TileLayer


class HeatMap(TileLayer):
    def __init__(self, data, name=None, min_opacity=0.5, max_zoom=18,
                 max_val=1.0, radius=25, blur=15, gradient=None, overlay=True):
        """Create a Heatmap layer

        Parameters
        ----------
        data : list of points of the form [lat, lng] or [lat, lng, weight]
            The points you want to plot.
            You can also provide a numpy.array of shape (n,2) or (n,3).
        name : str
            The name of the layer that will be created.
        min_opacity  : default 1.
            The minimum opacity the heat will start at.
        max_zoom : default 18
            Zoom level where the points reach maximum intensity (as intensity
            scales with zoom), equals maxZoom of the map by default
        max_val : float, default 1.
            Maximum point intensity
        radius : int, default 25
            Radius of each "point" of the heatmap
        blur : int, default 15
            Amount of blur
        gradient : dict, default None
            Color gradient config. e.g. {0.4: 'blue', 0.65: 'lime', 1: 'red'}
        """
        super(TileLayer, self).__init__(name=name)
        self._name = 'HeatMap'
        self.tile_name = name if name is not None else self.get_name()

        self.data = [[x for x in line] for line in data]
        self.min_opacity = min_opacity
        self.max_zoom = max_zoom
        self.max_val = max_val
        self.radius = radius
        self.blur = blur
        self.gradient = (json.dumps(gradient, sort_keys=True) if
                         gradient is not None else "null")
        self.overlay = overlay

        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.heatLayer(
                {{this.data}},
                {
                    minOpacity: {{this.min_opacity}},
                    maxZoom: {{this.max_zoom}},
                    max: {{this.max_val}},
                    radius: {{this.radius}},
                    blur: {{this.blur}},
                    gradient: {{this.gradient}}
                    })
                .addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)

    def render(self, **kwargs):
        super(TileLayer, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_child(
            JavascriptLink("https://leaflet.github.io/Leaflet.heat/dist/leaflet-heat.js"),  # noqa
            name='leaflet-heat.js')

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
