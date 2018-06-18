# -*- coding: utf-8 -*-

"""
Folium
-------

Make beautiful, interactive maps with Python and Leaflet.js

"""

from __future__ import (absolute_import, division, print_function)

from branca.colormap import StepColormap
# from branca.utilities import color_brewer

from folium.features import GeoJson, TopoJson
from folium.map import FitBounds, LegacyMap


def color_brewer(color_code, n=7):
    """
    Generate a colorbrewer color scheme of length 'len', type 'scheme.
    Live examples can be seen at http://colorbrewer2.org/

    """
    maximum_n = 253

    scheme_info = {'BuGn': 'Sequential',
                   'BuPu': 'Sequential',
                   'GnBu': 'Sequential',
                   'OrRd': 'Sequential',
                   'PuBu': 'Sequential',
                   'PuBuGn': 'Sequential',
                   'PuRd': 'Sequential',
                   'RdPu': 'Sequential',
                   'YlGn': 'Sequential',
                   'YlGnBu': 'Sequential',
                   'YlOrBr': 'Sequential',
                   'YlOrRd': 'Sequential',
                   'BrBg': 'Diverging',
                   'PiYG': 'Diverging',
                   'PRGn': 'Diverging',
                   'PuOr': 'Diverging',
                   'RdBu': 'Diverging',
                   'RdGy': 'Diverging',
                   'RdYlBu': 'Diverging',
                   'RdYlGn': 'Diverging',
                   'Spectral': 'Diverging',
                   'Accent': 'Qualitative',
                   'Dark2': 'Qualitative',
                   'Paired': 'Qualitative',
                   'Pastel1': 'Qualitative',
                   'Pastel2': 'Qualitative',
                   'Set1': 'Qualitative',
                   'Set2': 'Qualitative',
                   'Set3': 'Qualitative',
                   'Spectral_reverse': 'Sequential',
                   }

    schemes = {'BuGn': ['#EDF8FB', '#CCECE6', '#CCECE6',
                        '#66C2A4', '#41AE76', '#238B45', '#005824'],
               'BuPu': ['#EDF8FB', '#BFD3E6', '#9EBCDA',
                        '#8C96C6', '#8C6BB1', '#88419D', '#6E016B'],
               'GnBu': ['#F0F9E8', '#CCEBC5', '#A8DDB5',
                        '#7BCCC4', '#4EB3D3', '#2B8CBE', '#08589E'],
               'OrRd': ['#FEF0D9', '#FDD49E', '#FDBB84',
                        '#FC8D59', '#EF6548', '#D7301F', '#990000'],
               'PuBu': ['#F1EEF6', '#D0D1E6', '#A6BDDB',
                        '#74A9CF', '#3690C0', '#0570B0', '#034E7B'],
               'PuBuGn': ['#F6EFF7', '#D0D1E6', '#A6BDDB',
                          '#67A9CF', '#3690C0', '#02818A', '#016450'],
               'PuRd': ['#F1EEF6', '#D4B9DA', '#C994C7',
                        '#DF65B0', '#E7298A', '#CE1256', '#91003F'],
               'RdPu': ['#FEEBE2', '#FCC5C0', '#FA9FB5',
                        '#F768A1', '#DD3497', '#AE017E', '#7A0177'],
               'YlGn': ['#FFFFCC', '#D9F0A3', '#ADDD8E',
                        '#78C679', '#41AB5D', '#238443', '#005A32'],
               'YlGnBu': ['#FFFFCC', '#C7E9B4', '#7FCDBB',
                          '#41B6C4', '#1D91C0', '#225EA8', '#0C2C84'],
               'YlOrBr': ['#FFFFD4', '#FEE391', '#FEC44F',
                          '#FE9929', '#EC7014', '#CC4C02', '#8C2D04'],
               'YlOrRd': ['#FFFFB2', '#FED976', '#FEB24C',
                          '#FD8D3C', '#FC4E2A', '#E31A1C', '#B10026'],
               'BrBg': ['#8c510a', '#d8b365', '#f6e8c3',
                        '#c7eae5', '#5ab4ac', '#01665e'],
               'PiYG': ['#c51b7d', '#e9a3c9', '#fde0ef',
                        '#e6f5d0', '#a1d76a', '#4d9221'],
               'PRGn': ['#762a83', '#af8dc3', '#e7d4e8',
                        '#d9f0d3', '#7fbf7b', '#1b7837'],
               'PuOr': ['#b35806', '#f1a340', '#fee0b6',
                        '#d8daeb', '#998ec3', '#542788'],
               'RdBu': ['#b2182b', '#ef8a62', '#fddbc7',
                        '#d1e5f0', '#67a9cf', '#2166ac'],
               'RdGy': ['#b2182b', '#ef8a62', '#fddbc7',
                        '#e0e0e0', '#999999', '#4d4d4d'],
               'RdYlBu': ['#d73027', '#fc8d59', '#fee090',
                          '#e0f3f8', '#91bfdb', '#4575b4'],
               'RdYlGn': ['#d73027', '#fc8d59', '#fee08b',
                          '#d9ef8b', '#91cf60', '#1a9850'],
               'Spectral': ['#d53e4f', '#fc8d59', '#fee08b',
                            '#e6f598', '#99d594', '#3288bd'],
               'Accent': ['#7fc97f', '#beaed4', '#fdc086',
                          '#ffff99', '#386cb0', '#f0027f'],
               'Dark2': ['#1b9e77', '#d95f02', '#7570b3',
                         '#e7298a', '#66a61e', '#e6ab02'],
               'Paired': ['#a6cee3', '#1f78b4', '#b2df8a',
                          '#33a02c', '#fb9a99', '#e31a1c'],
               'Pastel1': ['#fbb4ae', '#b3cde3', '#ccebc5',
                           '#decbe4', '#fed9a6', '#ffffcc'],
               'Pastel2': ['#b3e2cd', '#fdcdac', '#cbd5e8',
                           '#f4cae4', '#e6f5c9', '#fff2ae'],
               'Set1': ['#e41a1c', '#377eb8', '#4daf4a',
                        '#984ea3', '#ff7f00', '#ffff33'],
               'Set2': ['#66c2a5', '#fc8d62', '#8da0cb',
                        '#e78ac3', '#a6d854', '#ffd92f'],
               'Set3': ['#8dd3c7', '#ffffb3', '#bebada',
                        '#fb8072', '#80b1d3', '#fdb462'],
               'Spectral_reverse': ['#9c3ff8', '#3da3e1', '#99d594',
                                    '#f9f651', '#f9cb51', '#fc8d59', '#d53e4f'],
               }

    # Raise an error if the n requested is greater than the maximum.
    if n > maximum_n:
        raise ValueError("The maximum number of colors in a"
                         " ColorBrewer sequential color series is 253")

    # Only if n is greater than six do we interpolate values.
    if n > 6:
        if color_code not in schemes:
            color_scheme = None
        else:
            # Check to make sure that it is not a qualitative scheme.
            if scheme_info[color_code] == 'Qualitative':
                raise ValueError("Expanded color support is not available"
                                 " for Qualitative schemes, restrict"
                                 " number of colors to 6")
            else:
                color_scheme = linear_gradient(schemes.get(color_code), n)
    else:
        color_scheme = schemes.get(color_code, None)
    return color_scheme


