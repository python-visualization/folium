# -*- coding: utf-8 -*-
import folium

from folium.plugins import Fullscreen

m = folium.Map(location=[41.9, -97.3], zoom_start=4)
Fullscreen(position = 'topright', title = 'Expand me', titleCancel = 'Exit me', 
              forceSeparateButton = True).add_to(m)

m.save(outfile='fullscreen.html')
