.. Folium documentation master file, created by

Folium: Python Data. Leaflet.js Maps.
====================================

Folium builds on the data wrangling strengths of the Python ecosystem and the mapping strengths of the Leaflet.js library. Manipulate your data in Python, then visualize it in on a Leaflet map via Folium.

Concept
-------
Folium makes it easy to visualize data that's been manipulated in Python on an interactive Leaflet map. It enables both the binding of data to a map for choropleth visualizations as well as passing Vincent/Vega visualizations as markers on the map.

The library has a number of built-in tilesets from OpenStreetMap, Mapbox, and Stamen, and supports custom tilesets with Mapbox or Cloudmade API keys. Folium supports both GeoJSON and TopoJSON overlays, as well as the binding of data to those overlays to create choropleth maps with color-brewer color schemes.

Installation
------------
::

$pip install folium

Base Maps
---------

To create a base map, simply pass starting coordinates to Folium, then create the map::

    import folium
    map_osm = folium.Map(location=[45.5236, -122.6750])
    map_osm.create_map(path='osm.html')

`Live example <http://bl.ocks.org/wrobstory/5545719>`_

Folium defaults to 960 x 500 pixels (to make it easy to generate maps for `bl.ocks <http://bl.ocks.org>`_ ). You can modify the width and height easily::

    map = folium.Map(location=[45.5236, -122.6750],  width=500, height = 300)

Folium also supports two zoom parameters:

- zoom_start:  The starting zoom level.
- max_zoom:  The maximum possible zoom.

::

    map = folium.Map(location=[45.5236, -122.6750], zoom_start=10, max_zoom=15)

Tilesets
~~~~~~~~

Folium natively supports five tilesets with no API key or custom URL required. You can pass any of the following strings to the `tiles` keyword:

- `'OpenStreetMap'`
- `'Mapbox Bright'`  (Limited levels of zoom)
- `'Mapbox Control Room'` (Limited levels of zoom)
- `'Stamen Terrain'`
- `'Stamen Toner'`

Example::

    map = folium.Map(location=[45.523, -122.675], tiles='Mapbox Control Room')

Folium also supports both Mapbox and Cloudmade tiles with an API key passed::

    map = folium.Map(location=[45.5236, -122.6750], tiles='Mapbox',
                     API_key='wrobstory.map-12345678')

Finally, Folium supports passing your own tile URL and attribution::

    tileset = r'http://{s}.tiles.yourtiles.com/{z}/{x}/{y}.png'
    map = folium.Map(location=[45.372, -121.6972], zoom_start=12,
                     tiles=tileset, attr='My Data Attribution')

Markers
-------

Folium supports of a number of different marker types, including simple markers, circle markers, and polygon markers. All markers support both text and `Vincent <https://github.com/wrobstory/vincent>`_ visualizations as popups.

Simple Markers
~~~~~~~~~~~~~~

`Live example <http://bl.ocks.org/wrobstory/5609718>`_

The simplest type is the standard Leaflet marker, which is referred to as the `simple_marker` in Folium::

    map.simple_marker([45.3288, -121.6625])

The marker can be passed a text string (which can be HTML formatted) for the popup message::

    map_1.simple_marker([45.3288, -121.6625], popup='My Popup Message')

To turn the popup off, pass `False` to the `popup_on` keyword::

    map_1.simple_marker([45.3288, -121.6625], popup_on=False)

Circle Markers
~~~~~~~~~~~~~~

`Live example <http://bl.ocks.org/wrobstory/5609747>`_

Circle markers are exactly what they sound like- simple circles on the map. The user can define the following parameters:

- `radius`: Circle radius in pixels
- `line_color`: Outer line color, either a simple color (blue, black, etc), or a hex string
- `fill_color`: Inner fill color, again simple or hex
- `fill_opacity`: Inner fill opacity

The popup rules covered in simple markers apply for all other markers types::

    map.circle_marker(location=[45.5215, -122.6261], radius=500,
                      popup='My Popup Info', line_color='#3186cc',
                      fill_color='#3186cc', fill_opacity=0.2)

Polygon Markers
~~~~~~~~~~~~~~

`Live example <http://bl.ocks.org/wrobstory/5609786>`_

