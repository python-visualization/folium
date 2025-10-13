Plugins
-------

.. toctree::
  :hidden:

  plugins/antpath
  plugins/boat_marker
  plugins/beautify_icon
  plugins/draw
  plugins/dual_map
  plugins/featuregroup_subgroup
  plugins/float_image
  plugins/fullscreen
  plugins/geocoder
  plugins/geoman
  plugins/grouped_layer_control
  plugins/heatmap
  plugins/heatmap_with_time
  plugins/locate_control
  plugins/marker_cluster
  plugins/mini_map
  plugins/measure_control
  plugins/mouse_position
  plugins/overlapping_marker_spiderfier
  plugins/pattern
  plugins/polygon_encoded
  plugins/polyline_encoded
  plugins/polyline_offset
  plugins/polyline_textpath
  plugins/realtime
  plugins/scroll_zoom_toggler
  plugins/search
  plugins/semi_circle
  plugins/side_by_side_layers
  plugins/tag_filter_button
  plugins/terminator
  plugins/timeline
  plugins/timeslider_choropleth
  plugins/timestamped_geojson
  plugins/treelayercontrol
  plugins/vector_tiles
  plugins/WmsTimeDimension

.. list-table::
    :widths: 25 75
    :header-rows: 1

    * - Plugin
      - Description
    * - :doc:`Ant Path <plugins/antpath>`
      - A flux animation (like walking of ants) along a polyline.
    * - :doc:`Boat Marker <plugins/boat_marker>`
      - A boat marker using HTML canvas for displaying yachts and sailboats with heading and optional wind information.
    * - :doc:`Beautify Icon <plugins/beautify_icon>`
      - Lightweight plugin that adds colorful iconic markers without image and gives full control of style to end user (i.e. Unlimited colors and CSS styling).
    * - :doc:`Draw <plugins/draw>`
      - Enables drawing features like polylines, polygons, rectangles, circles and markers through a very nice user-friendly interface with icons and hints.
    * - :doc:`Dual Map <plugins/dual_map>`
      - Synchronized view of two maps in the same window.
    * - :doc:`FeatureGroup Subgroup <plugins/featuregroup_subgroup>`
      - Create Feature Groups that add their child layers into a parent group.
    * - :doc:`Float Image <plugins/float_image>`
      - Add a floating image in the HTML canvas on top of the map.
    * - :doc:`Fullscreen <plugins/fullscreen>`
      - A fullscreen button control for modern browsers, using HTML Fullscreen API.
    * - :doc:`Geocoder <plugins/geocoder>`
      - A clean and extensible control for both geocoding and reverse geocoding using different geocoding providers.
    * - :doc:`Geoman <plugins/geoman>`
      - Interactive drawing and editing interface for polygons, polylines, circles, and other geometric shapes.
    * - :doc:`Grouped Layer Control <plugins/grouped_layer_control>`
      - Create layer control with support for grouping overlays together.
    * - :doc:`Heatmap <plugins/heatmap>`
      - A tiny, simple and fast heatmap plugin.
    * - :doc:`Heatmap with Time <plugins/heatmap_with_time>`
      - Create a time-aware heatmap.
    * - :doc:`Locate Control <plugins/locate_control>`
      - Geolocate a user over an encrypted connection.
    * - :doc:`Marker Cluster <plugins/marker_cluster>`
      - Beautiful, sophisticated, high performance marker clustering solution with smooth animations.
    * - :doc:`Measure Control <plugins/measure_control>`
      - Coordinate, linear, and area measure control.
    * - :doc:`Mini Map <plugins/mini_map>`
      - A small minimap showing the map at a different scale to aid navigation.
    * - :doc:`Mouse Position <plugins/mouse_position>`
      - A control that displays geographic coordinates of the mouse pointer, as it is moved over the map.
    * - :doc:`Overlapping Marker Spiderifier <plugins/overlapping_marker_spiderfier>`
      - Help manage overlapping markers by “spiderfying” them when clicked, making it easier to select individual markers.
    * - :doc:`Pattern <plugins/pattern>`
      - Add support for pattern fills on Paths.
    * - :doc:`Polygon Encoded <plugins/polygon_encoded>`
      - Draw a polygon directly from an encoded string.
    * - :doc:`Polyline Encoded <plugins/polyline_encoded>`
      - Draw a polyline directly from an encoded string.
    * - :doc:`Polyline Offset <plugins/polyline_offset>`
      - Shift relative pixel offset, without actually changing the actual latitude longitude values.
    * - :doc:`Polyline Textpath <plugins/polyline_textpath>`
      - Write text along polylines.
    * - :doc:`Realtime <plugins/realtime>`
      - Put realtime data (like live tracking, GPS information) on a map.
    * - :doc:`Scroll Zoom Toggler <plugins/scroll_zoom_toggler>`
      - Enable/Disable zooming via a button.
    * - :doc:`Search <plugins/search>`
      - A control for search Markers/Features location by custom property in LayerGroup/GeoJSON.
    * - :doc:`Semi Circle <plugins/semi_circle>`
      - Add a marker in the shape of a semicircle, similar to the Circle class.
    * - :doc:`Side by Side Layers <plugins/side_by_side_layers>`
      - A control to add a split screen to compare two map overlays.
    * - :doc:`Tag Filter Button <plugins/tag_filter_button>`
      - Creates a Tag Filter Button to filter elements based on different criteria.
    * - :doc:`Terminator <plugins/terminator>`
      - Overlay day and night regions on a map.
    * - :doc:`Timeline <plugins/timeline>`
      - Create a timeline with a time slider for geojson data with start and end times.
    * - :doc:`Timeslider Choropleth <plugins/timeslider_choropleth>`
      - Create a choropleth with a timeslider for timestamped data.
    * - :doc:`Timestamped GeoJSON <plugins/timestamped_geojson>`
      - Add GeoJSON data with timestamps to a map.
    * - :doc:`TreeLayerControl <plugins/treelayercontrol>`
      - Add a control for a tree of layers with checkboxes for visibility control.
    * - :doc:`Vector Tiles using VectorGridProtobuf <plugins/vector_tiles>`
      - Display gridded vector data (GeoJSON or TopoJSON sliced with geojson-vt, or protobuf vector tiles).
    * - :doc:`WMS Time Dimension <plugins/WmsTimeDimension>`
      - Create a time-aware WmsTileLayer.

      .. _custom_controls:

