# -*- coding: utf-8 -*-
"""
Features
------

Extra features Elements.
"""
from jinja2 import Template
import json

from .utilities import (color_brewer, _parse_size, legend_scaler,
                        _locations_mirror, _locations_tolist, image_to_url)

from .element import Element, Figure, JavascriptLink, CssLink, MacroElement
from .map import TileLayer, Icon

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
        # if attribution is None:
        #     raise ValueError('WMS must'
        #                      ' also be passed an attribution')
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
    def __init__(self, location, popup=None,
                 color='black', opacity=1, weight=2,
                 fill_color='blue', fill_opacity=1,
                 number_of_sides=4, rotation=0, radius=15):
        """TODO : docstring here"""
        super(RegularPolygonMarker, self).__init__()
        self._name = 'RegularPolygonMarker'
        self.location = location
        self.color = color
        self.opacity = opacity
        self.weight = weight
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.number_of_sides = number_of_sides
        self.rotation = rotation
        self.radius = radius
        if popup is not None:
            self.add_children(popup)

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
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet-dvf/0.2/leaflet-dvf.markers.min.js"),
            name='dvf_js')


class Vega(Element):
    def __init__(self, data, width='100%', height='100%',
                 left="0%", top="0%", position='relative'):
        """TODO : docstring here"""
        super(Vega, self).__init__()
        self._name = 'Vega'
        self.data = data

        # Size Parameters.
        self.width = _parse_size(width)
        self.height = _parse_size(height)
        self.left = _parse_size(left)
        self.top = _parse_size(top)
        self.position = position
        self._template = Template(u"")

    def render(self, **kwargs):
        self.json = json.dumps(self.data)

        self._parent.html.add_children(Element(Template("""
            <div id="{{this.get_name()}}"></div>
            """).render(this=self, kwargs=kwargs)), name=self.get_name())

        self._parent.script.add_children(Element(Template("""
            vega_parse({{this.json}},{{this.get_name()}});
            """).render(this=self)), name=self.get_name())

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
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

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"),
            name='d3')

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/vega/1.4.3/vega.min.js"),
            name='vega')

        figure.header.add_children(
            JavascriptLink("https://code.jquery.com/jquery-2.1.0.min.js"),
            name='jquery')

        figure.script.add_children(
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
                If file, then data will be read in the file and fully embedded in Leaflet's javascript.
                If dict, then data will be converted to JSON and embedded in the javascript.
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


class TopoJson(MacroElement):
    def __init__(self, data, object_path):
        """TODO docstring here.
        """
        super(TopoJson, self).__init__()
        self._name = 'TopoJson'
        if 'read' in dir(data):
            self.data = data.read()
        elif type(data) is dict:
            self.data = json.dumps(data)
        else:
            self.data = data

        self.object_path = object_path

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}}_data = {{this.data}};
                var {{this.get_name()}} = L.geoJson(topojson.feature(
                    {{this.get_name()}}_data,
                    {{this.get_name()}}_data.{{this.object_path}}
                    )).addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def render(self, **kwargs):
        super(TopoJson, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"),
            name='topojson')


