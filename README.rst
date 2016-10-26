.. image:: https://badge.fury.io/py/folium.png
   :target: http://badge.fury.io/py/folium
.. image:: https://api.travis-ci.org/python-visualization/folium.png?branch=master
   :target: https://travis-ci.org/python-visualization/folium
.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/python-visualization/folium?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. image:: https://zenodo.org/badge/18669/python-visualization/folium.svg
   :target: https://zenodo.org/badge/latestdoi/18669/python-visualization/folium

Folium
======

|Folium|

Python Data. Leaflet.js Maps.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Folium builds on the data wrangling strengths of the Python ecosystem
and the mapping strengths of the Leaflet.js library. Manipulate your
data in Python, then visualize it in on a Leaflet map via Folium.

Concept
-------

Folium makes it easy to visualize data that's been manipulated in Python
on an interactive Leaflet map. It enables both the binding of data to a
map for choropleth visualizations as well as passing Vincent/Vega
visualizations as markers on the map.

The library has a number of built-in tilesets from OpenStreetMap,
Mapbox, and Stamen, and supports custom tilesets with Mapbox 
or Cloudmade API keys. Folium supports both
GeoJSON and TopoJSON overlays, as well as the binding of data to those
overlays to create choropleth maps with color-brewer color schemes.

Installation
------------

.. code:: bash

    $ pip install folium

Getting Started
---------------

You can find most of the following examples in the notebook **folium_examples.ipynb** in the examples folder.

To create a base map, simply pass your starting coordinates to Folium:

.. code:: python

    import folium
    map_osm = folium.Map(location=[45.5236, -122.6750])
    map_osm.save('osm.html')

|baseOSM|

| Folium defaults to OpenStreetMap tiles, but Stamen Terrain, Stamen
  Toner,
| Mapbox Bright, and Mapbox Control room tiles are built in:

.. code:: python

    stamen = folium.Map(location=[45.5236, -122.6750], tiles='Stamen Toner',
                        zoom_start=13)
    stamen.save('stamen_toner.html')

|stamen|

Folium also supports Cloudmade and Mapbox custom tilesets- simply pass
your key to the ``API_key`` keyword:

.. code:: python

    custom = folium.Map(location=[45.5236, -122.6750], tiles='Mapbox',
                        API_key='wrobstory.map-12345678')

Lastly, Folium supports passing any Leaflet.js compatible custom
tileset:

.. code:: python

    tileset = r'http://{s}.tiles.yourtiles.com/{z}/{x}/{y}.png'
    map = folium.Map(location=[45.372, -121.6972], zoom_start=12,
                     tiles=tileset, attr='My Data Attribution')

Markers
-------

| Folium supports the plotting of numerous marker types, starting with a
  simple Leaflet
| style location marker with popup text:

.. code:: python

    map_1 = folium.Map(location=[45.372, -121.6972], zoom_start=12,
                       tiles='Stamen Terrain')
    folium.Marker([45.3288, -121.6625], popup='Mt. Hood Meadows').add_to(map_1)
    folium.Marker([45.3311, -121.7113], popup='Timberline Lodge').add_to(map_1)
    map_1.save('mthood.html')

|hood|

`Live example <http://bl.ocks.org/wrobstory/5609718>`__

Folium supports colors and marker icon types (from bootstrap)

.. code:: python

    map_1 = folium.Map(location=[45.372, -121.6972], zoom_start=12,tiles='Stamen Terrain')
    folium.Marker([45.3288, -121.6625], popup='Mt. Hood Meadows',
                       icon = folium.Icon(icon = 'cloud')).add_to(map_1)
    folium.Marker([45.3311, -121.7113], popup='Timberline Lodge',
                       icon = folium.Icon(color ='green')).add_to(map_1)
    folium.Marker([45.3300, -121.6823], popup='Some Other Location',
                       icon = folium.Icon(color ='red')).add_to(map_1)
    map_1.save('iconTest.html')

.. iconTest is broken, TODO: Link to the notebook directly.

Folium also supports circle-style markers, with custom size and color:

.. code:: python

    map_2 = folium.Map(location=[45.5236, -122.6750], tiles='Stamen Toner',
                       zoom_start=13)
    folium.Marker(location=[45.5244, -122.6699], popup='The Waterfront').add_to(map_2)
    folium.CircleMarker(location=[45.5215, -122.6261], radius=50,
                        popup='Laurelhurst Park', color='#3186cc',
                        fill_color='#3186cc').add_to(map_2)
    map_2.save('portland.html')

|circle|

`Live example <http://bl.ocks.org/wrobstory/5609747>`__

Folium has a convenience function to enable lat/lng popovers:

