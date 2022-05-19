"""
Test GroupedLayerControl
------------------
"""

import folium
from folium.plugins import groupedlayercontrol
from folium.utilities import normalize

from jinja2 import Template

# %%
def test_feature_group_sub_group():
    m = folium.Map([40., 70.], zoom_start=6)
    fg1 = folium.FeatureGroup(name='g1')
    fg2 = folium.FeatureGroup(name='g2')
    fg3 = folium.FeatureGroup(name='g3')
    folium.Marker([40, 74]).add_to(fg1)
    folium.Marker([38, 72]).add_to(fg2)
    folium.Marker([40, 72]).add_to(fg3)
    m.add_child(fg1)
    m.add_child(fg2)
    m.add_child(fg3)
    lc = groupedlayercontrol.GroupedLayerControl(groups={'groups1':['g1','g2']})
    lc.add_to(m)
    out = normalize(m._parent.render())

    # We verify that imports
    assert '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.js"></script>' in out
    assert '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.js.map"></script>' in out
    assert '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.css"/>' in out

    # Verify the script part is okay.
    tmpl = Template("""
        var {{ this.get_name() }} = {
            base_layers : {
                {%- for key, val in this.base_layers.items() %}
                {{ key|tojson }} : {{val}},
                {%- endfor %}
            },
            overlays :  {
                {%- for key, val in this.un_grouped_overlays.items() %}
                {{ key|tojson }} : {{val}},
                {%- endfor %}
            },
        };

        L.control.layers(
            {{ this.get_name() }}.base_layers,
            {{ this.get_name() }}.overlays,
            {{ this.options|tojson }}
        ).addTo({{this._parent.get_name()}});

        var groupedOverlays = {
            {%- for key, overlays in this.grouped_overlays.items() %}
            {{ key|tojson }} : {
                {%- for overlaykey, val in overlays.items() %}
                {{ overlaykey|tojson }} : {{val}},
                {%- endfor %}
            },
            {%- endfor %}
        };

        var options = {
            exclusiveGroups: [
                {%- for key, value in this.grouped_overlays.items() %}
                {{key|tojson}},
                {%- endfor %}
            ],
            collapsed: {{ this.options["collapsed"]|tojson }},
            autoZIndex: {{ this.options["autoZIndex"]|tojson }},
            position: {{ this.options["position"]|tojson }},
        };

        L.control.groupedLayers(
            null,
            groupedOverlays,
            options,
        ).addTo({{this._parent.get_name()}});

        {%- for val in this.layers_untoggle.values() %}
        {{ val }}.remove();
        {%- endfor %}
    """)
    assert normalize(tmpl.render(this=lc)) in out
