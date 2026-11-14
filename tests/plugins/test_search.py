import folium
from folium.plugins import Search
from folium.utilities import normalize


def test_search_opens_popup_bound_to_geojson_group():
    m = folium.Map([0, 0], tiles=None)
    layer = folium.GeoJson(
        {
            "type": "Feature",
            "properties": {"name": "Example"},
            "geometry": {"type": "Point", "coordinates": [0, 0]},
        },
        popup=folium.GeoJsonPopup(fields=["name"]),
    ).add_to(m)
    search = Search(layer, search_label="name").add_to(m)
    rendered = normalize(search._template.module.script(search))

    # GeoJsonPopup is bound to the group, not to each indexed feature.
    assert normalize(f"else if ({layer.get_name()}.getPopup())") in rendered
    assert normalize(f"e.layer.bindPopup({layer.get_name()}.getPopup()).openPopup().unbindPopup();") in rendered
