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
from jinja2 import Environment, PackageLoader
import utilities


class Map(object):
    '''Create a Map with Folium'''

    def __init__(self, location=None, width=960, height=500,
                 tiles='OpenStreetMap', API_key=None, max_zoom=18,
                 zoom_start=10, attr=None):
        '''Create a Map with Folium and Leaflet.js

        Folium supports OpenStreetMap, Stamen, and Cloudmade tiles natively.
        You can pass a custom tileset to Folium by passing a Leaflet-style
        URL to the tiles parameter:
        http://{s}.yourtiles.com/{z}/{x}/{y}.png

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Map (Northing, Easting).
        width: int, default 960
            Width of the map.
        height: int, default 500
            Height of the map.
        tiles: str, default 'OpenStreetMap'
            Map tileset to use. Can use "OpenStreetMap", "Cloudmade",
            "Stamen Toner", "Stamen Terrain", or pass a custom URL.
        API_key: str, default None
            API key for Cloudmade tiles.
        max_zoom: int, default 18
            Maximum zoom depth for the map.
        zoom_start: int, default 10
            Initial zoom level for the map.
        attr: string, default None
            Map tile attribution; only required if passing custom tile URL.

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
                                   mapbox.control-room/{z}/{x}/{y}.png',
                            attr: 'Mapbox attribution')

        '''

        #Init Map type and JSON
        self.map_type = 'base'
        self.json_data = None

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

        self.default_tiles = ['openstreetmap', 'cloudmade', 'stamenterrain',
                              'stamentoner']
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

    def simple_marker(self, location=None, popup='Pop Text', popup_on=True):
        '''Create a simple stock Leaflet marker on the map, with optional
        popup text.

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Marker (Northing, Easting)
        popup: string or Vincent object, default 'Pop Text'
            Input text or visualization for object. Can pass either text,
            or a Vincent object for visualization.
        popup_on: boolean, default True
            Pass false for no popup information on the marker

        Returns
        -------
        Marker names and HTML in obj.template_vars

        Example
        -------
        >>>map.simple_marker(location=[45.5, -122.3], popup='Portland, OR')

        '''
        self.mark_cnt['simple'] = count = self.mark_cnt.get('simple', 0) + 1

        mark_temp = self.env.get_template('simple_marker.js')

        #Get marker and popup
        marker = mark_temp.render({'marker': 'marker_' + str(count),
                                   'lat': location[0], 'lon': location[1]})

        popup_out = self._popup_render(popup=popup, mk_name='marker_',
                                       count=count,
                                       popup_on=popup_on)

        add_mark = 'map.addLayer(marker_{0})'.format(count)

        self.template_vars.setdefault('markers', []).append((marker,
                                                             popup_out,
                                                             add_mark))

    def circle_marker(self, location=None, radius=500, popup='Pop Text',
                      popup_on=True, line_color='black', fill_color='black',
                      fill_opacity=0.6):
        '''Create a simple circle marker on the map, with optional popup text.

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Marker (Northing, Easting)
        radius: int, default 500
            Circle radius, in pixels
        popup: string or Vincent object, default 'Pop Text'
            Input text or visualization for object. Can pass either text,
            or a Vincent object for visualization.
        popup_on: boolean, default True
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
        self.mark_cnt['circle'] = count = self.mark_cnt.get('circle', 0) + 1

        circle_temp = self.env.get_template('circle_marker.js')

        circle = circle_temp.render({'circle': 'circle_' + str(count),
                                     'radius': radius,
                                     'lat': location[0], 'lon': location[1],
                                     'line_color': line_color,
                                     'fill_color': fill_color,
                                     'fill_opacity': fill_opacity})

        popup_out = self._popup_render(popup=popup, mk_name='marker_',
                                       count=count,
                                       popup_on=popup_on)

        add_mark = 'map.addLayer(circle_{0})'.format(count)

        self.template_vars.setdefault('markers', []).append((circle,
                                                             popup_out,
                                                             add_mark))

    def lat_lng_popover(self):
        '''Enable popovers to display Lat and Lon on each click'''

        latlng_temp = self.env.get_template('lat_lng_popover.js')
        self.template_vars.update({'lat_lng_pop': latlng_temp.render()})

    def click_for_marker(self, popup=None):
        '''Enable the addition of markers via clicking on the map. The marker
        popup defaults to Lat/Lon, but custom text can be passed via the
        popup_txt parameter. Double click markers to remove them.

        Parameters
        ----------
        popup_text:
            Custom popup text

        Example
        -------
        >>>map.click_for_marker(popup_txt='Your Custom Text')

        '''
        latlng = '"Latitude: " + lat + "<br>Longitude: " + lng '
        click_temp = self.env.get_template('click_for_marker.js')
        if popup:
            popup_txt = ''.join(['"', popup, '"'])
        else:
            popup_txt = latlng
        click_str = click_temp.render({'popup': popup_txt})
        self.template_vars.update({'click_pop': click_str})

    def _popup_render(self, popup=None, mk_name=None, count=None,
                      popup_on=True):
        '''Popup renderer: either text or Vincent/Vega.

        Parameters
        ----------
        popup: str or Vincent tuple, default None
            String for text popup, or tuple of (Vincent object, json_path)
        mk_name: str, default None
            Type of marker. Simple, Circle, etc.
        count: int, default None
            Count of marker
        popup_on: boolean, default True
            If False, no popup will be rendered
        '''
        if not popup_on:
            return 'var no_pop = null;'
        else:
            if isinstance(popup, str):
                popup_temp = self.env.get_template('simple_popup.js')
                return popup_temp.render({'pop_name': mk_name + str(count),
                                          'pop_txt': popup})
            elif isinstance(popup, tuple):
                #Update template with JS libs
                vega_temp = self.env.get_template('vega_ref.js').render()
                jquery_temp = self.env.get_template('jquery_ref.js').render()
                d3_temp = self.env.get_template('d3_ref.js').render()
                vega_parse = self.env.get_template('vega_parse.js').render()
                self.template_vars.update({'vega': vega_temp,
                                           'd3': d3_temp,
                                           'jquery': jquery_temp,
                                           'vega_parse': vega_parse})

                #Parameters for Vega template
                vega = popup[0]
                mark = ''.join([mk_name, str(count)])
                json_out = popup[1]
                div_id = popup[1].split('.')[0]
                width, height = (vega.width + 75), (vega.height + 50)
                max_width = self.map_size['width']
                vega_id = '#' + div_id
                popup_temp = self.env.get_template('vega_marker.js')
                return popup_temp.render({'mark': mark, 'div_id': div_id,
                                          'width': width, 'height': height,
                                          'max_width': max_width,
                                          'json_out': json_out,
                                          'vega_id': vega_id})

    def geo_json(self, geo_path=None, data_out='data.json', data=None,
                 columns=None, key_on=None, threshold_scale=None,
                 fill_color='blue', fill_opacity=0.6, line_color='black',
                 line_weight=1, line_opacity=1, legend_name=None,
                 reset=False):
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
        sequential palettes on a D3 threshold scale. The scale defaults to the
        following quantiles: [0, 0.5, 0.75, 0.85, 0.9]. A custom scale can be
        passed to `threshold_scale` of length <=6, in order to match the
        color brewer range.


        Parameters
        ----------
        geo_path: string, default None
            URL or File path to your GeoJSON data
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
        legend_name: string, default None
            Title for data legend. If not passed, defaults to columns[1].
        reset: boolean, default False
            Remove all current geoJSON layers, start with new layer

        Output
        ------
        GeoJSON data layer in obj.template_vars

        Example
        -------
        >>>map.geo_json(geo_path='us-states.json', line_color='blue', line_weight=3)
        >>>map_geo(geo_path='geo.json', data=df, columns=['Data 1', 'Data 2'],
                   key_on='feature.properties.myvalue', fill_color='PuBu',
                   threshold_scale=[0, 20, 30, 40, 50, 60])
        '''

        if reset:
            reset_vars = ['json_paths', 'func_vars', 'color_scales', 'geo_styles',
                          'gjson_layers', 'map_legends']
            for var in reset_vars:
                self.template_vars.update({var: []})
            self.mark_cnt['geojson'] = 0

        def json_style(style_cnt, line_color, line_weight, line_opacity,
                       fill_color, fill_opacity, quant_fill):
            '''Generate JSON styling function from template'''
            style_temp = self.env.get_template('geojson_style.js')
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
        self.mark_cnt['geojson'] = self.mark_cnt.get('geo_json', 0) + 1

        #Get JSON map layer template pieces
        geo_path = ".defer(d3.json, '{0}')".format(geo_path)
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
            d_path = ".defer(d3.json, '{0}')".format(data_out)
            self.template_vars.setdefault('json_paths', []).append(d_path)

            #Add data variable to makeMap function
            data_var = '_'.join(['data', str(self.mark_cnt['geojson'])])
            self.template_vars.setdefault('func_vars', []).append(data_var)

            self.json_data = utilities.transform_data(data)
            self.json_path = data_out

            #D3 Color scale
            series = data[columns[1]]
            domain = threshold_scale or utilities.split_six(series=series)
            if len(domain) > 6:
                raise ValueError('The threshold scale must be of length <= 6')
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
            name = legend_name or columns[1]
            leg_templ = self.env.get_template('d3_map_legend.js')
            legend = leg_templ.render({'lin_max': int(domain[-1]*1.1),
                                       'caption': name})
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

        if self.json_data is not None:
            with open(self.json_path, 'w') as g:
                json.dump(self.json_data, g)
