# -*- coding: utf-8 -*-
"""
Folium
-------

Make beautiful, interactive maps with Python and Leaflet.js

"""

from __future__ import absolute_import

import warnings
import json

from folium.six import text_type, binary_type
from .map import LegacyMap, Icon, Marker, Popup, FitBounds
from .features import (WmsTileLayer, RegularPolygonMarker, Vega, GeoJson,
                       CircleMarker, LatLngPopup,
                       ClickForMarker, TopoJson, PolyLine, MultiPolyLine,
                       )
from .colormap import StepColormap
from .utilities import color_brewer


def initialize_notebook():
    """Initialize the IPython notebook display elements."""
    warnings.warn("%s is deprecated and no longer required." %
                  ("initialize_notebook",),
                  FutureWarning, stacklevel=2)
    pass


class Map(LegacyMap):
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

    Returns
    -------
    Folium LegacyMap Object

    Examples
    --------
    >>> map = folium.LegacyMap(location=[45.523, -122.675],
    ...                        width=750, height=500)
    >>> map = folium.LegacyMap(location=[45.523, -122.675],
                               tiles='Mapbox Control Room')
    >>> map = folium.LegacyMap(location=(45.523, -122.675), max_zoom=20,
                               tiles='Cloudmade', API_key='YourKey')
    >>> map = folium.LegacyMap(location=[45.523, -122.675], zoom_start=2,
                               tiles=('http://{s}.tiles.mapbox.com/v3/'
                                      'mapbox.control-room/{z}/{x}/{y}.png'),
                                attr='Mapbox attribution')
    """
    def create_map(self, path='map.html', plugin_data_out=True, template=None):
        """Write Map output to HTML.

        Parameters
        ----------
        path: string, default 'map.html'
            Path for HTML output for map
        plugin_data_out: boolean, default True
            Deprecated, not used anymore
        template: string, default None
            Deprecated, not used anymore
        """
        warnings.warn("%s is deprecated. Use %s instead" % ("Map.create_map",
                                                            "Map.save"),
                      FutureWarning, stacklevel=2)
        self.save(path)

    def add_wms_layer(self, wms_name=None, wms_url=None, wms_format=None,
                      wms_layers=None, wms_transparent=True):
        """Adds a simple tile layer.

        Parameters
        ----------
        wms_name: string
            name of wms layer
        wms_url : string
            url of wms layer
        """
        warnings.warn("%s is deprecated. Use %s instead" %
                      ("Map.add_wms_layer",
                       "Map.add_children(WmsTileLayer(...))"),
                      FutureWarning, stacklevel=2)
        wms = WmsTileLayer(wms_url, name=wms_name, format=wms_format,
                           layers=wms_layers, transparent=wms_transparent,
                           attr=None)
        self.add_children(wms, name=wms_name)

    def simple_marker(self, location=None, popup=None,
                      marker_color='blue', marker_icon='info-sign',
                      clustered_marker=False, icon_angle=0, popup_width=300):
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
        marker_color
            color of marker you want
        marker_icon
            icon from (http://getbootstrap.com/components/) you want on the
            marker
        clustered_marker
            boolean of whether or not you want the marker clustered with
            other markers

        Returns
        -------
        Marker names and HTML in obj.template_vars

        Examples
        --------
        >>> map.simple_marker(location=[45.5, -122.3], popup='Portland, OR')
        >>> map.simple_marker(location=[45.5, -122.3], popup=(vis, 'vis.json'))

        """
        warnings.warn("%s is deprecated. Use %s instead" %
                      ("simple_marker", "add_children(Marker)"),
                      FutureWarning, stacklevel=2)
        if clustered_marker:
            raise ValueError("%s is deprecated. Use %s instead" %
                             ("clustered_marker", "MarkerCluster"))
        if isinstance(popup, text_type) or isinstance(popup, binary_type):
            popup_ = Popup(popup, max_width=popup_width)
        elif isinstance(popup, tuple):
            popup_ = Popup(max_width=popup_width)
            Vega(
                json.loads(popup[0].to_json()),
                width="100%",
                height="100%",
                ).add_to(popup_)
        else:
            popup_ = None
        marker = Marker(location,
                        popup=popup_,
                        icon=Icon(color=marker_color,
                                  icon=marker_icon,
                                  angle=icon_angle))
        self.add_children(marker)

    def line(self, locations,
             line_color=None, line_opacity=None, line_weight=None,
             popup=None, popup_width=300, latlon=True):
        """Add a line to the map with optional styles.

        Parameters
        ----------
        locations: list of points (latitude, longitude)
            Latitude and Longitude of line (Northing, Easting)
        line_color: string, default Leaflet's default ('#03f')
        line_opacity: float, default Leaflet's default (0.5)
        line_weight: float, default Leaflet's default (5)
        popup: string or tuple, default 'Pop Text'
            Input text or visualization for object. Can pass either text,
            or a tuple of the form (Vincent object, 'vis_path.json')
            It is possible to adjust the width of text/HTML popups
            using the optional keywords `popup_width` (default is 300px).
        latlon: bool, default True
            Whether locations are given in the form [[lat, lon]]
            or not ([[lon, lat]] if False).
            Note that the default GeoJson format is latlon=False,
            while Leaflet polyline's default is latlon=True.

        Note: If the optional styles are omitted, they will not be included
        in the HTML output and will obtain the Leaflet defaults listed above.

        Examples
        --------
        >>> map.line(locations=[(45.5, -122.3), (42.3, -71.0)])
        >>> map.line(locations=[(45.5, -122.3), (42.3, -71.0)],
                     line_color='red', line_opacity=1.0)

        """
        warnings.warn("%s is deprecated. Use %s instead" %
                      ("line", "add_children(PolyLine)"),
                      FutureWarning, stacklevel=2)
        p = PolyLine(locations,
                     color=line_color,
                     weight=line_weight,
                     opacity=line_opacity,
                     latlon=latlon,
                     )

        if popup is not None:
            p.add_children(Popup(popup, max_width=popup_width))

        self.add_children(p)

    def multiline(self, locations, line_color=None, line_opacity=None,
                  line_weight=None, popup=None, popup_width=300, latlon=True):
        """Add a multiPolyline to the map with optional styles.

        A multiPolyline is single layer that consists of several polylines that
        share styling/popup.

        Parameters
        ----------
        locations: list of lists of points (latitude, longitude)
            Latitude and Longitude of line (Northing, Easting)
        line_color: string, default Leaflet's default ('#03f')
        line_opacity: float, default Leaflet's default (0.5)
        line_weight: float, default Leaflet's default (5)
        popup: string or tuple, default 'Pop Text'
            Input text or visualization for object. Can pass either text,
            or a tuple of the form (Vincent object, 'vis_path.json')
            It is possible to adjust the width of text/HTML popups
            using the optional keywords `popup_width` (default is 300px).
        latlon: bool, default True
            Whether locations are given in the form [[lat, lon]]
            or not ([[lon, lat]] if False).
            Note that the default GeoJson format is latlon=False,
            while Leaflet polyline's default is latlon=True.

        Note: If the optional styles are omitted, they will not be included
        in the HTML output and will obtain the Leaflet defaults listed above.

        Examples
        --------
        >>> m.multiline(locations=[[(45.5236, -122.675), (45.5236, -122.675)],
                                   [(45.5237, -122.675), (45.5237, -122.675)],
                                   [(45.5238, -122.675), (45.5238, -122.675)]])
        >>> m.multiline(locations=[[(45.5236, -122.675), (45.5236, -122.675)],
                                   [(45.5237, -122.675), (45.5237, -122.675)],
                                   [(45.5238, -122.675), (45.5238, -122.675)]],
                        line_color='red', line_weight=2,
                        line_opacity=1.0)
        FIXME: Add another example.
        """
        warnings.warn("%s is deprecated. Use %s instead" %
                      ("multiline", "add_children(MultiPolyLine)"),
                      FutureWarning, stacklevel=2)
        p = MultiPolyLine(locations,
                          color=line_color,
                          weight=line_weight,
                          opacity=line_opacity,
                          latlon=latlon)

        if popup is not None:
            p.add_children(Popup(popup, max_width=popup_width))

        self.add_children(p)

    def circle_marker(self, location=None, radius=500, popup=None,
                      line_color='black', fill_color='black',
                      fill_opacity=0.6, popup_width=300):
        """Create a simple circle marker on the map, with optional popup text
        or Vincent visualization.

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Marker (Northing, Easting)
        radius: int, default 500
            Circle radius, in pixels
        popup: string or tuple, default 'Pop Text'
            Input text or visualization for object. Can pass either text,
            or a tuple of the form (Vincent object, 'vis_path.json')
            It is possible to adjust the width of text/HTML popups
            using the optional keywords `popup_width` (default is 300px).
        line_color: string, default black
            Line color. Can pass hex value here as well.
        fill_color: string, default black
            Fill color. Can pass hex value here as well.
        fill_opacity: float, default 0.6
            Circle fill opacity

        Returns
        -------
        Circle names and HTML in obj.template_vars

        Examples
        --------
        >>> map.circle_marker(location=[45.5, -122.3],
                              radius=1000, popup='Portland, OR')
        >>> map.circle_marker(location=[45.5, -122.3],
                              radius=1000, popup=(bar_chart, 'bar_data.json'))

        """
        warnings.warn("%s is deprecated. Use %s instead" %
                      ("circle_marker", "add_children(CircleMarker)"),
                      FutureWarning, stacklevel=2)
        if isinstance(popup, text_type) or isinstance(popup, binary_type):
            popup_ = Popup(popup, max_width=popup_width)
        elif isinstance(popup, tuple):
            popup_ = Popup(Vega(json.loads(popup[0].to_json()),
                                width="100%", height="100%"),
                           max_width=popup_width)
        else:
            popup_ = None
        marker = CircleMarker(location,
                              radius=radius,
                              color=line_color,
                              fill_color=fill_color,
                              fill_opacity=fill_opacity,
                              popup=popup_)
        self.add_children(marker)

    def polygon_marker(self, location=None, line_color='black', line_opacity=1,
                       line_weight=2, fill_color='blue', fill_opacity=1,
                       num_sides=4, rotation=0, radius=15, popup=None,
                       popup_width=300):
        """Custom markers using the Leaflet Data Vis Framework.


        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Marker (Northing, Easting)
        line_color: string, default 'black'
            Marker line color
        line_opacity: float, default 1
            Line opacity, scale 0-1
        line_weight: int, default 2
            Stroke weight in pixels
        fill_color: string, default 'blue'
            Marker fill color
        fill_opacity: float, default 1
            Marker fill opacity
        num_sides: int, default 4
            Number of polygon sides
        rotation: int, default 0
            Rotation angle in degrees
        radius: int, default 15
            Marker radius, in pixels
        popup: string or tuple, default 'Pop Text'
            Input text or visualization for object. Can pass either text,
            or a tuple of the form (Vincent object, 'vis_path.json')
            It is possible to adjust the width of text/HTML popups
            using the optional keywords `popup_width` (default is 300px).

        Returns
        -------
        Polygon marker names and HTML in obj.template_vars

        """
        warnings.warn("%s is deprecated. Use %s instead" %
                      ("polygon_marker", "add_children(RegularPolygonMarker)"),
                      FutureWarning, stacklevel=2)
        if isinstance(popup, text_type) or isinstance(popup, binary_type):
            popup_ = Popup(popup, max_width=popup_width)
        elif isinstance(popup, tuple):
            popup_ = Popup(Vega(json.loads(popup[0].to_json()),
                                width="100%", height="100%"),
                           max_width=popup_width)
        else:
            popup_ = None
        marker = RegularPolygonMarker(location,
                                      popup=popup_,
                                      color=line_color,
                                      opacity=line_opacity,
                                      weight=line_weight,
                                      fill_color=fill_color,
                                      fill_opacity=fill_opacity,
                                      number_of_sides=num_sides,
                                      rotation=rotation,
                                      radius=radius)
        self.add_children(marker)

    def lat_lng_popover(self):
        """Enable popovers to display Lat and Lon on each click."""
        warnings.warn("%s is deprecated. Use %s instead" %
                      ("lat_lng_popover", "add_children(LatLngPopup)"),
                      FutureWarning, stacklevel=2)
        self.add_children(LatLngPopup())

    def click_for_marker(self, popup=None):
        """Enable the addition of markers via clicking on the map. The marker
        popup defaults to Lat/Lon, but custom text can be passed via the
        popup parameter. Double click markers to remove them.

        Parameters
        ----------
        popup:
            Custom popup text

        Examples
        --------
        >>> map.click_for_marker(popup='Your Custom Text')

        """
        warnings.warn("%s is deprecated. Use %s instead" %
                      ("click_for_marker", "add_children(ClickForMarker)"),
                      FutureWarning, stacklevel=2)
        self.add_children(ClickForMarker(popup=popup))

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
        self.add_children(FitBounds(bounds,
                                    padding_top_left=padding_top_left,
                                    padding_bottom_right=padding_bottom_right,
                                    padding=padding,
                                    max_zoom=max_zoom,
                                    )
                          )

    def add_plugin(self, plugin):
        """Adds a plugin to the map.

        Parameters
        ----------
            plugin: folium.plugins object
                A plugin to be added to the map. It has to implement the
                methods `render_html`, `render_css` and `render_js`.
        """
        warnings.warn("%s is deprecated. Use %s instead" %
                      ("add_plugin", "add_children"),
                      FutureWarning, stacklevel=2)
        self.add_children(plugin)

    def geo_json(self, *args, **kwargs):
        """This method is deprecated and will be removed in v0.2.1. See
        `Map.choropleth` instead.
        """
        warnings.warn('This method is deprecated. '
                      'Please use Map.choropleth instead.')
        return self.choropleth(*args, **kwargs)

    def choropleth(self, geo_path=None, geo_str=None, data_out='data.json',
                   data=None, columns=None, key_on=None, threshold_scale=None,
                   fill_color='blue', fill_opacity=0.6, line_color='black',
                   line_weight=1, line_opacity=1, legend_name="",
                   topojson=None, reset=False):
        """
        Apply a GeoJSON overlay to the map.

        Plot a GeoJSON overlay on the base map. There is no requirement
        to bind data (passing just a GeoJSON plots a single-color overlay),
        but there is a data binding option to map your columnar data to
        different feature objects with a color scale.

        If data is passed as a Pandas dataframe, the "columns" and "key-on"
        keywords must be included, the first to indicate which DataFrame
        columns to use, the second to indicate the layer in the GeoJSON
        on which to key the data. The 'columns' keyword does not need to be
        passed for a Pandas series.

        Colors are generated from color brewer (http://colorbrewer2.org/)
        sequential palettes on a D3 threshold scale. The scale defaults to the
        following quantiles: [0, 0.5, 0.75, 0.85, 0.9]. A custom scale can be
        passed to `threshold_scale` of length <=6, in order to match the
        color brewer range.

        TopoJSONs can be passed as "geo_path", but the "topojson" keyword must
        also be passed with the reference to the topojson objects to convert.
        See the topojson.feature method in the TopoJSON API reference:
        https://github.com/mbostock/topojson/wiki/API-Reference


        Parameters
        ----------
        geo_path: string, default None
            URL or File path to your GeoJSON data
        geo_str: string, default None
            String of GeoJSON, alternative to geo_path
        data_out: string, default 'data.json'
            Path to write Pandas DataFrame/Series to JSON if binding data
        data: Pandas DataFrame or Series, default None
            Data to bind to the GeoJSON.
        columns: dict or tuple, default None
            If the data is a Pandas DataFrame, the columns of data to be bound.
            Must pass column 1 as the key, and column 2 the values.
        key_on: string, default None
            Variable in the GeoJSON file to bind the data to. Must always
            start with 'feature' and be in JavaScript objection notation.
            Ex: 'feature.id' or 'feature.properties.statename'.
        threshold_scale: list, default None
            Data range for D3 threshold scale. Defaults to the following range
            of quantiles: [0, 0.5, 0.75, 0.85, 0.9], rounded to the nearest
            order-of-magnitude integer. Ex: 270 rounds to 200, 5600 to 6000.
        fill_color: string, default 'blue'
            Area fill color. Can pass a hex code, color name, or if you are
            binding data, one of the following color brewer palettes:
            'BuGn', 'BuPu', 'GnBu', 'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'RdPu',
            'YlGn', 'YlGnBu', 'YlOrBr', and 'YlOrRd'.
        fill_opacity: float, default 0.6
            Area fill opacity, range 0-1.
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
        reset: boolean, default False
            Remove all current geoJSON layers, start with new layer

        Returns
        -------
        GeoJSON data layer in obj.template_vars

        Examples
        --------
        >>> m.choropleth(geo_path='us-states.json', line_color='blue',
        ...              line_weight=3)
        >>> m.choropleth(geo_path='geo.json', data=df,
        ...              columns=['Data 1', 'Data 2'],
        ...              key_on='feature.properties.myvalue',
        ...              fill_color='PuBu',
        ...              threshold_scale=[0, 20, 30, 40, 50, 60])
        >>> m.choropleth(geo_path='countries.json',
        ...              topojson='objects.countries')

        """
        if threshold_scale and len(threshold_scale) > 6:
            raise ValueError
        if data is not None and not color_brewer(fill_color):
            raise ValueError('Please pass a valid color brewer code to '
                             'fill_local. See docstring for valid codes.')

        # Create GeoJson object
        if geo_path:
            geo_data = open(geo_path)
        elif geo_str:
            geo_data = geo_str
        else:
            geo_data = {}

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

        # Compute color_domain
        if threshold_scale:
            color_domain = list(threshold_scale)
        elif color_data:
            # To avoid explicit pandas dependency ; changed default behavior.
            warnings.warn("'threshold_scale' default behavior has changed."
                          " Now you get a linear scale between the 'min' and"
                          " the 'max' of your data."
                          " To get former behavior, use"
                          " folium.utilities.split_six.",
                          FutureWarning, stacklevel=2)
            data_min = min(color_data.values())
            data_max = max(color_data.values())
            if data_min == data_max:
                data_min = (data_min if data_min < 0 else 0
                            if data_min > 0 else -1)
                data_max = (data_max if data_max > 0 else 0
                            if data_max < 0 else 1)
            data_min, data_max = (1.01*data_min-0.01*data_max,
                                  1.01*data_max-0.01*data_min)
            nb_class = 6
            color_domain = [data_min+i*(data_max-data_min)*1./nb_class
                            for i in range(1+nb_class)]
        else:
            color_domain = None

        if color_domain and key_on:
            key_on = key_on[8:] if key_on.startswith('feature.') else key_on
            color_range = color_brewer(fill_color, n=len(color_domain))

            def get_by_key(obj, key):
                return (obj.get(key, None) if len(key.split('.')) <= 1 else
                        get_by_key(obj.get(key.split('.')[0], None),
                                   '.'.join(key.split('.')[1:])))

            def color_scale_fun(x):
                return color_range[len(
                    [u for u in color_domain if
                     u <= color_data[get_by_key(x, key_on)]])]
        else:
            def color_scale_fun(x):
                return fill_color

        def style_function(x):
            return {
                "weight": line_weight,
                "opactiy": line_opacity,
                "color": line_color,
                "fillOpacity": fill_opacity,
                "fillColor": color_scale_fun(x)
            }

        if topojson:
            geo_json = TopoJson(geo_data, topojson, style_function=style_function)  # noqa
        else:
            geo_json = GeoJson(geo_data, style_function=style_function)

        self.add_children(geo_json)

        # Create ColorMap.
        if color_domain:
            brewed = color_brewer(fill_color, n=len(color_domain))
            color_scale = StepColormap(
                brewed[1:len(color_domain)],
                index=color_domain,
                vmin=color_domain[0],
                vmax=color_domain[-1],
                )
            self.add_children(color_scale)

    def image_overlay(self, data, opacity=0.25, min_lat=-90.0, max_lat=90.0,
                      min_lon=-180.0, max_lon=180.0, origin='upper',
                      colormap=None, image_name=None, filename=None,
                      mercator_project=False):
        """
        Simple image overlay of raster data from a numpy array.  This is a
        lightweight way to overlay geospatial data on top of a map.  If your
        data is high res, consider implementing a WMS server and adding a WMS
        layer.

        This function works by generating a PNG file from a numpy array.  If
        you do not specify a filename, it will embed the image inline.
        Otherwise, it saves the file in the current directory, and then adds
        it as an image overlay layer in leaflet.js.  By default, the image is
        placed and stretched using bounds that cover the entire globe.

        Parameters
        ----------
        data: numpy array OR url string, required.
            if numpy array, must be a image format,
            i.e., NxM (mono), NxMx3 (rgb), or NxMx4 (rgba)
            if url, must be a valid url to a image (local or external)
        opacity: float, default 0.25
            Image layer opacity in range 0 (transparent) to 1 (opaque)
        min_lat: float, default -90.0
        max_lat: float, default  90.0
        min_lon: float, default -180.0
        max_lon: float, default  180.0
        image_name: string, default None
            The name of the layer object in leaflet.js
        filename: string, default None
            Optional file name of output.png for image overlay.
            Use `None` for inline PNG.
        origin : ['upper' | 'lower'], optional, default 'upper'
            Place the [0,0] index of the array in the upper left or lower left
            corner of the axes.

        colormap : callable, used only for `mono` image.
            Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
            for transforming a mono image into RGB.
            It must output iterables of length 3 or 4, with values
            between 0 and 1. Hint: you can use colormaps from `matplotlib.cm`.

        mercator_project : bool, default False, used only for array-like image.
            Transforms the data to project (longitude,latitude) coordinates
            to the Mercator projection.

        Returns
        -------
        Image overlay data layer in obj.template_vars

        Examples
        --------
        # assumes a map object `m` has been created
        >>> import numpy as np
        >>> data = np.random.random((100,100))

        # to make a rgba from a specific matplotlib colormap:
        >>> import matplotlib.cm as cm
        >>> cmapper = cm.cm.ColorMapper('jet')
        >>> data2 = cmapper.to_rgba(np.random.random((100,100)))
        >>> # Place the data over all of the globe (will be pretty pixelated!)
        >>> m.image_overlay(data)
        >>> # Put it only over a single city (Paris).
        >>> m.image_overlay(data, min_lat=48.80418, max_lat=48.90970,
        ...                 min_lon=2.25214, max_lon=2.44731)

        """
        msg = ('This method is deprecated. Please use '
               '`Map.add_children(folium.plugins.ImageOverlay(...))` instead.')
        warnings.warn(msg)
        from .plugins import ImageOverlay
        from .utilities import write_png

        if filename:
            image = write_png(data, origin=origin, colormap=colormap)
            open(filename, 'wb').write(image)
            data = filename

        self.add_children(ImageOverlay(data, [[min_lat, min_lon],
                                              [max_lat, max_lon]],
                                       opacity=opacity,
                                       origin=origin,
                                       colormap=colormap,
                                       mercator_project=mercator_project))
