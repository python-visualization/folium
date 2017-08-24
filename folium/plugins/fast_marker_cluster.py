# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from folium.plugins.marker_cluster import MarkerCluster
from folium.utilities import _validate_coordinates

from jinja2 import Template


class FastMarkerCluster(MarkerCluster):
    """
    Add marker clusters to a map using in-browser rendering.
    Using FastMarkerCluster it is possible to render 000's of
    points far quicker than the MarkerCluster class.

    Be aware that the FastMarkerCluster class passes an empty
    list to the parent class' __init__ method during initialisation.
    This means that the add_child method is never called, and
    no reference to any marker data are retained. Methods such
    as get_bounds() are therefore not available when using it.

    Parameters
    ----------
    data: list
        List of list of shape [[], []]. Data points should be of
        the form [[lat, lng]].

    callback: string, default None
        A string representation of a valid Javascript function
        that will be passed a lat, lon coordinate pair. See the
        FasterMarkerCluster for an example of a custom callback.

    """
    def __init__(self, data, callback=None):
        super(FastMarkerCluster, self).__init__([])
        self._name = 'FastMarkerCluster'
        self._data = _validate_coordinates(data)

        if callback is None:
            self._callback = ('var callback;\n' +
                              'callback = function (row) {\n' +
                              '\tvar icon, marker;\n' +
                              '\t// Returns a L.marker object\n' +
                              '\ticon = L.AwesomeMarkers.icon();\n' +
                              '\tmarker = L.marker(new L.LatLng(row[0], ' +
                              'row[1]));\n' +
                              '\tmarker.setIcon(icon);\n' +
                              '\treturn marker;\n' +
                              '};')
        else:
            self._callback = 'var callback = {};'.format(callback)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
            {{this._callback}}

            (function(){
                var data = {{this._data}};
                var map = {{this._parent.get_name()}};
                var cluster = L.markerClusterGroup();

                for (var i = 0; i < data.length; i++) {
                    var row = data[i];
                    var marker = callback(row);
                    marker.addTo(cluster);
                }

                cluster.addTo(map);
            })();
            {% endmacro %}""")
