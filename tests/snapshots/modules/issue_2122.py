import folium
from folium import Control, TileLayer

m = folium.Map(location=[39.949610, -75.150282], zoom_start=5, zoom_control=False)
tiles = TileLayer(
    tiles="OpenStreetMap",
    show=False,
    control=False,
)
tiles.add_to(m)

minimap = Control("MiniMap", tiles)
minimap.add_js_link(
    "minimap_js",
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet-minimap/3.6.1/Control.MiniMap.min.js",
)
minimap.add_css_link(
    "minimap_css",
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet-minimap/3.6.1/Control.MiniMap.css",
)
minimap.add_to(m)

ruler = Control("Ruler", tiles)
ruler.add_js_link(
    "ruler_js",
    "https://cdn.rawgit.com/gokertanrisever/leaflet-ruler/master/src/leaflet-ruler.js",
)
ruler.add_css_link(
    "ruler_css",
    "https://cdn.rawgit.com/gokertanrisever/leaflet-ruler/master/src/leaflet-ruler.css",
)
ruler.add_to(m)