def linear_gradient(hexList, nColors):
    """
    Given a list of hexcode values, will return a list of length
    nColors where the colors are linearly interpolated between the
    (r, g, b) tuples that are given.

    Examples
    --------
    >>> linear_gradient([(0, 0, 0), (255, 0, 0), (255, 255, 0)], 100)

    """
    def _scale(start, finish, length, i):
        """
        Return the value correct value of a number that is in between start
        and finish, for use in a loop of length *length*.

        """
        base = 16

        fraction = float(i) / (length - 1)
        raynge = int(finish, base) - int(start, base)
        thex = hex(int(int(start, base) + fraction * raynge)).split('x')[-1]
        if len(thex) != 2:
            thex = '0' + thex
        return thex

    allColors = []
    # Separate (R, G, B) pairs.
    for start, end in zip(hexList[:-1], hexList[1:]):
        # Linearly intepolate between pair of hex ###### values and
        # add to list.
        nInterpolate = 765
        for index in range(nInterpolate):
            r = _scale(start[1:3], end[1:3], nInterpolate, index)
            g = _scale(start[3:5], end[3:5], nInterpolate, index)
            b = _scale(start[5:7], end[5:7], nInterpolate, index)
            allColors.append(''.join(['#', r, g, b]))

    # Pick only nColors colors from the total list.
    result = []
    for counter in range(nColors):
        fraction = float(counter) / (nColors - 1)
        index = int(fraction * (len(allColors) - 1))
        result.append(allColors[index])
    return result


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
    >>> map = folium.LegacyMap(
    ...    location=[45.523, -122.675],
    ...    zoom_start=2,
    ...    tiles='http://{s}.tiles.mapbox.com/v3/mapbox.control-room/{z}/{x}/{y}.png',
    ...    attr='Mapbox attribution'
    ...)

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

    def choropleth(self, geo_data, data=None, columns=None, key_on=None,
                   threshold_scale=None, fill_color='blue', fill_opacity=0.6,
                   line_color='black', line_weight=1, line_opacity=1, name=None,
                   legend_name='', topojson=None, reset=False, smooth_factor=None,
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

        TopoJSONs can be passed as "geo_data", but the "topojson" keyword must
        also be passed with the reference to the topojson objects to convert.
        See the topojson.feature method in the TopoJSON API reference:
        https://github.com/topojson/topojson/wiki/API-Reference


        Parameters
        ----------
        geo_data: string/object
            URL, file path, or data (json, dict, geopandas, etc) to your GeoJSON geometries
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
        >>> m.choropleth(geo_data='us-states.json', line_color='blue',
        ...              line_weight=3)
        >>> m.choropleth(geo_data='geo.json', data=df,
        ...              columns=['Data 1', 'Data 2'],
        ...              key_on='feature.properties.myvalue',
        ...              fill_color='PuBu',
        ...              threshold_scale=[0, 20, 30, 40, 50, 60])
        >>> m.choropleth(geo_data='countries.json',
        ...              topojson='objects.countries')
        >>> m.choropleth(geo_data='geo.json', data=df,
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
            color = color_scale_fun(x)  # added
            return {
                'weight': line_weight,
                'opacity': line_opacity,
                'color': color,  # changed from default color
                'fillOpacity': fill_opacity,
                'fillColor': color
            }

        def highlight_function(x):
            return {
                'weight': line_weight + 2,
                'fillOpacity': fill_opacity + .2
            }

        if topojson:
            geo_json = TopoJson(
                geo_data,
                topojson,
                name=name,
                style_function=style_function,
                smooth_factor=smooth_factor)
        else:
            geo_json = GeoJson(
                geo_data,
                name=name,
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
