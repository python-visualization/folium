# -*- coding: utf-8 -*-

"""
Map
------

Classes for drawing maps.

"""

from __future__ import unicode_literals

import json
from collections import OrderedDict

from jinja2 import Environment, PackageLoader, Template

from branca.six import text_type, binary_type
from branca.utilities import _parse_size
from branca.element import (Element, Figure, MacroElement, Html,
                            JavascriptLink, CssLink)

ENV = Environment(loader=PackageLoader('folium', 'templates'))

_default_js = [
    ('leaflet',
     'https://unpkg.com/leaflet@1.0.1/dist/leaflet.js'),
    ('jquery',
     'https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js'),
    ('bootstrap',
     'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'),
    ('awesome_markers',
     'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js'),  # noqa
    ('marker_cluster_src',
     'https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.0.0/leaflet.markercluster-src.js'),  # noqa
    ('marker_cluster',
     'https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.0.0/leaflet.markercluster.js'),  # noqa
    ]

_default_css = [
    ('leaflet_css',
     'https://unpkg.com/leaflet@1.0.1/dist/leaflet.css'),
    ('bootstrap_css',
     'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css'),
    ('bootstrap_theme_css',
     'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css'),  # noqa
    ('awesome_markers_font_css',
     'https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css'),  # noqa
    ('awesome_markers_css',
     'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css'),  # noqa
    ('marker_cluster_default_css',
     'https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.0.0/MarkerCluster.Default.css'),  # noqa
    ('marker_cluster_css',
     'https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.0.0/MarkerCluster.css'),  # noqa
    ('awesome_rotate_css',
     'https://rawgit.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css'),  # noqa
    ]


