# -*- coding: utf-8 -*-
"""
Features
------

Extra features Elements.
"""
from jinja2 import Template
import json

from .utilities import (color_brewer, _parse_size, legend_scaler,
                        _locations_mirror, _locations_tolist, image_to_url,
                        text_type, binary_type)

from .element import Element, Figure, JavascriptLink, CssLink, MacroElement
from .map import Layer, Icon, Marker, Popup

class WmsTileLayer(Layer):
    def __init__(self, url, name=None,
                 format=None, layers=None, transparent=True,
                 attr=None, overlay=True, control=True):
        """
        TODO docstring here

        """
        super(WmsTileLayer, self).__init__(overlay=overlay, control=control)
        self._name = 'WmsTileLayer'
        self.tile_name = name if name is not None else 'WmsTileLayer_'+self._id
        self.url = url
        self.format = format
        self.layers = layers
        self.transparent = transparent
        self.attr = attr

        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.tileLayer.wms(
                '{{ this.url }}',
                {
                    format:'{{ this.format }}',
                    transparent: {{ this.transparent.__str__().lower() }},
                    layers:'{{ this.layers }}'
                    {% if this.attr %}, attribution:'{{this.attr}}'{% endif %}
                    }
                ).addTo({{this._parent.get_name()}});

        {% endmacro %}
        """)  # noqa

class RegularPolygonMarker(Marker):
    def __init__(self, location, color='black', opacity=1, weight=2,
                 fill_color='blue', fill_opacity=1,
                 number_of_sides=4, rotation=0, radius=15, popup=None):
        """Custom markers using the Leaflet Data Vis Framework.

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Marker (Northing, Easting)
        color: string, default 'black'
            Marker line color
        opacity: float, default 1
            Line opacity, scale 0-1
        weight: int, default 2
            Stroke weight in pixels
        fill_color: string, default 'blue'
            Marker fill color
        fill_opacity: float, default 1
            Marker fill opacity
        number_of_sides: int, default 4
            Number of polygon sides
        rotation: int, default 0
            Rotation angle in degrees
        radius: int, default 15
            Marker radius, in pixels
        popup: string or folium.Popup, default None
            Input text or visualization for object. Can pass either text,
            or a folium.Popup object.
            If None, no popup will be displayed.

        Returns
        -------
        Polygon marker names and HTML in obj.template_vars

        For more information, see https://humangeo.github.io/leaflet-dvf/
        """
        super(RegularPolygonMarker, self).__init__(location, popup=popup)
        self._name = 'RegularPolygonMarker'
        self.color = color
        self.opacity = opacity
        self.weight = weight
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.number_of_sides = number_of_sides
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
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet-dvf/0.2/leaflet-dvf.markers.min.js"),  # noqa
            name='dvf_js')


class Vega(Element):
    def __init__(self, data, width=None, height=None,
                 left="0%", top="0%", position='relative'):
        """
        TODO docstring here

        """
        super(Vega, self).__init__()
        self._name = 'Vega'
        self.data = data.to_json() if hasattr(data,'to_json') else data
        if isinstance(self.data,text_type) or isinstance(data,binary_type):
            self.data = json.loads(self.data)

        # Size Parameters.
        self.width = _parse_size(self.data.get('width','100%') if width is None else width)
        self.height = _parse_size(self.data.get('height','100%') if height is None else height)
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
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"),  # noqa
            name='d3')

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/vega/1.4.3/vega.min.js"),  # noqa
            name='vega')

        figure.header.add_children(
            JavascriptLink("https://code.jquery.com/jquery-2.1.0.min.js"),
            name='jquery')

        figure.script.add_children(
            Template("""function vega_parse(spec, div) {
            vg.parse.spec(spec, function(chart) { chart({el:div}).update(); });}"""),  # noqa
            name='vega_parse')

class GeoJson(MacroElement):
    def __init__(self, data, style_function=None):
        """
        Creates a GeoJson plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
        data: file, dict or str.
            The GeoJSON data you want to plot.
            * If file, then data will be read in the file and fully
              embedded in Leaflet's JavaScript.
            * If dict, then data will be converted to JSON and embedded
              in the JavaScript.
            * If str, then data will be passed to the JavaScript as-is.
        style_function: function, default None
            A function mapping a GeoJson Feature to a style dict.

        Examples
        --------
        >>> # Providing file that shall be embeded.
        >>> GeoJson(open('foo.json'))
        >>> # Providing filename that shall not be embeded.
        >>> GeoJson('foo.json')
        >>> # Providing dict.
        >>> GeoJson(json.load(open('foo.json')))
        >>> # Providing string.
        >>> GeoJson(open('foo.json').read())

        >>> # Providing a style_function that put all states in green, but Alabama in blue.
        >>> style_function=lambda x: {'fillColor': '#0000ff' if x['properties']['name']=='Alabama' else '#00ff00'}
        >>> GeoJson(geojson, style_function=style_function)
        """
        super(GeoJson, self).__init__()
        self._name = 'GeoJson'
        if hasattr(data,'read'):
            self.embed = True
            self.data = json.load(data)
        elif isinstance(data,dict):
            self.embed = True
            self.data = data
        elif isinstance(data, text_type) or isinstance(data, binary_type):
            if data.lstrip()[0] in '[{': # This is a GeoJSON inline string
                self.embed = True
                self.data = json.loads(data)
            else:  # This is a filename
                self.embed = False
                self.data = data
        else:
            raise ValueError('Unhandled data type.')

        if style_function is None:
            style_function = lambda x: {}
        self.style_function = style_function

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.geoJson(
                    {% if this.embed %}{{this.style_data()}}{% else %}"{{this.data}}"{% endif %})
                    .addTo({{this._parent.get_name()}});
                {{this.get_name()}}.setStyle(function(feature) {return feature.properties.style;});
            {% endmacro %}
            """)  # noqa

    def style_data(self):
        if 'features' not in self.data.keys():
            # Catch case when GeoJSON is just a single Feature or a geometry.
            if not (isinstance(self.data, dict) and 'geometry' in self.data.keys()):
                # Catch case when GeoJSON is just a geometry.
                self.data = {'type' : 'Feature', 'geometry' : self.data}
            self.data = {'type' : 'FeatureCollection', 'features' : [self.data]}

        for feature in self.data['features']:
            feature.setdefault('properties',{}).setdefault('style',{}).update(
                self.style_function(feature))
        return json.dumps(self.data)

