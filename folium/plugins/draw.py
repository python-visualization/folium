# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template


class Draw(MacroElement):
    """
    Vector drawing and editing plugin for Leaflet.

    Examples
    --------
    >>> m = folium.Map()
    >>> Draw().draw.add_to(m)

    For more info please check
    https://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html

    """
    def __init__(self):
        super(Draw, self).__init__()
        self._name = 'DrawControl'

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
            // FeatureGroup is to store editable layers.
            var drawnItems = new L.featureGroup().addTo({{this._parent.get_name()}});
            var {{this.get_name()}} = new L.Control.Draw({
                "edit": {"featureGroup": drawnItems}
                });
            {{this._parent.get_name()}}.addControl({{this.get_name()}});
            {{this._parent.get_name()}}.on(L.Draw.Event.CREATED, function (event) {
              var layer = event.layer,
                  type = event.layerType,
                  coords;
              var coords = JSON.stringify(layer.toGeoJSON());
              layer.on('click', function() {
                alert(coords);
                console.log(coords);
                });
               drawnItems.addLayer(layer);
             });
            {% endmacro %}
            """)

    def render(self, **kwargs):
        super(Draw, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdn.rawgit.com/Leaflet/Leaflet.draw/v0.4.12/dist/leaflet.draw.js'))  # noqa

        figure.header.add_child(
            CssLink('https://cdn.rawgit.com/Leaflet/Leaflet.draw/v0.4.12/dist/leaflet.draw.css'))  # noqa
