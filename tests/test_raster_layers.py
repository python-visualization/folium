# -*- coding: utf-8 -*-

"""
Test raster_layers
-----------------

"""

from __future__ import (absolute_import, division, print_function)
import requests

import folium

from jinja2 import Template


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


def test_verify_maximum_native_zoom_levels():
    """Verify that the max available zoom levels in the code are correct."""
    _env = folium.raster_layers.ENV
    tile_layer = folium.raster_layers.TileLayer()
    tilesets = ['openstreetmap', 'mapboxcontrolroom', 'mapboxbright',
                'stamenterrain', 'stamentoner', 'stamenwatercolor',
                'cartodbpositron', 'cartodbdark_matter']
    for name in tilesets:
        if name.startswith('stamen'):
            continue  # stamen is weird, gives HTTP 503, infite zoom.
        zoom_in_code = tile_layer._get_max_native_zoom(name)
        template = 'tiles/' + name + '/tiles.txt'
        tiles = _env.get_template(template).render()
        session = requests.session()
        if _is_working_zoom_level(zoom_in_code, tiles, session):
            step = 1
            test_range = range(zoom_in_code + 1, 40)
        else:
            step = -1
            test_range = range(zoom_in_code - 1, 1, step)
        for zoom in test_range:
            if not _is_working_zoom_level(zoom, tiles, session):
                zoom_in_test = zoom - step
                break
        else:
            raise RuntimeError('Did not get any respons for tileset {}.'.format(name))  # noqa
        if zoom_in_test != zoom_in_code:
            txt = ('max_native_zoom of tileset {} is {} in the code, but the'
                   ' test indicates it should be {}.')
            raise ValueError(txt.format(name, zoom_in_code, zoom_in_test))


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
    m = folium.Map(location=[45.52, -122.67], tiles=url,
                   attr='attribution',
                   subdomains='1234')

    url_with_name = 'http://{s}.custom_tiles-subdomains.org/{z}/{x}/{y}.png'
    tile_layer = folium.raster_layers.TileLayer(
        tiles=url,
        name='subdomains2',
        attr='attribution',
        subdomains='5678'
    )
    tile_layer.add_to(m)

    m.add_tile_layer(
        tiles=url_with_name, attr='attribution',
        subdomains='9012'
    )

    out = m._parent.render()
    assert '1234' in out
    assert '5678' in out
    assert '9012' in out


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
                    '{{ this.url }}',
                    {{ this.bounds }},
                    {{ this.options }}
                    ).addTo({{this._parent.get_name()}});
    """)
    assert tmpl.render(this=io) in out

    bounds = m.get_bounds()
    assert bounds == [[0, -180], [90, 180]], bounds
