# -*- coding: utf-8 -*-
"""
Features
------

Extra features Elements.
"""
from jinja2 import Template
import json

from .utilities import color_brewer, _parse_size

from .element import Element, Figure, JavascriptLink, CssLink, Div, MacroElement
from .map import Map, TileLayer, Icon, Marker, Popup

class WmsTileLayer(TileLayer):
    def __init__(self, url, name=None,
                 format=None, layers=None, transparent=True,
                attribution=None):
        """TODO docstring here
        Parameters
        ----------
        """
        super(TileLayer, self).__init__()
        self._name = 'WmsTileLayer'
        self.tile_name = name if name is not None else 'WmsTileLayer_'+self._id
        self.url = url
        self.format = format
        self.layers = layers
        self.transparent = transparent
        #if attribution is None:
        #    raise ValueError('WMS must'
        #                     ' also be passed an attribution')
        self.attribution = attribution

        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.tileLayer.wms(
                '{{ this.url }}',
                {
                    format:'{{ this.format }}',
                    transparent: {{ this.transparent.__str__().lower() }},
                    layers:'{{ this.layers }}'
                    {% if this.attribution %}, attribution:'{{this.attribution}}'{% endif %}
                    }
                ).addTo({{this._parent.get_name()}});

        {% endmacro %}
        """)

class RegularPolygonMarker(MacroElement):
    def __init__(self, location, popup=None, icon=None,
                 color='black', opacity=1, weight=2,
                 fill_color='blue', fill_opacity=1,
                 number_of_sides=4, rotation=0, radius=15):
        """TODO : docstring here"""
        super(RegularPolygonMarker, self).__init__()
        self._name = 'RegularPolygonMarker'
        self.location = location
        self.icon = "new L.Icon.Default()" if icon is None else icon
        self.color   = color
        self.opacity = opacity
        self.weight  = weight
        self.fill_color  = fill_color
        self.fill_opacity= fill_opacity
        self.number_of_sides= number_of_sides
        self.rotation = rotation
        self.radius = radius

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
            var {{this.get_name()}} = new L.RegularPolygonMarker(
                new L.LatLng({{this.location[0]}},{{this.location[1]}}),
                {
                    icon : new L.Icon.Default(),
                    color: '{{this.color}}',
                    opacity: {{this.opacity}},
                    weight: {{this.weight}},
                    fillColor: '{{this.fill_color}}',
                    fillOpacity: {{this.fill_opacity}},
                    numberOfSides: {{this.number_of_sides}},
                    rotation: {{this.rotation}},
                    radius: {{this.radius}}
                    }
                )
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)
    def render(self, **kwargs):
        super(RegularPolygonMarker, self).render()

        figure = self.get_root()
        assert isinstance(figure,Figure), ("You cannot render this Element "
            "if it's not in a Figure.")

        figure.header.add_children(\
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet-dvf"
                           "/0.2/leaflet-dvf.markers.min.js"),
            name='dvf_js')

class Vega(Element):
    def __init__(self, data, width='100%', height='100%',
                 left="0%", top="0%", position='relative'):
        """TODO : docstring here"""
        super(Vega, self).__init__()
        self._name = 'Vega'
        self.data = data

        # Size Parameters.
        self.width  = _parse_size(width)
        self.height = _parse_size(height)
        self.left = _parse_size(left)
        self.top  = _parse_size(top)
        self.position = position


        self._template = Template(u"")
    def render(self, **kwargs):
        self.json = json.dumps(self.data)

        self._parent.html.add_children(Element(Template("""
            <div id="{{this.get_name()}}"
                style="width: {{this.width[0]}}{{this.width[1]}}; height: {{this.height[0]}}{{this.height[1]}};">
                </div>
            """).render(this=self, kwargs=kwargs)), name=self.get_name())

        self._parent.script.add_children(Element(Template("""
            vega_parse({{this.json}},{{this.get_name()}});
            """).render(this=self)), name=self.get_name())

        figure = self.get_root()
        assert isinstance(figure,Figure), ("You cannot render this Element "
            "if it's not in a Figure.")

        figure.header.add_children(Element(Template("""
            <style> #{{this.get_name()}} {
                position : {{this.position}};
                width : {{this.width[0]}}{{this.width[1]}};
                height: {{this.height[0]}}{{this.height[1]}};
                left: {{this.left[0]}}{{this.left[1]}};
                top: {{this.top[0]}}{{this.top[1]}};
            </style>
            """).render(this=self, **kwargs)), name=self.get_name())

        figure.header.add_children(\
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"),
            name='d3')

        figure.header.add_children(\
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/vega/1.4.3/vega.min.js"),
            name='vega')

        figure.header.add_children(\
            JavascriptLink("https://code.jquery.com/jquery-2.1.0.min.js"),
            name='jquery')

        figure.script.add_children(\
            Template("""function vega_parse(spec, div) {
            vg.parse.spec(spec, function(chart) { chart({el:div}).update(); });}"""),
            name='vega_parse')

class GeoJson(MacroElement):
    def __init__(self, data):
        """Creates a GeoJson plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
            data: file, dict or str.
                The geo-json data you want to plot.
                If file, then data will be read in the file and fully embeded in Leaflet's javascript.
                If dict, then data will be converted to json and embeded in the javascript.
                If str, then data will be passed to the javascript as-is.

                examples :
                    # providing file
                    GeoJson(open('foo.json'))

                    # providing dict
                    GeoJson(json.load(open('foo.json')))

                    # providing string
                    GeoJson(open('foo.json').read())
        """
        super(GeoJson, self).__init__()
        self._name = 'GeoJson'
        if 'read' in dir(data):
            self.data = data.read()
        elif type(data) is dict:
            self.data = json.dumps(data)
        else:
            self.data = data

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.geoJson({{this.data}}).addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

class GeoJsonStyle(MacroElement):
    def __init__(self, color_domain, color_code, color_data=None, key_on='feature.properties.color'):
        """TODO : docstring here.
        """
        super(GeoJsonStyle, self).__init__()
        self._name = 'GeoJsonStyle'

        self.color_domain = color_domain
        self.color_range = color_brewer(color_code, n=len(color_domain))
        self.color_data = json.dumps(color_data)
        self.key_on = key_on

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = {
                    color_scale : d3.scale.threshold()
                          .domain({{this.color_domain}})
                          .range({{this.color_range}}),
                    color_data : {{this.color_data}},
                    color_function : function(feature) {
                        {% if this.color_data=='null' %}
                            return this.color_scale({{this.key_on}});
                        {% else %}
                            return this.color_scale(this.color_data[{{this.key_on}}]);
                        {% endif %}
                        },
                    };

                {{this._parent.get_name()}}.setStyle(function(feature) {
                    return {
                        fillColor: {{this.get_name()}}.color_function(feature),
                        weight: 2,
                        opacity: 1,
                        color: 'white',
                        dashArray: '3',
                        fillOpacity: 0.7
                        };
                    });
            {% endmacro %}
            """)
    def render(self,**kwargs):
        super(GeoJsonStyle,self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure,Figure), ("You cannot render this Element "
            "if it's not in a Figure.")

        figure.header.add_children(\
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"),
                                   name='d3')

class MarkerCluster(MacroElement):
    """Adds a MarkerCluster layer on the map."""
    def __init__(self):
        """Creates a MarkerCluster element to append into a map with
        Map.add_children.

        Parameters
        ----------
        """
        super(MarkerCluster, self).__init__()
        self._name = 'MarkerCluster'
        self._template = Template(u"""
            {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.markerClusterGroup();
            {{this._parent.get_name()}}.addLayer({{this.get_name()}});
            {% endmacro %}
            """)
    def render(self, **kwargs):
        super(MarkerCluster, self).render()

        figure = self.get_root()
        assert isinstance(figure,Figure), ("You cannot render this Element "
            "if it's not in a Figure.")
        figure.header.add_children(\
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster"
                           "/0.4.0/leaflet.markercluster-src.js"),
            name='marker_cluster_src')

        figure.header.add_children(\
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster"
                           "/0.4.0/leaflet.markercluster.js"),
            name='marker_cluster')

        figure.header.add_children(\
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.css"),
            name='marker_cluster_css')

        figure.header.add_children(\
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.Default.css"),
            name="marker_cluster_default_css")
