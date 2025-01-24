import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: Limit Data Return",
    page_icon="🤏",
    layout="wide",
)

"""
# streamlit-folium: Limit Data Return

By default, st_folium returns quite a few data fields (zoom, bounds, last active
drawing,
 all drawings, etc). If you only need a subset of these fields, you can pass a list of
 the fields you want returned to the `returned_objects` parameter.
"""

"""
### Example: Only return the last object clicked on the map

Try clicking on the tooltips below. Note that clicking elsewhere on the map, or zooming
or scrolling will not cause the app to rerun.

"""

with st.echo(code_location="below"):
    import streamlit as st
    from streamlit_folium import st_folium

    import folium

    m = folium.Map(location=[39.949610, -75.150282], zoom_start=13)

    folium.Marker(
        [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
    ).add_to(m)
    folium.Marker(
        [39.95887, -75.150026],
        popup="Independence Hall",
        tooltip="Independence Hall",
    ).add_to(m)
    folium.Marker(
        [39.965570, -75.180966],
        popup="Philadelphia Museum of Art",
        tooltip="Philadelphia Museum of Art",
    ).add_to(m)

    c1, c2 = st.columns(2)
    with c1:
        output = st_folium(
            m, width=700, height=500, returned_objects=["last_object_clicked"]
        )

    with c2:
        st.write(output)
