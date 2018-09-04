
"""
Uses plain python and opens the folium map in a browser window. No IPython, Jupyter or else is required.

"""

import numpy as np
import folium
from folium.plugins import HeatMap

# create a dummy map
data = (np.random.normal(size=(100, 3)) *
        np.array([[1, 1, 1]]) +
        np.array([[48, 5, 1]])).tolist()
folium_map = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)
HeatMap(data).add_to(folium_map)

# open in in browser
folium_map.show_in_browser()

