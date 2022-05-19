from collections import OrderedDict

from folium.elements import JSCSSMixin
from folium.map import Layer, LayerControl
from folium.utilities import parse_options

from jinja2 import Template


class GroupedLayerControl(JSCSSMixin, LayerControl):
    """
    Creates a GroupedLayerControl object to be added on a folium map.
    Allows grouping overlays together so that within groups, overlays are
    mutually exclusive (radio buttons).

    Parameters
    ----------
    groups : dict
          A dictionary where the keys are group names and the values are overlay names to be
          displayed with radio buttons. Overlays NOT specified in this dictionary are
          added with check boxes.
    position : str
          The position of the control (one of the map corners), can be
          'topleft', 'topright', 'bottomleft' or 'bottomright'
          default: 'topright'
    collapsed : bool, default True
          If true the control will be collapsed into an icon and expanded on
          mouse hover or touch.
    autoZIndex : bool, default True
          If true the control assigns zIndexes in increasing order to all of
          its layers so that the order is preserved when switching them on/off.
    **kwargs
        Additional (possibly inherited) options. See
        https://leafletjs.com/reference-1.6.0.html#control-layers

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
        **kwargs
    ):
        super(GroupedLayerControl, self).__init__()
        self._name = 'GroupedLayerControl'
        self.groups = {x: key for key, sublist in groups.items() for x in sublist}
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
