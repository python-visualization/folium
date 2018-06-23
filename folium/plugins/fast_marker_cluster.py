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
    name : string, default None
        The name of the Layer, as it will appear in LayerControls.
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    options : dict, default None
        A dictionary with options for Leaflet.markercluster. See
        https://github.com/Leaflet/Leaflet.markercluster for options.

    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{ this.get_name() }} = (function(){
                {{this._callback}}

                var data = {{ this._data }};
                var cluster = L.markerClusterGroup({{ this.options }});

                for (var i = 0; i < data.length; i++) {
                    var row = data[i];
                    var marker = callback(row);
                    marker.addTo(cluster);
                }

                cluster.addTo({{ this._parent.get_name() }});
                return cluster;
            })();
            {% endmacro %}""")

    def __init__(self, data, callback=None, options=None,
                 name=None, overlay=True, control=True, show=True):
        super(FastMarkerCluster, self).__init__(name=name, overlay=overlay,
                                                control=control, show=show,
                                                options=options)
        self._name = 'FastMarkerCluster'
        self._data = _validate_coordinates(data)

        if callback is None:
            self._callback = """
                var callback = function (row) {
                    var icon = L.AwesomeMarkers.icon();
                    var marker = L.marker(new L.LatLng(row[0], row[1]));
                    marker.setIcon(icon);
                    return marker;
                };"""
        else:
            self._callback = 'var callback = {};'.format(callback)