Custom Controls via ``Control`` (add text/UI without a full plugin)
===================================================================

Folium’s ``Control`` (Leaflet’s ``L.Control``) lets you add small custom UI elements—
like always-visible text, badges, or buttons—**without** writing a full Folium plugin.
Below is a minimal example that injects a Leaflet control containing text.

.. code-block:: python

   from folium import Map
   from branca.element import Element

   # 1) Create a map
   m = Map(location=[0, 0], zoom_start=2)

   # 2) Get the JS map variable name Folium uses (needed to attach the control)
   map_var = m.get_name()

   # 3) Inject a small Leaflet control that renders HTML text
   control_js = f"""
   <script>
   // Define a small custom control
   var CustomText = L.Control.extend({{
     onAdd: function(map) {{
       var div = L.DomUtil.create('div');
       div.innerHTML = 'My Label';
       div.style.background = 'white';
       div.style.padding = '4px 8px';
       div.style.border = '1px solid #ccc';
       div.style.borderRadius = '4px';
       div.style.font = '14px/1.2 sans-serif';
       return div;
     }},
     onRemove: function(map) {{}}
   }});

   // Factory and add to the map in the top-right corner
   L.control.customText = function(opts) {{
     return new CustomText(opts);
   }};
   L.control.customText({{ position: 'topright' }}).addTo({map_var});
   </script>
   """

   m.get_root().html.add_child(Element(control_js))
   m.save("map_with_custom_text_control.html")

**Notes & tips**

- This approach is best for **small UI** (labels, badges, short instructions).
- For **text tied to a geographic point**, see :py:class:`folium.features.DivIcon`.
- If your control overlaps with other UI, change the Leaflet position
  (``'topleft'``, ``'topright'``, ``'bottomleft'``, ``'bottomright'``) or use custom CSS.
- For larger features, consider wrapping JS in a proper Folium element (e.g. a
  :class:`branca.element.MacroElement`) and reusing it across maps.

.. seealso::

   Leaflet Controls: https://leafletjs.com/reference.html#control
   • API: :py:class:`folium.features.Control`