class LegacyMap(MacroElement):
    """Create a Map with Folium and Leaflet.js

    Generate a base map of given width and height with either default
    tilesets or a custom tileset URL. The following tilesets are built-in
    to Folium. Pass any of the following to the "tiles" keyword:

        - "OpenStreetMap"
        - "Mapbox Bright" (Limited levels of zoom for free tiles)
        - "Mapbox Control Room" (Limited levels of zoom for free tiles)
        - "Stamen" (Terrain, Toner, and Watercolor)
        - "Cloudmade" (Must pass API key)
        - "Mapbox" (Must pass API key)
        - "CartoDB" (positron and dark_matter)

    You can pass a custom tileset to Folium by passing a Leaflet-style
    URL to the tiles parameter:
    http://{s}.yourtiles.com/{z}/{x}/{y}.png

    Parameters
    ----------
    location: tuple or list, default None
        Latitude and Longitude of Map (Northing, Easting).
    width: pixel int or percentage string (default: '100%')
        Width of the map.
    height: pixel int or percentage string (default: '100%')
        Height of the map.
    tiles: str, default 'OpenStreetMap'
        Map tileset to use. Can choose from a list of built-in tiles,
        pass a custom URL or pass `None` to create a map without tiles.
    API_key: str, default None
        API key for Cloudmade or Mapbox tiles.
    max_zoom: int, default 18
        Maximum zoom depth for the map.
    zoom_start: int, default 10
        Initial zoom level for the map.
    attr: string, default None
        Map tile attribution; only required if passing custom tile URL.
    detect_retina: bool, default False
        If true and user is on a retina display, it will request four
        tiles of half the specified size and a bigger zoom level in place
        of one to utilize the high resolution.
    crs : str, default 'EPSG3857'
        Defines coordinate reference systems for projecting geographical points
        into pixel (screen) coordinates and back.
        You can use Leaflet's values :
        * EPSG3857 : The most common CRS for online maps, used by almost all
        free and commercial tile providers. Uses Spherical Mercator projection.
        Set in by default in Map's crs option.
        * EPSG4326 : A common CRS among GIS enthusiasts.
        Uses simple Equirectangular projection.
        * EPSG3395 : Rarely used by some commercial tile providers.
        Uses Elliptical Mercator projection.
        * Simple : A simple CRS that maps longitude and latitude into
        x and y directly. May be used for maps of flat surfaces
        (e.g. game maps). Note that the y axis should still be inverted
        (going from bottom to top).
    control_scale : bool, default False
        Whether to add a control scale on the map.
    prefer_canvas : bool, default False
        Forces Leaflet to use the Canvas back-end (if available) for
        vector layers instead of SVG. This can increase performance
        considerably in some cases (e.g. many thousands of circle
        markers on the map).
    no_touch : bool, default False
        Forces Leaflet to not use touch events even if it detects them.
    disable_3d : bool, default False
        Forces Leaflet to not use hardware-accelerated CSS 3D
        transforms for positioning (which may cause glitches in some
        rare environments) even if they're supported.

    Returns
    -------
    Folium LegacyMap Object

    Examples
    --------
    >>> map = folium.LegacyMap(location=[45.523, -122.675],
    ...                        width=750, height=500)
    >>> map = folium.LegacyMap(location=[45.523, -122.675],
    ...                        tiles='Mapbox Control Room')
    >>> map = folium.LegacyMap(location=(45.523, -122.675), max_zoom=20,
    ...                        tiles='Cloudmade', API_key='YourKey')
    >>> map = folium.LegacyMap(location=[45.523, -122.675], zoom_start=2,
    ...                        tiles=('http://{s}.tiles.mapbox.com/v3/'
    ...                               'mapbox.control-room/{z}/{x}/{y}.png'),
    ...                        attr='Mapbox attribution')
    """
    def __init__(self, location=None, width='100%', height='100%',
                 left="0%", top="0%", position='relative',
                 tiles='OpenStreetMap', API_key=None, max_zoom=18, min_zoom=1,
                 zoom_start=10, continuous_world=False, world_copy_jump=False,
                 no_wrap=False, attr=None, min_lat=-90, max_lat=90,
                 min_lon=-180, max_lon=180, max_bounds=True,
                 detect_retina=False, crs='EPSG3857', control_scale=False,
                 prefer_canvas=False, no_touch=False, disable_3d=False):
        super(LegacyMap, self).__init__()
        self._name = 'Map'
        self._env = ENV

        if not location:
            # If location is not passed we center and ignore zoom.
            self.location = [0, 0]
            self.zoom_start = min_zoom
        else:
            self.location = location
            self.zoom_start = zoom_start

        Figure().add_child(self)

        # Map Size Parameters.
        self.width = _parse_size(width)
        self.height = _parse_size(height)
        self.left = _parse_size(left)
        self.top = _parse_size(top)
        self.position = position

        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
        self.max_bounds = max_bounds
        self.continuous_world = continuous_world
        self.no_wrap = no_wrap
        self.world_copy_jump = world_copy_jump

        self.crs = crs
        self.control_scale = control_scale

        self.global_switches = GlobalSwitches(prefer_canvas, no_touch, disable_3d)

        if tiles:
            self.add_tile_layer(
                tiles=tiles, min_zoom=min_zoom, max_zoom=max_zoom,
                continuous_world=continuous_world, no_wrap=no_wrap, attr=attr,
                API_key=API_key, detect_retina=detect_retina
            )

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                position : {{this.position}};
                width : {{this.width[0]}}{{this.width[1]}};
                height: {{this.height[0]}}{{this.height[1]}};
                left: {{this.left[0]}}{{this.left[1]}};
                top: {{this.top[0]}}{{this.top[1]}};
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div class="folium-map" id="{{this.get_name()}}" ></div>
        {% endmacro %}

        {% macro script(this, kwargs) %}

            {% if this.max_bounds %}
                var southWest = L.latLng({{ this.min_lat }}, {{ this.min_lon }});
                var northEast = L.latLng({{ this.max_lat }}, {{ this.max_lon }});
                var bounds = L.latLngBounds(southWest, northEast);
            {% else %}
                var bounds = null;
            {% endif %}

            var {{this.get_name()}} = L.map(
                                  '{{this.get_name()}}',
                                  {center: [{{this.location[0]}},{{this.location[1]}}],
                                  zoom: {{this.zoom_start}},
                                  maxBounds: bounds,
                                  layers: [],
                                  worldCopyJump: {{this.world_copy_jump.__str__().lower()}},
                                  crs: L.CRS.{{this.crs}}
                                 });
            {% if this.control_scale %}L.control.scale().addTo({{this.get_name()}});{% endif %}
        {% endmacro %}
        """)  # noqa

    def _repr_html_(self, **kwargs):
        """Displays the Map in a Jupyter notebook.
        """
        if self._parent is None:
            self.add_to(Figure())
            out = self._parent._repr_html_(**kwargs)
            self._parent = None
        else:
            out = self._parent._repr_html_(**kwargs)
        return out

    def add_tile_layer(self, tiles='OpenStreetMap', name=None,
                       API_key=None, max_zoom=18, min_zoom=1,
                       continuous_world=False, attr=None, active=False,
                       detect_retina=False, no_wrap=False, **kwargs):
        """
        Add a tile layer to the map. See TileLayer for options.

        """
        tile_layer = TileLayer(tiles=tiles, name=name,
                               min_zoom=min_zoom, max_zoom=max_zoom,
                               attr=attr, API_key=API_key,
                               detect_retina=detect_retina,
                               continuous_world=continuous_world,
                               no_wrap=no_wrap)
        self.add_child(tile_layer, name=tile_layer.tile_name)

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        # Set global switches
        figure.header.add_child(self.global_switches, name='global_switches')

        # Import Javascripts
        for name, url in _default_js:
            figure.header.add_child(JavascriptLink(url), name=name)

        # Import Css
        for name, url in _default_css:
            figure.header.add_child(CssLink(url), name=name)

        figure.header.add_child(Element(
            '<style>html, body {'
            'width: 100%;'
            'height: 100%;'
            'margin: 0;'
            'padding: 0;'
            '}'
            '</style>'), name='css_style')

        figure.header.add_child(Element(
            '<style>#map {'
            'position:absolute;'
            'top:0;'
            'bottom:0;'
            'right:0;'
            'left:0;'
            '}'
            '</style>'), name='map_style')

        super(LegacyMap, self).render(**kwargs)


class GlobalSwitches(Element):
    def __init__(self, prefer_canvas=False, no_touch=False, disable_3d=False):
        super(GlobalSwitches, self).__init__()
        self._name = 'GlobalSwitches'

        self.prefer_canvas = prefer_canvas
        self.no_touch = no_touch
        self.disable_3d = disable_3d

        self._template = Template(
            '<script>'
            'L_PREFER_CANVAS = {% if this.prefer_canvas %}true{% else %}false{% endif %}; '
            'L_NO_TOUCH = {% if this.no_touch %}true{% else %}false{% endif %}; '
            'L_DISABLE_3D = {% if this.disable_3d %}true{% else %}false{% endif %};'
            '</script>'
        )


class Layer(MacroElement):
    """An abstract class for everything that is a Layer on the map.
    It will be used to define whether an object will be included in
    LayerControls.

    Parameters
    ----------
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    """
    def __init__(self, name=None, overlay=False, control=True):
        super(Layer, self).__init__()
        self.layer_name = name if name is not None else self.get_name()
        self.overlay = overlay
        self.control = control


class TileLayer(Layer):
    """Create a tile layer to append on a Map.

    Parameters
    ----------
    tiles: str, default 'OpenStreetMap'
        Map tileset to use. Can choose from this list of built-in tiles:
            - "OpenStreetMap"
            - "Mapbox Bright" (Limited levels of zoom for free tiles)
            - "Mapbox Control Room" (Limited levels of zoom for free tiles)
            - "Stamen" (Terrain, Toner, and Watercolor)
            - "Cloudmade" (Must pass API key)
            - "Mapbox" (Must pass API key)
            - "CartoDB" (positron and dark_matter)

        You can pass a custom tileset to Folium by passing a Leaflet-style
        URL to the tiles parameter:
        http://{s}.yourtiles.com/{z}/{x}/{y}.png
    min_zoom: int, default 1
        Minimal zoom for which the layer will be displayed.
    max_zoom: int, default 18
        Maximal zoom for which the layer will be displayed.
    attr: string, default None
        Map tile attribution; only required if passing custom tile URL.
    API_key: str, default None
        API key for Cloudmade or Mapbox tiles.
    detect_retina: bool, default False
        If true and user is on a retina display, it will request four
        tiles of half the specified size and a bigger zoom level in place
        of one to utilize the high resolution.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    """
    def __init__(self, tiles='OpenStreetMap', min_zoom=1, max_zoom=18,
                 attr=None, API_key=None, detect_retina=False,
                 continuous_world=False, name=None, overlay=False,
                 control=True, no_wrap=False):
        self.tile_name = (name if name is not None else
                          ''.join(tiles.lower().strip().split()))
        super(TileLayer, self).__init__(name=self.tile_name, overlay=overlay,
                                        control=control)
        self._name = 'TileLayer'
        self._env = ENV

        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.no_wrap = no_wrap
        self.continuous_world = continuous_world

        self.detect_retina = detect_retina

        self.tiles = ''.join(tiles.lower().strip().split())
        if self.tiles in ('cloudmade', 'mapbox') and not API_key:
            raise ValueError('You must pass an API key if using Cloudmade'
                             ' or non-default Mapbox tiles.')
        templates = list(self._env.list_templates(
            filter_func=lambda x: x.startswith('tiles/')))
        tile_template = 'tiles/'+self.tiles+'/tiles.txt'
        attr_template = 'tiles/'+self.tiles+'/attr.txt'

        if tile_template in templates and attr_template in templates:
            self.tiles = self._env.get_template(tile_template).render(API_key=API_key)  # noqa
            self.attr = self._env.get_template(attr_template).render()
        else:
            self.tiles = tiles
            if not attr:
                raise ValueError('Custom tiles must'
                                 ' also be passed an attribution.')
            if isinstance(attr, binary_type):
                attr = text_type(attr, 'utf8')
            self.attr = attr

        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.tileLayer(
                '{{this.tiles}}',
                {
                    maxZoom: {{this.max_zoom}},
                    minZoom: {{this.min_zoom}},
                    continuousWorld: {{this.continuous_world.__str__().lower()}},
                    noWrap: {{this.no_wrap.__str__().lower()}},
                    attribution: '{{this.attr}}',
                    detectRetina: {{this.detect_retina.__str__().lower()}}
                    }
                ).addTo({{this._parent.get_name()}});

        {% endmacro %}
        """)  # noqa


