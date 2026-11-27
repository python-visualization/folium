"""
Test TimestampedWmsTileLayers
-----------------------------

"""

import folium
from folium import plugins
from folium.utilities import normalize


def test_timestamped_wms_tile_layers_respects_show():
    m = folium.Map()
    hidden = folium.WmsTileLayer(
        url="https://example.com/wms",
        layers="hidden",
        name="Hidden",
        overlay=True,
        show=False,
    ).add_to(m)
    shown = folium.WmsTileLayer(
        url="https://example.com/wms",
        layers="shown",
        name="Shown",
        overlay=True,
    ).add_to(m)
    plugins.TimestampedWmsTileLayers([hidden, shown]).add_to(m)
    folium.LayerControl().add_to(m)

    out = normalize(m._parent.render())

    def wrapped(layer):
        start = out.index(f"var {layer.get_name()} = L.timeDimension.layer.wms(")
        end = out.find("var ", start + 1)
        return out[start:end]

    assert ".addTo(" not in wrapped(hidden)
    assert f"{shown.get_name()}.addTo({m.get_name()});" in wrapped(shown)
    assert f'"Hidden" : {hidden.get_name()},' in out
