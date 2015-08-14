# -*- coding: utf-8 -*-
"""
Marker Cluster plugin
---------------------

Creates a MarkerCluster plugin to add on a folium map.
"""
import json

from .plugin import Plugin

class MarkerCluster(Plugin):
    """Adds a MarkerCluster layer on the map."""
    def __init__(self, data):
        """Creates a MarkerCluster plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
            data: list of list or array of shape (n,3).
                Data points of the form [[lat, lng, popup]].
        """
        super(MarkerCluster, self).__init__()
        self.plugin_name = 'MarkerCluster'
        self.data = [tuple(x) for x in data]

    def render_header(self, nb):
        """Generates the HTML part of the plugin."""
        return """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.css" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.Default.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster.js"></script>
        """ if nb==0 else ""

    def render_js(self, nb):
        """Generates the Javascript part of the plugin."""
        out = """
        var addressPoints = """+json.dumps(self.data)+""";

        var markers = L.markerClusterGroup();

        for (var i = 0; i < addressPoints.length; i++) {
            var a = addressPoints[i];
            var title = a[2];
            var marker = L.marker(new L.LatLng(a[0], a[1]), { title: title });
            marker.bindPopup(title);
            markers.addLayer(marker);
        }

        map.addLayer(markers);
        """
        return out
