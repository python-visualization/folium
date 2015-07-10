# -*- coding: utf-8 -*-

from uuid import uuid4
import json

class ScrollZoomToggler():
    """Adds a button to enable/disable zoom scrolling."""
    def __init__(self, zoom_enabled=False):
        """Creates a ScrollZoomToggler plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
            zoom_enabled: bool, default False
                Whether the zoom scrolling shall be enabled at display.
        """
        self.zoom_enabled = zoom_enabled
        self.name = "ScrollZoomToggler_"+uuid4().hex

    def render_html(self):
        """Generates the HTML part of the plugin."""
        return """<img id="{}" alt="scroll"
       src="https://cdnjs.cloudflare.com/ajax/libs/ionicons/1.5.2/png/512/arrow-move.png"
       onclick="toggleScroll()"></img>""".format(self.name)

    def render_css(self):
        """Generates the CSS part of the plugin."""
        return """
        #"""+self.name+""" {
            position:absolute;
            width:35px;
            bottom:10px;
            height:35px;
            left:10px;
            background-color:#fff;
            text-align:center;
            line-height:35px;
            vertical-align: middle;
            }
            """

    def render_js(self):
        """Generates the Javascript part of the plugin."""
        out = """
        map.scrollEnabled = true;

        var toggleScroll = function() {
            if (map.scrollEnabled) {
                map.scrollEnabled = false;
                map.scrollWheelZoom.disable();
                }
            else {
                map.scrollEnabled = true;
                map.scrollWheelZoom.enable();
                }
            };
        """
        if not self.zoom_enabled:
            out += "\n        toggleScroll();"
        return out

class MarkerCluster():
    """Adds a MarkerCluster layer on the map."""
    def __init__(self, data):
        """Creates a MarkerCluster plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
            data: list of list or array of shape (n,3).
                Data points of the form [[lat, lng, popup]].
        """
        self.data = [tuple(x) for x in data]
        self.name = "MarkerCluster_"+uuid4().hex

    def render_html(self):
        """Generates the HTML part of the plugin."""
        return """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.css" />
	    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.Default.css" />
	    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster.js"></script>
        """

    def render_css(self):
        """Generates the CSS part of the plugin."""
        return ""

    def render_js(self):
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
