# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from ..utilities import camelize

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
    layer: GeoJson, TopoJson, FeatureGroup, MarkerCluster class object.
        The map layer to index in the Search view.
    search_label: str, optional
        'properties' key in layer to index Search, if layer is GeoJson/TopoJson.
    search_zoom: int, optional
        Zoom level to set the map to on match.
        By default zooms to Polygon/Line bounds and points
        on their natural extent.
    geom_type: str, default 'Point'
        Feature geometry type. "Point","Line" or "Polygon"
    position: str, default 'topleft'
        Change the position of the search bar, can be:
        'topleft', 'topright', 'bottomright' or 'bottomleft',
    placeholder: str, default 'Search'
        Placeholder text inside the Search box if nothing is entered.
    collapsed: boolean, default False
        Whether the Search box should be collapsed or not.
    **kwargs.
        Assorted style options to change feature styling on match.
        Use the same way as vector layer arguments.

    See https://github.com/stefanocudini/leaflet-search for more information.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{this.layer.get_name()}}searchControl = new L.Control.Search({
                layer: {{this.layer.get_name()}},
                {% if this.search_label %}
                propertyName: '{{this.search_label}}',
                {% endif %}
                collapsed: {{this.collapsed|tojson|safe}},
                textPlaceholder: '{{this.placeholder}}',
            {% if this.geom_type == 'Point' %}
                initial: false,
                {% if this.search_zoom %}
                    zoom: {{this.search_zoom}},
                {% endif %}
                position:'{{this.position}}',
                hideMarkerOnCollapse: true
            {% else %}
                marker: false,
                moveToLocation: function(latlng, title, map) {
                var zoom = {% if this.search_zoom %} {{ this.search_zoom }} {% else %} map.getBoundsZoom(latlng.layer.getBounds()) {% endif %}
                    map.flyTo(latlng, zoom); // access the zoom
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
            {{this._parent.get_name()}}.addControl( {{this.layer.get_name()}}searchControl );

        {% endmacro %}
        """)  # noqa

    def __init__(self, layer, search_label=None, search_zoom=None, geom_type='Point', position='topleft',
                 placeholder='Search', collapsed=False, **kwargs):
        super(Search, self).__init__()
        assert isinstance(layer,
                          (GeoJson, MarkerCluster, FeatureGroup, TopoJson)
                          ), "Search can only index FeatureGroup, MarkerCluster, GeoJson, and TopoJson layers at " \
                             "this time."
        self.layer = layer
        self.search_label = search_label
        self.search_zoom = search_zoom
        self.geom_type = geom_type
        self.position = position
        self.placeholder = placeholder
        self.collapsed = collapsed
        self.options = json.dumps({camelize(key): value for key, value in kwargs.items()}) if len(kwargs.items()) > 0 \
            else None

    def test_params(self, keys):
        if keys is not None:
            assert self.search_label in keys, "The label '{}' was not available in {}".format(self.search_label, keys)
        assert isinstance(self._parent, Map), "Search can only be added to folium Map objects."

    def render(self, **kwargs):
        if isinstance(self.layer, GeoJson):
            keys = tuple(self.layer.data['features'][0]['properties'].keys())
        elif isinstance(self.layer, TopoJson):
            obj_name = self.layer.object_path.split('.')[-1]
            keys = tuple(self.layer.data['objects'][obj_name]['geometries'][0]['properties'].keys())
        else:
            keys = None
        self.test_params(keys=keys)
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