class GeoJsonStyle(MacroElement):
    def __init__(self, color_domain, color_code, color_data=None,
                 key_on='feature.properties.color',
                 weight=1, opacity=1, color='black',
                 fill_opacity=0.6, dash_array=0):
        """TODO : docstring here.
        """
        super(GeoJsonStyle, self).__init__()
        self._name = 'GeoJsonStyle'

        self.color_domain = color_domain
        self.color_range = color_brewer(color_code, n=len(color_domain))
        self.color_data = json.dumps(color_data)
        self.key_on = key_on

        self.weight = weight
        self.opacity = opacity
        self.color = color
        self.fill_color = color_code
        self.fill_opacity = fill_opacity
        self.dash_array = dash_array

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                {% if not this.color_range %}
                    var {{this.get_name()}} = {
                        color_function : function(feature) {
                            return '{{this.fill_color}}';
                            },
                        };
                {%else%}
                    var {{this.get_name()}} = {
                        color_scale : d3.scale.threshold()
                              .domain({{this.color_domain}})
                              .range({{this.color_range}}),
                        color_data : {{this.color_data}},
                        color_function : function(feature) {
                            {% if this.color_data=='null' %}
                                return this.color_scale({{this.key_on}});
                            {% else %}
                                return
                                  this.color_scale(this.color_data[{{this.key_on}}]);
                            {% endif %}
                            },
                        };
                {%endif%}

                {{this._parent.get_name()}}.setStyle(function(feature) {
                    return {
                        fillColor: {{this.get_name()}}.color_function(feature),
                        weight: {{this.weight}},
                        opacity: {{this.opacity}},
                        color: '{{this.color}}',
                        fillOpacity: {{this.fill_opacity}},
                        dashArray: '{{this.dash_array}}'
                        };
                    });
            {% endmacro %}
            """)

    def render(self, **kwargs):
        super(GeoJsonStyle, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"),
            name='d3')


class ColorScale(MacroElement):
    def __init__(self, color_domain, color_code, caption=""):
        """TODO : docstring here.
        """
        super(ColorScale, self).__init__()
        self._name = 'ColorScale'

        self.color_domain = color_domain
        self.color_range = color_brewer(color_code, n=len(color_domain))
        self.tick_labels = legend_scaler(self.color_domain)

        self.caption = caption
        self.fill_color = color_code

        self._template = self._env.get_template('color_scale.js')

    def render(self, **kwargs):
        super(ColorScale, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_children(
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
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")
        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster-src.js"),
            name='marker_cluster_src')

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster.js"),
            name='marker_cluster')

        figure.header.add_children(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.css"),
            name='marker_cluster_css')

        figure.header.add_children(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.Default.css"),
            name="marker_cluster_default_css")


class DivIcon(MacroElement):
    def __init__(self, width=30, height=30):
        """TODO : docstring here"""
        super(DivIcon, self).__init__()
        self._name = 'DivIcon'
        self.width = width
        self.height = height

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.divIcon({
                    className: 'leaflet-div-icon',
                    'iconSize': [{{ this.width }},{{ this.height }}]
                    });
                {{this._parent.get_name()}}.setIcon({{this.get_name()}});
            {% endmacro %}
            """)


class CircleMarker(MacroElement):
    def __init__(self, location, radius=500, color='black',
                 fill_color='black', fill_opacity=0.6, popup=None):
        """TODO : docstring here
        """
        super(CircleMarker, self).__init__()
        self._name = 'CircleMarker'
        self.location = location
        self.radius = radius
        self.color = color
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        if popup is not None:
            self.add_children(popup)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.circle(
                [{{this.location[0]}},{{this.location[1]}}],
                {{ this.radius }},
                {
                    color: '{{ this.color }}',
                    fillColor: '{{ this.fill_color }}',
                    fillOpacity: {{ this.fill_opacity }}
                    }
                )
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)


class LatLngPopup(MacroElement):
    def __init__(self):
        """TODO : docstring here
        """
        super(LatLngPopup, self).__init__()
        self._name = 'LatLngPopup'

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
                                    "<br>Longitude: " + e.latlng.lng.toFixed(4))
                        .openOn({{this._parent.get_name()}});
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """)


class ClickForMarker(MacroElement):
    def __init__(self, popup=None):
        """TODO : docstring here
        """
        super(ClickForMarker, self).__init__()
        self._name = 'ClickForMarker'

        if popup:
            self.popup = ''.join(['"', popup, '"'])
        else:
            self.popup = '"Latitude: " + lat + "<br>Longitude: " + lng '

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                function newMarker(e){
                    var new_mark = L.marker().setLatLng(e.latlng).addTo({{this._parent.get_name()}});
                    new_mark.dragging.enable();
                    new_mark.on('dblclick', function(e){ {{this._parent.get_name()}}.removeLayer(e.target)})
                    var lat = e.latlng.lat.toFixed(4),
                       lng = e.latlng.lng.toFixed(4);
                    new_mark.bindPopup({{ this.popup }});
                    };
                {{this._parent.get_name()}}.on('click', newMarker);
            {% endmacro %}
            """)


