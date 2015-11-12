# -*- coding: utf-8 -*-
"""
Map
------

Classes for drawing maps.
"""
import warnings
import json
from collections import OrderedDict

from jinja2 import Template

from .six import text_type, binary_type
from .utilities import _parse_size

from .element import Element, Figure, MacroElement, Html

class Map(MacroElement):
    def __init__(self, location=None, width='100%', height='100%',
                 left="0%", top="0%", position='relative',
                 tiles='OpenStreetMap', API_key=None, max_zoom=18, min_zoom=1,
                 zoom_start=10, attr=None, min_lat=-90, max_lat=90,
                 min_lon=-180, max_lon=180, detect_retina=False):
        """Create a Map with Folium and Leaflet.js

        Generate a base map of given width and height with either default
        tilesets or a custom tileset URL. The following tilesets are built-in
        to Folium. Pass any of the following to the "tiles" keyword:
            - "OpenStreetMap"
            - "MapQuest Open"
            - "MapQuest Open Aerial"
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
            Map tileset to use. Can use defaults or pass a custom URL.
        API_key: str, default None
            API key for Cloudmade or Mapbox tiles.
        max_zoom: int, default 18
            Maximum zoom depth for the map.
        zoom_start: int, default 10
            Initial zoom level for the map.
        attr: string, default None
            Map tile attribution; only required if passing custom tile URL.
        detect_retina: bool, default False
            If true and user is on a retina display, it will request four tiles of half the specified
            size and a bigger zoom level in place of one to utilize the high resolution.

        Returns
        -------
        Folium Map Object

        Examples
        --------
        >>>map = folium.Map(location=[45.523, -122.675], width=750, height=500)
        >>>map = folium.Map(location=[45.523, -122.675],
                            tiles='Mapbox Control Room')
        >>>map = folium.Map(location=(45.523, -122.675), max_zoom=20,
                            tiles='Cloudmade', API_key='YourKey')
        >>>map = folium.Map(location=[45.523, -122.675], zoom_start=2,
                            tiles=('http://{s}.tiles.mapbox.com/v3/'
                                    'mapbox.control-room/{z}/{x}/{y}.png'),
                            attr='Mapbox attribution')

        """
        super(Map, self).__init__()
        self._name = 'Map'

        if not location:
            # If location is not passed, we center the map at 0,0 and ignore zoom
            self.location = [0, 0]
            self.zoom_start = min_zoom
        else:
            self.location = location
            self.zoom_start = zoom_start

        Figure().add_children(self)

        # Map Size Parameters.
        self.width  = _parse_size(width)
        self.height = _parse_size(height)
        self.left = _parse_size(left)
        self.top  = _parse_size(top)
        self.position = position

        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon

        self.add_tile_layer(tiles=tiles, min_zoom=min_zoom, max_zoom=max_zoom,
                            attr=attr, API_key=API_key, detect_retina=detect_retina)

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

            var southWest = L.latLng({{ this.min_lat }}, {{ this.min_lon }});
            var northEast = L.latLng({{ this.max_lat }}, {{ this.max_lon }});
            var bounds = L.latLngBounds(southWest, northEast);

            var {{this.get_name()}} = L.map('{{this.get_name()}}', {
                                           center:[{{this.location[0]}},{{this.location[1]}}],
                                           zoom: {{this.zoom_start}},
                                           maxBounds: bounds,
                                           layers: []
                                         });
        {% endmacro %}
        """)

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
                       attr=None, tile_name=None, tile_url=None,
                       active=False, detect_retina=False, **kwargs):
        if tile_name is not None:
            name = tile_name
            warnings.warn("'tile_name' is deprecated. Please use 'name' instead.")
        if tile_url is not None:
            tiles = tile_url
            warnings.warn("'tile_url' is deprecated. Please use 'tiles' instead.")

        tile_layer = TileLayer(tiles=tiles, name=name,
                               min_zoom=min_zoom, max_zoom=max_zoom,
                               attr=attr, API_key=API_key, detect_retina=detect_retina)
        self.add_children(tile_layer, name=tile_layer.tile_name)

class TileLayer(MacroElement):
    def __init__(self, tiles='OpenStreetMap', name=None,
                 min_zoom=1, max_zoom=18, attr=None, API_key=None, overlay = False,
                detect_retina=False):
        """TODO docstring here
        Parameters
        ----------
        """
        super(TileLayer, self).__init__()
        self._name = 'TileLayer'
        self.tile_name = name if name is not None else ''.join(tiles.lower().strip().split())

        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

        self.overlay = overlay
        self.detect_retina = detect_retina

        self.tiles = ''.join(tiles.lower().strip().split())
        if self.tiles in ('cloudmade', 'mapbox') and not API_key:
            raise ValueError('You must pass an API key if using Cloudmade'
                             ' or non-default Mapbox tiles.')
        templates = list(self._env.list_templates(filter_func=lambda x: x.startswith('tiles/')))
        tile_template = 'tiles/'+self.tiles+'/tiles.txt'
        attr_template = 'tiles/'+self.tiles+'/attr.txt'

        if tile_template in templates and attr_template in templates:
            self.tiles = self._env.get_template(tile_template).render(API_key=API_key)
            self.attr  = self._env.get_template(attr_template).render()
        else:
            self.tiles = tiles
            if not attr:
                raise ValueError('Custom tiles must'
                                 ' also be passed an attribution')
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
                    attribution: '{{this.attr}}',
                    detectRetina: {{this.detect_retina.__str__().lower()}}
                    }
                ).addTo({{this._parent.get_name()}});

        {% endmacro %}
        """)

