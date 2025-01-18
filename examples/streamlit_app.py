import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation",
    page_icon=":world_map:️",
    layout="wide",
)

"# streamlit-folium"

"""streamlit-folium integrates two great open-source projects in the Python ecosystem:
[Streamlit](https://streamlit.io) and
[Folium](https://python-visualization.github.io/folium/)!"""

"""
Currently, there are two functions defined:

- `st_folium()`: a bi-directional Component, taking a Folium/Branca object and plotting
  to the Streamlit app. Upon mount/interaction with the Streamlit app, st_folium()
  returns a Dict with selected information including the bounding box and items clicked
  on

- `folium_static()`: takes a folium.Map, folium.Figure, or branca.element.Figure object
  and displays it in a Streamlit app.
"""

"""
On its own, Folium is limited to _display-only_ visualizations; the Folium API generates
the proper [leaflet.js](https://leafletjs.com/) specification, as HTML and displays it.
Some interactivity is provided (depending on how the Folium API is utilized), but the
biggest drawback is that the interactivity from the visualization isn't passed back to
Python, and as such, you can't make full use of the functionality provided by the
leaflet.js library.

`streamlit-folium` builds upon the convenient [Folium
API](https://python-visualization.github.io/folium/modules.html) for building geospatial
visualizations by adding a _bi-directional_ data transfer functionality. This not only
allows for increased interactivity between the web browser and Python, but also the use
of larger datasets through intelligent querying.

### Bi-directional data model
"""
left, right = st.columns(2)


with left:
    """
    If we take a look at the example from the Home page, it might seem trivial. We
    define a single point with a marker and pop-up and display it:
    """
    with st.echo():
        import streamlit as st
        from streamlit_folium import st_folium

        import folium

        # center on Liberty Bell, add marker
        m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
        folium.Marker(
            [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
        ).add_to(m)

        # call to render Folium map in Streamlit
        st_data = st_folium(m, width=725)

with right:
    """
    But behind the scenes, a lot more is happening _by default_. The return value of
    `st_folium` is set to `st_data`, and within this Python variable is information
    about what is being displayed on the screen:
    """

    st_data

    """
    As the user interacts with the data visualization, the values for `bounds` are
    constantly updating, along with `zoom`. With these values available in Python, we
    can now limit queries based on bounding box, change the marker size based on the
    `zoom` value and much more!
    """
