# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template


class Search(MacroElement):
    """
    Adds a search tool to your map.

    Parameters
    ----------
    data: str/JSON
        GeoJSON strings
    search_zoom: int
        zoom level when searching features, default 12
    search_label: str
        label to index the search, default 'name'
    geom_type: str
        geometry type, default 'Point'
    position: str
        Change the position of the search bar, can be:
        'topleft', 'topright', 'bottomright' or 'bottomleft',
        default 'topleft'

    See https://github.com/stefanocudini/leaflet-search for more information.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}

            var {{this.get_name()}} = new L.GeoJSON({{this.data}});

            {{this._parent.get_name()}}.addLayer({{this.get_name()}});

            var searchControl = new L.Control.Search({
                layer: {{this.get_name()}},
                propertyName: '{{this.search_label}}',
            {% if this.geom_type == 'Point' %}
                initial: false,
                zoom: {{this.search_zoom}},
                position:'{{this.position}}',
                hideMarkerOnCollapse: true
            {% endif %}
            {% if this.geom_type == 'Polygon' %}
                marker: false,
                moveToLocation: function(latlng, title, map) {
                var zoom = {{this._parent.get_name()}}.getBoundsZoom(latlng.layer.getBounds());
                    {{this._parent.get_name()}}.setView(latlng, zoom); // access the zoom
                }
            {% endif %}
                });
                searchControl.on('search:locationfound', function(e) {

                    e.layer.setStyle({fillColor: '#3f0', color: '#0f0'});
                    if(e.layer._popup)
                        e.layer.openPopup();

                }).on('search:collapsed', function(e) {

                    {{this.get_name()}}.eachLayer(function(layer) {   //restore feature color
                        {{this.get_name()}}.resetStyle(layer);
                    });
                });
            {{this._parent.get_name()}}.addControl( searchControl );

        {% endmacro %}
        """)  # noqa

    def __init__(self, data, search_zoom=12, search_label='name', geom_type='Point', position='topleft'):
        super(Search, self).__init__()
        self.position = position
        self.data = data
        self.search_label = search_label
        self.search_zoom = search_zoom
        self.geom_type = geom_type

    def render(self, **kwargs):
        super(Search, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdn.jsdelivr.net/npm/leaflet-search@2.9.7/dist/leaflet-search.min.js'),  # noqa
            name='Leaflet.Search.js'
        )

        figure.header.add_child(
            CssLink('https://cdn.jsdelivr.net/npm/leaflet-search@2.9.7/dist/leaflet-search.min.css'),  # noqa
            name='Leaflet.Search.css'
        )
