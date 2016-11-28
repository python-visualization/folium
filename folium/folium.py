# -*- coding: utf-8 -*-
"""
Folium
-------

Make beautiful, interactive maps with Python and Leaflet.js

"""

from __future__ import absolute_import

from branca.colormap import StepColormap
from branca.utilities import color_brewer

from .map import LegacyMap, FitBounds
from .features import GeoJson, TopoJson


class Map(LegacyMap):
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
                               tiles='Mapbox Control Room')
    >>> map = folium.LegacyMap(location=(45.523, -122.675), max_zoom=20,
                               tiles='Cloudmade', API_key='YourKey')
    >>> map = folium.LegacyMap(location=[45.523, -122.675], zoom_start=2,
                               tiles=('http://{s}.tiles.mapbox.com/v3/'
                                      'mapbox.control-room/{z}/{x}/{y}.png'),
                                attr='Mapbox attribution')

    """

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

    def choropleth(self, geo_path=None, geo_str=None, data_out='data.json',
                   data=None, columns=None, key_on=None, threshold_scale=None,
                   fill_color='blue', fill_opacity=0.6, line_color='black',
                   line_weight=1, line_opacity=1, legend_name="",
                   topojson=None, reset=False, smooth_factor=None,
                   highlight=None):
        """
        Apply a GeoJSON overlay to the map.

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
        smooth_factor: float, default None
            How much to simplify the polyline on each zoom level. More means
            better performance and smoother look, and less means more accurate
            representation. Leaflet defaults to 1.0.
        highlight: boolean, default False
            Enable highlight functionality when hovering over a GeoJSON area.

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
        >>> m.choropleth(geo_path='geo.json', data=df,
        ...              columns=['Data 1', 'Data 2'],
        ...              key_on='feature.properties.myvalue',
        ...              fill_color='PuBu',
        ...              threshold_scale=[0, 20, 30, 40, 50, 60],
        ...              highlight=True)

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
                     get_by_key(x, key_on) in color_data and
                     u <= color_data[get_by_key(x, key_on)]])]
        else:
            def color_scale_fun(x):
                return fill_color

        def style_function(x):
            return {
                "weight": line_weight,
                "opacity": line_opacity,
                "color": line_color,
                "fillOpacity": fill_opacity,
                "fillColor": color_scale_fun(x)
            }

        def highlight_function(x):
            return {
                "weight": line_weight + 2,
                "fillOpacity": fill_opacity + .2
            }

        if topojson:
            geo_json = TopoJson(
                geo_data,
                topojson,
                style_function=style_function,
                smooth_factor=smooth_factor)
        else:
            geo_json = GeoJson(
                geo_data,
                style_function=style_function,
                smooth_factor=smooth_factor,
                highlight_function=highlight_function if highlight else None)

        self.add_child(geo_json)

        # Create ColorMap.
        if color_domain:
            brewed = color_brewer(fill_color, n=len(color_domain))
            color_scale = StepColormap(
                brewed[1:len(color_domain)],
                index=color_domain,
                vmin=color_domain[0],
                vmax=color_domain[-1],
                caption=legend_name,
                )
            self.add_child(color_scale)
