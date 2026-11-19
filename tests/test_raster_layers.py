"""
Test raster_layers
------------------

"""

import warnings

import numpy as np
import pytest
import xyzservices

import folium
from folium.template import Template
from folium.utilities import normalize


def test_tile_layer():
    m = folium.Map([48.0, 5.0], zoom_start=6)
    layer = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

    folium.raster_layers.TileLayer(
        tiles=layer, name="OpenStreetMap", attr="attribution"
    ).add_to(m)

    folium.raster_layers.TileLayer(
        tiles=layer, name="OpenStreetMap2", attr="attribution2", overlay=True
    ).add_to(m)

    folium.LayerControl().add_to(m)
    m._repr_html_()

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def _is_working_zoom_level(zoom, tiles, session):
    """Check if the zoom level works for the given tileset."""
    url = tiles.format(s="a", x=0, y=0, z=zoom)
    response = session.get(url, timeout=5)
    if response.status_code < 400:
        return True
    return False


def test_custom_tile_subdomains():
    """Test custom tile subdomains."""
    url = "http://{s}.custom_tiles.org/{z}/{x}/{y}.png"
    m = folium.Map()
    folium.TileLayer(
        tiles=url, name="subdomains2", attr="attribution", subdomains="mytilesubdomain"
    ).add_to(m)
    out = m._parent.render()
    assert "mytilesubdomain" in out


def test_wms():
    m = folium.Map([40, -100], zoom_start=4)
    url = "http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi"
    w = folium.raster_layers.WmsTileLayer(
        url=url,
        name="test",
        fmt="image/png",
        layers="nexrad-n0r-900913",
        attr="Weather data © 2012 IEM Nexrad",
        transparent=True,
        cql_filter="something",
    )
    w.add_to(m)
    html = m.get_root().render()

    # verify this special case wasn't converted to lowerCamelCase
    assert '"cql_filter": "something",' in html
    assert "cqlFilter" not in html

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_image_overlay():
    """Test image overlay."""
    data = [
        [[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[1, 1, 0, 0.5], [0, 0, 1, 1], [0, 0, 1, 1]],
    ]

    m = folium.Map()
    io = folium.raster_layers.ImageOverlay(
        data, [[0, -180], [90, 180]], mercator_project=True
    )
    io.add_to(m)
    m._repr_html_()

    out = m._parent.render()

    # Verify the URL generation.
    url = (
        "data:image/png;base64,"
        "iVBORw0KGgoAAAANSUhEUgAAAAMAAAACCAYAAACddGYaAAA"
        "AF0lEQVR42mP4z8AARFDw/z/DciC5DoQBV78H/mpWZYkAAAAASUVORK5CYII="
    )
    assert io.url == url

    # Verify the script part is okay.
    tmpl = Template("""
        var {{this.get_name()}} = L.imageOverlay(
            "{{ this.url }}",
            {{ this.bounds }},
            {{ this.options }}
        );
        {{ this.get_name() }}.addTo({{this._parent.get_name()}});
    """)
    assert normalize(tmpl.render(this=io)) in normalize(out)

    bounds = m.get_bounds()
    assert bounds == [[0, -180], [90, 180]], bounds


def test_image_overlay_mercator_project_keeps_uint8_colors():
    data = np.full((4, 3, 4), (100, 50, 200, 255), dtype="uint8")
    bounds = [[40, 0], [50, 10]]

    plain = folium.raster_layers.ImageOverlay(data, bounds)
    projected = folium.raster_layers.ImageOverlay(data, bounds, mercator_project=True)

    assert projected.url == plain.url


@pytest.mark.parametrize(
    "tiles", ["CartoDB DarkMatter", xyzservices.providers.CartoDB.DarkMatter]
)
def test_xyzservices(tiles):
    m = folium.Map([48.0, 5.0], tiles=tiles, zoom_start=6)

    folium.raster_layers.TileLayer(
        tiles=xyzservices.providers.CartoDB.Positron,
    ).add_to(m)
    folium.LayerControl().add_to(m)

    out = m._parent.render()
    assert (
        xyzservices.providers.CartoDB.DarkMatter.build_url(
            fill_subdomain=False, scale_factor="{r}"
        )
        in out
    )
    assert (
        xyzservices.providers.CartoDB.Positron.build_url(
            fill_subdomain=False, scale_factor="{r}"
        )
        in out
    )


@pytest.mark.parametrize(
    "tiles", ["CartoDB Positron", xyzservices.providers.CartoDB.Positron]
)
def test_tile_layer_api_key(tiles):
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # no "API key required" warning
        layer = folium.TileLayer(tiles, api_key="my-key")
    assert layer.tiles == xyzservices.providers.CartoDB.Positron.build_url(
        fill_subdomain=False, scale_factor="{r}", apikey="my-key"
    )
    assert layer.tiles.endswith("?key=my-key")
    assert "api_key" not in layer.options
    assert "apiKey" not in layer.options


def test_tile_layer_api_key_other_placeholder_name():
    # MapBox calls its token placeholder `accessToken`, not `apikey`.
    layer = folium.TileLayer("MapBox", api_key="my-token")
    assert "access_token=my-token" in layer.tiles


def test_tile_layer_api_key_does_not_modify_provider():
    provider = xyzservices.providers.CartoDB.Positron
    folium.TileLayer(provider, api_key="my-key")
    assert provider.requires_token()


def test_tile_layer_api_key_rejects_custom_url():
    with pytest.raises(ValueError, match="custom tile URL"):
        folium.TileLayer(
            "https://{s}.example.com/{z}/{x}/{y}.png", attr="x", api_key="my-key"
        )


def test_tile_layer_api_key_rejects_provider_without_placeholder():
    with pytest.raises(ValueError, match="no API key placeholder"):
        folium.TileLayer("OpenStreetMap", api_key="my-key")
