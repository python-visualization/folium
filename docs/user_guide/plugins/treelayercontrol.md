```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

# TreeLayerControl
Create a Layer Control allowing a tree structure for the layers.

See https://github.com/jjimenezshaw/Leaflet.Control.Layers.Tree for more
information.

## Simple example

```{code-cell} ipython3
import folium
from folium.plugins.treelayercontrol import TreeLayerControl
from folium.features import Marker

m = folium.Map(location=[46.603354, 1.8883335], zoom_start=5)
osm = folium.TileLayer("openstreetmap").add_to(m)

overlay_tree = {
    "label": "Points of Interest",
    "select_all_checkbox": "Un/select all",
    "children": [
        {
            "label": "Europe",
            "select_all_checkbox": True,
            "children": [
                {
                    "label": "France",
                    "select_all_checkbox": True,
                    "children": [
                        { "label": "Tour Eiffel", "layer": Marker([48.8582441, 2.2944775]).add_to(m) },
                        { "label": "Notre Dame", "layer": Marker([48.8529540, 2.3498726]).add_to(m) },
                        { "label": "Louvre", "layer": Marker([48.8605847, 2.3376267]).add_to(m) },
                    ]
                }, {
                    "label": "Germany",
                    "select_all_checkbox": True,
                    "children": [
                        { "label": "Branderburger Tor", "layer": Marker([52.5162542, 13.3776805]).add_to(m)},
                        { "label": "Kölner Dom", "layer": Marker([50.9413240, 6.9581201]).add_to(m)},
                    ]
                }, {"label": "Spain",
                    "select_all_checkbox": "De/seleccionar todo",
                    "children": [
                        { "label": "Palacio Real", "layer": Marker([40.4184145, -3.7137051]).add_to(m)},
                        { "label": "La Alhambra", "layer": Marker([37.1767829, -3.5892795]).add_to(m)},
                    ]
                }
            ]
        }, {
            "label": "Asia",
            "select_all_checkbox": True,
            "children": [
                {
                    "label": "Jordan",
                    "select_all_checkbox": True,
                    "children": [
                        { "label": "Petra", "layer": Marker([30.3292215, 35.4432464]).add_to(m) },
                        { "label": "Wadi Rum", "layer": Marker([29.6233486, 35.4390656]).add_to(m) }
                    ]
                }, {
                }
            ]
        }
    ]
}

control = TreeLayerControl(overlay_tree=overlay_tree).add_to(m)
```
