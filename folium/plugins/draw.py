from branca.element import MacroElement

from folium.elements import JSCSSMixin
from folium.template import Template

# Each corner maps to the pair of CSS edge offsets that pins the export button
# there. "topright" reproduces the historical hard-coded placement exactly.
_EXPORT_POSITION_CSS = {
    "topright": "top: 90px;\n                    right: 10px;",
    "topleft": "top: 90px;\n                    left: 10px;",
    "bottomright": "bottom: 20px;\n                    right: 10px;",
    "bottomleft": "bottom: 20px;\n                    left: 10px;",
}


def _export_position_to_css(export_position):
    try:
        return _EXPORT_POSITION_CSS[export_position]
    except KeyError:
        raise ValueError(
            "export_position must be one of "
            f"{sorted(_EXPORT_POSITION_CSS)}, not {export_position!r}"
        ) from None


class Draw(JSCSSMixin, MacroElement):
    '''
    Vector drawing and editing plugin for Leaflet.

    Parameters
    ----------
    export : bool, default False
        Add a small button that exports the drawn shapes as a geojson file.
    feature_group : FeatureGroup, optional
        The FeatureGroup object that will hold the editable figures. This can
        be used to initialize the Draw plugin with predefined Layer objects.
    filename : string, default 'data.geojson'
        Name of geojson file
    position : {'topleft', 'toprigth', 'bottomleft', 'bottomright'}
        Position of control.
        See https://leafletjs.com/reference.html#control
    export_position : {'topright', 'topleft', 'bottomright', 'bottomleft'}
        Corner of the map to place the export button in, when ``export``
        is True. Defaults to 'topright'. Use this to keep the button clear
        of other controls such as a LayerControl.
    show_geometry_on_click : bool, default True
        When True, opens an alert with the geometry description on click.
    draw_options : dict, optional
        The options used to configure the draw toolbar. See
        http://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html#drawoptions
    edit_options : dict, optional
        The options used to configure the edit toolbar. See
        https://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html#editpolyoptions
    on : dict, optional
        Event handlers to attach to the created layer. Pass a mapping from the
        names of the events to their `JsCode` handlers.

    Examples
    --------
    >>> m = folium.Map()
    >>> Draw(
    ...     export=True,
    ...     filename="my_data.geojson",
    ...     show_geometry_on_click=False,
    ...     position="topleft",
    ...     draw_options={"polyline": {"allowIntersection": False}},
    ...     edit_options={"poly": {"allowIntersection": False}},
    ...     on={"click": JsCode("""
    ...         function(event) {
    ...            alert(JSON.stringify(this.toGeoJSON()));
    ...         }
    ...     """)},
    ... ).add_to(m)

    For more info please check
    https://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html

    '''

    _template = Template("""
        {% macro html(this, kwargs) %}
            {% if this.export %}
            <style>
                #export_{{ this.get_name() }} {
                    position: absolute;
                    {{ this.export_position_css }}
                    z-index: 999;
                    background: white;
                    color: black;
                    padding: 6px;
                    border-radius: 4px;
                    font-family: 'Helvetica Neue';
                    cursor: pointer;
                    font-size: 12px;
                    text-decoration: none;
                }
            </style>
            <a href='#' id='export_{{ this.get_name() }}'>Export</a>
            {% endif %}
        {% endmacro %}

        {% macro script(this, kwargs) %}
            var options = {
              position: {{ this.position|tojson }},
              draw: {{ this.draw_options|tojson }},
              edit: {{ this.edit_options|tojson }},
            }
            {%- if this.feature_group  %}
                var drawnItems_{{ this.get_name() }} =
                    {{ this.feature_group.get_name() }};
            {%- else %}
                // FeatureGroup is to store editable layers.
                var drawnItems_{{ this.get_name() }} =
                    new L.featureGroup().addTo(
                        {{ this._parent.get_name() }}
                    );
            {%- endif %}

            options.edit.featureGroup = drawnItems_{{ this.get_name() }};
            var {{ this.get_name() }} = new L.Control.Draw(
                options
            ).addTo( {{this._parent.get_name()}} );
            {{ this._parent.get_name() }}.on(L.Draw.Event.CREATED, function(e) {
                var layer = e.layer,
                    type = e.layerType;
                var coords = JSON.stringify(layer.toGeoJSON());
                {%- if this.show_geometry_on_click %}
                layer.on('click', function() {
                    alert(coords);
                    console.log(coords);
                });
                {%- endif %}

                {%- for event, handler in this.on.items()   %}
                layer.on(
                    "{{event}}",
                    {{handler}}
                );
                {%- endfor %}
                drawnItems_{{ this.get_name() }}.addLayer(layer);
            });
            {{ this._parent.get_name() }}.on('draw:created', function(e) {
                drawnItems_{{ this.get_name() }}.addLayer(e.layer);
            });

            {% if this.export %}
            document.getElementById('export_{{ this.get_name() }}').onclick = function(e) {
                var data = drawnItems_{{ this.get_name() }}.toGeoJSON();
                var convertedData = 'text/json;charset=utf-8,'
                    + encodeURIComponent(JSON.stringify(data));
                document.getElementById('export_{{ this.get_name() }}').setAttribute(
                    'href', 'data:' + convertedData
                );
                document.getElementById('export_{{ this.get_name() }}').setAttribute(
                    'download', {{ this.filename|tojson }}
                );
            }
            {% endif %}
        {% endmacro %}
        """)

    default_js = [
        (
            "leaflet_draw_js",
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.2/leaflet.draw.js",
        )
    ]
    default_css = [
        (
            "leaflet_draw_css",
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.2/leaflet.draw.css",
        )
    ]

    def __init__(
        self,
        export=False,
        feature_group=None,
        filename="data.geojson",
        position="topleft",
        export_position="topright",
        show_geometry_on_click=True,
        draw_options=None,
        edit_options=None,
        on=None,
    ):
        super().__init__()
        self._name = "DrawControl"
        self.export = export
        self.feature_group = feature_group
        self.filename = filename
        self.position = position
        self.export_position_css = _export_position_to_css(export_position)
        self.show_geometry_on_click = show_geometry_on_click
        self.draw_options = draw_options or {}
        self.edit_options = edit_options or {}
        self.on = on or {}
