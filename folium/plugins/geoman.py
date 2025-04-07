from branca.element import MacroElement

from folium.elements import JSCSSMixin
from folium.template import Template
from folium.utilities import remove_empty


class GeoMan(JSCSSMixin, MacroElement):
    """
    An Open Source Leaflet Plugin for editing polygons

    Examples
    --------
    >>> m = folium.Map()
    >>> Geoman().add_to(m)

    For more info please check
    https://github.com/geoman-io/leaflet-geoman/

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
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
            /* The global varianble below is needed to prevent streamlit-folium
               from barfing :-(
            */
            var drawnItems = drawnItems_{{ this.get_name() }};

            {{this._parent.get_name()}}.pm.addControls(
                {{this.options|tojavascript}}
            )
            drawnItems_{{ this.get_name() }}.eachLayer(function(layer){
                L.PM.reInitLayer(layer);
                {%- for event, handler in this.on.items()   %}
                layer.on(
                    "{{event}}",
                    {{handler}}
                );
                {%- endfor %}
            });

            {{ this._parent.get_name() }}.on("pm:create", function(e) {
                var layer = e.layer,
                    type = e.layerType;

                {%- for event, handler in this.on.items()   %}
                layer.on(
                    "{{event}}",
                    {{handler}}
                );
                {%- endfor %}
                drawnItems_{{ this.get_name() }}.addLayer(layer);
            });
            {{ this._parent.get_name() }}.on("pm:remove", function(e) {
                var layer = e.layer,
                    type = e.layerType;
                drawnItems_{{ this.get_name() }}.removeLayer(layer);
            });

        {% endmacro %}
        """
    )

    default_js = [
        (
            "leaflet_geoman_js",
            "https://unpkg.com/@geoman-io/leaflet-geoman-free@latest/dist/leaflet-geoman.js",
        )
    ]
    default_css = [
        (
            "leaflet_geoman_css",
            "https://unpkg.com/@geoman-io/leaflet-geoman-free@latest/dist/leaflet-geoman.css",
        )
    ]

    def __init__(
        self,
        position="topleft",
        feature_group=None,
        on=None,
        **kwargs,
    ):
        super().__init__()
        self._name = "GeoMan"
        self.feature_group = feature_group
        self.on = on or {}
        self.options = remove_empty(
            position=position, layer_group=feature_group, **kwargs
        )
