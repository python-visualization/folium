import folium
from folium import JsCode
from folium.plugins import GeoMan, MousePosition

m = folium.Map(tiles=None, location=[39.949610, -75.150282], zoom_start=5)
MousePosition().add_to(m)

# This can be used to test the connection to streamlit
# by returning the resulting GeoJson
handler = JsCode(
    """
  (e) => {
      var map = %(map)s;
      var layers = L.PM.Utils.findLayers(map);
      var lg = L.layerGroup(layers);
      console.log(lg.toGeoJSON());
  }
  """  # noqa: UP031
    % dict(map=m.get_name())
)

# For manual testing
click = JsCode(
    """
  (e) => {
      console.log(e.target);
      console.log(e.target.toGeoJSON());
  }
  """
)

# Just a few customizations for the snapshot tests
# The test succeeds if the position is to the right
# and if the buttons for markers and circles are not
# shown.
gm = GeoMan(
    position="topright", draw_marker=False, draw_circle=False, on={"click": click}
).add_to(m)

# For manual testing of the global options
gm.set_global_options(
    {
        "snappable": True,
        "snapDistance": 20,
    }
)

# Make rectangles green
gm.enable_draw("Rectangle", path_options={"color": "green"})
gm.disable_draw()

# On any event that updates the layers, we trigger the handler
event_handlers = {
    "pm:create": handler,
    "pm:remove": handler,
    "pm:update": handler,
    "pm:rotateend": handler,
    "pm:cut": handler,
    "pm:undoremove": handler,
}

m.on(**event_handlers)
