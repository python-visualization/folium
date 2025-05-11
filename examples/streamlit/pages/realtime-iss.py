import streamlit as st
from streamlit_folium import st_folium

import folium
from folium.plugins import Realtime

st.set_page_config(page_title="iss", layout="wide")

m = folium.Map()

source = folium.JsCode(
    """
    function(responseHandler, errorHandler) {
        var url = 'https://api.wheretheiss.at/v1/satellites/25544';

        fetch(url)
        .then((response) => {
            return response.json().then((data) => {
                var { id, timestamp, longitude, latitude } = data;

                return {
                    'type': 'FeatureCollection',
                    'features': [{
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [longitude, latitude]
                        },
                        'properties': {
                            'id': id,
                            'timestamp': timestamp
                        }
                    }]
                };
            })
        })
        .then(responseHandler)
        .catch(errorHandler);
    }
"""
)

on_each_feature = folium.JsCode(
    """
    (feature, layer) => {
        layer.on("click", (event) => {
            Streamlit.setComponentValue({
                id: feature.properties.id,
                // Be careful, on_each_feature binds only once.
                // You need to extract the current location from
                // the event.
                location: event.sourceTarget.feature.geometry
            });
        });
    }
"""
)

realtime = Realtime(source, on_each_feature=on_each_feature, interval=1000).add_to(m)
realtime.on(
    update=folium.JsCode(
        """
        (e) => {
            console.log('update ', e.target._map);
            var map = e.target._map;
            var realtime = e.target;
            map.fitBounds(realtime.getBounds(), {maxZoom: 8});
        }
        """
    )
)

left, right = st.columns(2)
with left:
    data = st_folium(m, width=1000, returned_objects=[], debug=True)

with right:
    st.write(data)
