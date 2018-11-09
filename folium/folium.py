# -*- coding: utf-8 -*-

"""
Make beautiful, interactive maps with Python and Leaflet.js

"""

from __future__ import (absolute_import, division, print_function)

import os
import time
import warnings

from branca.element import CssLink, Element, Figure, JavascriptLink, MacroElement

from folium.map import FitBounds
from folium.raster_layers import TileLayer
from folium.utilities import _parse_size, _validate_location

from jinja2 import Environment, PackageLoader, Template

ENV = Environment(loader=PackageLoader('folium', 'templates'))


_default_js = [
    ('leaflet',
     'https://cdn.jsdelivr.net/npm/leaflet@1.3.4/dist/leaflet.js'),
    ('jquery',
     'https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js'),
    ('bootstrap',
     'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'),
    ('awesome_markers',
     'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js'),  # noqa
    ]

_default_css = [
    ('leaflet_css',
     'https://cdn.jsdelivr.net/npm/leaflet@1.3.4/dist/leaflet.css'),
    ('bootstrap_css',
     'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css'),
    ('bootstrap_theme_css',
     'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css'),  # noqa
    ('awesome_markers_font_css',
     'https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css'),  # noqa
    ('awesome_markers_css',
     'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css'),  # noqa
    ('awesome_rotate_css',
     'https://rawcdn.githack.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css'),  # noqa
    ]


class GlobalSwitches(Element):

    _template = Template(
        '<script>'
        'L_PREFER_CANVAS={% if this.prefer_canvas %}true{% else %}false{% endif %}; '
        'L_NO_TOUCH={% if this.no_touch %}true{% else %}false{% endif %}; '
        'L_DISABLE_3D={% if this.disable_3d %}true{% else %}false{% endif %};'
        '</script>'
    )

    def __init__(self, prefer_canvas=False, no_touch=False, disable_3d=False):
        super(GlobalSwitches, self).__init__()
        self._name = 'GlobalSwitches'

        self.prefer_canvas = prefer_canvas
        self.no_touch = no_touch
        self.disable_3d = disable_3d


class Map(MacroElement):
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
    URL to the tiles parameter: ``http://{s}.yourtiles.com/{z}/{x}/{y}.png``

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
    min_zoom: int, default 0
        Minimum allowed zoom level for the tile layer that is created.
    max_zoom: int, default 18
        Maximum allowed zoom level for the tile layer that is created.
    max_native_zoom: int, default None
        The highest zoom level at which the tile server can provide tiles.
        If provided you can zoom in past this level. Else tiles will turn grey.
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
    zoom_control : bool, default True
        Display zoom controls on the map.

    Returns
    -------
    Folium Map Object

    Examples
    --------
    >>> map = folium.Map(location=[45.523, -122.675],
    ...                        width=750, height=500)
    >>> map = folium.Map(location=[45.523, -122.675],
                               tiles='Mapbox Control Room')
    >>> map = folium.Map(location=(45.523, -122.675), max_zoom=20,
                               tiles='Cloudmade', API_key='YourKey')
    >>> map = folium.Map(
    ...    location=[45.523, -122.675],
    ...    zoom_start=2,
    ...    tiles='http://{s}.tiles.mapbox.com/v3/mapbox.control-room/{z}/{x}/{y}.png',
    ...    attr='Mapbox attribution'
    ...)

    """
    _template = Template(u"""
{% macro header(this, kwargs) %}
    <meta name="viewport" content="width=device-width,
        initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <style>#{{this.get_name()}} {
        position: {{this.position}};
        width: {{this.width[0]}}{{this.width[1]}};
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
        '{{this.get_name()}}', {
        center: [{{this.location[0]}}, {{this.location[1]}}],
        zoom: {{this.zoom_start}},
        maxBounds: bounds,
        layers: [],
        worldCopyJump: {{this.world_copy_jump.__str__().lower()}},
        crs: L.CRS.{{this.crs}},
        zoomControl: {{this.zoom_control.__str__().lower()}},
        });
{% if this.control_scale %}L.control.scale().addTo({{this.get_name()}});{% endif %}
    
    {% if this.objects_to_stay_in_front %}
    function objects_in_front() {
        {% for obj in this.objects_to_stay_in_front %}    
            {{ obj.get_name() }}.bringToFront();
        {% endfor %}
    };

