# -*- coding: utf-8 -*-
"""
Marker plugin
--------------

"""
from jinja2 import Template
import json

from .plugin import Plugin
from .links import JavascriptLink

class Popup(Plugin):
    def __init__(self, html, max_width=300):
        super(Popup, self).__init__()
        self.plugin_name = 'Popup'
        self.html = json.dumps(html)
        self.max_width = max_width
        self.map = None

    def render(self, **kwargs):
        assert self.map is not None, "Cannot render a Popup that have no 'map' attribute."
        #{{ pop_name }}.bindPopup({{ pop_txt }});
        #{{ pop_name }}._popup.options.maxWidth = {{ width }};
        self.map.figure.script['Popup_'+self.object_name] = Template("""
        var Popup_{id} = L.popup({{
            maxWidth: '{maxWidth}'
            }}).setContent({html});""".format(
                html=self.html,
                maxWidth=self.max_width,
                id=self.object_name,
                ))
        return 'Popup_'+self.object_name

class VegaPopup(Plugin):
    def __init__(self, data, max_width=300):
        super(VegaPopup, self).__init__()
        self.plugin_name = 'VegaPopup'
        self.data = data
        self.map = None

    def render(self, **kwargs):
        assert self.map is not None, "Cannot render a Popup that have no 'map' attribute."
        #{{ pop_name }}.bindPopup({{ pop_txt }});
        #{{ pop_name }}._popup.options.maxWidth = {{ width }};
        self.map.figure.header['d3'    ] = JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js")
        self.map.figure.header['vega'  ] = JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/vega/1.4.3/vega.min.js")
        self.map.figure.header['jquery'] = JavascriptLink("https://code.jquery.com/jquery-2.1.0.min.js")
        self.map.figure.script['vega_parse'] = Template("""function vega_parse(spec, div) {
            vg.parse.spec(spec, function(chart) { chart({el:div}).update(); });}""")

        self.map.figure.script['VegaPopup_'+self.object_name] = Template("""
            var VegaPopup_{id} = $('<div id="VegaPopup_{id}" style="width: 675px; height: 350px;"></div>')[0];
            vega_parse({json},VegaPopup_{id});
            """.format(id=self.object_name,
                       json=json.dumps(self.data),
                      ))
        return "VegaPopup_{id}".format(id=self.object_name)

class Icon(Plugin):
    def __init__(self, color='blue', icon='info-sign', angle=0):
        super(Icon, self).__init__()
        self.plugin_name = 'Icon'
        self.color = color
        self.icon = icon
        self.angle = angle
        self.map = None

    def render(self, **kwargs):
        assert self.map is not None, "Cannot render an Icon that have no 'map' attribute."
        self.map.figure.script['Icon_'+self.object_name] = Template("""
        var Icon_{id} = L.AwesomeMarkers.icon({{
            icon: '{icon}',
            markerColor: '{color}',
            prefix: 'glyphicon',
            extraClasses: 'fa-rotate-{angle}'
            }});""".format(
                icon=self.icon,
                color=self.color,
                angle=self.angle,
                id=self.object_name,
                ))
        return 'Icon_'+self.object_name

class Marker(Plugin):
    def __init__(self, location, popup=None, icon=None):
        """Create a simple stock Leaflet marker on the map, with optional
        popup text or Vincent visualization.

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Marker (Northing, Easting)
        popup: string or tuple, default 'Pop Text'
            Input text or visualization for object. Can pass either text,
            or a tuple of the form (Vincent object, 'vis_path.json')
            It is possible to adjust the width of text/HTML popups
            using the optional keywords `popup_width` (default is 300px).
        icon: Icon plugin
            the Icon plugin to use to render the marker.

        Returns
        -------
        Marker names and HTML in obj.template_vars

        Example
        -------
        >>>map.simple_marker(location=[45.5, -122.3], popup='Portland, OR')
        >>>map.simple_marker(location=[45.5, -122.3], popup=(vis, 'vis.json'))

        """
        super(Marker, self).__init__()
        self.plugin_name = 'Marker'
        self.location = location
        self.icon = Template("new L.Icon.Default()") if icon is None else icon
        self.popup = Template("") if popup is None else popup

    def add_to_map(self, map):
        """Adds the plugin on a folium.map object."""
        super(Marker, self).add_to_map(map)
        self.icon.map = map
        self.popup.map = map

    def render_js(self, nb):
        return """
        var Marker_{id} = L.marker([{location[0]},{location[1]}], {{icon:{icon}}}){popup};
        map.addLayer(Marker_{id});
        """.format(
            id=self.object_name,
            location = self.location,
            icon = self.icon.render(),
            popup = ".bindPopup({})".format(self.popup.render()),
            )
