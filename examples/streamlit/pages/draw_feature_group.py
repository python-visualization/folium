import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: Draw Support",
    page_icon=":pencil:",
    layout="wide",
)

"""
# streamlit-folium: Draw Support

Folium supports some of the [most popular leaflet
plugins](https://python-visualization.github.io/folium/plugins.html). In this example,
we can add the
[`Draw`](https://python-visualization.github.io/folium/plugins.html#folium.plugins.Draw)
plugin to our map, which allows for drawing geometric shapes on the map.

When a shape is drawn on the map, the coordinates that represent that shape are passed
back as a geojson feature via the `all_drawings` and `last_active_drawing` data fields.

Draw something below to see the return value back to Streamlit!
"""

with st.echo(code_location="below"):
    import streamlit as st
    from streamlit_folium import st_folium

    import folium
    from folium.plugins import Draw

    m = folium.Map(location=[39.949610, -75.150282], zoom_start=5, png_enabled=True)
    items = folium.FeatureGroup()
    marker = folium.Marker(location=[38, -83]).add_to(items)
    items.add_to(m)

    Draw(export=False, feature_group=items, show_geometry_on_click=False).add_to(m)

    c1, c2 = st.columns(2)
    with c1:
        output = st_folium(m, width=700, height=500)

    with c2:
        st.write(output)
