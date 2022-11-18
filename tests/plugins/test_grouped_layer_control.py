import folium
from folium.plugins import groupedlayercontrol
from folium.utilities import normalize


def test_feature_group_sub_group():
    m = folium.Map([40.0, 70.0], zoom_start=6)
    fg1 = folium.FeatureGroup(name="g1")
    fg2 = folium.FeatureGroup(name="g2")
    fg3 = folium.FeatureGroup(name="g3")
    folium.Marker([40, 74]).add_to(fg1)
    folium.Marker([38, 72]).add_to(fg2)
    folium.Marker([40, 72]).add_to(fg3)
    m.add_child(fg1)
    m.add_child(fg2)
    m.add_child(fg3)
    lc = groupedlayercontrol.GroupedLayerControl(groups={"groups1": [fg1, fg2]})
    lc.add_to(m)
    out = normalize(m._parent.render())

    assert (
        "https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.js"
        in out
    )

    assert (
        normalize(
            f"""
        L.control.groupedLayers(
            null,
            {{
                "groups1" : {{
                    "g1" : {fg1.get_name()},
                    "g2" : {fg2.get_name()},
                }},
            }},
            {{"exclusiveGroups": ["groups1"]}},
         ).addTo({m.get_name()});
         {fg2.get_name()}.remove();
    """
        )
        in out
    )
