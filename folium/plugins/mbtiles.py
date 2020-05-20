# -*- coding: utf-8 -*-

from branca.element import Figure, JavascriptLink
from jinja2 import Template

from folium.raster_layers import TileLayer

_default_js = _default_js = [
    ('sql-js',
     'https://unpkg.com/sql.js@0.3.2/js/sql.js'),
    ('MBTiles',
     'https://unpkg.com/leaflet.tilelayer.mbtiles@latest/Leaflet.TileLayer.MBTiles.js')
    ]


class MBTiles(TileLayer):
    """
    Class to display raster tiles in MBTiles format.

    See https://wiki.openstreetmap.org/wiki/MBTiles for overview.
    See https://www.npmjs.com/package/Leaflet.TileLayer.MBTiles for original Leaflet plugin.

    Example
    -------
    # Map from Folium Quickstart
    m = folium.Map(
        location=[45.5236, -122.6750],
        tiles='Stamen Toner',
        zoom_start=13
    )

    # Add mbtiles layer to Map
    MBTiles(
        location=[45.5236, -122.6750],
        tiles='path/to/your_tiles.mbtiles',
        zoom_start=13
    ).add_to(m)
    """

    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.tileLayer.mbTiles(
                {{ this.tiles|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)  # noqa

    def render(self, **kwargs):
        super().render()

        figure = self.get_root()
        assert isinstance(figure, Figure), 'You cannot render this Element if it is not in a Figure.'

        # Import Javascripts
        for name, url in _default_js:
            figure.header.add_child(JavascriptLink(url), name=name)

