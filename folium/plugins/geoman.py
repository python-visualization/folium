from branca.element import MacroElement

from folium.elements import JSCSSMixin, leaflet_method
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
            /* ensure the name is usable */
            var {{this.get_name()}} = {{this._parent.get_name()}}.pm;
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
            /* The global variable below is needed to prevent streamlit-folium
               from barfing :-(
            */
            var drawnItems = drawnItems_{{ this.get_name() }};

            {{this.get_name()}}.addControls(
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

    def __init__(self, position="topleft", feature_group=None, on=None, **kwargs):
        super().__init__()
        self._name = "GeoMan"
        self.feature_group = feature_group
        self.on = on or {}
        self.options = remove_empty(position=position, **kwargs)

    @leaflet_method
    def set_global_options(self, **kwargs):
        pass

    @leaflet_method
    def enable_draw(self, shape, /, **kwargs):
        pass

    @leaflet_method
    def disable_draw(self):
        pass

    @leaflet_method
    def set_path_options(self, *, options_modifier, **options):
        pass

    @leaflet_method
    def enable_global_edit_mode(self, **options):
        pass

    @leaflet_method
    def disable_global_edit_mode(self):
        pass

    @leaflet_method
    def enable_global_drag_mode(self):
        pass

    @leaflet_method
    def disable_global_drag_mode(self):
        pass

    @leaflet_method
    def enable_global_removal_mode(self):
        pass

    @leaflet_method
    def disable_global_removal_mode(self):
        pass

    @leaflet_method
    def enable_global_cut_mode(self):
        pass

    @leaflet_method
    def disable_global_cut_mode(self):
        pass

    @leaflet_method
    def enable_global_rotation_mode(self):
        pass

    @leaflet_method
    def disable_global_rotation_mode(self):
        pass
