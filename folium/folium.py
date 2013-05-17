# -*- coding: utf-8 -*-
'''
Folium
-------

Make beautiful, interactive maps with Python and Leaflet.js

'''

from __future__ import print_function
from __future__ import division
import codecs
import json
import pandas as pd
from jinja2 import Environment, PackageLoader, Template
import markers as mk
import utilities


class Map(object):
    '''Create a Map with Folium'''

    def __init__(self, location=None, width=960, height=500,
                 tiles='OpenStreetMap', API_key=None, max_zoom=18,
                 zoom_start=10, attr=None):
        '''Create a Map with Folium and Leaflet.js

        Folium supports OpenStreetMap, Mapbox, and Cloudmade tiles natively.
        You can pass a custom tileset to Folium by passing a Leaflet-style
        URL to the tiles parameter:
        http://{s}.yourtiles.com/{z}/{x}/{y}.png

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Map (Northing, Easting)
        width: int, default 960
            Width of the map
        height: int, default 500
            Height of the map
        tiles: str, default 'OpenStreetMap'
            Map tileset to use. Can use "OpenStreetMap", "Cloudmade", "Mapbox",
            "Mapbox Dark", or pass a custom URL
        API_key: str, default None
            API key for Cloudmade tiles
        max_zoom: int, default 18
            Maximum zoom depth for the map
        zoom_start: int, default 10
            Initial zoom level for the map
        attr: string, default None
            Map tile attribution; only required if passing custom tile URL

        Returns
        -------
        Folium Map Object

        Examples
        --------
        >>>map = folium.Map(location=[45.523, -122.675], width=750, height=500)
        >>>map = folium.Map(location=(45.523, -122.675), max_zoom=20,
                            tiles='Cloudmade', API_key='YourKey')
        >>>map = folium.Map(location=[45.523, -122.675], zoom_start=2,
                            tiles='http://a.tiles.mapbox.com/v3/
                                   mapbox.control-room/{z}/{x}/{y}.png')

        '''

        #Map type, default base
        self.map_type = 'base'

        #Mark counter and JSON
        self.mark_cnt = {}
        self.json_data = None

        #Location
        if not location:
            raise ValueError('You must pass a Lat/Lon location to initialize'
                             ' your map')
        self.location = location

        #Map Size Parameters
        self.map_size = {'width': width, 'height': height}
        self._size = ('style="width: {0}px; height: {1}px"'
                      .format(width, height))

        #Templates
        self.env = Environment(loader=PackageLoader('folium', 'templates'))
        self.template_vars = {'lat': location[0], 'lon': location[1],
                              'size': self._size, 'max_zoom': max_zoom,
                              'zoom_level': zoom_start}

        #Tiles
        self.tiles = ''.join(tiles.lower().strip().split())
        if self.tiles == 'cloudmade' and not API_key:
            raise ValueError('You must pass an API key if using Cloudmade'
                             ' tiles.')

        self.default_tiles = ['openstreetmap', 'mapbox', 'cloudmade',
                              'mapboxdark']
        self.tile_types = {}
        for tile in self.default_tiles:
            self.tile_types[tile] = {'templ':
                                     self.env.get_template(tile + '_tiles.txt'),
                                     'attr':
                                     self.env.get_template(tile + '_att.txt')}

        if self.tiles in self.tile_types:
            self.template_vars['Tiles'] = (self.tile_types[self.tiles]['templ']
                                           .render(API_key=API_key))
            self.template_vars['attr'] = (self.tile_types[self.tiles]['attr']
                                          .render())
        else:
            self.template_vars['Tiles'] = tiles
            if not attr:
                raise ValueError('Custom tiles must also be passed an attribution')
            self.template_vars['attr'] = unicode(attr, 'utf8')
            self.tile_types.update({'Custom': {'template': tiles, 'attr': attr}})

    def simple_marker(self, location=None, popup_txt='Pop Text', popup=True):
        '''Create a simple stock Leaflet marker on the map, with optional
        popup text.

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Marker (Northing, Easting)
        popup_txt: string, default 'Pop Text'
            Input text for popup. HTML tags can be passed to style text:
            "<b>Popup text</b><br>Line 2"
        popup: boolean, default True
            Pass false for no popup information on the marker

        Returns
        -------
        Marker names and HTML in obj.template_vars

        Example
        -------
        >>>map.simple_marker(location=[45.5, -122.3], popup_txt='Portland, OR')

        '''
        self.mark_cnt['simple'] = self.mark_cnt.get('simple', 0) + 1
        marker = mk.simple_marker(location, popup_txt, popup,
                                  self.mark_cnt['simple'])
        self.template_vars.setdefault('markers', []).append(marker)

    def circle_marker(self, location=None, radius=500, popup_txt='Pop Text',
                      popup=True, line_color='black', fill_color='black',
                      fill_opacity=0.6):
        '''Create a simple circle marker on the map, with optional popup text.

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Marker (Northing, Easting)
        radius: int, default 500
            Circle radius, in pixels
        popup_txt: string, default 'Pop Text'
            Input text for popup. HTML tags can be passed to style text:
            "<b>Popup text</b><br>Line 2"
        popup: boolean, default True
            Pass false for no popup information on the marker
        line_color: string, default black
            Line color. Can pass hex value here as well.
        fill_color: string, default black
            Fill color. Can pass hex value here as well.
        fill_opacity: float, default 0.6
            Circle fill opacity

        Returns
        -------
        Circle names and HTML in obj.template_vars

        Example
        -------
        >>>map.circle_marker(location=[45.5, -122.3],
                             radius=1000, popup_txt='Portland, OR')

        '''
        self.mark_cnt['circle'] = self.mark_cnt.get('circle', 0) + 1
        marker = mk.circle_marker(location, radius, line_color, fill_color,
                                  fill_opacity, popup_txt, popup,
                                  self.mark_cnt['circle'])

        self.template_vars.setdefault('markers', []).append(marker)

    def lat_lng_popover(self):
        '''Enable popovers to display Lat and Lon on each click'''

        latlng_temp = self.env.get_template('lat_lng_popover.txt')
        self.template_vars.update({'lat_lng_pop': latlng_temp.render()})

    def click_for_marker(self, popup_txt=None):
        '''Enable the addition of markers via clicking on the map. The marker
        popup defaults to Lat/Lon, but custom text can be passed via the
        popup_txt parameter. Doubleclick markers to remove them.

        Parameters
        ----------
        popup_text:
            Custom popup text

        Example
        -------
        >>>map.click_for_marker(popup_txt='Your Custom Text')

        '''
        latlng = '"Latitude: " + lat + "<br>Longitude: " + lng '
        click_temp = self.env.get_template('click_for_marker.txt')
        if popup_txt:
            popup = ''.join(['"', popup_txt, '"'])
        else:
            popup = latlng
        click_str = click_temp.render({'popup': popup})
        self.template_vars.update({'click_pop': click_str})

    def geo_json(self, path, data_path='data.json', data=None, columns=None,
                 threshold_range=None, key_on=None, line_color='black',
                 line_weight=1, line_opacity=1, fill_color='blue',
                 fill_opacity=0.6, legend_name=None, reset=False):
        '''Apply a GeoJSON overlay to the map.

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
        sequential palettes on a D3 quantize scale. The 'color_range'
        sets the scale range, which defaults to [0: data.max()]


        Parameters
        ----------
        path: string
            URL or File path to your GeoJSON data
        data_path: string
            Path to write Pandas DataFrame/Series to JSON if binding data
        data: Pandas DataFrame or Series, default None
            Data to bind to the GeoJSON.
        columns: dict or tuple, default None
            If the data is a Pandas DataFrame, the columns to bind to. Must
            pass column 1 as the key, and column 2 the data
        threshold_range: list, default 'auto'
            Data range for D3 threshold scale. Passing 'auto' will divide the
            scale into 6 bins, rounding to nearest order-of-magnitude integer
            to keep the legend clean. Ex: 2340 will round to 2000.
        key_on: string, default None
            Variable in the GeoJSON file to bind the data to. Must always
            start with 'feature' and be in JavaScript objection notation.
            Ex: 'feature.id' or 'feature.properties.statename'
        line_color: string, default 'black'
            GeoJSON geopath line color
        line_weight: int, default 1
            GeoJSON geopath line weight
        line_opacity: float, default 1
            GeoJSON geopath line opacity, range 0-1
        fill_color: string, default 'blue'
            Area fill color. Can pass a hex code, or if you are binding data,
            one of the following color brewer palettes:
            'BuGn', 'BuPu', 'GnBu', 'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'RdPu',
            'YlGn', 'YlGnBu', 'YlOrBr', and 'YlOrRd'.
        fill_opacity: float, default 0.6
            Area fill opacity, range 0-1
        legend_name: string, default None
            Title for data legend. If not passed, defaults to columns[1].
        reset: boolean, default False
            Remove all current geoJSON layers, start with new layer

        Output
        ------
        GeoJSON data layer in obj.template_vars

        Example
        -------
        >>>map.geo_json('us-states.json', line_color='blue', line_weight=3)
        '''

        if reset:
            reset_vars = ['json_paths', 'func_vars', 'color_scales', 'geo_styles',
                          'gjson_layers']
            for var in reset_vars:
                self.template_vars.update({var: []})
            self.mark_cnt['geo_json'] = 0

        def json_style(style_cnt, line_color, line_weight, line_opacity,
                       fill_color, fill_opacity, quant_fill):
            '''Generate JSON styling function from template'''
            style_temp = self.env.get_template('geojson_style.txt')
            style = style_temp.render({'style': style_cnt,
                                       'line_color': line_color,
                                       'line_weight': line_weight,
                                       'line_opacity': line_opacity,
                                       'fill_color': fill_color,
                                       'fill_opacity': fill_opacity,
                                       'quantize_fill': quant_fill})
            return style

        #Set map type to geo_json
        self.map_type = 'geojson'

        #Set counter for GeoJSON and set iterations
        self.mark_cnt['geojson'] = self.mark_cnt.get('geojson', 0) + 1

        #Get JSON map layer template pieces
        geo_path = ".defer(d3.json, '{0}')".format(path)
        map_var = '_'.join(['gjson', str(self.mark_cnt['geojson'])])
        style_count = '_'.join(['style', str(self.mark_cnt['geojson'])])

        #Get Data binding pieces if available
        if data is not None:

            #Create DataFrame with only the relevant columns
            if isinstance(data, pd.DataFrame):
                data = pd.concat([data[columns[0]], data[columns[1]]], axis=1)

            #Save data to JSON
            self.json_data = utilities.transform_data(data)

            #Add data to queue
            d_path = ".defer(d3.json, '{0}')".format(data_path)
            self.template_vars.setdefault('json_paths', []).append(d_path)

            #Add data variable to makeMap function
            data_var = '_'.join(['data', str(self.mark_cnt['geojson'])])
            self.template_vars.setdefault('func_vars', []).append(data_var)

            self.json_data = utilities.transform_data(data)
            self.json_path = data_path

            #D3 Color scale
            series = data[columns[1]]
            domain = threshold_range or utilities.split_six(series=series)
            if not utilities.color_brewer(fill_color):
                raise ValueError('Please pass a valid color brewer code to '
                                 'fill_local. See docstring for valid codes.')

            palette = utilities.color_brewer(fill_color)
            d3range = palette[0: len(domain) + 1]

            color_temp = self.env.get_template('d3_threshold.js')
            d3scale = color_temp.render({'domain': domain,
                                         'range': d3range})
            self.template_vars.setdefault('color_scales', []).append(d3scale)

            #Create legend
            leg_templ = self.env.get_template('d3_map_legend.js')
            legend = leg_templ.render({'lin_max': int(domain[-1]*1.1),
                                       'caption': columns[1]})
            self.template_vars.setdefault('map_legends', []).append(legend)

            #Style with color brewer colors
            matchColor = 'color(matchKey({0}, {1}))'.format(key_on, data_var)
            style = json_style(style_count, line_color, line_weight,
                               line_opacity, None, fill_opacity, matchColor)
        else:
            self.json_data = None
            style = json_style(style_count, line_color, line_weight,
                               line_opacity, fill_color, fill_opacity, None)

        layer = ('gJson_layer_{0} = L.geoJson({1}, {{style: {2}}}).addTo(map)'
                 .format(self.mark_cnt['geojson'], map_var, style_count))

        self.template_vars.setdefault('json_paths', []).append(geo_path)
        self.template_vars.setdefault('func_vars', []).append(map_var)
        self.template_vars.setdefault('geo_styles', []).append(style)
        self.template_vars.setdefault('gjson_layers', []).append(layer)

    def _build_map(self):
        '''Build HTML/JS/CSS from Templates given current map type'''
        map_types = {'base': 'fol_template.html',
                     'geojson': 'geojson_template.html'}

        #Check current map type
        type_temp = map_types[self.map_type]

        html_templ = self.env.get_template(type_temp)
        self.HTML = html_templ.render(self.template_vars)

    def create_map(self, path='map.html'):
        '''Write Map output to HTML and data output to JSON if available'''

        self._build_map()

        with codecs.open(path, 'w', 'utf-8') as f:
            f.write(self.HTML)

        if self.json_data:
            with open(self.json_path, 'w') as g:
                json.dump(self.json_data, g)