.. code:: python

    map_3 = folium.Map(location=[46.1991, -122.1889], tiles='Stamen Terrain',
                       zoom_start=13)
    folium.LatLngPopup().add_to(map_3)
    map_3.save('sthelens.html')

|latlng|

`Live example <http://bl.ocks.org/wrobstory/5609756>`__

Click-for-marker functionality will allow for on-the-fly placement of
markers:

.. code:: python

    map_4 = folium.Map(location=[46.8527, -121.7649], tiles='Stamen Terrain',
                       zoom_start=13)
    folium.Marker(location=[46.8354, -121.7325], popup='Camp Muir').add_to(map_4)
    folium.ClickForMarker(popup='Waypoint').add_to(map_4)
    map_4.save('mtrainier.html')

|waypoints|

`Live example <http://bl.ocks.org/wrobstory/5609762>`__

Folium also supports the Polygon marker set from the
`Leaflet-DVF <https://github.com/humangeo/leaflet-dvf>`__:

.. code:: python

    map_5 = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    folium.RegularPolygonMarker(location=[45.5012, -122.6655], popup='Ross Island Bridge',
                       fill_color='#132b5e', number_of_sides=3, radius=10).add_to(map_5)
    folium.RegularPolygonMarker(location=[45.5132, -122.6708], popup='Hawthorne Bridge',
                       fill_color='#45647d', number_of_sides=4, radius=10).add_to(map_5)
    folium.RegularPolygonMarker(location=[45.5275, -122.6692], popup='Steel Bridge',
                       fill_color='#769d96', number_of_sides=6, radius=10).add_to(map_5)
    folium.RegularPolygonMarker(location=[45.5318, -122.6745], popup='Broadway Bridge',
                       fill_color='#769d96', number_of_sides=8, radius=10).add_to(map_5)
    map_5.save('bridges.html')

|polygon|

`Live example <http://bl.ocks.org/wrobstory/5609786>`__

Vincent/Vega Markers
--------------------

Folium enables passing
`vincent <https://github.com/wrobstory/vincent>`__ visualizations to any
marker type, with the visualization as the popover:

.. code:: python

    buoy_map = folium.Map(location=[46.3014, -123.7390], zoom_start=7,
                          tiles='Stamen Terrain')
    popup1 = folium.Popup(max_width=800,
                         ).add_child(folium.Vega(vis1, width=500, height=250))
    folium.RegularPolygonMarker([47.3489, -124.708],
                         fill_color='#43d9de', radius=12, popup=popup1).add_to(buoy_map)
    popup2 = folium.Popup(max_width=800,
                         ).add_child(folium.Vega(vis2, width=500, height=250))
    folium.RegularPolygonMarker([44.639, -124.5339],
                         fill_color='#43d9de', radius=12, popup=popup2).add_to(buoy_map)
    popup3 = folium.Popup(max_width=800,
                         ).add_child(folium.Vega(vis3, width=500, height=250))
    folium.RegularPolygonMarker([46.216, -124.1280],
                         fill_color='#43d9de', radius=12, popup=popup3).add_to(buoy_map)
    buoy_map.save('NOAA_buoys.html')

|vincent|

`Live example <http://bl.ocks.org/wrobstory/5609803>`__

GeoJSON/TopoJSON Overlays
-------------------------

Both GeoJSON and TopoJSON layers can be passed to the map as an overlay,
and multiple layers can be visualized on the same map:

.. code:: python

    geo_path = r'data/antarctic_ice_edge.json'
    topo_path = r'data/antarctic_ice_shelf_topo.json'

    ice_map = folium.Map(location=[-59.1759, -11.6016],
                       tiles='Mapbox Bright', zoom_start=2)
    ice_map.choropleth(geo_path=geo_path)
    ice_map.choropleth(geo_path=topo_path, topojson='objects.antarctic_ice_shelf')
    ice_map.save('ice_map.html')

|ice|

`Live example <http://bl.ocks.org/wrobstory/5609811>`__

Choropleth Maps
---------------

Folium allows for the binding of data between Pandas DataFrames/Series
and Geo/TopoJSON geometries. `Color Brewer <http://colorbrewer2.org/>`__
sequential color schemes are built-in to the library, and can be passed
to quickly visualize different combinations:

.. code:: python

    import folium
    import pandas as pd

    state_geo = r'data/us-states.json'
    state_unemployment = r'data/US_Unemployment_Oct2012.csv'

    state_data = pd.read_csv(state_unemployment)

    #Let Folium determine the scale
    map = folium.Map(location=[48, -102], zoom_start=3)
    map.choropleth(geo_path=state_geo, data=state_data,
                 columns=['State', 'Unemployment'],
                 key_on='feature.id',
                 fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
                 legend_name='Unemployment Rate (%)')
    map.save('us_states.html')

