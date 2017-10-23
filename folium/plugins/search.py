# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template


class Search(MacroElement):
    """
    Adds a search tool to your map.

    Parameters
    ----------
    position : str
          change the position of the search bar, can be:
          'topleft', 'topright', 'bottomright' or 'bottomleft'
          default: 'topleft'
    See https://github.com/stefanocudini/leaflet-search for more information.

    """

    def __init__(self, data, search_zoom=12, search_label='name', geom_type='Point',
                 position='topleft', popup_on_found=True):
        super(Search, self).__init__()
        self.position = position
        self.data = data
        self.search_label = search_label
        self.search_zoom = search_zoom
        self.geom_type = geom_type
        self.popup_on_found = popup_on_found

        self._template = Template("""
        {% macro script(this, kwargs) %}

            var {{this.get_name()}} = new L.geoJson.css({{this.data}});

            {{this._parent.get_name()}}.addLayer({{this.get_name()}});

            if ('{{this.geom_type}}' == 'Point'){
                var searchControl = new L.Control.Search({
                    layer: {{this.get_name()}},
                    propertyName: '{{this.search_label}}',
                    initial: false,
                    zoom: {{this.search_zoom}},
                    position:'{{this.position}}',
                    hideMarkerOnCollapse: true
                });
                if ({{'true' if this.popup_on_found else 'false'}}) {
                    searchControl.on('search:locationfound', function(e) {

                        if(e.layer._popup)
                            e.layer.openPopup();

                    });
                };

            } else if ('{{this.geom_type}}' == 'Polygon') {
                var searchControl = new L.Control.Search({
                    layer: {{this.get_name()}},
                    propertyName: '{{this.search_label}}',
                    marker: false,
                    position:'{{this.position}}',
                    moveToLocation: function(latlng, title, map) {
                        var zoom = {{this._parent.get_name()}}.getBoundsZoom(latlng.layer.getBounds());
                        {{this._parent.get_name()}}.setView(latlng, zoom); // access the zoom
                    }
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
            }

    
            {{this._parent.get_name()}}.addControl( searchControl ); 

        {% endmacro %}
        """)  # noqa

    def render(self, **kwargs):
        super(Search, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdn.jsdelivr.net/npm/leaflet-search@2.3.6/dist/leaflet-search.min.js'),  # noqa
            name='Leaflet.Search.js'
        )

        figure.header.add_child(
            CssLink('https://cdn.jsdelivr.net/npm/leaflet-search@2.3.6/dist/leaflet-search.min.css'),  # noqa
            name='Leaflet.Search.css'
        )

        figure.header.add_child(
            JavascriptLink('https://cdn.rawgit.com/albburtsev/Leaflet.geojsonCSS/master/leaflet.geojsoncss.min.js'),  # noqa
            name='Leaflet.GeoJsonCss.js'
        )