class TopoJson(MacroElement):
    def __init__(self, data, object_path):
        """
        TODO docstring here

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
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"),  # noqa
            name='topojson')

class ColorScale(MacroElement):
    def __init__(self, color_domain, color_code, caption=""):
        """
        TODO docstring here

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
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"),  # noqa
            name='d3')


class MarkerCluster(Layer):
    """Adds a MarkerCluster layer on the map."""
    def __init__(self, overlay=True, control=True):
        """Creates a MarkerCluster element to append into a map with
        Map.add_children.

        Parameters
        ----------
        """
        super(MarkerCluster, self).__init__(overlay=overlay, control=control)
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
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster-src.js"),  # noqa
            name='marker_cluster_src')

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster.js"),  # noqa
            name='marker_cluster')

        figure.header.add_children(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.css"),  # noqa
            name='marker_cluster_css')

        figure.header.add_children(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.Default.css"),  # noqa
            name="marker_cluster_default_css")


class DivIcon(MacroElement):
    def __init__(self, html=None, icon_size=None, icon_anchor=None,
                 popup_anchor=None, class_name='empty'):
        """
        Represents a lightweight icon for markers that uses a simple `div`
        element instead of an image.

        Parameters
        ----------
        icon_size : tuple of 2 int
            Size of the icon image in pixels.
        icon_anchor : tuple of 2 int
            The coordinates of the "tip" of the icon
            (relative to its top left corner).
            The icon will be aligned so that this point is at the
            marker's geographical location.
        popup_anchor : tuple of 2 int
            The coordinates of the point from which popups will "open",
            relative to the icon anchor.
        class_name : string
            A custom class name to assign to the icon.
            Leaflet defaults is 'leaflet-div-icon' which draws a little white
            square with a shadow.  We set it 'empty' in folium.
        html : string
            A custom HTML code to put inside the div element.

        For more information see:
        http://leafletjs.com/reference.html#divicon

        """
        super(DivIcon, self).__init__()
        self._name = 'DivIcon'
        self.icon_size = icon_size
        self.icon_anchor = icon_anchor
        self.popup_anchor = popup_anchor
        self.html = html
        self.className = class_name

        self._template = Template(u"""
            {% macro script(this, kwargs) %}

                var {{this.get_name()}} = L.divIcon({
                    {% if this.icon_size %}iconSize: [{{this.icon_size[0]}},{{this.icon_size[1]}}],{% endif %}
                    {% if this.icon_anchor %}iconAnchor: [{{this.icon_anchor[0]}},{{this.icon_anchor[1]}}],{% endif %}
                    {% if this.popup_anchor %}popupAnchor: [{{this.popup_anchor[0]}},{{this.popup_anchor[1]}}],{% endif %}
                    {% if this.className %}className: '{{this.className}}',{% endif %}
                    {% if this.html %}html: '{{this.html}}',{% endif %}
                    });
                {{this._parent.get_name()}}.setIcon({{this.get_name()}});
            {% endmacro %}
            """)  # noqa


