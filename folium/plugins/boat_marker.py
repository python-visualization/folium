# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import json

from jinja2 import Template

from branca.element import Figure, JavascriptLink
from folium.map import Marker
from folium.utilities import _validate_location


class BoatMarker(Marker):
    """
    Creates a BoatMarker plugin to append into a map with
    Map.add_plugin.

    Parameters
    ----------
    location: tuple of length 2, default None
        The latitude and longitude of the marker.
        If None, then the middle of the map is used.

    heading: int, default 0
        Heading of the boat to an angle value between 0 and 360 degrees

    wind_heading: int, default None
        Heading of the wind to an angle value between 0 and 360 degrees
        If None, then no wind is represented.

    wind_speed: int, default 0
        Speed of the wind in knots.

    speed: int, default 0
        Speed of the boat in kilometers per hour

    animate: boolean, default True
        Option to animate marker travel

    update_frequency: int, default 500
        Update frequency for marker location changes

    """

    def __init__(self, location, popup=None, icon=None,
                 heading=0, wind_heading=None, wind_speed=0, speed=0,
                 animate=True, update_frequency=500, **kwargs):
        super(BoatMarker, self).__init__(
            _validate_location(location),
            popup=popup,
            icon=icon
        )
        self._name = 'BoatMarker'
        self.heading = heading
        self.wind_heading = wind_heading
        self.wind_speed = wind_speed
        self.speed = speed  # kilometers per hour
        self.kwargs = json.dumps(kwargs)
        self.animate = 1 if animate else 0
        self.update_frequency = update_frequency  # milliseconds

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.boatMarker(
                    [{{this.location[0]}},{{this.location[1]}}],
                    {{this.kwargs}}).addTo({{this._parent.get_name()}});
                var animate = {{this.animate}}
                var boatMarker = {{this.get_name()}};
                boatMarker.setHeadingWind({{this.heading}},
                    {{this.wind_speed}}, {{this.wind_heading}});

                if (animate === 1 && {{this.speed}} > 0) {
                    var updatesPerHour = function(s) {
                        return parseInt(
                            (60*60*1000)/s
                        );
                    }
                    var updateInterval = updatesPerHour(
                        {{this.update_frequency}});

                    window.setInterval(function() {
                        var destination = turf.destination(
                            boatMarker.toGeoJSON(),
                            {{this.speed}} / updateInterval,
                            {{this.heading}},
                            "kilometers");

                        boatMarker.setLatLng(
                            destination.geometry.coordinates.reverse());

                        if (!{{this._parent.get_name()}}.getBounds().contains({{this.get_name()}}.getLatLng())) {
                            {{this._parent.get_name()}}.panTo({{this.get_name()}}.getLatLng());
                        }
                    }, {{this.update_frequency}});
                }
            {% endmacro %}
            """)

    def render(self, **kwargs):
        super(BoatMarker, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')
        figure.header.add_child(
            JavascriptLink('https://api.tiles.mapbox.com/mapbox.js/plugins/turf/v2.0.0/turf.min.js'),  # noqa
            name='turf')

        figure.header.add_child(
            JavascriptLink('https://unpkg.com/leaflet.boatmarker/leaflet.boatmarker.min.js'),  # noqa
            name='boatmarker')
