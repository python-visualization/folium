from folium.elements import JSCSSMixin
from folium.map import Layer, LayerControl
from folium.utilities import parse_options

from jinja2 import Template
from collections import OrderedDict

class GroupedLayerControl(JSCSSMixin, LayerControl):
    """
    """
    default_js = [
        ('leaflet.groupedlayercontrol.min.js',
         'https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.js'),
        ('leaflet.groupedlayercontrol.min.js.map',
         'https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.js.map')
    ]
    default_css = [
        ('leaflet.groupedlayercontrol.min.css',
         'https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.css')
    ]

    _template = Template("""
        {% macro script(this,kwargs) %}
            var {{ this.get_name() }} = {
                base_layers : {
                    {%- for key, val in this.base_layers.items() %}
                    {{ key|tojson }} : {{val}},
                    {%- endfor %}
                },
                overlays :  {
                    {%- for key, val in this.un_grouped_overlays.items() %}
                    {{ key|tojson }} : {{val}},
                    {%- endfor %}
                },
            };

            L.control.layers(
                {{ this.get_name() }}.base_layers,
                {{ this.get_name() }}.overlays,
                {{ this.options|tojson }}
            ).addTo({{this._parent.get_name()}});

            var groupedOverlays = {
                {%- for key, overlays in this.grouped_overlays.items() %}
                {{ key|tojson }} : {
                    {%- for overlaykey, val in overlays.items() %}
                    {{ overlaykey|tojson }} : {{val}},
                    {%- endfor %}
                },
                {%- endfor %}
            };

            var options = {
                exclusiveGroups: [
                    {%- for key, value in this.grouped_overlays.items() %}
                    {{key|tojson}},
                    {%- endfor %}
                ],
                collapsed: {{ this.options["collapsed"]|tojson }},
                autoZIndex: {{ this.options["autoZIndex"]|tojson }},
                position: {{ this.options["position"]|tojson }},
            };

            L.control.groupedLayers(
                null,
                groupedOverlays,
                options,
            ).addTo({{this._parent.get_name()}});

            {%- for val in this.layers_untoggle.values() %}
            {{ val }}.remove();
            {%- endfor %}

        {% endmacro %}
        """)


    def __init__(
        self, 
        groups,
        position='topright', 
        collapsed=False, 
        autoZIndex=True, 
        groupCheckboxes=True,
        **kwargs
    ):
        super(GroupedLayerControl, self).__init__()
        self._name = 'GroupedLayerControl'
        self.groups = {x:key for key,sublist in groups.items() for x in sublist}
        self.groupCheckboxes = groupCheckboxes
        self.options = parse_options(
            position=position,
            collapsed=collapsed,
            autoZIndex=autoZIndex,
            **kwargs
        )
        self.base_layers = OrderedDict()
        self.un_grouped_overlays = OrderedDict()
        self.layers_untoggle = OrderedDict()
        self.grouped_overlays = OrderedDict()
        for val in self.groups.values():
            self.grouped_overlays[val] = OrderedDict()

    def reset(self):
        self.base_layers = OrderedDict()
        self.un_grouped_overlays = OrderedDict()
        self.layers_untoggle = OrderedDict()
        self.grouped_overlays = OrderedDict()

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        for item in self._parent._children.values():
            if not isinstance(item, Layer) or not item.control:
                continue
            key = item.layer_name
            
            if not item.overlay:
                self.base_layers[key] = item.get_name()
                if len(self.base_layers) > 1:
                    self.layers_untoggle[key] = item.get_name()
            else:
                if key in self.groups.keys():
                    self.grouped_overlays[self.groups[key]][key] = item.get_name()
                    if not item.show:
                        self.layers_untoggle[key] = item.get_name()
                else:
                    self.un_grouped_overlays[key] = item.get_name()
                    if not item.show:
                        self.layers_untoggle[key] = item.get_name()
        super(GroupedLayerControl, self).render()