# -*- coding: utf-8 -*-

"""
Leaflet GeoJson and miscellaneous features.

"""

from __future__ import (absolute_import, division, print_function)

import json
import warnings

from branca.colormap import LinearColormap, StepColormap
from branca.element import (Element, Figure, JavascriptLink, MacroElement)
from branca.utilities import color_brewer

from folium.folium import Map
from folium.map import (FeatureGroup, Icon, Layer, Marker, Tooltip)
from folium.utilities import (
    _iter_tolist,
    _parse_size,
    get_bounds,
    image_to_url,
    none_max,
    none_min,
)
from folium.vector_layers import PolyLine

from jinja2 import Template

import numpy as np

import requests

from six import binary_type, text_type


class RegularPolygonMarker(Marker):
    """
    Custom markers using the Leaflet Data Vis Framework.

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
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.

    https://humangeo.github.io/leaflet-dvf/

    """
    _template = Template(u"""
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
                ).addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def __init__(self, location, color='black', opacity=1, weight=2,
                 fill_color='blue', fill_opacity=1, number_of_sides=4,
                 rotation=0, radius=15, popup=None, tooltip=None):
        super(RegularPolygonMarker, self).__init__(
            _iter_tolist(location),
            popup=popup, tooltip=tooltip
        )
        self._name = 'RegularPolygonMarker'
        self.color = color
        self.opacity = opacity
        self.weight = weight
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.number_of_sides = number_of_sides
        self.rotation = rotation
        self.radius = radius

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        super(RegularPolygonMarker, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet-dvf/0.3.0/leaflet-dvf.markers.min.js'),  # noqa
            name='dvf_js')


class Vega(Element):
    """
    Creates a Vega chart element.

    Parameters
    ----------
    data: JSON-like str or object
        The Vega description of the chart.
        It can also be any object that has a method `to_json`,
        so that you can (for instance) provide a `vincent` chart.
    width: int or str, default None
        The width of the output element.
        If None, either data['width'] (if available) or '100%' will be used.
        Ex: 120, '120px', '80%'
    height: int or str, default None
        The height of the output element.
        If None, either data['width'] (if available) or '100%' will be used.
        Ex: 120, '120px', '80%'
    left: int or str, default '0%'
        The horizontal distance of the output with respect to the parent
        HTML object. Ex: 120, '120px', '80%'
    top: int or str, default '0%'
        The vertical distance of the output with respect to the parent
        HTML object. Ex: 120, '120px', '80%'
    position: str, default 'relative'
        The `position` argument that the CSS shall contain.
        Ex: 'relative', 'absolute'

    """
    _template = Template(u'')

    def __init__(self, data, width=None, height=None,
                 left='0%', top='0%', position='relative'):
        super(Vega, self).__init__()
        self._name = 'Vega'
        self.data = data.to_json() if hasattr(data, 'to_json') else data
        if isinstance(self.data, text_type) or isinstance(data, binary_type):
            self.data = json.loads(self.data)

        # Size Parameters.
        self.width = _parse_size(self.data.get('width', '100%') if
                                 width is None else width)
        self.height = _parse_size(self.data.get('height', '100%') if
                                  height is None else height)
        self.left = _parse_size(left)
        self.top = _parse_size(top)
        self.position = position

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        self.json = json.dumps(self.data)

        self._parent.html.add_child(Element(Template("""
            <div id="{{this.get_name()}}"></div>
            """).render(this=self, kwargs=kwargs)), name=self.get_name())

        self._parent.script.add_child(Element(Template("""
            vega_parse({{this.json}},{{this.get_name()}});
            """).render(this=self)), name=self.get_name())

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(Element(Template("""
            <style> #{{this.get_name()}} {
                position : {{this.position}};
                width : {{this.width[0]}}{{this.width[1]}};
                height: {{this.height[0]}}{{this.height[1]}};
                left: {{this.left[0]}}{{this.left[1]}};
                top: {{this.top[0]}}{{this.top[1]}};
            </style>
            """).render(this=self, **kwargs)), name=self.get_name())

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js'),  # noqa
            name='d3')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/vega/1.4.3/vega.min.js'),  # noqa
            name='vega')

        figure.header.add_child(
            JavascriptLink('https://code.jquery.com/jquery-2.1.0.min.js'),
            name='jquery')

        figure.script.add_child(
            Template("""function vega_parse(spec, div) {
            vg.parse.spec(spec, function(chart) { chart({el:div}).update(); });}"""),  # noqa
            name='vega_parse')


class VegaLite(Element):
    """
    Creates a Vega-Lite chart element.

    Parameters
    ----------
    data: JSON-like str or object
        The Vega-Lite description of the chart.
        It can also be any object that has a method `to_json`,
        so that you can (for instance) provide an `Altair` chart.
    width: int or str, default None
        The width of the output element.
        If None, either data['width'] (if available) or '100%' will be used.
        Ex: 120, '120px', '80%'
    height: int or str, default None
        The height of the output element.
        If None, either data['width'] (if available) or '100%' will be used.
        Ex: 120, '120px', '80%'
    left: int or str, default '0%'
        The horizontal distance of the output with respect to the parent
        HTML object. Ex: 120, '120px', '80%'
    top: int or str, default '0%'
        The vertical distance of the output with respect to the parent
        HTML object. Ex: 120, '120px', '80%'
    position: str, default 'relative'
        The `position` argument that the CSS shall contain.
        Ex: 'relative', 'absolute'

    """
    _template = Template(u'')

    def __init__(self, data, width=None, height=None,
                 left='0%', top='0%', position='relative'):
        super(VegaLite, self).__init__()
        self._name = 'VegaLite'
        self.data = data.to_json() if hasattr(data, 'to_json') else data
        if isinstance(self.data, text_type) or isinstance(data, binary_type):
            self.data = json.loads(self.data)

        # Size Parameters.
        self.width = _parse_size(self.data.get('width', '100%') if
                                 width is None else width)
        self.height = _parse_size(self.data.get('height', '100%') if
                                  height is None else height)
        self.left = _parse_size(left)
        self.top = _parse_size(top)
        self.position = position

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        self.json = json.dumps(self.data)

        self._parent.html.add_child(Element(Template("""
            <div id="{{this.get_name()}}"></div>
            """).render(this=self, kwargs=kwargs)), name=self.get_name())

        self._parent.script.add_child(Element(Template("""
            var embedSpec = {
                mode: "vega-lite",
                spec: {{this.json}}
            };
            vg.embed(
                {{this.get_name()}}, embedSpec, function(error, result) {}
            );
        """).render(this=self)), name=self.get_name())

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(Element(Template("""
            <style> #{{this.get_name()}} {
                position : {{this.position}};
                width : {{this.width[0]}}{{this.width[1]}};
                height: {{this.height[0]}}{{this.height[1]}};
                left: {{this.left[0]}}{{this.left[1]}};
                top: {{this.top[0]}}{{this.top[1]}};
            </style>
            """).render(this=self, **kwargs)), name=self.get_name())

        figure.header.add_child(
            JavascriptLink('https://d3js.org/d3.v3.min.js'),
            name='d3')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/vega/2.6.5/vega.min.js'),  # noqa
            name='vega')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/vega-lite/1.3.1/vega-lite.min.js'),  # noqa
            name='vega-lite')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/vega-embed/2.2.0/vega-embed.min.js'),  # noqa
            name='vega-embed')


class GeoJson(Layer):
    """
    Creates a GeoJson object for plotting into a Map.

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
        Function mapping a GeoJson Feature to a style dict.
    highlight_function: function, default None
        Function mapping a GeoJson Feature to a style dict for mouse events.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    smooth_factor: float, default None
        How much to simplify the polyline on each zoom level. More means
        better performance and smoother look, and less means more accurate
        representation. Leaflet defaults to 1.0.
    tooltip: GeoJsonTooltip, Tooltip or str, default None
        Display a text when hovering over the object. Can utilize the data,
        see folium.GeoJsonTooltip for info on how to do that.

    Examples
    --------
    >>> # Providing file that shall be embedded.
    >>> GeoJson(open('foo.json'))
    >>> # Providing filename that shall not be embedded.
    >>> GeoJson('foo.json')
    >>> # Providing dict.
    >>> GeoJson(json.load(open('foo.json')))
    >>> # Providing string.
    >>> GeoJson(open('foo.json').read())

    >>> # Provide a style_function that color all states green but Alabama.
    >>> style_function = lambda x: {'fillColor': '#0000ff' if
    ...                             x['properties']['name']=='Alabama' else
    ...                             '#00ff00'}
    >>> GeoJson(geojson, style_function=style_function)

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        {% if this.highlight %}
            {{this.get_name()}}_onEachFeature = function onEachFeature(feature, layer) {
                layer.on({
                    mouseout: function(e) {
                        e.target.setStyle(e.target.feature.properties.style);},
                    mouseover: function(e) {
                        e.target.setStyle(e.target.feature.properties.highlight);},
                    click: function(e) {
                        {{this._parent.get_name()}}.fitBounds(e.target.getBounds());}
                    });
            };
        {% endif %}
        var {{this.get_name()}} = L.geoJson(
            {% if this.embed %}{{this.style_data()}}{% else %}"{{this.data}}"{% endif %}
            {% if this.smooth_factor is not none or this.highlight %}
                , {
                {% if this.smooth_factor is not none  %}
                    smoothFactor:{{this.smooth_factor}}
                {% endif %}

                {% if this.highlight %}
                    {% if this.smooth_factor is not none  %}
                    ,
                    {% endif %}
                    onEachFeature: {{this.get_name()}}_onEachFeature
                {% endif %}
                }
            {% endif %}
            ).addTo({{this._parent.get_name()}});
        {{this.get_name()}}.setStyle(function(feature) {return feature.properties.style;});
        {% endmacro %}
        """)  # noqa

    def __init__(self, data, style_function=None, name=None,
                 overlay=True, control=True, show=True,
                 smooth_factor=None, highlight_function=None, tooltip=None):
        super(GeoJson, self).__init__(name=name, overlay=overlay,
                                      control=control, show=show)
        self._name = 'GeoJson'
        if isinstance(data, dict):
            self.embed = True
            self.data = data
        elif isinstance(data, text_type) or isinstance(data, binary_type):
            self.embed = True
            if data.lower().startswith(('http:', 'ftp:', 'https:')):
                self.data = requests.get(data).json()
            elif data.lstrip()[0] in '[{':  # This is a GeoJSON inline string
                self.data = json.loads(data)
            else:  # This is a filename
                with open(data) as f:
                    self.data = json.loads(f.read())
        elif hasattr(data, '__geo_interface__'):
            self.embed = True
            if hasattr(data, 'to_crs'):
                data = data.to_crs(epsg='4326')
            self.data = json.loads(json.dumps(data.__geo_interface__))  # noqa
        else:
            raise ValueError('Unhandled object {!r}.'.format(data))
        self.style_function = style_function or (lambda x: {})

        self.highlight = highlight_function is not None

        self.highlight_function = highlight_function or (lambda x: {})

        self.smooth_factor = smooth_factor

        if isinstance(tooltip, (GeoJsonTooltip, Tooltip)):
            self.add_child(tooltip)
        elif tooltip is not None:
            self.add_child(Tooltip(tooltip))

    def style_data(self):
        """
        Applies `self.style_function` to each feature of `self.data` and
        returns a corresponding JSON output.

        """
        if 'features' not in self.data.keys():
            # Catch case when GeoJSON is just a single Feature or a geometry.
            if not (isinstance(self.data, dict) and 'geometry' in self.data.keys()):  # noqa
                # Catch case when GeoJSON is just a geometry.
                self.data = {'type': 'Feature', 'geometry': self.data}
            self.data = {'type': 'FeatureCollection', 'features': [self.data]}

        for feature in self.data['features']:
            feature.setdefault('properties', {}).setdefault('style', {}).update(self.style_function(feature))  # noqa
            feature.setdefault('properties', {}).setdefault('highlight', {}).update(self.highlight_function(feature))  # noqa
        return json.dumps(self.data, sort_keys=True)

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """
        return get_bounds(self.data, lonlat=True)


class TopoJson(Layer):
    """
    Creates a TopoJson object for plotting into a Map.

    Parameters
    ----------
    data: file, dict or str.
        The TopoJSON data you want to plot.
        * If file, then data will be read in the file and fully
        embedded in Leaflet's JavaScript.
        * If dict, then data will be converted to JSON and embedded
        in the JavaScript.
        * If str, then data will be passed to the JavaScript as-is.
    object_path: str
        The path of the desired object into the TopoJson structure.
        Ex: 'objects.myobject'.
    style_function: function, default None
        A function mapping a TopoJson geometry to a style dict.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    smooth_factor: float, default None
        How much to simplify the polyline on each zoom level. More means
        better performance and smoother look, and less means more accurate
        representation. Leaflet defaults to 1.0.
    tooltip: GeoJsonTooltip, Tooltip or str, default None
        Display a text when hovering over the object. Can utilize the data,
        see folium.GeoJsonTooltip for info on how to do that.

    Examples
    --------
    >>> # Providing file that shall be embeded.
    >>> TopoJson(open('foo.json'), 'object.myobject')
    >>> # Providing filename that shall not be embeded.
    >>> TopoJson('foo.json', 'object.myobject')
    >>> # Providing dict.
    >>> TopoJson(json.load(open('foo.json')), 'object.myobject')
    >>> # Providing string.
    >>> TopoJson(open('foo.json').read(), 'object.myobject')

    >>> # Provide a style_function that color all states green but Alabama.
    >>> style_function = lambda x: {'fillColor': '#0000ff' if
    ...                             x['properties']['name']=='Alabama' else
    ...                             '#00ff00'}
    >>> TopoJson(topo_json, 'object.myobject', style_function=style_function)

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        var {{this.get_name()}}_data = {{this.style_data()}};
        var {{this.get_name()}} = L.geoJson(topojson.feature(
            {{this.get_name()}}_data,
            {{this.get_name()}}_data.{{this.object_path}})
                {% if this.smooth_factor is not none %}
                    , {smoothFactor: {{this.smooth_factor}}}
                {% endif %}
                ).addTo({{this._parent.get_name()}});
        {{this.get_name()}}.setStyle(function(feature) {return feature.properties.style;});
        {% endmacro %}
        """)  # noqa

    def __init__(self, data, object_path, style_function=None,
                 name=None, overlay=True, control=True, show=True,
                 smooth_factor=None, tooltip=None):
        super(TopoJson, self).__init__(name=name, overlay=overlay,
                                       control=control, show=show)
        self._name = 'TopoJson'

        if 'read' in dir(data):
            self.embed = True
            self.data = json.load(data)
        elif type(data) is dict:
            self.embed = True
            self.data = data
        else:
            self.embed = False
            self.data = data

        self.object_path = object_path

        if style_function is None:
            def style_function(x):
                return {}
        self.style_function = style_function

        self.smooth_factor = smooth_factor

        if isinstance(tooltip, (GeoJsonTooltip, Tooltip)):
            self.add_child(tooltip)
        elif tooltip is not None:
            self.add_child(Tooltip(tooltip))

    def style_data(self):
        """
        Applies self.style_function to each feature of self.data and returns
        a corresponding JSON output.

        """
        def recursive_get(data, keys):
            if len(keys):
                return recursive_get(data.get(keys[0]), keys[1:])
            else:
                return data
        geometries = recursive_get(self.data, self.object_path.split('.'))['geometries']  # noqa
        for feature in geometries:
            feature.setdefault('properties', {}).setdefault('style', {}).update(self.style_function(feature))  # noqa
        return json.dumps(self.data, sort_keys=True)

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        super(TopoJson, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js'),  # noqa
            name='topojson')

    def get_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]]

        """
        if not self.embed:
            raise ValueError('Cannot compute bounds of non-embedded TopoJSON.')

        xmin, xmax, ymin, ymax = None, None, None, None

        for arc in self.data['arcs']:
            x, y = 0, 0
            for dx, dy in arc:
                x += dx
                y += dy
                xmin = none_min(x, xmin)
                xmax = none_max(x, xmax)
                ymin = none_min(y, ymin)
                ymax = none_max(y, ymax)
        return [
            [
                self.data['transform']['translate'][1] + self.data['transform']['scale'][1] * ymin,  # noqa
                self.data['transform']['translate'][0] + self.data['transform']['scale'][0] * xmin  # noqa
            ],
            [
                self.data['transform']['translate'][1] + self.data['transform']['scale'][1] * ymax,  # noqa
                self.data['transform']['translate'][0] + self.data['transform']['scale'][0] * xmax  # noqa
            ]
        ]


class GeoJsonTooltip(Tooltip):
    """
    Create a tooltip that uses data from either geojson or topojson.

    Parameters
    ----------
    fields: list or tuple.
        Labels of GeoJson/TopoJson 'properties' or GeoPandas GeoDataFrame
        columns you'd like to display.
    aliases: list/tuple of strings, same length/order as fields, default None.
        Optional aliases you'd like to display in the tooltip as field name
        instead of the keys of `fields`.
    labels: bool, default True.
        Set to False to disable displaying the field names or aliases.
    localize: bool, default False.
        This will use JavaScript's .toLocaleString() to format 'clean' values
        as strings for the user's location; i.e. 1,000,000.00 comma separators,
        float truncation, etc.
        *Available for most of JavaScript's primitive types (any data you'll
        serve into the template).
    style: str, default None.
        HTML inline style properties like font and colors. Will be applied to
        a div with the text in it.
    sticky: bool, default True
        Whether the tooltip should follow the mouse.
    **kwargs: Assorted.
        These values will map directly to the Leaflet Options. More info
        available here: https://leafletjs.com/reference-1.2.0#tooltip

    Examples
    --------
    # Provide fields and aliases, with Style.
    >>> Tooltip(
    >>>     fields=['CNTY_NM', 'census-pop-2015', 'census-md-income-2015'],
    >>>     aliases=['County', '2015 Census Population', '2015 Median Income'],
    >>>     localize=True,
    >>>     style=('background-color: grey; color: white; font-family:'
    >>>            'courier new; font-size: 24px; padding: 10px;')
    >>> )
    # Provide fields, with labels off and fixed tooltip positions.
    >>> Tooltip(fields=('CNTY_NM',), labels=False, sticky=False)
    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        {{ this._parent.get_name() }}.bindTooltip(
            function(layer){
            // Convert non-primitive to String.
            let handleObject = (feature)=>typeof(feature)=='object' ? JSON.stringify(feature) : feature;
            let fields = {{ this.fields }};
            {% if this.aliases %}
            let aliases = {{ this.aliases }};
            {% endif %}
            return '<table{% if this.style %} style="{{this.style}}"{% endif%}>' +
            String(
                fields.map(
                columnname=>
                    `<tr style="text-align: left;">{% if this.labels %}
                    <th style="padding: 4px; padding-right: 10px;">{% if this.aliases %}
                        ${aliases[fields.indexOf(columnname)]
                        {% if this.localize %}.toLocaleString(){% endif %}}
                    {% else %}
                    ${ columnname{% if this.localize %}.toLocaleString(){% endif %}}
                    {% endif %}</th>
                    {% endif %}
                    <td style="padding: 4px;">${handleObject(layer.feature.properties[columnname])
                    {% if this.localize %}.toLocaleString(){% endif %}}</td></tr>`
                ).join(''))
                +'</table>'
            }, {{ this.options }});
        {% endmacro %}
        """)

    def __init__(self, fields, aliases=None, labels=True,
                 localize=False, style=None, sticky=True, **kwargs):
        super(GeoJsonTooltip, self).__init__(
            text='', style=style, sticky=sticky, **kwargs
        )
        self._name = 'GeoJsonTooltip'

        assert isinstance(fields, (list, tuple)), 'Please pass a list or ' \
                                                  'tuple to fields.'
        if aliases is not None:
            assert isinstance(aliases, (list, tuple))
            assert len(fields) == len(aliases), 'fields and aliases must have' \
                                                ' the same length.'
        assert isinstance(labels, bool), 'labels requires a boolean value.'
        assert isinstance(localize, bool), 'localize must be bool.'
        assert 'permanent' not in kwargs,  'The `permanent` option does not ' \
                                           'work with GeoJsonTooltip.'

        self.fields = fields
        self.aliases = aliases
        self.labels = labels
        self.localize = localize
        if style:
            assert isinstance(style, str), \
                'Pass a valid inline HTML style property string to style.'
            # noqa outside of type checking.
            self.style = style

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        if isinstance(self._parent, GeoJson):
            keys = tuple(self._parent.data['features'][0]['properties'].keys())
        elif isinstance(self._parent, TopoJson):
            obj_name = self._parent.object_path.split('.')[-1]
            keys = tuple(self._parent.data['objects'][obj_name][
                             'geometries'][0]['properties'].keys())
        else:
            raise TypeError('You cannot add a GeoJsonTooltip to anything else '
                            'than a GeoJson or TopoJson object.')
        keys = tuple(x for x in keys if x not in ('style', 'highlight'))
        for value in self.fields:
            assert value in keys, ('The field {} is not available in the data. '
                                   'Choose from: {}.'.format(value, keys))
        super(GeoJsonTooltip, self).render(**kwargs)


class Choropleth(FeatureGroup):
    """Apply a GeoJSON overlay to the map.

    Plot a GeoJSON overlay on the base map. There is no requirement
    to bind data (passing just a GeoJSON plots a single-color overlay),
    but there is a data binding option to map your columnar data to
    different feature objects with a color scale.

    If data is passed as a Pandas DataFrame, the "columns" and "key-on"
    keywords must be included, the first to indicate which DataFrame
    columns to use, the second to indicate the layer in the GeoJSON
    on which to key the data. The 'columns' keyword does not need to be
    passed for a Pandas series.

    Colors are generated from color brewer (http://colorbrewer2.org/)
    sequential palettes. By default, linear binning is used between
    the min and the max of the values. Custom binning can be achieved
    with the `bins` parameter.

    TopoJSONs can be passed as "geo_data", but the "topojson" keyword must
    also be passed with the reference to the topojson objects to convert.
    See the topojson.feature method in the TopoJSON API reference:
    https://github.com/topojson/topojson/wiki/API-Reference


    Parameters
    ----------
    geo_data: string/object
        URL, file path, or data (json, dict, geopandas, etc) to your GeoJSON
        geometries
    data: Pandas DataFrame or Series, default None
        Data to bind to the GeoJSON.
    columns: dict or tuple, default None
        If the data is a Pandas DataFrame, the columns of data to be bound.
        Must pass column 1 as the key, and column 2 the values.
    key_on: string, default None
        Variable in the `geo_data` GeoJSON file to bind the data to. Must
        start with 'feature' and be in JavaScript objection notation.
        Ex: 'feature.id' or 'feature.properties.statename'.
    bins: int or sequence of scalars or str, default 6
        If `bins` is an int, it defines the number of equal-width
        bins between the min and the max of the values.
        If `bins` is a sequence, it directly defines the bin edges.
        For more information on this parameter, have a look at
        numpy.histogram function.
    fill_color: string, default 'blue'
        Area fill color. Can pass a hex code, color name, or if you are
        binding data, one of the following color brewer palettes:
        'BuGn', 'BuPu', 'GnBu', 'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'RdPu',
        'YlGn', 'YlGnBu', 'YlOrBr', and 'YlOrRd'.
    nan_fill_color: string, default 'black'
        Area fill color for nan or missing values.
        Can pass a hex code, color name.
    fill_opacity: float, default 0.6
        Area fill opacity, range 0-1.
    nan_fill_opacity: float, default fill_opacity
        Area fill opacity for nan or missing values, range 0-1.
    line_color: string, default 'black'
        GeoJSON geopath line color.
    line_weight: int, default 1
        GeoJSON geopath line weight.
    line_opacity: float, default 1
        GeoJSON geopath line opacity, range 0-1.
    legend_name: string, default empty string
        Title for data legend.
    topojson: string, default None
        If using a TopoJSON, passing "objects.yourfeature" to the topojson
        keyword argument will enable conversion to GeoJSON.
    smooth_factor: float, default None
        How much to simplify the polyline on each zoom level. More means
        better performance and smoother look, and less means more accurate
        representation. Leaflet defaults to 1.0.
    highlight: boolean, default False
        Enable highlight functionality when hovering over a GeoJSON area.
    name : string, optional
        The name of the layer, as it will appear in LayerControls
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).

    Returns
    -------
    GeoJSON data layer in obj.template_vars

    Examples
    --------
    >>> Choropleth(geo_data='us-states.json', line_color='blue',
    ...            line_weight=3)
    >>> Choropleth(geo_data='geo.json', data=df,
    ...            columns=['Data 1', 'Data 2'],
    ...            key_on='feature.properties.myvalue',
    ...            fill_color='PuBu',
    ...            bins=[0, 20, 30, 40, 50, 60])
    >>> Choropleth(geo_data='countries.json',
    ...            topojson='objects.countries')
    >>> Choropleth(geo_data='geo.json', data=df,
    ...            columns=['Data 1', 'Data 2'],
    ...            key_on='feature.properties.myvalue',
    ...            fill_color='PuBu',
    ...            bins=[0, 20, 30, 40, 50, 60],
    ...            highlight=True)
    """

    def __init__(self, geo_data, data=None, columns=None, key_on=None,    # noqa
                 bins=6, fill_color='blue', nan_fill_color='black',
                 fill_opacity=0.6, nan_fill_opacity=None, line_color='black',
                 line_weight=1, line_opacity=1, name=None, legend_name='',
                 overlay=True, control=True, show=True,
                 topojson=None, smooth_factor=None, highlight=None,
                 **kwargs):
        super(Choropleth, self).__init__(name=name, overlay=overlay,
                                         control=control, show=show)
        self._name = 'Choropleth'

        if data is not None and not color_brewer(fill_color):
            raise ValueError('Please pass a valid color brewer code to '
                             'fill_local. See docstring for valid codes.')

        if nan_fill_opacity is None:
            nan_fill_opacity = fill_opacity

        if 'threshold_scale' in kwargs:
            if kwargs['threshold_scale'] is not None:
                bins = kwargs['threshold_scale']
            warnings.warn(
                'choropleth `threshold_scale` parameter is now depreciated '
                'in favor of the `bins` parameter.', DeprecationWarning)

        # Create color_data dict
        if hasattr(data, 'set_index'):
            # This is a pd.DataFrame
            color_data = data.set_index(columns[0])[columns[1]].to_dict()
        elif hasattr(data, 'to_dict'):
            # This is a pd.Series
            color_data = data.to_dict()
        elif data:
            color_data = dict(data)
        else:
            color_data = None

        self.color_scale = None

        if color_data is not None and key_on is not None:
            real_values = np.array(list(color_data.values()))
            real_values = real_values[~np.isnan(real_values)]
            _, bin_edges = np.histogram(real_values, bins=bins)

            bins_min, bins_max = min(bin_edges), max(bin_edges)
            if np.any((real_values < bins_min) | (real_values > bins_max)):
                raise ValueError(
                    'All values are expected to fall into one of the provided '
                    'bins (or to be Nan). Please check the `bins` parameter '
                    'and/or your data.')

            # We add the colorscale
            nb_bins = len(bin_edges) - 1
            color_range = color_brewer(fill_color, n=nb_bins)
            self.color_scale = StepColormap(
                color_range,
                index=bin_edges,
                vmin=bins_min,
                vmax=bins_max,
                caption=legend_name)

            # then we 'correct' the last edge for numpy digitize
            # (we add a very small amount to fake an inclusive right interval)
            increasing = bin_edges[0] <= bin_edges[-1]
            bin_edges[-1] = np.nextafter(
                bin_edges[-1],
                (1 if increasing else -1) * np.inf)

            key_on = key_on[8:] if key_on.startswith('feature.') else key_on

            def get_by_key(obj, key):
                return (obj.get(key, None) if len(key.split('.')) <= 1 else
                        get_by_key(obj.get(key.split('.')[0], None),
                                   '.'.join(key.split('.')[1:])))

            def color_scale_fun(x):
                key_of_x = get_by_key(x, key_on)

                if key_of_x not in color_data.keys():
                    return nan_fill_color, nan_fill_opacity

                value_of_x = color_data[key_of_x]
                if np.isnan(value_of_x):
                    return nan_fill_color, nan_fill_opacity

                color_idx = np.digitize(value_of_x, bin_edges, right=False) - 1
                return color_range[color_idx], fill_opacity

        else:
            def color_scale_fun(x):
                return fill_color, fill_opacity

        def style_function(x):
            color, opacity = color_scale_fun(x)
            return {
                'weight': line_weight,
                'opacity': line_opacity,
                'color': line_color,
                'fillOpacity': opacity,
                'fillColor': color
            }

        def highlight_function(x):
            return {
                'weight': line_weight + 2,
                'fillOpacity': fill_opacity + .2
            }

        if topojson:
            self.geojson = TopoJson(
                geo_data,
                topojson,
                style_function=style_function,
                smooth_factor=smooth_factor)
        else:
            self.geojson = GeoJson(
                geo_data,
                style_function=style_function,
                smooth_factor=smooth_factor,
                highlight_function=highlight_function if highlight else None)

        self.add_child(self.geojson)
        if self.color_scale:
            self.add_child(self.color_scale)

    def render(self, **kwargs):
        """Render the GeoJson/TopoJson and color scale objects."""
        if self.color_scale:
            # ColorMap needs Map as its parent
            assert isinstance(self._parent, Map), ('Choropleth must be added'
                                                   ' to a Map object.')
            self.color_scale._parent = self._parent

        super(Choropleth, self).render(**kwargs)


class DivIcon(MacroElement):
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


    http://leafletjs.com/reference-1.2.0.html#divicon

    """
    _template = Template(u"""
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

    def __init__(self, html=None, icon_size=None, icon_anchor=None,
                 popup_anchor=None, class_name='empty'):
        super(DivIcon, self).__init__()
        self._name = 'DivIcon'
        self.icon_size = icon_size
        self.icon_anchor = icon_anchor
        self.popup_anchor = popup_anchor
        self.html = html
        self.className = class_name


class LatLngPopup(MacroElement):
    """
    When one clicks on a Map that contains a LatLngPopup,
    a popup is shown that displays the latitude and longitude of the pointer.

    """
    _template = Template(u"""
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

    def __init__(self):
        super(LatLngPopup, self).__init__()
        self._name = 'LatLngPopup'


class ClickForMarker(MacroElement):
    """
    When one clicks on a Map that contains a ClickForMarker,
    a Marker is created at the pointer's position.

    Parameters
    ----------
    popup: str, default None
        Text to display in the markers' popups.
        If None, the popups will display the marker's latitude and longitude.

    """
    _template = Template(u"""
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

    def __init__(self, popup=None):
        super(ClickForMarker, self).__init__()
        self._name = 'ClickForMarker'

        if popup:
            self.popup = ''.join(['"', popup, '"'])
        else:
            self.popup = '"Latitude: " + lat + "<br>Longitude: " + lng '


class CustomIcon(Icon):
    """
    Create a custom icon, based on an image.

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
    _template = Template(u"""
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

    def __init__(self, icon_image, icon_size=None, icon_anchor=None,
                 shadow_image=None, shadow_size=None, shadow_anchor=None,
                 popup_anchor=None):
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


class ColorLine(FeatureGroup):
    """
    Draw data on a map with specified colors.

    Parameters
    ----------
    positions: tuple or list
        The list of points latitude and longitude
    colors: tuple or list
        The list of segments colors.
        It must have length equal to `len(positions)-1`.
    colormap: branca.colormap.Colormap or list or tuple
        The colormap to use. If a list or tuple of colors is provided,
        a LinearColormap will be created from it.
    nb_steps: int, default 12
        To have lighter output the colormap will be discretized
        to that number of colors.
    opacity: float, default 1
        Line opacity, scale 0-1
    weight: int, default 2
        Stroke weight in pixels
    **kwargs
        Further parameters available. See folium.map.FeatureGroup

    Returns
    -------
    A ColorLine object that you can `add_to` a Map.

    """
    def __init__(self, positions, colors, colormap=None, nb_steps=12,
                 weight=None, opacity=None, **kwargs):
        super(ColorLine, self).__init__(**kwargs)
        self._name = 'ColorLine'

        if colormap is None:
            cm = LinearColormap(['green', 'yellow', 'red'],
                                vmin=min(colors),
                                vmax=max(colors),
                                ).to_step(nb_steps)
        elif isinstance(colormap, LinearColormap):
            cm = colormap.to_step(nb_steps)
        elif isinstance(colormap, list) or isinstance(colormap, tuple):
            cm = LinearColormap(colormap,
                                vmin=min(colors),
                                vmax=max(colors),
                                ).to_step(nb_steps)
        else:
            cm = colormap
        out = {}
        for (lat1, lng1), (lat2, lng2), color in zip(positions[:-1], positions[1:], colors):  # noqa
            out.setdefault(cm(color), []).append([[lat1, lng1], [lat2, lng2]])
        for key, val in out.items():
            self.add_child(PolyLine(val, color=key, weight=weight, opacity=opacity))  # noqa