class FeatureGroup(Layer):
    """
    Create a FeatureGroup layer ; you can put things in it and handle them
    as a single layer.  For example, you can add a LayerControl to
    tick/untick the whole group.

    Parameters
    ----------
    name : str, default None
        The name of the featureGroup layer.
        It will be displayed in the LayerControl.
        If None get_name() will be called to get the technical (ugly) name.
    overlay : bool, default True
        Whether your layer will be an overlay (ticked with a check box in
        LayerControls) or a base layer (ticked with a radio button).
    """
    def __init__(self, name=None, overlay=True, control=True):
        super(FeatureGroup, self).__init__(overlay=overlay, control=control, name=name)  # noqa
        self._name = 'FeatureGroup'

        self.tile_name = name if name is not None else self.get_name()

        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.featureGroup(
                ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)


class LayerControl(MacroElement):
    """
    Creates a LayerControl object to be added on a folium map.

    Parameters
    ----------
    position : str
          The position of the control (one of the map corners), can be
          'topleft', 'topright', 'bottomleft' or 'bottomright'
          default: 'topright'
    collapsed : boolean
          If true the control will be collapsed into an icon and expanded on
          mouse hover or touch.
          default: True
    autoZIndex : boolean
          If true the control assigns zIndexes in increasing order to all of
          its layers so that the order is preserved when switching them on/off.
          default: True
    """
    def __init__(self, position='topright', collapsed=True, autoZIndex=True):
        super(LayerControl, self).__init__()
        self._name = 'LayerControl'
        self.position = position
        self.collapsed = str(collapsed).lower()
        self.autoZIndex = str(autoZIndex).lower()
        self.base_layers = OrderedDict()
        self.overlays = OrderedDict()

        self._template = Template("""
        {% macro script(this,kwargs) %}
            var {{this.get_name()}} = {
                base_layers : { {% for key,val in this.base_layers.items() %}"{{key}}" : {{val}},{% endfor %} },
                overlays : { {% for key,val in this.overlays.items() %}"{{key}}" : {{val}},{% endfor %} }
                };
            L.control.layers(
                {{this.get_name()}}.base_layers,
                {{this.get_name()}}.overlays,
                {position: '{{this.position}}',
                 collapsed: {{this.collapsed}},
                 autoZIndex: {{this.autoZIndex}}
                }).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)  # noqa

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        # We select all Layers for which (control and not overlay).
        self.base_layers = OrderedDict(
            [(val.layer_name, val.get_name()) for key, val in
             self._parent._children.items() if isinstance(val, Layer) and
             (not hasattr(val, 'overlay') or not val.overlay) and
             (not hasattr(val, 'control') or val.control)])
        # We select all Layers for which (control and overlay).
        self.overlays = OrderedDict(
            [(val.layer_name, val.get_name()) for key, val in
             self._parent._children.items() if isinstance(val, Layer) and
             (hasattr(val, 'overlay') and val.overlay) and
             (not hasattr(val, 'control') or val.control)])
        super(LayerControl, self).render()


class Icon(MacroElement):
    """
    Creates an Icon object that will be rendered
    using Leaflet.awesome-markers.

    Parameters
    ----------
    color : str, default 'blue'
        The color of the marker. You can use:

            ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
             'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
             'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
             'gray', 'black', 'lightgray']

    icon_color : str, default 'white'
        The color of the drawing on the marker. You can use colors above,
        or an html color code.
    icon : str, default 'info-sign'
        The name of the marker sign.
        See Font-Awesome website to choose yours.
        Warning : depending on the icon you choose you may need to adapt
        the `prefix` as well.
    angle : int, default 0
        The icon will be rotated by this amount of degrees.
    prefix : str, default 'glyphicon'
        The prefix states the source of the icon. 'fa' for font-awesome or
        'glyphicon' for bootstrap 3.

    For more details see:
    https://github.com/lvoogdt/Leaflet.awesome-markers
    """
    def __init__(self, color='blue', icon_color='white', icon='info-sign',
                 angle=0, prefix='glyphicon'):
        super(Icon, self).__init__()
        self._name = 'Icon'
        self.color = color
        self.icon = icon
        self.icon_color = icon_color
        self.angle = angle
        self.prefix = prefix

        self._template = Template(u"""
            {% macro script(this, kwargs) %}

                var {{this.get_name()}} = L.AwesomeMarkers.icon({
                    icon: '{{this.icon}}',
                    iconColor: '{{this.icon_color}}',
                    markerColor: '{{this.color}}',
                    prefix: '{{this.prefix}}',
                    extraClasses: 'fa-rotate-{{this.angle}}'
                    });
                {{this._parent.get_name()}}.setIcon({{this.get_name()}});
            {% endmacro %}
            """)


class Marker(MacroElement):
    """Create a simple stock Leaflet marker on the map, with optional
    popup text or Vincent visualization.

    Parameters
    ----------
    location: tuple or list, default None
        Latitude and Longitude of Marker (Northing, Easting)
    popup: string or folium.Popup, default None
        Input text or visualization for object.
    icon: Icon plugin
        the Icon plugin to use to render the marker.

    Returns
    -------
    Marker names and HTML in obj.template_vars

    Examples
    --------
    >>> Marker(location=[45.5, -122.3], popup='Portland, OR')
    >>> Marker(location=[45.5, -122.3], popup=folium.Popup('Portland, OR'))
    """
    def __init__(self, location, popup=None, icon=None):
        super(Marker, self).__init__()
        self._name = 'Marker'
        self.location = location
        if icon is not None:
            self.add_child(icon)
        if isinstance(popup, text_type) or isinstance(popup, binary_type):
            self.add_child(Popup(popup))
        elif popup is not None:
            self.add_child(popup)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}

            var {{this.get_name()}} = L.marker(
                [{{this.location[0]}},{{this.location[1]}}],
                {
                    icon: new L.Icon.Default()
                    }
                )
                .addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def _get_self_bounds(self):
        """Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]]
        """
        return [[self.location[0], self.location[1]],
                [self.location[0], self.location[1]]]


class Popup(Element):
    """Create a Popup instance that can be linked to a Layer.

    Parameters
    ----------
    html: string or Element
        Content of the Popup.
    max_width: int, default 300
        The maximal width of the popup.
    """
    def __init__(self, html=None, max_width=300):
        super(Popup, self).__init__()
        self._name = 'Popup'
        self.header = Element()
        self.html = Element()
        self.script = Element()

        self.header._parent = self
        self.html._parent = self
        self.script._parent = self

        if isinstance(html, Element):
            self.html.add_child(html)
        elif isinstance(html, text_type) or isinstance(html, binary_type):
            self.html.add_child(Html(text_type(html)))

        self.max_width = max_width

        self._template = Template(u"""
            var {{this.get_name()}} = L.popup({maxWidth: '{{this.max_width}}'});

            {% for name, element in this.html._children.items() %}
                var {{name}} = $('{{element.render(**kwargs).replace('\\n',' ')}}')[0];
                {{this.get_name()}}.setContent({{name}});
            {% endfor %}

            {{this._parent.get_name()}}.bindPopup({{this.get_name()}});

            {% for name, element in this.script._children.items() %}
                {{element.render()}}
            {% endfor %}
        """)  # noqa

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        for name, child in self._children.items():
            child.render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.script.add_child(Element(
            self._template.render(this=self, kwargs=kwargs)),
            name=self.get_name())


class FitBounds(MacroElement):
    """Fit the map to contain a bounding box with the
    maximum zoom level possible.

    Parameters
    ----------
    bounds: list of (latitude, longitude) points
        Bounding box specified as two points [southwest, northeast]
    padding_top_left: (x, y) point, default None
        Padding in the top left corner. Useful if some elements in
        the corner, such as controls, might obscure objects you're zooming
        to.
    padding_bottom_right: (x, y) point, default None
        Padding in the bottom right corner.
    padding: (x, y) point, default None
        Equivalent to setting both top left and bottom right padding to
        the same value.
    max_zoom: int, default None
        Maximum zoom to be used.
    """
    def __init__(self, bounds, padding_top_left=None,
                 padding_bottom_right=None, padding=None, max_zoom=None):
        super(FitBounds, self).__init__()
        self._name = 'FitBounds'
        self.bounds = json.loads(json.dumps(bounds))
        options = {
            'maxZoom': max_zoom,
            'paddingTopLeft': padding_top_left,
            'paddingBottomRight': padding_bottom_right,
            'padding': padding,
        }
        self.fit_bounds_options = json.dumps({key: val for key, val in
                                              options.items() if val},
                                             sort_keys=True)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                {% if this.autobounds %}
                    var autobounds = L.featureGroup({{ this.features }}).getBounds()
                {% endif %}

                {{this._parent.get_name()}}.fitBounds(
                    {% if this.bounds %}{{ this.bounds }}{% else %}"autobounds"{% endif %},
                    {{ this.fit_bounds_options }}
                    );
            {% endmacro %}
            """)  # noqa