{{ this.get_name() }}.on("overlayadd", objects_in_front);
$(document).ready(objects_in_front);
{% endif %}
{% endmacro %}
""")  # noqa

    def __init__(self, location=None, width='100%', height='100%',
                 left='0%', top='0%', position='relative',
                 tiles='OpenStreetMap', API_key=None, max_zoom=18, min_zoom=0,
                 max_native_zoom=None, zoom_start=10, world_copy_jump=False,
                 no_wrap=False, attr=None, min_lat=-90, max_lat=90,
                 min_lon=-180, max_lon=180, max_bounds=False,
                 detect_retina=False, crs='EPSG3857', control_scale=False,
                 prefer_canvas=False, no_touch=False, disable_3d=False,
                 subdomains='abc', png_enabled=False, zoom_control=True):
        super(Map, self).__init__()
        self._name = 'Map'
        self._env = ENV
        # Undocumented for now b/c this will be subject to a re-factor soon.
        self._png_image = None
        self.png_enabled = png_enabled

        if not location:
            # If location is not passed we center and zoom out.
            self.location = [0, 0]
            self.zoom_start = 1
        else:
            self.location = _validate_location(location)
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
        self.no_wrap = no_wrap
        self.world_copy_jump = world_copy_jump

        self.crs = crs
        self.control_scale = control_scale
        self.zoom_control = zoom_control

        self.global_switches = GlobalSwitches(
            prefer_canvas,
            no_touch,
            disable_3d
        )

        self.objects_to_stay_in_front = []

        if tiles:
            self.add_tile_layer(
                tiles=tiles, min_zoom=min_zoom, max_zoom=max_zoom,
                max_native_zoom=max_native_zoom, no_wrap=no_wrap, attr=attr,
                API_key=API_key, detect_retina=detect_retina,
                subdomains=subdomains
            )

    def _repr_html_(self, **kwargs):
        """Displays the HTML Map in a Jupyter notebook."""
        if self._parent is None:
            self.add_to(Figure())
            out = self._parent._repr_html_(**kwargs)
            self._parent = None
        else:
            out = self._parent._repr_html_(**kwargs)
        return out

    def _to_png(self, delay=3):
        """Export the HTML to byte representation of a PNG image.

        Uses Phantom JS to render the HTML and record a PNG. You may need to
        adjust the `delay` time keyword argument if maps render without data or tiles.

        Examples
        --------
        >>> map._to_png()
        >>> map._to_png(time=10)  # Wait 10 seconds between render and snapshot.
        """

        if self._png_image is None:
            import selenium.webdriver

            driver = selenium.webdriver.PhantomJS(
                service_log_path=os.path.devnull
            )
            driver.get('about:blank')
            html = self.get_root().render()
            html = html.replace('\'', '"').replace('"', '\\"')
            html = html.replace('\n', '')
            driver.execute_script('document.write(\"{}\")'.format(html))
            driver.maximize_window()
            # Ignore user map size.
            # todo: fix this
            # driver.execute_script("document.body.style.width = '100%';")  # noqa
            # We should probably monitor if some element is present,
            # but this is OK for now.
            time.sleep(delay)
            png = driver.get_screenshot_as_png()
            driver.quit()
            self._png_image = png
        return self._png_image

    def _repr_png_(self):
        """Displays the PNG Map in a Jupyter notebook."""
        # The notebook calls all _repr_*_ by default.
        # We don't want that here b/c this one is quite slow.
        if not self.png_enabled:
            return None
        return self._to_png()

    def add_tile_layer(self, tiles='OpenStreetMap', name=None,
                       API_key=None, max_zoom=18, min_zoom=0,
                       max_native_zoom=None, attr=None, active=False,
                       detect_retina=False, no_wrap=False, subdomains='abc',
                       **kwargs):
        """
        Add a tile layer to the map. See TileLayer for options.

        """
        tile_layer = TileLayer(tiles=tiles, name=name,
                               min_zoom=min_zoom, max_zoom=max_zoom,
                               max_native_zoom=max_native_zoom,
                               attr=attr, API_key=API_key,
                               detect_retina=detect_retina,
                               subdomains=subdomains,
                               no_wrap=no_wrap)
        self.add_child(tile_layer, name=tile_layer.tile_name)

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

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

        super(Map, self).render(**kwargs)

    def fit_bounds(self, bounds, padding_top_left=None,
                   padding_bottom_right=None, padding=None, max_zoom=None):
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

        Examples
        --------
        >>> map.fit_bounds([[52.193636, -2.221575], [52.636878, -1.139759]])

        """
        self.add_child(FitBounds(bounds,
                                 padding_top_left=padding_top_left,
                                 padding_bottom_right=padding_bottom_right,
                                 padding=padding,
                                 max_zoom=max_zoom,
                                 )
                       )

    def choropleth(self, *args, **kwargs):
        """Call the Choropleth class with the same arguments.

        This method may be deleted after a year from now (Nov 2018).
        """
        warnings.warn(
            'The choropleth  method has been deprecated. Instead use the new '
            'Choropleth class, which has the same arguments. See the example '
            'notebook \'GeoJSON_and_choropleth\' for how to do this.',
            FutureWarning
        )
        from folium.features import Choropleth
        self.add_child(Choropleth(*args, **kwargs))

    def keep_in_front(self, *args):
        """Pass one or multiples object that must stay in front.

        The ordering matters, the last one is put on top.

        Parameters
        ----------
        *args :
            Variable length argument list. Any folium object that counts as an
            overlay. For example FeatureGroup or a vector object such as Marker.
        """
        for obj in args:
            self.objects_to_stay_in_front.append(obj)
