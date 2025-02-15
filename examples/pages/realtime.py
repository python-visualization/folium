import streamlit as st
from streamlit_folium import st_folium

import folium
from folium.plugins import Realtime

"""
# streamlit-folium: Realtime Support

streamlit-folium supports the Realtime plugin, which can pull geo data
periodically from a datasource. The example below shows a map that
displays the current location of the International Space Station.

Since Realtime fetches data from an external source the actual
contents of the data is unknown when creating the map. If you want
to react to map events, such as clicking on a Feature, you can pass
a `JsCode` object to the plugin.

Inside the `JsCode` object you have access to the Streamlit object,
which allows you to set a return value for your Streamlit app.
"""

with st.echo():
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
            layer.bindTooltip(`${feature.properties.timestamp}`);
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

    update_feature = folium.JsCode(
        """
        (feature, layer) => {
            L.Realtime.prototype.options.updateFeature(feature, layer);
            if(layer) {
                layer.unbindTooltip();
                layer.bindTooltip(`${feature.properties.timestamp}`);
            }
        }
    """
    )

    Realtime(
        source,
        on_each_feature=on_each_feature,
        update_feature=update_feature,
        interval=10000,
    ).add_to(m)

    data = st_folium(m, returned_objects=[], debug=False)

    st.write(data)
