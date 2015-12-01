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

Folium is compatible with Python 2 as well as Python 3.

Base Maps
---------

To create a base map, call on the `Map` class::

    Map(location=None, width='100%', height='100%', tiles='OpenStreetMap', API_key=None, max_zoom=18, min_zoom=1, zoom_start=10, attr=None, min_lat=-90, max_lat=90, min_lon=-180, max_lon=180, detect_retina=False)

Parameters:

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
	    If true and user is on a retina display, it will request four
	    tiles of half the specified size and a bigger zoom level in place
	    of one to utilize the high resolution.

Returns:

	folium.Map object


Example::

    import folium
    fo_map = folium.Map(location=[45.5236, -122.6750])

You can modify the width and height easily of the map using pixels or percentage::

    fo_map = folium.Map(location=[45.5236, -122.6750], width=500, height = 300)

Folium also supports three zoom parameters:


::

    fo_map = folium.Map(location=[45.5236, -122.6750], zoom_start=10, max_zoom=15)

To save the map to file, simply call the `.save()` function which can take a string or a file object::

    fo_map.save('fo_map.html')

`Base Maps - Live example <http://bl.ocks.org/wrobstory/5545719>`_

Tilesets
~~~~~~~~

Folium natively supports five tilesets with no API key or custom URL required. You can pass any of the following strings to the `tiles` keyword:

- `'OpenStreetMap'` (Default)
- `'MapQuest Open'`
- `'MapQuest Open Aerial'`
- `'Mapbox Bright'`  (Limited levels of zoom)
- `'Mapbox Control Room'` (Limited levels of zoom)
- `'Stamen'` (Terrain, Toner, and Watercolor)
- `'Cloudmade'` (Must pass API key)
- `'Mapbox'` (Must pass API key)
- `'CartoDB'` (positron and dark_matter)

Example::

    fo_map = folium.Map(location=[45.523, -122.675], tiles='Mapbox Control Room')

Folium also supports both Mapbox and Cloudmade tiles with an API key passed::

    fo_map = folium.Map(location=[45.5236, -122.6750], tiles='Mapbox', API_key='wrobstory.map-12345678')

Finally, Folium supports passing your own tile URL and attribution::

    tileset = r'http://{s}.tiles.yourtiles.com/{z}/{x}/{y}.png'
    fo_map = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles=tileset)

Adding Elements
-------

Folium supports a number of different Leaflet elements that can be added to the map. Some of these are markers support `Vincent <https://github.com/wrobstory/vincent>`_ visualizations, text, and HTML formatting as popups. In order to add the marker to the map, `add_children` can be called on the variable assigned to the map::

	fo_map.add_children(child, name=None, index=None)

Parameters:

	child: element name, required
		Created element, e.g. Markers
	name: string, default None
		Custom name to be given to child
	index: integer, default None
		Custom number to assign to child

::

Standard Markers
~~~~~~~~~~~~~~

The simplest type is the standard marker, which is referred to as `Marker` in Folium::

    Marker(location, popup=None, icon=None)


Example::

    standard_marker = folium.Marker(location=[45.3288, -121.6625])
    fo_map.addchildren(standard_marker)

The marker can accept the previously assigned `simple_popup` variable, which can be HTML formatted, as the message::

    standard_marker = folium.Marker(location=[45.3288, -121.6625], popup='My Popup')

`Standard Markers - Live example <http://bl.ocks.org/wrobstory/5609718>`_

Circle Markers
~~~~~~~~~~~~~~

Circle markers are exactly what they sound like- simple circles on the map. The user can define the following parameters::

	CircleMarker(location, radius=500, color='black', fill_color='black', fill_opacity=0.6, popup=None)

Example::

    circle_marker = folium.CircleMarker(location=[45.5215, -122.6261], color='#3186cc', fill_color='#3186cc', fill_opacity=0.2)
    fo_map.addchildren(circle_marker)

`Circle Markers - Live example <http://bl.ocks.org/wrobstory/5609747>`_

Polygon Markers
~~~~~~~~~~~~~~

To create custom shape polygons, the `RegularPolygonMarker` can be used by varying its parameters as needed::

	RegularPolygonMarker(location, popup=None, color='black', opacity=1, weight=2, fill_color='blue', fill_opacity=1, number_of_sides=4, rotation=0, radius=15)


