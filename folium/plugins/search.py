# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from ..utilities import camelize, get_parent_map

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template

from folium import Map

from folium.features import FeatureGroup, GeoJson, TopoJson

from folium.plugins import MarkerCluster


class Search(MacroElement):
    """
    Adds a search tool to your map.

    Parameters
    ----------
    search_label: str
        label to index the search, default 'name'
    search_zoom: int, optional
        Zoom level to set the map to on match.
        By default zooms to Polygon/Line bounds and points
        on their natural extent.
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
            let {{this.layer.get_name()}}searchZoom = {{this.search_zoom}};
            
            var {{this.layer.get_name()}}searchControl = new L.Control.Search({
                layer: {{this.layer.get_name()}},
                propertyName: '{{this.search_label}}',
                collapsed: {{this.collapsed}},
                textPlaceholder: '{{this.placeholder}}',
            {% if this.geom_type == 'Point' %}
                initial: false,
                zoom: {{this.layer.get_name()}}searchZoom?{{this.layer.get_name()}}searchZoom:{{this.parent_map_name}}.getZoom(),
                position:'{{this.position}}',
                hideMarkerOnCollapse: true
            {% else %}
                marker: false,
                moveToLocation: function(latlng, title, map) {
                var zoom = {{this.layer.get_name()}}searchZoom?{{this.layer.get_name()}}searchZoom:map.getBoundsZoom(latlng.layer.getBounds())
                    map.setView(latlng, zoom); // access the zoom
                }
            {% endif %}
                });
                {{this.layer.get_name()}}searchControl.on('search:locationfound', function(e) {
                    {{this.layer.get_name()}}.setStyle(function(feature){
                        return feature.properties.style
                    })
                    {% if this.options %}
                    e.layer.setStyle({{ this.options }});
                    {% endif %}
                    if(e.layer._popup)
                        e.layer.openPopup();
                })
                {{this.layer.get_name()}}searchControl.on('search:collapsed', function(e) {
                        {{this.layer.get_name()}}.setStyle(function(feature){
                            return feature.properties.style
                    });
                });
            {{this.parent_map_name}}.addControl( {{this.layer.get_name()}}searchControl );

        {% endmacro %}
        """)  # noqa

    def __init__(self, layer=None, search_label='name', search_zoom=None, geom_type='Point', position='topleft',
                 placeholder='Search', collapsed=True, **kwargs):
        super(Search, self).__init__()
        assert isinstance(layer, folium.GeoJson), "Search can only be added to GeoJson objects."
        self.layer = layer
        self.search_label = search_label
        self.search_zoom = json.dumps(search_zoom)
        self.geom_type = geom_type
        self.position = position
        self.placeholder = placeholder
        self.collapsed = json.dumps(collapsed)
        self.options = json.dumps({camelize(key): value for key, value in kwargs.items()}) if len(kwargs.items()) > 0 \
            else None

    def test_params(self, keys, parent):
        assert self.search_label in keys, "The label '{}' was not available in {}".format(self.search_label, keys)
        assert isinstance(self._parent, folium.Map), "Search can only be added to folium Map objects."

    def render(self, **kwargs):
        keys = list(self.layer.data['features'][0]['properties'].keys())
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
