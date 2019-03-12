# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import json

from branca.element import JavascriptLink

from folium.vector_layers import path_options
from folium.vector_layers import PolyLine


class PolyLineOffset(PolyLine):
    """
    Class adding offset capabilities to the PolyLine class.

    This plugin adds to folium Polylines the ability to be drawn with a
    relative pixel offset, without modifying their actual coordinates. The offset
    value can be either negative or positive, for left- or right-side offset,
    and remains constant across zoom levels.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: str or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, optional
        Display a text when hovering over the object.
    offset: int, default 0
        Relative pixel offset to draw a line parallel to an existant one,
        at a fixed distance.
    **kwargs:
        Polyline options. See their Github page for the
        available parameters.

    See https://github.com/bbecquet/Leaflet.PolylineOffset

    Examples
    --------
    >>> map = folium.Map(location=[58.0, -11.0],
    ...                  zoom_start=4,
    ...                  tiles="Mapbox Bright")
    >>> ll = [ [58.44773, -28.65234], [53, -23.33496]]
    >>> plugins.PolyLineOffset(ll, color="#f00", opacity=1, offset=-5).add_to(map)
    >>> plugins.PolyLineOffset(ll, color="#080", opacity=1, offset=10).add_to(map)

    """

    def __init__(self, locations, popup=None, tooltip=None, **kwargs):
        super(PolyLineOffset, self).__init__(
            locations=locations, popup=popup, tooltip=tooltip
        )
        self._name = "PolyLineOffset"
        # Polyline + PolyLineOffset defaults.
        options = path_options(line=True, **kwargs)
        options.update({"offset": kwargs.pop("offset", 0)})
        self.options = json.dumps(options, sort_keys=True, indent=2)

    def render(self, **kwargs):
        super(PolyLineOffset, self).render()
        figure = self.get_root()
        figure.header.add_child(
            JavascriptLink(
                "https://cdn.jsdelivr.net/npm/leaflet-polylineoffset@1.1.1/leaflet.polylineoffset.min.js"
            ),  # noqa
            name="polylineoffset",
        )
