import folium

# Library of Congress coordinates (latitude, longitude)
loc_coordinates = (38.8886, -77.0047)

# Create a Folium map centered around the Library of Congress
m = folium.Map(tiles=None, location=loc_coordinates, zoom_start=15)

# Define the DivIcon with the custom icon.  This variable can be used in one marker successfully, but will fail if we use it in two markers.


svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" height="35"
width="35">
<path d="M12
21.5C10.65 20.65 8.2 20 6.5 20C4.85 20 3.15 20.3 1.75 21.05C1.65 21.1 1.6 21.1
1.5 21.1C1.25 21.1 1 20.85 1 20.6V6C1.6 5.55 2.25 5.25 3 5C4.11 4.65 5.33 4.5
6.5 4.5C8.45 4.5 10.55 4.9 12 6C13.45 4.9 15.55 4.5 17.5 4.5C18.67 4.5 19.89
4.65 21 5C21.75 5.25 22.4 5.55 23 6V20.6C23 20.85 22.75 21.1 22.5 21.1C22.4
21.1 22.35 21.1 22.25 21.05C20.85 20.3 19.15 20 17.5 20C15.8 20 13.35 20.65 12
21.5M11 7.5C9.64 6.9 7.84 6.5 6.5 6.5C5.3 6.5 4.1 6.65 3 7V18.5C4.1 18.15 5.3
18 6.5 18C7.84 18 9.64 18.4 11 19V7.5M13 19C14.36 18.4 16.16 18 17.5 18C18.7 18
19.9 18.15 21 18.5V7C19.9 6.65 18.7 6.5 17.5 6.5C16.16 6.5 14.36 6.9 13
7.5V19M14 16.35C14.96 16 16.12 15.83 17.5 15.83C18.54 15.83 19.38 15.91 20
16.07V14.57C19.13 14.41 18.29 14.33 17.5 14.33C16.16 14.33 15 14.5 14
14.76V16.35M14 13.69C14.96 13.34 16.12 13.16 17.5 13.16C18.54 13.16 19.38 13.24
20 13.4V11.9C19.13 11.74 18.29 11.67 17.5 11.67C16.22 11.67 15.05 11.82 14
12.12V13.69M14 11C14.96 10.67 16.12 10.5 17.5 10.5C18.41 10.5 19.26 10.59 20
10.78V9.23C19.13 9.08 18.29 9 17.5 9C16.18 9 15 9.15 14 9.46V11Z"/></svg>"""

icon = folium.DivIcon(
    icon_anchor=(15, 15),
    html=f"<div>{svg}</div>",
)


folium.Marker(
    location=(38.886970844230866, -77.00471380332),
    popup="Library of Congress:  James Madison Building",
    icon=icon,
).add_to(m)

folium.Marker(location=loc_coordinates, popup="Library of Congress", icon=icon).add_to(
    m
)