Polygon markers are based on the `Leaflet DVF Framework <https://github.com/humangeo/leaflet-dvf>`_.They take a number of parameters that define their color and shape:

- `line_color`: Outer line color, either a simple color (blue, black, etc), or a hex string
- `line_opacity`: Outer line opacity
- `line_weight`: Outer line weight, in pixels
- `fill_color`: Inner fill color, again simple or hex
- `fill_opacity`: Inner fill opacity
- `num_sides`: Number of sides on the marker. `3` creates a triangle, `6` a hexagon, etc.
- `rotation`: Rotation of the marker in degrees
- `radius`: Circle radius in pixels

::

    map_5.polygon_marker(location=[45.5012, -122.6655], popup='Ross Island Bridge',
                         fill_color='#132b5e', num_sides=3, radius=10, rotation=60)

Lat/Lng Popups
~~~~~~~~~~~~~~

`Live example <http://bl.ocks.org/wrobstory/5609756>`_

Folium supports a convenience function that will enable Lat/Lng popups anywhere you click on the map, using the following method::

    map.lat_lng_popover()

Click-for-Marker
~~~~~~~~~~~~~~~~

`Live example <http://bl.ocks.org/wrobstory/5609762>`_

Use the `click_for_marker` method to enable a marker on each map click, with custom text if desired. Double-click to remove the marker::

    map.click_for_marker(popup='Waypoint')

Vincent Popups
~~~~~~~~~~~~~~

`Live example <http://bl.ocks.org/wrobstory/5609803>`_

The popup parameter in any marker can be passed a `Vincent <https://github.com/wrobstory/vincent>`_ visualization as the popup. Vincent visualizations must be passed as a tuple of the form `(vincent_object, vis_path)`, where `vis_path` is the path to your Vincent.vega json output::

    vis = vincent.Bar()
    vis.tabular_data([10, 20, 30, 40, 30, 20])
    vis.to_json('vis.json')
    map.polygon_marker(location=[45.5, -122.5], popup=(vis, 'vis.json'))

Other features
--------------

Polyline
~~~~~~~~

You can plot a line by simply passing an iterable of coordinates to the method `line`::

    map.line(locations=[[45.3288, -121.6625],
        [45.324224, -121.657763]
        [45.318702, -121.652871]])

You can specify the following parameters:

- `line_color`: line color, either a simple color (blue, black, etc), or a hex string
- `line_weight`: line weight, in pixels
- `line_opacity`: fill opacity

Polylines also support popups, through the `popup` and `popup_on` parameters, similarly to markers.


Data Mapping: GeoJSON and TopoJSON
----------------------------------

Folium allows you to plot a GeoJSON or TopoJSON overlay on the map. There is no requirement to bind data (passing just a Geo/TopoJSON will plot a single color overlay), but there is a data binding option to map Python Pandas columnar data to different feature objects on a color scale. Folium allows you to pass multiple Geo/TopoJSON datasets if you desire to create multiple overlays on a single map.

Let's start with a simple GeoJSON. Just pass the path to your file, and it will be plotted as an overlay::

    map.geo_json(geo_path='my_geo.json')

A short primer on ogr2ogr and TopoJSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TopoJSON is just as simple, but requires one additional parameter, which is the object feature that will be converted in the browser to a GeoJSON. See the TopoJSON `topojson.feature` method `API reference <https://github.com/mbostock/topojson/wiki/API-Reference#wiki-feature>`_ for further details. The second passed parameter typically starts with `objects` in a standard TopoJSON conversion::

    map.geo_json(geo_path='us_states.json', topojson='objects.states')

Here are a couple tips to avoid headaches when working with Leaflet maps and geo files. First, for this particular ogr2ogr->topoJSON workflow, I've had the best luck with EPSG:4326 (a geographic coordinate system with WGS84 datum) without having to muck around in Leaflet with projection settings. The ogr2ogr command could look something like this::

    $ogr2ogr -f 'ESRI Shapefile' -t_srs 'EPSG:4326' output.shp input.shp

Converting with a TopoJSON command in it's simplest form would look like the following::

    $topojson -o output.json input.shp