class CircleMarker(Marker):
    def __init__(self, location, radius=500, color='black',
                 fill_color='black', fill_opacity=0.6, popup=None):
        """
        TODO docstring here

        """
        super(CircleMarker, self).__init__(location, popup=popup)
        self._name = 'CircleMarker'
        self.radius = radius
        self.color = color
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity

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
        """
        TODO docstring here

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
            """)  # noqa


class ClickForMarker(MacroElement):
    def __init__(self, popup=None):
        """
        TODO docstring here

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
            """)  # noqa


class PolyLine(MacroElement):
    def __init__(self, locations, color=None, weight=None,
                 opacity=None, latlon=True, popup=None):
        """
        Creates a PolyLine object to append into a map with
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
        popup: string or folium.Popup, default None
            Input text or visualization for object.
        """
        super(PolyLine, self).__init__()
        self._name = 'PolyLine'
        self.data = (_locations_mirror(locations) if not latlon else
                     _locations_tolist(locations))
        self.color = color
        self.weight = weight
        self.opacity = opacity
        if isinstance(popup, text_type) or isinstance(popup, binary_type):
            self.add_children(Popup(popup))
        elif popup is not None:
            self.add_children(popup)

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
            """)  # noqa


class MultiPolyLine(MacroElement):
    def __init__(self, locations, color=None, weight=None,
                 opacity=None, latlon=True, popup=None):
        """
        Creates a MultiPolyLine object to append into a map with
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
        popup: string or folium.Popup, default None
            Input text or visualization for object.
        """
        super(MultiPolyLine, self).__init__()
        self._name = 'MultiPolyLine'
        self.data = (_locations_mirror(locations) if not latlon else
                     _locations_tolist(locations))
        self.color = color
        self.weight = weight
        self.opacity = opacity
        if isinstance(popup, text_type) or isinstance(popup, binary_type):
            self.add_children(Popup(popup))
        elif popup is not None:
            self.add_children(popup)

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
            """)  # noqa

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
            * If file, it's content will be converted as embedded in the
              output file.
            * If array-like, it will be converted to PNG base64 string
              and embedded in the output.
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
            """)  # noqa
