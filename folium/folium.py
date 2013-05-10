# -*- coding: utf-8 -*-
'''
Folium
-------

Make beautiful, interactive maps with Python and Leaflet.js

'''

from __future__ import print_function
from __future__ import division
import codecs
from jinja2 import Environment, PackageLoader, Template
import markers as mk
import pdb


class Map(object):
    '''Create a Map with Folium'''

    def __init__(self, location=None, width=960, height=500, fullscreen=False,
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
        fill_window = boolean, default False
            Pass True for map to fill entire browser window, rather than
            be set to a width or height
        tiles: str, default 'OpenStreetMap'
            Map tileset to use. Can use "OpenStreetMap", "Cloudmade", "Mapbox",
            or pass a custom URL
        API_key: str, default None
            API key for Cloudmade tiles
        max_zoom: int, default 18
            Maximum zoom depth for the map
        zoom_start: int, default 10
            Initial zoom level for the map
        attribution: string, default None
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

        #Mark counter
        self.mark_cnt = {}

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
        if fullscreen:
            self.map_size = 'fullscreen'
            self.template_vars.pop('size')

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

    def _build_map(self):
        '''Build HTML/JS/CSS from Templates'''

        html_templ = self.env.get_template('fol_template.html')
        self.HTML = html_templ.render(self.template_vars)

    def create_map(self, path='map.html'):
        '''Write Map output to HTML'''

        self._build_map()

        with codecs.open(path, 'w', 'utf-8') as f:
            f.write(self.HTML)