class LayerControl(MacroElement):
    """Adds a layer control to the map."""
    def __init__(self):
        """Creates a LayerControl object to be added on a folium map.

        Parameters
        ----------
        """
        super(LayerControl, self).__init__()
        self._name = 'LayerControl'

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
                {{this.get_name()}}.overlays
                ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)

    def render(self, **kwargs):
        """TODO : docstring here."""
        self.base_layers = OrderedDict([(val.tile_name,val.get_name()) \
                       for key,val in self._parent._children.items() if isinstance(val,TileLayer) and not val.overlay])
        self.overlays = OrderedDict([(val.tile_name,val.get_name()) \
                       for key,val in self._parent._children.items() if isinstance(val,TileLayer) and val.overlay])

        super(LayerControl, self).render()

class Icon(MacroElement):
    def __init__(self, color='blue', icon_color='white', icon='info-sign', angle=0, prefix='glyphicon'):
        """Creates an Icon object, that will be rendered using Leaflet.awesome-markers.

        Parameters
        ----------
        color : str, default 'blue'
            The color of the marker. You can use:
                ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige',
                 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue',
                 'lightgreen', 'gray', 'black', 'lightgray']
        icon_color : str, default 'white'
            The color of the drawing on the marker. You can use colors above, or an html color code.
        icon : str, default 'info-sign'
            The name of the marker sign. See Font-Awesome website to choose yours.
            Warning : depending on the icon you choose, you may need to adapt the `prefix` as well.
        angle : int, default 0
            The icon will be rotated by this amount of degrees.
        prefix : str, default 'glyphicon'
            The prefix states the source of the icon. 'fa' for font-awesome or 'glyphicon' for bootstrap 3.

        For more details, see https://github.com/lvoogdt/Leaflet.awesome-markers
        """
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
        self._name = 'Marker'
        self.location = location
        if icon is not None:
            self.add_children(icon)
        if popup is not None:
            self.add_children(popup)

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

class Popup(Element):
    def __init__(self, html, max_width=300):
        super(Popup, self).__init__()
        self._name = 'Popup'
        self.header = Element()
        self.html   = Element()
        self.script = Element()

        self.header._parent = self
        self.html._parent = self
        self.script._parent = self

        if isinstance(html, Element):
            self.add_children(html)
        elif isinstance(html, text_type) or isinstance(html,binary_type):
            self.html.add_children(Html(text_type(html)))

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
        """)

    def render(self, **kwargs):
        """TODO : docstring here."""
        for name, child in self._children.items():
            child.render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure,Figure), ("You cannot render this Element "
            "if it's not in a Figure.")

        figure.script.add_children(Element(\
            self._template.render(this=self, kwargs=kwargs)), name=self.get_name())

class FitBounds(MacroElement):
    def __init__(self, bounds, padding_top_left=None,
                   padding_bottom_right=None, padding=None, max_zoom=None):
        """Fit the map to contain a bounding box with the maximum zoom level possible.

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
        super(FitBounds, self).__init__()
        self._name = 'FitBounds'
        self.bounds = json.loads(json.dumps(bounds))
        options = {
            'maxZoom': max_zoom,
            'paddingTopLeft': padding_top_left,
            'paddingBottomRight': padding_bottom_right,
            'padding': padding,
        }
        self.fit_bounds_options = json.dumps({key:val for key,val in options.items() if val},
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
            """)
