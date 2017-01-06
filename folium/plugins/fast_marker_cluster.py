# -*- coding: utf-8 -*-
"""
Marker Cluster plugin
---------------------

Creates a MarkerCluster plugin to add on a folium map.
"""

from jinja2 import Template

from . import MarkerCluster


class FastMarkerCluster(MarkerCluster):
    """Creates a FasterMarkerCluster plugin to append into a map with
        FasterMarkerCluster(data, callback=create_marker).add_to(map)
        map.add_to(fig).

        Parameters
        ----------
            data: list of list or array of shape (n,2).
                Data points of the form [[lat, lng]].

            callback: list of length n.

            popup: popup for each marker
    """
    def __init__(self, data, callback=None):
        super(FastMarkerCluster, self).__init__([])
        self._name = 'Script'
        self._data = data
        if callback is None:
            self._callback = self.create_marker()
        else:
            self._callback = "var callback = {};".format(callback)

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

    def create_marker(self):
        """Returns a L.msarker object"""
        t = ('var callback;\n' +
             'callback = function (row) {\n' +
             '\tvar icon, marker;\n' +
             '\t// Returns a L.marker object\n' +
             '\ticon = L.AwesomeMarkers.icon();\n' +
             '\tmarker = L.marker(new L.LatLng(row[0], row[1]));\n' +
             '\tmarker.setIcon(icon);\n' +
             '\treturn marker;\n' +
             '};')

        return t
