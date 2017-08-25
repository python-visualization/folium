# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from folium.map import Layer

from jinja2 import Template


class VideoOverlay(Layer):
    """
    Used to load and display a video over the map.

    Parameters
    ----------
    video_url: URL of the video
    bounds: list
        Video bounds on the map in the form [[lat_min, lon_min],
        [lat_max, lon_max]]
    opacity: float, default Leaflet's default (1.0)
    attr: string, default Leaflet's default ('')

    """
    def __init__(self, video_url, bounds, opacity=1., attr=None,
                 autoplay=True, loop=True):
        super(VideoOverlay, self).__init__()
        self._name = 'VideoOverlay'

        self.video_url = video_url

        self.bounds = json.loads(json.dumps(bounds))
        options = {
            'opacity': opacity,
            'attribution': attr,
            'loop': loop,
            'autoplay': autoplay,
        }
        self.options = json.dumps(options)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.videoOverlay(
                    '{{ this.video_url }}',
                    {{ this.bounds }},
                    {{ this.options }}
                    ).addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]]

        """
        return self.bounds
