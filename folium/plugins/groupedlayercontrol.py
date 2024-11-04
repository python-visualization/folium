from branca.element import MacroElement

from folium.elements import JSCSSMixin
from folium.template import Template


class GroupedLayerControl(JSCSSMixin, MacroElement):
    """
    Create a Layer Control with groups of overlays.

    Parameters
    ----------
    groups : dict
          A dictionary where the keys are group names and the values are lists
          of layer objects.
          e.g. {
              "Group 1": [layer1, layer2],
              "Group 2": [layer3, layer4]
            }
    exclusive_groups: bool, default True
         Whether to use radio buttons (default) or checkboxes.
         If you want to use both, use two separate instances of this class.
    **kwargs
        Additional (possibly inherited) options. See
        https://leafletjs.com/reference.html#control-layers

    """

    default_js = [
        (
            "leaflet.groupedlayercontrol.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.js",  # noqa
        ),
    ]
    default_css = [
        (
            "leaflet.groupedlayercontrol.min.css",
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.css",  # noqa
        )
    ]

    _template = Template(
        """
        {% macro script(this,kwargs) %}

            L.control.groupedLayers(
                null,
                {
                    {%- for group_name, overlays in this.grouped_overlays.items() %}
                    {{ group_name|tojson }} : {
                        {%- for overlaykey, val in overlays.items() %}
                        {{ overlaykey|tojson }} : {{val}},
                        {%- endfor %}
                    },
                    {%- endfor %}
                },
                {{ this.options|tojavascript }},
            ).addTo({{this._parent.get_name()}});

            {%- for val in this.layers_untoggle %}
            {{ val }}.remove();
            {%- endfor %}

        {% endmacro %}
        """
    )

    def __init__(self, groups, exclusive_groups=True, **kwargs):
        super().__init__()
        self._name = "GroupedLayerControl"
        self.options = dict(**kwargs)
        if exclusive_groups:
            self.options["exclusiveGroups"] = list(groups.keys())
        self.layers_untoggle = set()
        self.grouped_overlays = {}
        for group_name, sublist in groups.items():
            self.grouped_overlays[group_name] = {}
            for element in sublist:
                self.grouped_overlays[group_name][
                    element.layer_name
                ] = element.get_name()
                if not element.show:
                    self.layers_untoggle.add(element.get_name())
                # make sure the elements used in GroupedLayerControl
                # don't show up in the regular LayerControl.
                element.control = False
            if exclusive_groups:
                # only enable the first radio button
                for element in sublist[1:]:
                    self.layers_untoggle.add(element.get_name())