class PolyLine(MacroElement):
    def __init__(self, locations, color=None, weight=None,
                 opacity=None, latlon=True):
        """Creates a PolyLine object to append into a map with
        Map.add_children.

        Parameters
        ----------
            locations: list of points (latitude, longitude)
                Latitude and Longitude of line (Northing, Easting)
            color: string, default Leaflet's default ('#03f')
            weight: float, default Leaflet's default (5)
            opacity: float, default Leaflet's default (0.5)
            latlon: bool, default True
                Whether locations are given in the form [[lat, lon]]
                or not ([[lon, lat]] if False).
                Note that the default GeoJson format is latlon=False,
                while Leaflet polyline's default is latlon=True.
        """
        super(PolyLine, self).__init__()
        self._name = 'PolyLine'
        self.data = (_locations_mirror(locations) if not latlon else
                     _locations_tolist(locations))
        self.color = color
        self.weight = weight
        self.opacity = opacity

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.polyline(
                    {{this.data}},
                    {
                        {% if this.color != None %}color: '{{ this.color }}',{% endif %}
                        {% if this.weight != None %}weight: {{ this.weight }},{% endif %}
                        {% if this.opacity != None %}opacity: {{ this.opacity }},{% endif %}
                        });
                {{this._parent.get_name()}}.addLayer({{this.get_name()}});
            {% endmacro %}
            """)


class MultiPolyLine(MacroElement):
    def __init__(self, locations, color=None, weight=None,
                 opacity=None, latlon=True):
        """Creates a MultiPolyLine object to append into a map with
        Map.add_children.

        Parameters
        ----------
            locations: list of points (latitude, longitude)
                Latitude and Longitude of line (Northing, Easting)
            color: string, default Leaflet's default ('#03f')
            weight: float, default Leaflet's default (5)
            opacity: float, default Leaflet's default (0.5)
            latlon: bool, default True
                Whether locations are given in the form [[lat, lon]]
                or not ([[lon, lat]] if False).
                Note that the default GeoJson format is latlon=False,
                while Leaflet polyline's default is latlon=True.
        """
        super(MultiPolyLine, self).__init__()
        self._name = 'MultiPolyLine'
        self.data = (_locations_mirror(locations) if not latlon else
                     _locations_tolist(locations))
        self.color = color
        self.weight = weight
        self.opacity = opacity

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.multiPolyline(
                    {{this.data}},
                    {
                        {% if this.color != None %}color: '{{ this.color }}',{% endif %}
                        {% if this.weight != None %}weight: {{ this.weight }},{% endif %}
                        {% if this.opacity != None %}opacity: {{ this.opacity }},{% endif %}
                        });
                {{this._parent.get_name()}}.addLayer({{this.get_name()}});
            {% endmacro %}
            """)


