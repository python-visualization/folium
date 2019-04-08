# -*- coding: utf-8 -*-

from branca.element import CssLink, Element, Figure, JavascriptLink, MacroElement

from jinja2 import Template


class Draw(MacroElement):
    """
    Vector drawing and editing plugin for Leaflet.

    Parameters
    ----------
    export : bool, default False
        Add a small button that exports the drawn shapes as a geojson file.
    filename : string, default 'data.geojson'
        Name of geojson file
    position : {'topleft', 'toprigth', 'bottomleft', 'bottomright'}
        Position of control.
        See https://leafletjs.com/reference-1.4.0.html#control
    draw_options : dict, optional
        The options used to configure the draw toolbar. See
        http://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html#drawoptions
    edit_options : dict, optional
        The options used to configure the edit toolbar. See
        https://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html#editpolyoptions

    Examples
    --------
    >>> m = folium.Map()
    >>> Draw(
    ...     export=True,
    ...     filename='my_data.geojson',
    ...     position='topleft',
    ...     draw_options={'polyline': {'allowIntersection': False}},
    ...     edit_options={'poly': {'allowIntersection': False}}
    ... ).add_to(m)

    For more info please check
    https://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var options = {
              position: {{ this.position|tojson }},
              draw: {{ this.draw_options }},
              edit: {{ this.edit_options }},
            }
            // FeatureGroup is to store editable layers.
            var drawnItems = new L.featureGroup().addTo(
                {{ this._parent.get_name() }}
            );
            options.edit.featureGroup = drawnItems;
            var {{ this.get_name() }} = new L.Control.Draw(
                options
            ).addTo( {{this._parent.get_name()}} );
            {{ this._parent.get_name() }}.on(L.Draw.Event.CREATED, function(e) {
                var layer = e.layer,
                    type = e.layerType;
                var coords = JSON.stringify(layer.toGeoJSON());
                layer.on('click', function() {
                    alert(coords);
                    console.log(coords);
                });
                drawnItems.addLayer(layer);
             });
            {{ this._parent.get_name() }}.on('draw:created', function(e) {
                drawnItems.addLayer(e.layer);
            });
            document.getElementById('export').onclick = function(e) {
                var data = drawnItems.toGeoJSON();
                var convertedData = 'text/json;charset=utf-8,'
                    + encodeURIComponent(JSON.stringify(data));
                document.getElementById('export').setAttribute(
                    'href', 'data:' + convertedData
                );
                document.getElementById('export').setAttribute(
                    'download', {{ this.filename|tojson }}
                );
            }
        {% endmacro %}
        """)

    def __init__(self, export=False, filename='data.geojson',
                 position='topleft', draw_options=None, edit_options=None):
        super(Draw, self).__init__()
        self._name = 'DrawControl'
        self.export = export
        self.filename = filename
        self.position = position
        self.draw_options = draw_options or {}
        self.edit_options = edit_options or {}

    def render(self, **kwargs):
        super(Draw, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.2/leaflet.draw.js'))  # noqa
        figure.header.add_child(
            CssLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.2/leaflet.draw.css'))  # noqa

        export_style = """
            <style>
                #export {
                    position: absolute;
                    top: 5px;
                    right: 10px;
                    z-index: 999;
                    background: white;
                    color: black;
                    padding: 6px;
                    border-radius: 4px;
                    font-family: 'Helvetica Neue';
                    cursor: pointer;
                    font-size: 12px;
                    text-decoration: none;
                    top: 90px;
                }
            </style>
        """
        export_button = """<a href='#' id='export'>Export</a>"""
        if self.export:
            figure.header.add_child(Element(export_style), name='export')
            figure.html.add_child(Element(export_button), name='export_button')
