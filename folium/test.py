import folium

map_1 = folium.Map(location=[45.372, -121.6972], zoom_start=12,tiles='Stamen Terrain')
map_1.simple_marker([45.3288, -121.6625], popup='Mt. Hood Meadows',marker_icon='cloud')
map_1.simple_marker([45.3311, -121.7113], popup='Timberline Lodge',marker_color='green')
map_1.simple_marker([45.3300, -121.6823], popup='simple',marker_color='red',marker_icon='info-sign')
map_1.create_map(path='iconTest.html')