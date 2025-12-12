import pytest

import folium
from folium.plugins import groupedlayercontrol
from folium.utilities import normalize


def test_grouped_layer_control():
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
    out = m._parent.render()
    print(out)
    out = normalize(out)

    assert (
        "https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.js"
        in out
    )

    expected = normalize(f"""
        L.control.groupedLayers(
            null,
            {{
                "groups1" : {{
                    "g1" : {fg1.get_name()},
                    "g2" : {fg2.get_name()},
                }},
            }},
            {{"exclusiveGroups": ["groups1",],}},
         ).addTo({m.get_name()});
         {fg2.get_name()}.remove();
    """)
    assert expected in out


@pytest.mark.parametrize("positional", [False, True])
def test_grouped_layer_control_base_layers(positional):
    m = folium.Map([40.0, 70.0], zoom_start=6, tiles=None)
    osm = folium.TileLayer("OpenStreetMap", name="osm").add_to(m)
    topo = folium.TileLayer("OpenTopoMap", name="topo", show=False).add_to(m)
    fg1 = folium.FeatureGroup(name="g1").add_to(m)
    fg2 = folium.FeatureGroup(name="g2").add_to(m)
    if positional:
        control = groupedlayercontrol.GroupedLayerControl(
            {"groups1": [fg1, fg2]}, True, [osm, topo]
        )
    else:
        control = groupedlayercontrol.GroupedLayerControl(
            groups={"groups1": [fg1, fg2]}, base_layers=[osm, topo]
        )
    control.add_to(m)
    lc = folium.LayerControl().add_to(m)
    out = normalize(m._parent.render())

    expected = normalize(f"""
        L.control.groupedLayers(
            {{
                "osm" : {osm.get_name()},
                "topo" : {topo.get_name()},
            }},
            {{
                "groups1" : {{
                    "g1" : {fg1.get_name()},
                    "g2" : {fg2.get_name()},
                }},
            }},
            {{"exclusiveGroups": ["groups1",],}},
         ).addTo({m.get_name()});
    """)
    assert expected in out
    # The base layers are no longer listed in the regular LayerControl.
    assert not lc.base_layers


@pytest.mark.parametrize("exclusive_groups", [False, True])
@pytest.mark.parametrize("group_checkboxes", [False, True])
def test_grouped_layer_control_group_checkboxes(exclusive_groups, group_checkboxes):
    m = folium.Map([40.0, 70.0], zoom_start=6, tiles=None)
    osm = folium.TileLayer("OpenStreetMap", name="osm").add_to(m)
    fg1 = folium.FeatureGroup(name="g1").add_to(m)
    fg2 = folium.FeatureGroup(name="g2").add_to(m)
    hidden = folium.FeatureGroup(name="hidden", show=False).add_to(m)
    groupedlayercontrol.GroupedLayerControl(
        groups={"groups1": [fg1, fg2, hidden]},
        exclusive_groups=exclusive_groups,
        base_layers=[osm],
        group_checkboxes=group_checkboxes,
        collapsed=False,
    ).add_to(m)
    lc = folium.LayerControl().add_to(m)
    out = normalize(m._parent.render())

    assert ('"groupCheckboxes": true' in out) == group_checkboxes
    assert ('"exclusiveGroups": ["groups1",]' in out) == exclusive_groups
    assert (f"{fg2.get_name()}.remove();" in out) == exclusive_groups
    assert f"{fg1.get_name()}.remove();" not in out
    assert f"{hidden.get_name()}.remove();" in out
    assert '"collapsed": false' in out
    assert f'"osm" : {osm.get_name()}' in out
    assert not lc.base_layers
    assert not lc.overlays


def test_grouped_layer_control_group_checkboxes_default():
    m = folium.Map()
    fg = folium.FeatureGroup(name="g1").add_to(m)
    groupedlayercontrol.GroupedLayerControl(
        groups={"groups1": [fg]}, exclusive_groups=False
    ).add_to(m)

    assert '"groupCheckboxes"' not in m._parent.render()


def test_grouped_layer_control_group_checkboxes_camel_case():
    m = folium.Map()
    fg = folium.FeatureGroup(name="g1").add_to(m)
    groupedlayercontrol.GroupedLayerControl(
        groups={"groups1": [fg]}, exclusive_groups=False, groupCheckboxes=True
    ).add_to(m)

    assert '"groupCheckboxes": true' in m._parent.render()
