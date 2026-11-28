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


def test_search_restores_layer_map_membership():
    m = folium.Map([0, 0], tiles=None)
    layer = folium.GeoJson(_geojson_point(), show=False).add_to(m)
    search = Search(layer, search_label="name").add_to(m)
    rendered = normalize(search._template.module.script(search))

    # L.Control.Search adds its layer to the map, so a layer that was not on
    # the map before must be removed again right after the control is added.
    name = layer.get_name()
    was_on_map = normalize(f"var {name}WasOnMap = {m.get_name()}.hasLayer( {name} );")
    add_control = normalize(f"{m.get_name()}.addControl( {name}searchControl );")
    remove_layer = f"if (!{name}WasOnMap) {{{name}.remove();}}"
    assert was_on_map in rendered
    assert add_control in rendered
    assert remove_layer in rendered
    assert (
        rendered.index(was_on_map)
        < rendered.index(add_control)
        < rendered.index(remove_layer)
    )