class ImageOverlay(MacroElement):
    def __init__(self, image, bounds, opacity=1., attribution=None,
                 origin='upper', colormap=None, mercator_project=False):
        """Used to load and display a single image over specific bounds of
        the map, implements ILayer interface.

        Parameters
        ----------
            image: string, file or array-like object
                The data you want to draw on the map.
                * If string, it will be written directly in the output file.
                * If file, it's content will be converted as embeded in the output file.
                * If array-like, it will be converted to PNG base64 string and embedded in the output.
            bounds: list
                Image bounds on the map in the form [[lat_min, lon_min], [lat_max, lon_max]]
            opacity: float, default Leaflet's default (1.0)
            attr: string, default Leaflet's default ("")
            origin : ['upper' | 'lower'], optional, default 'upper'
                Place the [0,0] index of the array in the upper left or
                lower left corner of the axes.
            colormap : callable, used only for `mono` image.
                Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
                for transforming a mono image into RGB.
                It must output iterables of length 3 or 4, with values between 0. and 1.
                Hint : you can use colormaps from `matplotlib.cm`.
            mercator_project : bool, default False, used only for array-like image.
                Transforms the data to project (longitude, latitude)
                coordinates to the Mercator projection.
        """
        super(ImageOverlay, self).__init__()
        self._name = 'ImageOverlay'

        self.url = image_to_url(image, origin=origin,
                                mercator_project=mercator_project,
                                bounds=bounds)

        self.bounds = json.loads(json.dumps(bounds))
        options = {
            'opacity': opacity,
            'attribution': attribution,
        }
        self.options = json.dumps({key: val for key, val
                                   in options.items() if val},
                                  sort_keys=True)
        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.imageOverlay(
                    '{{ this.url }}',
                    {{ this.bounds }},
                    {{ this.options }}
                    ).addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)


class CustomIcon(Icon):
    def __init__(self, icon_image, icon_size=None, icon_anchor=None,
                 shadow_image=None, shadow_size=None, shadow_anchor=None,
                 popup_anchor=None):
        """Create a custom icon, based on an image.

        Parameters
        ----------
            icon_image :  string, file or array-like object
                The data you want to use as an icon.
                * If string, it will be written directly in the output file.
                * If file, it's content will be converted as embedded in the output file.
                * If array-like, it will be converted to PNG base64 string and embedded in the output.
            icon_size : tuple of 2 int
                Size of the icon image in pixels.
            icon_anchor : tuple of 2 int
                The coordinates of the "tip" of the icon
                (relative to its top left corner).
                The icon will be aligned so that this point is at the
                marker's geographical location.
            shadow_image :  string, file or array-like object
                The data for the shadow image. If not specified,
                no shadow image will be created.
            shadow_size : tuple of 2 int
                Size of the shadow image in pixels.
            shadow_anchor : tuple of 2 int
                The coordinates of the "tip" of the shadow relative to its
                top left corner (the same as icon_anchor if not specified).
            popup_anchor : tuple of 2 int
                The coordinates of the point from which popups will "open",
                relative to the icon anchor.
        """
        super(Icon, self).__init__()
        self._name = 'CustomIcon'
        self.icon_url = image_to_url(icon_image)
        self.icon_size = icon_size
        self.icon_anchor = icon_anchor

        self.shadow_url = (image_to_url(shadow_image)
                           if shadow_image is not None else None)
        self.shadow_size = shadow_size
        self.shadow_anchor = shadow_anchor
        self.popup_anchor = popup_anchor

        self._template = Template(u"""
            {% macro script(this, kwargs) %}

                var {{this.get_name()}} = L.icon({
                    iconUrl: '{{this.icon_url}}',
                    {% if this.icon_size %}iconSize: [{{this.icon_size[0]}},{{this.icon_size[1]}}],{% endif %}
                    {% if this.icon_anchor %}iconAnchor: [{{this.icon_anchor[0]}},{{this.icon_anchor[1]}}],{% endif %}

                    {% if this.shadow_url %}shadowUrl: '{{this.shadow_url}}',{% endif %}
                    {% if this.shadow_size %}shadowSize: [{{this.shadow_size[0]}},{{this.shadow_size[1]}}],{% endif %}
                    {% if this.shadow_anchor %}shadowAnchor: [{{this.shadow_anchor[0]}},{{this.shadow_anchor[1]}}],{% endif %}

                    {% if this.popup_anchor %}popupAnchor: [{{this.popup_anchor[0]}},{{this.popup_anchor[1]}}],{% endif %}
                    });
                {{this._parent.get_name()}}.setIcon({{this.get_name()}});
            {% endmacro %}
            """)