|states_1|

`Live example <http://bl.ocks.org/wrobstory/5609830>`__

Folium creates the legend on the upper right based on a D3 threshold
scale, and makes the best-guess at values via quantiles. Passing your
own threshold values is simple:

.. code:: python

    map.choropleth(geo_path=state_geo, data=state_data,
                 columns=['State', 'Unemployment'],
                 threshold_scale=[5, 6, 7, 8, 9, 10],
                 key_on='feature.id',
                 fill_color='BuPu', fill_opacity=0.7, line_opacity=0.5,
                 legend_name='Unemployment Rate (%)',
                 reset=True)
    map.save('us_states.html')

|states_2|

`Live example <http://bl.ocks.org/wrobstory/5609856>`__

By binding data via the Pandas DataFrame, different datasets can be
quickly visualized. In the following example, the ``df`` DataFrame
contains six columns with different economic data, a few of which we
will visualize:

.. code:: python

    #Number of employed with auto scale
    map_1 = folium.Map(location=[48, -102], zoom_start=3)
    map_1.choropleth(geo_path=county_geo, data_out='data1.json', data=df,
                   columns=['GEO_ID', 'Employed_2011'],
                   key_on='feature.id',
                   fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.3,
                   topojson='objects.us_counties_20m')
    map_1.save('map_1.html')

|counties_1|

`Live example <http://bl.ocks.org/wrobstory/5609889>`__

.. code:: python

    #Unemployment with custom defined scale
    map_2 = folium.Map(location=[40, -99], zoom_start=4)
    map_2.choropleth(geo_path=county_geo, data_out='data2.json', data=df,
                   columns=['GEO_ID', 'Unemployment_rate_2011'],
                   key_on='feature.id',
                   threshold_scale=[0, 5, 7, 9, 11, 13],
                   fill_color='YlGnBu', line_opacity=0.3,
                   legend_name='Unemployment Rate 2011 (%)',
                   topojson='objects.us_counties_20m')
    map_2.save('map_2.html')

|counties_2|

`Live example <http://bl.ocks.org/wrobstory/5609934>`__

.. code:: python

    #Median Household income
    map_3 = folium.Map(location=[40, -99], zoom_start=4)
    map_3.choropleth(geo_path=county_geo, data_out='data3.json', data=df,
                   columns=['GEO_ID', 'Median_Household_Income_2011'],
                   key_on='feature.id',
                   fill_color='PuRd', line_opacity=0.3,
                   legend_name='Median Household Income 2011 ($)',
                   topojson='objects.us_counties_20m')
    map_3.save('map_3.html')

|counties_3|

`Live example <http://bl.ocks.org/wrobstory/5609959>`__

Dependencies
------------

Jinja2

Pandas (Map Data Binding only)

Numpy (Map Data Binding only)

Vincent (Map Data Binding only)

Status
------

Beta

Docs
----

https://folium.readthedocs.org/

.. |Folium| image:: http://farm3.staticflickr.com/2860/8754661081_c40e5a214c_o.jpg
.. |baseOSM| image:: http://farm6.staticflickr.com/5334/8754817259_de071db265_c.jpg
.. |stamen| image:: http://farm3.staticflickr.com/2883/8755937912_1d9ef78118_c.jpg
.. |hood| image:: http://farm4.staticflickr.com/3666/8755937936_d7efbc6dee_c.jpg
.. |iconTest| image:: http://cl.ly/image/2b0l1K0v370P/icon_test.png
.. |circle| image:: http://farm9.staticflickr.com/8280/8755938394_9f491ef79f_c.jpg
.. |latlng| image:: http://farm4.staticflickr.com/3698/8755938152_14bc024bde_c.jpg
.. |waypoints| image:: http://farm6.staticflickr.com/5343/8754817433_2ecde65790_c.jpg
.. |polygon| image:: http://farm8.staticflickr.com/7405/8754817131_24285bff5f_c.jpg
.. |vincent| image:: http://farm4.staticflickr.com/3699/8754817119_4a14ebc3fe_c.jpg
.. |ice| image:: http://farm8.staticflickr.com/7335/8754817253_f32155f902_c.jpg
.. |states_1| image:: http://farm3.staticflickr.com/2837/8755937872_ed5ec8e854_c.jpg
.. |states_2| image:: http://farm9.staticflickr.com/8542/8754816951_752b8a7867_c.jpg
.. |counties_1| image:: http://farm4.staticflickr.com/3792/8755938318_bc82a81c64_c.jpg
.. |counties_2| image:: http://farm9.staticflickr.com/8140/8754817355_2bfea43ff5_c.jpg
.. |counties_3| image:: http://farm4.staticflickr.com/3755/8755938218_06fdc51d40_c.jpg