If using those commands verbatim, the `geo_json` input would then look like the following::

    map.geo_json(geo_path='ouput.json', topojson='objects.input')

A more realistic dataset would look something like::

    $ogr2ogr -f 'ESRI Shapefile' -t_srs 'EPSG:4326' countries_4326.shp countries.shp
    $topojson -o countries.json countries_4326.shp

and then in Python::

    map.geo_json(geo_path='countries.json', topojson='objects.countries_4326')

Binding Data
~~~~~~~~~~~~

One of the key features of Folium is the ability to bind data from a Pandas DataFrame or Series to a GeoJSON or TopoJSON. Let's walk through the key parameters:

- `data_out`: That data from the DataFrame/Series will be written to this path and read by Leaflet/D3
- `data`: The Pandas DataFrame or Series
- `columns`: A dict or tuple. The first value must reference the column with the "key" data, aka the value that needs to match that of the Geo/TopoJSON parameters. The second must reference the column of the values that are being mapped.
- `key_on`: The value in the Geo/TopoJSON that is being bound to the Pandas data. This value must always start with `'feature'`. Ex: `'feature.id'` or `'feature.properties.statename'`

::

    map.geo_json(geo_path='geo.json', data_out='data.json', data=df,
                 columns=['Keys', 'Values'], key_on='features.properties.key')

As a more realistic example, here is what it would look like to map data from State Names to Unemployment levels::

    map.geo_json(geo_path=state_geo, data=state_data,
                 columns=['State', 'Unemployment'],
                 key_on='feature.id',
                 fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
                 legend_name='Unemployment Rate (%)')

`Live example <http://bl.ocks.org/wrobstory/5609830>`_

Color Scales
~~~~~~~~~~~~

Folium currently supports D3 threshold scales. By default, Folium uses the following range of quantiles as the scale values: `[0, 0.5, 0.75, 0.85, 0.9]`, with each rounded to the nearest order-of-magnitude integer. So, for instance, 270 rounds to 200, 5600 to 6000, and so on.

Here's a live example of a `default threshold scale <http://bl.ocks.org/wrobstory/5609830>`_

You are also free to pass your own scale to the `threshold_scale` keyword. For example::

    map.geo_json(geo_path=state_geo, data=state_data,
                 columns=['State', 'Unemployment'],
                 threshold_scale=[5, 6, 7, 8, 9, 10],
                 key_on='feature.id',
                 fill_color='BuPu', fill_opacity=0.7, line_opacity=0.5,
                 legend_name='Unemployment Rate (%)',
                 reset=True)

`Live example <http://bl.ocks.org/wrobstory/5609856>`_

The colors for these scales come from the `color brewer <http://colorbrewer2.org/>`_ sequential scales. Any of the following can be passed to the `fill_color` keyword:

- `BuGn`
- `BuPu`
- `GnBu`
- `OrRd`
- `PuBu`
- `PuBuGn`
- `PuRd`
- `RdPu`
- `YlGn`
- `YlGnBu`
- `YlOrBr`
- `YlOrRd`

Misc GeoJSON Parameters
~~~~~~~~~~~~~~~~~~~~~~~

The following parameters will be of use when creating Geo/TopoJSON layers:

- `legend_name`: Pass a custom name to the legend. Defaults to the DataFrame/Series column name
- `reset`: Deletes all previous map data, starts fresh with new dataset being passed.

Choropleth Examples
~~~~~~~~~~~~~~~~~~~

The following live examples demonstrate how to use multiple columns of the same dataframe with different color scales to visualize multiple datasets quickly:

- `US Employed by county <http://bl.ocks.org/wrobstory/5609889>`_, `'YlOrRd'` colorbrew, default legend title and scale
- `US Unemployed by county <http://bl.ocks.org/wrobstory/5609934>`_, `'YlGnBu'` colorbrew, custom scale and legend title
- `US Median Household Income by county <http://bl.ocks.org/wrobstory/5609959>`_, `'PuRd'` colorbrew, custom scale and legend title

Create Map
----------

The `create_map` method writes your HTML (and JSON/JS if necessary) to the path of your choice. The `plugin_data_out` parameter can be set to `'False`' if you don't wish to write any JavaScript plugin libraries to your path.


Contents:

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`search`

