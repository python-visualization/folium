# -*- coding: utf-8 -*-
'''
Folium
-------

Make beautiful, interactive maps with Python and Leaflet.js

'''

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import codecs
import functools
import json
from uuid import uuid4

from jinja2 import Environment, PackageLoader
from pkg_resources import resource_string, resource_filename

from folium import utilities
from folium.six import text_type, binary_type, iteritems

import datetime
import pytz


ENV = Environment(loader=PackageLoader('folium', 'templates'))


def initialize_notebook():
    """Initialize the IPython notebook display elements"""
    try:
        from IPython.core.display import display, HTML
    except ImportError:
        print("IPython Notebook could not be loaded.")

    lib_css = ENV.get_template('ipynb_init_css.html')
    lib_js = ENV.get_template('ipynb_init_js.html')
    leaflet_dvf = ENV.get_template('leaflet-dvf.markers.min.js')
    leaflet_playback = ENV.get_template('LeafletPlayback.min.js')


    display(HTML(lib_css.render()))
    display(HTML(lib_js.render({'leaflet_dvf': leaflet_dvf.render()})))

def iter_obj(type):
    '''Decorator to keep count of different map object types in self.mk_cnt'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.mark_cnt[type] = self.mark_cnt.get(type, 0) + 1
            func_result = func(self, *args, **kwargs)
            return func_result
        return wrapper
    return decorator


class Map(object):
    '''Create a Map with Folium'''

    def __init__(self, location=None, width=960, height=500,
                 tiles='OpenStreetMap', API_key=None, max_zoom=18, min_zoom=1,
                 zoom_start=10, attr=None, min_lat=-90, max_lat=90,
                 min_lon=-180, max_lon=180,playback=False):
        '''Create a Map with Folium and Leaflet.js

        Generate a base map of given width and height with either default
        tilesets or a custom tileset URL. The following tilesets are built-in
        to Folium. Pass any of the following to the "tiles" keyword:
            -"OpenStreetMap"
            -"MapQuest Open"
            -"MapQuest Open Aerial"
            -"Mapbox Bright" (Limited levels of zoom for free tiles)
            -"Mapbox Control Room" (Limited levels of zoom for free tiles)
            -"Stamen Terrain"
            -"Stamen Toner"
            -"Cloudmade" (Must pass API key)
            -"Mapbox" (Must pass API key)
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
            Map tileset to use. Can use defaults or pass a custom URL.
        API_key: str, default None
            API key for Cloudmade or Mapbox tiles.
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
        >>>map = folium.Map(location=[45.523, -122.675],
                            tiles='Mapbox Control Room')
        >>>map = folium.Map(location=(45.523, -122.675), max_zoom=20,
                            tiles='Cloudmade', API_key='YourKey')
        >>>map = folium.Map(location=[45.523, -122.675], zoom_start=2,
                            tiles=('http://{s}.tiles.mapbox.com/v3/'
                                    'mapbox.control-room/{z}/{x}/{y}.png'),
                            attr='Mapbox attribution')

        '''

        #Inits
        self.map_path = None
        self.render_iframe = False
        self.map_type = 'base'
        self.map_id = '_'.join(['folium', uuid4().hex])

        #Mark counter, JSON, Plugins
        self.mark_cnt = {}
        self.json_data = {}
        self.plugins = {}

        #Location
        if not location:
            raise ValueError('You must pass a Lat/Lon location to initialize'
                             ' your map')
        self.location = location

        #Map Size Parameters
        self.width = width
        self.height = height
        self.map_size = {'width': width, 'height': height}
        self._size = ('style="width: {0}px; height: {1}px"'
                      .format(width, height))

        #Templates
        self.env = ENV
        self.template_vars = dict(lat=location[0],
                                  lon=location[1],
                                  size=self._size,
                                  max_zoom=max_zoom,
                                  zoom_level=zoom_start,
                                  map_id=self.map_id,
                                  min_zoom=min_zoom,
                                  min_lat=min_lat,
                                  max_lat=max_lat,
                                  min_lon=min_lon,
                                  max_lon=max_lon,
                                  playback=playback)

        #Tiles
        self.tiles = ''.join(tiles.lower().strip().split())
        if self.tiles in ('cloudmade', 'mapbox') and not API_key:
            raise ValueError('You must pass an API key if using Cloudmade'
                             ' or non-default Mapbox tiles.')

        self.default_tiles = ['openstreetmap', 'mapboxcontrolroom',
                              'mapquestopen', 'mapquestopenaerial',
                              'mapboxbright', 'mapbox', 'cloudmade',
                              'stamenterrain', 'stamentoner']
        self.tile_types = {}
        for tile in self.default_tiles:
            tile_path = 'tiles/%s' % tile
            self.tile_types[tile] = {
                'templ': self.env.get_template('%s/%s' % (tile_path,
                                                          'tiles.txt')),
                'attr': self.env.get_template('%s/%s' % (tile_path,
                                                         'attr.txt')),
            }

        if self.tiles in self.tile_types:
            self.template_vars['Tiles'] = (self.tile_types[self.tiles]['templ']
                                           .render(API_key=API_key))
            self.template_vars['attr'] = (self.tile_types[self.tiles]['attr']
                                          .render())
        else:
            self.template_vars['Tiles'] = tiles
            if not attr:
                raise ValueError('Custom tiles must'
                                 ' also be passed an attribution')
            if isinstance(attr, binary_type):
                attr = text_type(attr, 'utf8')
            self.template_vars['attr'] = attr
            self.tile_types.update({'Custom': {'template': tiles,
                                               'attr': attr}})

        self.added_layers = []
        self.template_vars.setdefault('wms_layers', [])
        self.template_vars.setdefault('tile_layers', [])
        self.template_vars.setdefault('playback_markers', [])

    @iter_obj('simple')
    def add_tile_layer(self, tile_name=None,tile_url=None,active=False):
        '''adds a simple tile layer
        Parameters
        ----------
        tile_name: string
            name of the tile layer
        tile_url: string
            url location of the tile layer
        active: boolean
            should the layer be active when added
        '''
        if not tile_name in self.added_layers:
            tile_name = tile_name.replace (" ", "_")
            tile_temp = self.env.get_template('tile_layer.js')

            tile = tile_temp.render({'tile_name': tile_name,
                                       'tile_url': tile_url
                                       })

            self.template_vars.setdefault('tile_layers', []).append((tile))

            self.added_layers.append({tile_name:tile_url})


    @iter_obj('simple')
    def add_wms_layer(self, wms_name=None, wms_url=None, wms_format=None,
                      wms_layers=None, wms_transparent=True):
        '''adds a simple tile layer
        Parameters
        ----------
        wms_name: string
            name of wms layer
        wms_url : string
            url of wms layer
        '''
        if not wms_name in self.added_layers:
            wms_name = wms_name.replace (" ", "_")
            wms_temp = self.env.get_template('wms_layer.js')

            wms = wms_temp.render({
                'wms_name': wms_name,
                'wms_url': wms_url,
                'wms_format': wms_format,
                'wms_layer_names':wms_layers,
                'wms_transparent':str(wms_transparent).lower()})

            self.template_vars.setdefault('wms_layers', []).append((wms))

            self.added_layers.append({wms_name:wms_url})

    @iter_obj('simple')
    def add_layers_to_map(self):
        '''
        Required function to actually add the layers to the html packet
        '''
        layers_temp = self.env.get_template('add_layers.js')

        data_string = ''
        for i, layer in enumerate(self.added_layers):
            name = list(layer.keys())[0]
            data_string+='\"'
            data_string+=name
            data_string+='\"'
            data_string+=': '
            data_string+=name
            if i < len(self.added_layers)-1:
                data_string+=",\n"
            else:
                data_string+="\n"

        data_layers = layers_temp.render({'layers': data_string})
        self.template_vars.setdefault('data_layers', []).append((data_string))

    @iter_obj('playback')
    def playback_marker(self, location=None, popup='Pop Text', popup_on=True,
                      marker_color='blue', marker_icon='info-sign',
                      playback_marker=True, time=datetime.datetime.now(), icon_angle=0, width=300):
        '''Create a time enabled Leaflet marker on the map, with optional
        popup text or Vincent visualization.        
        '''
        print ('create playback marker')
        pass


    @iter_obj('simple')
    def simple_marker(self, location=None, popup='Pop Text', popup_on=True,
                      marker_color='blue', marker_icon='info-sign',
                      clustered_marker=False, icon_angle=0, width=300):
        '''Create a simple stock Leaflet marker on the map, with optional
        popup text or Vincent visualization.

        Parameters
        ----------
        location: tuple or list, default None
            Latitude and Longitude of Marker (Northing, Easting)
        popup: string or tuple, default 'Pop Text'
            Input text or visualization for object. Can pass either text,
            or a tuple of the form (Vincent object, 'vis_path.json')
            It is possible to adjust the width of text/HTML popups
            using the optional keywords `width`.  (Leaflet default is 300px.)
        popup_on: boolean, default True
            Pass false for no popup information on the marker
        marker_color
            color of marker you want
        marker_icon
            icon from (http://getbootstrap.com/components/) you want on the marker
        clustered_marker
            boolean of whether or not you want the marker clustered with
            other markers

        Returns
        -------
        Marker names and HTML in obj.template_vars

        Example
        -------
        >>>map.simple_marker(location=[45.5, -122.3], popup='Portland, OR')
        >>>map.simple_marker(location=[45.5, -122.3], popup=(vis, 'vis.json'))

        '''
        count = self.mark_cnt['simple']

        mark_temp = self.env.get_template('simple_marker.js')

        marker_num = 'marker_{0}'.format(count)
        add_line = "{'icon':"+marker_num+"_icon}"

        icon_temp = self.env.get_template('simple_icon.js')
        icon = icon_temp.render({'icon': marker_icon,
                                 'icon_name': marker_num+"_icon",
                                 'markerColor': marker_color,
                                 'icon_angle': icon_angle
                                })

        #Get marker and popup
        marker = mark_temp.render({'marker': 'marker_' + str(count),
                                   'lat': location[0],
                                   'lon': location[1],
                                   'icon': add_line
                                   })

        popup_out = self._popup_render(popup=popup, mk_name='marker_',
                                       count=count, popup_on=popup_on,
                                       width=width)



        if clustered_marker:
            add_mark = 'clusteredmarkers.addLayer(marker_{0})'.format(count)
            self.template_vars.setdefault('cluster_markers', []).append((icon,
                                                             marker,
                                                             popup_out,
                                                             add_mark))
        else:
            add_mark = 'map.addLayer(marker_{0})'.format(count)
            self.template_vars.setdefault('custom_markers', []).append((icon,
                                                             marker,
                                                             popup_out,
                                                             add_mark))

    @iter_obj('line')
    def line(self, locations,
             line_color=None, line_opacity=None, line_weight=None):
        '''Add a line to the map with optional styles.

        Parameters
        ----------
        locations: list of points (latitude, longitude)
            Latitude and Longitude of line (Northing, Easting)
        line_color: string, default Leaflet's default ('#03f')
        line_opacity: float, default Leaflet's default (0.5)
        line_weight: float, default Leaflet's default (5)

        Note: If the optional styles are omitted, they will not be included
        in the HTML output and will obtain the Leaflet defaults listed above.

        Example
        -------
        >>>map.line(locations=[(45.5, -122.3), (42.3, -71.0)])
        >>>map.line(locations=[(45.5, -122.3), (42.3, -71.0)],
                    line_color='red', line_opacity=1.0)

        '''
        count = self.mark_cnt['line']

        line_temp = self.env.get_template('polyline.js')

        polyline_opts = {'color': line_color,
                'weight': line_weight,
                'opacity': line_opacity}

        varname = 'line_{}'.format(count)
        line_rendered = line_temp.render({'line': varname,
                                          'locations': locations,
                                          'options': polyline_opts})

        add_line = 'map.addLayer({});'.format(varname)

        self.template_vars.setdefault('lines', []).append((line_rendered,
                                                           add_line))


    @iter_obj('multiline')
    def multiline(self, locations,
             line_color=None, line_opacity=None, line_weight=None):
        '''Add a multiPolyline to the map with optional styles.

        A multiPolyline is single layer that consists of several polylines that
        share styling/popup.

        Parameters
        ----------
        locations: list of lists of points (latitude, longitude)
            Latitude and Longitude of line (Northing, Easting)
        line_color: string, default Leaflet's default ('#03f')
        line_opacity: float, default Leaflet's default (0.5)
        line_weight: float, default Leaflet's default (5)

        Note: If the optional styles are omitted, they will not be included
        in the HTML output and will obtain the Leaflet defaults listed above.

        Example
        -------
        >>>map.multiline(locations=[[(45.5236, -122.6750), (45.5236, -122.6751)],
                                    [(45.5237, -122.6750), (45.5237, -122.6751)],
                                    [(45.5238, -122.6750), (45.5238, -122.6751)]])
        >>>map.multiline(locations=[[(45.5236, -122.6750), (45.5236, -122.6751)],
                                    [(45.5237, -122.6750), (45.5237, -122.6751)],
                                    [(45.5238, -122.6750), (45.5238, -122.6751)]],
                                    line_color='red',
                                    line_weight=2,
                                    line_opacity=1.0)
        '''

        count = self.mark_cnt['multiline']

        multiline_temp = self.env.get_template('multi_polyline.js')

        multiline_opts = {'color': line_color,
                'weight': line_weight,
                'opacity': line_opacity}

        varname = 'multiline_{}'.format(count)
        multiline_rendered = multiline_temp.render({'multiline': varname,
                                          'locations': locations,
                                          'options': multiline_opts})

        add_multiline = 'map.addLayer({});'.format(varname)

        self.template_vars.setdefault('multilines', []).append((multiline_rendered,
                                                           add_multiline))



    @iter_obj('circle')
    def circle_marker(self, location=None, radius=500, popup='Pop Text',
                      popup_on=True, line_color='black', fill_color='black',
                      fill_opacity=0.6):
        '''Create a simple circle marker on the map, with optional popup text
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
                             radius=1000, popup='Portland, OR')
        >>>map.circle_marker(location=[45.5, -122.3],
                             radius=1000, popup=(bar_chart, 'bar_data.json'))

        '''
        count = self.mark_cnt['circle']

        circle_temp = self.env.get_template('circle_marker.js')

        circle = circle_temp.render({'circle': 'circle_' + str(count),
                                     'radius': radius,
                                     'lat': location[0], 'lon': location[1],
                                     'line_color': line_color,
                                     'fill_color': fill_color,
                                     'fill_opacity': fill_opacity})

        popup_out = self._popup_render(popup=popup, mk_name='circle_',
                                       count=count,
                                       popup_on=popup_on)

        add_mark = 'map.addLayer(circle_{0})'.format(count)

        self.template_vars.setdefault('markers', []).append((circle,
                                                             popup_out,
                                                             add_mark))

    @iter_obj('polygon')
    def polygon_marker(self, location=None, line_color='black', line_opacity=1,
                       line_weight=2, fill_color='blue', fill_opacity=1,
                       num_sides=4, rotation=0, radius=15, popup='Pop Text',
                       popup_on=True):
        '''Custom markers using the Leaflet Data Vis Framework.


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
        popup_on: boolean, default True
            Pass false for no popup information on the marker

        Returns
        -------
        Polygon marker names and HTML in obj.template_vars

        '''

        count = self.mark_cnt['polygon']

        poly_temp = self.env.get_template('poly_marker.js')

        polygon = poly_temp.render({'marker': 'polygon_' + str(count),
                                    'lat': location[0],
                                    'lon': location[1],
                                    'line_color': line_color,
                                    'line_opacity': line_opacity,
                                    'line_weight': line_weight,
                                    'fill_color': fill_color,
                                    'fill_opacity': fill_opacity,
                                    'num_sides': num_sides,
                                    'rotation': rotation,
                                    'radius': radius})

        popup_out = self._popup_render(popup=popup, mk_name='polygon_',
                                       count=count,
                                       popup_on=popup_on)

        add_mark = 'map.addLayer(polygon_{0})'.format(count)

        self.template_vars.setdefault('markers', []).append((polygon,
                                                             popup_out,
                                                             add_mark))
        #Update JS/CSS and other Plugin files
        js_temp = self.env.get_template('dvf_js_ref.txt').render()
        self.template_vars.update({'dvf_js': js_temp})

        polygon_js = resource_string('folium',
                                     'plugins/leaflet-dvf.markers.min.js')

        self.plugins.update({'leaflet-dvf.markers.min.js': polygon_js})

    def lat_lng_popover(self):
        '''Enable popovers to display Lat and Lon on each click'''

        latlng_temp = self.env.get_template('lat_lng_popover.js')
        self.template_vars.update({'lat_lng_pop': latlng_temp.render()})

    def click_for_marker(self, popup=None):
        '''Enable the addition of markers via clicking on the map. The marker
        popup defaults to Lat/Lon, but custom text can be passed via the
        popup parameter. Double click markers to remove them.

        Parameters
        ----------
        popup:
            Custom popup text

        Example
        -------
        >>>map.click_for_marker(popup='Your Custom Text')

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
                      popup_on=True, width=300):
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
                                          'pop_txt': json.dumps(popup),
                                          'width': width})
            elif isinstance(popup, tuple):
                #Update template with JS libs
                vega_temp = self.env.get_template('vega_ref.txt').render()
                jquery_temp = self.env.get_template('jquery_ref.txt').render()
                d3_temp = self.env.get_template('d3_ref.txt').render()
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
                width = vega.width
                height = vega.height
                if isinstance(vega.padding, dict):
                    width += vega.padding['left']+vega.padding['right']
                    height += vega.padding['top']+vega.padding['bottom']
                else:
                    width += 75
                    height += 50
                max_width = self.map_size['width']
                vega_id = '#' + div_id
                popup_temp = self.env.get_template('vega_marker.js')
                return popup_temp.render({'mark': mark, 'div_id': div_id,
                                          'width': width, 'height': height,
                                          'max_width': max_width,
                                          'json_out': json_out,
                                          'vega_id': vega_id})

    @iter_obj('geojson')
    def geo_json(self, geo_path=None, geo_str=None, data_out='data.json',
                 data=None, columns=None, key_on=None, threshold_scale=None,
                 fill_color='blue', fill_opacity=0.6, line_color='black',
                 line_weight=1, line_opacity=1, legend_name=None,
                 topojson=None, reset=False):
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
        legend_name: string, default None
            Title for data legend. If not passed, defaults to columns[1].
        topojson: string, default None
            If using a TopoJSON, passing "objects.yourfeature" to the topojson
            keyword argument will enable conversion to GeoJSON.
        reset: boolean, default False
            Remove all current geoJSON layers, start with new layer

        Output
        ------
        GeoJSON data layer in obj.template_vars

        Example
        -------
        >>>map.geo_json(geo_path='us-states.json', line_color='blue',
                        line_weight=3)
        >>>map.geo_json(geo_path='geo.json', data=df,
                        columns=['Data 1', 'Data 2'],
                        key_on='feature.properties.myvalue', fill_color='PuBu',
                        threshold_scale=[0, 20, 30, 40, 50, 60])
        >>>map.geo_json(geo_path='countries.json', topojson='objects.countries')
        '''

        if reset:
            reset_vars = ['json_paths', 'func_vars', 'color_scales',
                          'geo_styles', 'gjson_layers', 'map_legends',
                          'topo_convert']
            for var in reset_vars:
                self.template_vars.update({var: []})
            self.mark_cnt['geojson'] = 1

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

        #Set map type to geojson
        self.map_type = 'geojson'

        #Get JSON map layer template pieces, convert TopoJSON if necessary
        # geo_str is really a hack
        if geo_path:
            geo_path = ".defer(d3.json, '{0}')".format(geo_path)
        elif geo_str:
            geo_path = (".defer(function(callback)"
                        "{{callback(null, JSON.parse('{}'))}})").format(geo_str)

        if topojson is None:
            map_var = '_'.join(['gjson', str(self.mark_cnt['geojson'])])
            layer_var = map_var
        else:
            map_var = '_'.join(['tjson', str(self.mark_cnt['geojson'])])
            topo_obj = '.'.join([map_var, topojson])
            layer_var = '_'.join(['topo', str(self.mark_cnt['geojson'])])
            topo_templ = self.env.get_template('topo_func.js')
            topo_func = topo_templ.render({'map_var': layer_var,
                                           't_var': map_var,
                                           't_var_obj': topo_obj})
            topo_lib = self.env.get_template('topojson_ref.txt').render()
            self.template_vars.update({'topojson': topo_lib})
            self.template_vars.setdefault('topo_convert',
                                          []).append(topo_func)

        style_count = '_'.join(['style', str(self.mark_cnt['geojson'])])

        #Get Data binding pieces if available
        if data is not None:

            import pandas as pd

            #Create DataFrame with only the relevant columns
            if isinstance(data, pd.DataFrame):
                data = pd.concat([data[columns[0]], data[columns[1]]], axis=1)

            #Save data to JSON
            self.json_data[data_out] = utilities.transform_data(data)

            #Add data to queue
            d_path = ".defer(d3.json, '{0}')".format(data_out)
            self.template_vars.setdefault('json_paths', []).append(d_path)

            #Add data variable to makeMap function
            data_var = '_'.join(['data', str(self.mark_cnt['geojson'])])
            self.template_vars.setdefault('func_vars', []).append(data_var)

            #D3 Color scale
            series = data[columns[1]]
            if threshold_scale and len(threshold_scale) > 6:
                raise ValueError
            domain = threshold_scale or utilities.split_six(series=series)
            if len(domain) > 253:
                raise ValueError('The threshold scale must be of length <= 253')
            if not utilities.color_brewer(fill_color):
                raise ValueError('Please pass a valid color brewer code to '
                                 'fill_local. See docstring for valid codes.')

            palette = utilities.color_brewer(fill_color, len(domain))
            d3range = palette[0: len(domain) + 1]
            tick_labels = utilities.legend_scaler(domain)

            color_temp = self.env.get_template('d3_threshold.js')
            d3scale = color_temp.render({'domain': domain,
                                         'range': d3range})
            self.template_vars.setdefault('color_scales', []).append(d3scale)

            #Create legend
            name = legend_name or columns[1]
            leg_templ = self.env.get_template('d3_map_legend.js')
            legend = leg_templ.render({'lin_max': int(domain[-1]*1.1),
                                       'tick_labels': tick_labels,
                                       'caption': name})
            self.template_vars.setdefault('map_legends', []).append(legend)

            #Style with color brewer colors
            matchColor = 'color(matchKey({0}, {1}))'.format(key_on, data_var)
            style = json_style(style_count, line_color, line_weight,
                               line_opacity, None, fill_opacity, matchColor)
        else:
            style = json_style(style_count, line_color, line_weight,
                               line_opacity, fill_color, fill_opacity, None)

        layer = ('gJson_layer_{0} = L.geoJson({1}, {{style: {2}}}).addTo(map)'
                 .format(self.mark_cnt['geojson'], layer_var, style_count))

        self.template_vars.setdefault('json_paths', []).append(geo_path)
        self.template_vars.setdefault('func_vars', []).append(map_var)
        self.template_vars.setdefault('geo_styles', []).append(style)
        self.template_vars.setdefault('gjson_layers', []).append(layer)

    def _build_map(self, html_templ=None, templ_type='string'):
        '''Build HTML/JS/CSS from Templates given current map type'''
        if html_templ is None:
            map_types = {'base': 'fol_template.html',
                         'geojson': 'geojson_template.html'}

            #Check current map type
            type_temp = map_types[self.map_type]

            html_templ = self.env.get_template(type_temp)
        else:
            if templ_type == 'string':
                html_templ = self.env.from_string(html_templ)

        self.HTML = html_templ.render(self.template_vars)

    def create_map(self, path='map.html', plugin_data_out=True, template=None):
        '''Write Map output to HTML and data output to JSON if available

        Parameters:
        -----------
        path: string, default 'map.html'
            Path for HTML output for map
        plugin_data_out: boolean, default True
            If using plugins such as awesome markers, write all plugin
            data such as JS/CSS/images to path
        template: string, default None
            Custom template to render

        '''
        self.map_path = path
        self._build_map(template)

        with codecs.open(path, 'w', 'utf8') as f:
            f.write(self.HTML)

        if self.json_data:
            for path, data in iteritems(self.json_data):
                with open(path, 'w') as g:
                    json.dump(data, g)

        if self.plugins and plugin_data_out:
            for name, plugin in iteritems(self.plugins):
                with open(name, 'w') as f:
                    if isinstance(plugin, binary_type):
                        plugin = text_type(plugin, 'utf8')
                    f.write(plugin)

    def _repr_html_(self):
        """Build the HTML representation for IPython."""
        map_types = {'base': 'ipynb_repr.html',
                     'geojson': 'ipynb_iframe.html'}

        #Check current map type
        type_temp = map_types[self.map_type]
        if self.render_iframe:
            type_temp = 'ipynb_iframe.html'
        templ = self.env.get_template(type_temp)
        self._build_map(html_templ=templ, templ_type='temp')
        if self.map_type == 'geojson' or self.render_iframe:
            if not self.map_path:
                raise ValueError('Use create_map to set the path!')
            return templ.render(path=self.map_path, width=self.width,
                                height=self.height)
        return self.HTML

    def display(self):
        """Display the visualization inline in the IPython notebook.

        This is deprecated, use the following instead::

            from IPython.display import display
            display(viz)
        """
        from IPython.core.display import display, HTML
        display(HTML(self._repr_html_()))
