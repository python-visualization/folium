"""
Test raster_layers
------------------

"""
import folium
from folium.utilities import normalize

from jinja2 import Template

import xyzservices


def test_tile_layer():
    m = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)
    layer = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

    folium.raster_layers.TileLayer(
        tiles=layer,
        name='OpenStreetMap',
        attr='attribution'
    ).add_to(m)

    folium.raster_layers.TileLayer(
        tiles=layer,
        name='OpenStreetMap2',
        attr='attribution2',
        overlay=True).add_to(m)

    folium.LayerControl().add_to(m)
    m._repr_html_()

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def _is_working_zoom_level(zoom, tiles, session):
    """Check if the zoom level works for the given tileset."""
    url = tiles.format(s='a', x=0, y=0, z=zoom)
    response = session.get(url, timeout=5)
    if response.status_code < 400:
        return True
    return False


def test_custom_tile_subdomains():
    """Test custom tile subdomains."""
    url = 'http://{s}.custom_tiles.org/{z}/{x}/{y}.png'
    m = folium.Map()
    folium.TileLayer(
        tiles=url,
        name='subdomains2',
        attr='attribution',
        subdomains='mytilesubdomain'
    ).add_to(m)
    out = m._parent.render()
    assert 'mytilesubdomain' in out


def test_wms():
    m = folium.Map([40, -100], zoom_start=4)
    url = 'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi'
    w = folium.raster_layers.WmsTileLayer(
        url=url,
        name='test',
        fmt='image/png',
        layers='nexrad-n0r-900913',
        attr=u'Weather data © 2012 IEM Nexrad',
        transparent=True
    )
    w.add_to(m)
    m._repr_html_()

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_image_overlay():
    """Test image overlay."""
    data = [[[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[1, 1, 0, 0.5], [0, 0, 1, 1], [0, 0, 1, 1]]]

    m = folium.Map()
    io = folium.raster_layers.ImageOverlay(
        data, [[0, -180], [90, 180]],
        mercator_project=True
    )
    io.add_to(m)
    m._repr_html_()

    out = m._parent.render()

    # Verify the URL generation.
    url = ('data:image/png;base64,'
           'iVBORw0KGgoAAAANSUhEUgAAAAMAAAACCAYAAACddGYaAAA'
           'AF0lEQVR42mP4z8AARFDw/z/DeiA5H4QBV60H6ABl9ZIAAAAASUVORK5CYII=')
    assert io.url == url

    # Verify the script part is okay.
    tmpl = Template("""
        var {{this.get_name()}} = L.imageOverlay(
            "{{ this.url }}",
            {{ this.bounds }},
            {{ this.options }}
            ).addTo({{this._parent.get_name()}});
    """)
    assert normalize(tmpl.render(this=io)) in normalize(out)

    bounds = m.get_bounds()
    assert bounds == [[0, -180], [90, 180]], bounds


def test_xyzservices():
    m = folium.Map([48., 5.], tiles=xyzservices.providers.Stamen.Toner, zoom_start=6)

    folium.raster_layers.TileLayer(
        tiles=xyzservices.providers.Stamen.Terrain,
    ).add_to(m)
    folium.LayerControl().add_to(m)

    out = m._parent.render()
    assert xyzservices.providers.Stamen.Toner.build_url(
        fill_subdomain=False, scale_factor="{r}"
    ) in out
    assert xyzservices.providers.Stamen.Terrain.build_url(
        fill_subdomain=False, scale_factor="{r}"
    ) in out
