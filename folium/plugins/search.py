# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from ..utilities import camelize, get_parent_map

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template

from folium.features import GeoJson

class Search(MacroElement):
    """
    Adds a search tool to your map.

    Parameters
    ----------
    search_label: str
        label to index the search, default 'name'
    search_zoom: int
        optional zoom level to set the map to on match, default None.
        if None, will zoom to Polygon bounds and points on their
        natural extent.
    geom_type: str
        geometry type, default 'Point'
    position: str
        Change the position of the search bar, can be:
        'topleft', 'topright', 'bottomright' or 'bottomleft',
        default 'topleft'
    **kwargs.
        Assorted style options to change feature styling on match.
        Use the same way as vector layer arguments.

    See https://github.com/stefanocudini/leaflet-search for more information.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            let searchZoom = {{this.search_zoom}};
            
            var searchControl = new L.Control.Search({
                layer: {{this._parent.get_name()}},
                propertyName: '{{this.search_label}}',
            {% if this.geom_type == 'Point' %}
                initial: false,
                zoom: searchZoom?searchZoom:{{this._parent._parent.get_name()}}.getZoom(),
                position:'{{this.position}}',
                hideMarkerOnCollapse: true
            {% endif %}
            {% if this.geom_type == 'Polygon' %}
                marker: false,
                moveToLocation: function(latlng, title, map) {
                var zoom = searchZoom?searchZoom:map.getBoundsZoom(latlng.layer.getBounds())
                    map.setView(latlng, zoom); // access the zoom
                }
            {% endif %}
                });
                searchControl.on('search:locationfound', function(e) {
                    {{this._parent.get_name()}}.setStyle(function(feature){
                        return feature.properties.style
                    })
                    {% if this.options %}
                    e.layer.setStyle({{ this.options }});
                    {% endif %}
                    if(e.layer._popup)
                        e.layer.openPopup();
                })
                .on('search:collapsed', function(e) {
                        {{this._parent.get_name()}}.setStyle(function(feature){
                            return feature.properties.style
                    });
                });
            {{this.parent_map_name}}.addControl( searchControl );

        {% endmacro %}
        """)  # noqa

    def __init__(self, search_label='name', search_zoom=None, geom_type='Point', position='topleft', **kwargs):
        super(Search, self).__init__()
        self.search_label = search_label
        self.search_zoom = json.dumps(search_zoom)
        self.geom_type = geom_type
        self.position = position
        self.options = json.dumps({camelize(key): value for key, value in kwargs.items()})

    def test_params(self, keys, parent):
        assert self.search_label in keys, "The label '{}' was not available in {}".format(self.search_label, keys)
        assert isinstance(parent, GeoJson), "Search can only be added to GeoJson objects."

    def render(self, **kwargs):
        keys = list(self._parent.data['features'][0]['properties'].keys())
        self.test_params(keys=keys, parent=self._parent)
        self.parent_map_name = get_parent_map(self)
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
