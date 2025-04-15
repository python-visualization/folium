from streamlit_folium import st_folium

import folium

# Library of Congress coordinates (latitude, longitude)
loc_coordinates = (38.8886, -77.0047)

# Create a Folium map centered around the Library of Congress
map_lc = folium.Map(location=loc_coordinates, zoom_start=15)

# Define the DivIcon with the custom icon.  This variable can be used in one marker successfully, but will fail if we use it in two markers.


icon = folium.DivIcon(
    icon_anchor=(15, 15),
    html="""<div><img src="/app/static/book-open-variant-outline.png" height="35" width="35"/></div>""",
)


marker1 = folium.Marker(
    location=(38.886970844230866, -77.00471380332),
    popup="Library of Congress:  James Madison Building",
).add_to(map_lc)

marker2 = folium.Marker(
    location=loc_coordinates, popup="Library of Congress", icon=icon
).add_to(map_lc)
marker1.set_icon(icon)
marker2.set_icon(icon)

st_folium(map_lc, width=600, height=500)
