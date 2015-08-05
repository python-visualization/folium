# -*- coding: utf-8 -*-
"""
Boat marker
-----------

Creates a marker shaped like a boat. Optionally you can append a wind direction. 
"""
import json

from .plugin import Plugin

class BoatMarker(Plugin):
    """Adds a BoatMarker layer on the map."""
    def __init__(self, position=None, heading=0, wind_heading=None, wind_speed=0, **kwargs):
        """Creates a BoatMarker plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
            position: tuple of length 2, default None
                The latitude and longitude of the marker.
                If None, then the middle of the map is used.

            heading: int, default 0
                Heading of the boat to an angle value between 0 and 360 degrees

            wind_heading: int, default None
                Heading of the wind to an angle value between 0 and 360 degrees
                If None, then no wind is represented.

            wind_speed: int, default 0
                Speed of the wind in knots.
        """
        super(BoatMarker, self).__init__()
        self.plugin_name = 'BoatMarker'
        self.position = None if position is None else tuple(position)
        self.heading = heading
        self.wind_heading = wind_heading
        self.wind_speed = wind_speed
        self.kwargs = kwargs.copy()
        
    def render_header(self, nb):
        """Generates the HTML part of the plugin."""
        return """
            <script src="https://thomasbrueggemann.github.io/leaflet.boatmarker/js/leaflet.boatmarker.min.js"></script>
            """  if nb==0 else ""

    def render_js(self, nb):
        """Generates the Javascript part of the plugin."""
        kwargs_str =  "{%s}" % ",".join(["%s : %s" % (key,json.dumps(val)) for (key,val) in self.kwargs.items()])
        position_str = "map.getCenter()" if self.position is None else "[%.12f,%.12f]"%self.position
        out = 'var boatMarker_%s = L.boatMarker(%s, %s).addTo(map);' % (nb,position_str,kwargs_str)
        
        if self.wind_heading is None:
            out += "boatMarker_%s.setHeading(%s);" % (nb,int(self.heading))
        else:
            out += "boatMarker_%s.setHeadingWind(%s, %s, %s);"%(nb,int(self.heading),
                                                             int(self.wind_speed),
                                                             int(self.wind_heading),
                                                             )
        return out
