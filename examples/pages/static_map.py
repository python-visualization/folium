import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: Static Map",
    page_icon=":ice:",
    layout="wide",
)

"""
# streamlit-folium: Non-interactive Map

If you don't need any data returned from the map, you can just
pass returned_objects=[] to st_folium. The streamlit app will not rerun
when the user interacts with the map, and you will not get any data back from the map.

---

"""
"### Basic `returned_objects=[]` Example"

with st.echo():
    import streamlit as st
    from streamlit_folium import st_folium

    import folium

    # center on Liberty Bell, add marker
    m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
    folium.Marker(
        [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
    ).add_to(m)

    # call to render Folium map in Streamlit, but don't get any data back
    # from the map (so that it won't rerun the app when the user interacts)
    st_folium(m, width=725, returned_objects=[])
