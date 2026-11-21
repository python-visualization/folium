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
    assert (
        normalize(
            f"e.layer.bindPopup({layer.get_name()}.getPopup()).openPopup().unbindPopup();"
        )
        in rendered
    )


def _geojson_point():
    return {
        "type": "Feature",
        "properties": {"name": "Example"},
        "geometry": {"type": "Point", "coordinates": [0, 0]},
    }


def test_search_keeps_hidden_layer_hidden():
    m = folium.Map([0, 0], tiles=None)
    layer = folium.GeoJson(_geojson_point(), show=False).add_to(m)
    search = Search(layer, search_label="name").add_to(m)
    rendered = normalize(search._template.module.script(search))

    # L.Control.Search adds its layer to the map, so it must be removed again.
    add_control = normalize(
        f"{m.get_name()}.addControl( {layer.get_name()}searchControl );"
    )
    remove_layer = normalize(f"{layer.get_name()}.remove();")
    assert add_control in rendered
    assert remove_layer in rendered
    assert rendered.index(add_control) < rendered.index(remove_layer)


def test_search_does_not_remove_shown_layer():
    m = folium.Map([0, 0], tiles=None)
    layer = folium.GeoJson(_geojson_point()).add_to(m)
    search = Search(layer, search_label="name").add_to(m)
    rendered = normalize(search._template.module.script(search))

    assert normalize(f"{layer.get_name()}.remove();") not in rendered