Example::

	poly_maker = folium.RegularPolygonMarker(location=[45.5012, -122.6655], popup='Ross Island Bridge', color='#132b5e', number_of_sides=3, radius=10, rotation=60)
	fo_map.add_children(poly_maker)


Polygon markers are based on the `Leaflet DVF Framework <https://github.com/humangeo/leaflet-dvf>`_.They take a number of parameters that define their color and shape:

- `line_color`: Outer line color, either a simple color (blue, black, etc), or a hex string
- `line_opacity`: Outer line opacity
- `line_weight`: Outer line weight, in pixels
- `fill_color`: Inner fill color, again simple or hex
- `fill_opacity`: Inner fill opacity
- `num_sides`: Number of sides on the marker. `3` creates a triangle, `6` a hexagon, etc.
- `rotation`: Rotation of the marker in degrees
- `radius`: Circle radius in pixels


`Polygon Markers - Live example <http://bl.ocks.org/wrobstory/5609786>`_

Live Markers
~~~~~~~~~~~~~~~~

Use the `ClickForMarker` method to enable a marker on each map click, with custom text if desired. Double-click to remove the marker::

    folium.ClickForMarker(popup='Waypoint')


`Click For Marker - Live example <http://bl.ocks.org/wrobstory/5609762>`_

Vincent Popups
~~~~~~~~~~~~~~

`Live example <http://bl.ocks.org/wrobstory/5609803>`_

The popup parameter in any marker can be passed a `Vincent <https://github.com/wrobstory/vincent>`_ visualization as the popup. Vincent visualizations must be passed as a tuple of the form `(vincent_object, vis_path)`, where `vis_path` is the path to your Vincent.vega json output::

    vis = vincent.Bar()
    vis.tabular_data([10, 20, 30, 40, 30, 20])
    vis.to_json('vis.json')
    map.polygon_marker(location=[45.5, -122.5], popup=(vis, 'vis.json'))

Poly Lines
--------------

Polyline
~~~~~~~~

You can plot a line by passing an iterable of coordinates to the method `PolyLine`::

	folium.Polyline(locations, color=None, weight=None, opacity=None, latlon=True)


Example::

    p_line = folium.PolyLine(locations=[[45.3288, -121.6625], [45.324224, -121.657763], [45.318702, -121.652871]])
    fo_map.add_children(p_line)


Multiple Polylines
~~~~~~~~~~~~~~

To add multiple Polylines into a single layer, the `MultiPolyLine` class can be instantiated with an array of arrays::

	folium.Polyline(locations, color=None, weight=None, opacity=None, latlon=True)


Other Features
--------------

Assigning Popups
~~~~~~~~~~~~~~

In order to provide additional customization to the popup, the `Popup` class can be called using the following::

	folium.Popup(html, max_width=300)

Example::

	simple_popup = folium.Popup('My Popup', max_width=500)
	standard_marker = folium.Marker(location=[45.3288, -121.6625], popup=simple_popup)


Lat/Lng Popups
~~~~~~~~~~~~~~

Folium supports a convenient method that will enable Lat/Lng popups anywhere you click on the map, using the following method::

    folium.LatLngPopup()

`Lat/Long Popup - Live example <http://bl.ocks.org/wrobstory/5609756>`_

Layer Control
~~~~~~~~~~~~~~

If multiple layers are present, `LayerControl()` allows them to be listed and provide `FeatureGroup` (see next item) then ability to turn them on or off::

	folium.LayerControl()

Feature Group
~~~~~~~~~~~~~~

To control multiple objects simultaneously, the `FeatureGroup` instance can be called and individual elements can be added as needed::

	folium.FeatureGroup(name=None, overlay=True)

Example::

	fo_map = folium.Map(location=[45.5012, -122.6655])

	circle_marker = folium.CircleMarker(location=[45.5215, -122.6261], color='black', fill_color='black', fill_opacity=1)

	feature_group = folium.FeatureGroup()
	feature_group.add_children(circle_marker)

	
	fo_map.add_children(feature_group)
	fo_map.add_children(folium.LayerControl())

	fo_map.save('map.html')



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
                 columns=['Keys', 'Values'], key_on='feature.properties.key')

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

