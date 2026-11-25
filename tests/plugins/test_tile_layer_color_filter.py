"""
Test TileLayerColorFilter
-------------------------
"""

import json
import re

import pytest

import folium
from folium import plugins
from folium.raster_layers import TileLayer

PLUGIN_SCRIPT = (
    '<script src="https://cdn.jsdelivr.net/npm/leaflet.tilelayer.colorfilter@2.0.0/'
    'dist/leaflet-tilelayer-colorfilter-global.min.js"></script>'
)


def layer_options(rendered: str, name: str) -> dict:
    """Return the options dict folium rendered for a tile layer."""
    pattern = rf'var {name} = L\.tileLayer\(\s*"[^"]*",\s*(\{{.*?\}})\s*\);'
    match = re.search(pattern, rendered, re.S)
    assert match is not None, f"no L.tileLayer call found for {name}"
    # the options are rendered as a JavaScript object, which allows trailing
    # commas that json does not accept.
    return json.loads(re.sub(r",(\s*[}\]])", r"\1", match.group(1)))


def test_tile_layer_color_filter():
    m = folium.Map([52.1, 5.1], zoom_start=5, tiles=None)
    layer = plugins.TileLayerColorFilter(
        ["invert:100%", "hue-rotate:180deg"], name="dark"
    ).add_to(m)

    rendered = m.get_root().render()

    assert PLUGIN_SCRIPT in rendered
    # the plugin patches L.TileLayer, so it has to load after Leaflet itself.
    assert rendered.index("leaflet@1.9.4/dist/leaflet.js") < rendered.index(
        "leaflet.tilelayer.colorfilter@2.0.0"
    )
    assert layer_options(rendered, layer.get_name())["colorFilter"] == [
        "invert:100%",
        "hue-rotate:180deg",
    ]


def test_tile_layer_color_filter_keeps_tile_layer_arguments():
    m = folium.Map([52.1, 5.1], zoom_start=5, tiles=None)
    layer = plugins.TileLayerColorFilter(
        "grayscale:100%",
        tiles="OpenStreetMap",
        min_zoom=3,
        max_zoom=12,
        name="gray",
    ).add_to(m)

    options = layer_options(m.get_root().render(), layer.get_name())
    assert options["minZoom"] == 3
    assert options["maxZoom"] == 12
    assert options["colorFilter"] == ["grayscale:100%"]


def test_tile_layer_color_filter_normalizes_filters():
    layer = plugins.TileLayerColorFilter(["inv:100", "gray:80", "hue:180deg"])
    assert layer.options["colorFilter"] == [
        "invert:100%",
        "grayscale:80%",
        "hue-rotate:180deg",
    ]


def test_plain_tile_layer_gets_no_color_filter():
    m = folium.Map([52.1, 5.1], zoom_start=5, tiles=None)
    layer = TileLayer().add_to(m)

    rendered = m.get_root().render()

    assert PLUGIN_SCRIPT not in rendered
    assert "colorFilter" not in layer_options(rendered, layer.get_name())


@pytest.mark.parametrize(
    "filter,message",
    [
        ("notafilter:1", "Unknown color filter"),
        ("invert:abc", "Invalid value"),
        ("invert:-10", "Invalid value"),
        ("invert:10.5%", "Invalid value"),
        ("invert:100deg", "Wrong unit"),
        ("blur:10%", "Wrong unit"),
    ],
)
def test_tile_layer_color_filter_invalid(filter, message):
    with pytest.raises(ValueError, match=message):
        plugins.TileLayerColorFilter(filter)


def test_tile_layer_color_filter_requires_strings():
    with pytest.raises(ValueError, match="Filters must be strings"):
        plugins.TileLayerColorFilter([100])  # type: ignore[list-item]
