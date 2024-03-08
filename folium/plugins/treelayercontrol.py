from typing import Union

from branca.element import MacroElement

from folium.elements import JSCSSMixin
from folium.template import Template
from folium.utilities import parse_options


class TreeLayerControl(JSCSSMixin, MacroElement):
    """
    Create a Layer Control allowing a tree structure for the layers.
    See https://github.com/jjimenezshaw/Leaflet.Control.Layers.Tree for more
    information.

    Parameters
    ----------
    base_tree : dict
        A dictionary defining the base layers.
        Valid elements are

        children: list
            Array of child nodes for this node. Each node is a dict that has the same valid elements as base_tree.
        label: str
            Text displayed in the tree for this node. It may contain HTML code.
        layer: Layer
            The layer itself. This needs to be added to the map.
        name: str
            Text displayed in the toggle when control is minimized.
            If not present, label is used. It makes sense only when
            namedToggle is true, and with base layers.
        radioGroup: str, default ''
            Text to identify different radio button groups.
            It is used in the name attribute in the radio button.
            It is used only in the overlays layers (ignored in the base
            layers), allowing you to have radio buttons instead of checkboxes.
            See that radio groups cannot be unselected, so create a 'fake'
            layer (like L.layersGroup([])) if you want to disable it.
            Default '' (that means checkbox).
        collapsed: bool, default False
            Indicate whether this tree node should be collapsed initially,
            useful for opening large trees partially based on user input or
            context.
        selectAllCheckbox: bool or str
            Displays a checkbox to select/unselect all overlays in the
            sub-tree. In case of being a <str>, that text will be the title
            (tooltip). When any overlay in the sub-tree is clicked, the
            checkbox goes into indeterminate state (a dash in the box).
    overlay_tree: dict
        Similar to baseTree, but for overlays.
    closed_symbol: str, default '+',
        Symbol displayed on a closed node (that you can click to open).
    opened_symbol: str, default '-',
        Symbol displayed on an opened node (that you can click to close).
    space_symbol: str, default ' ',
        Symbol between the closed or opened symbol, and the text.
    selector_back: bool, default False,
        Flag to indicate if the selector (+ or −) is after the text.
    named_toggle: bool, default False,
        Flag to replace the toggle image (box with the layers image) with the
        'name' of the selected base layer. If the name field is not present in
        the tree for this layer, label is used. See that you can show a
        different name when control is collapsed than the one that appears
        in the tree when it is expanded.
    collapse_all: str, default '',
        Text for an entry in control that collapses the tree (baselayers or
        overlays). If empty, no entry is created.
    expand_all: str, default '',
        Text for an entry in control that expands the tree. If empty, no entry
        is created
    label_is_selector: str, default 'both',
        Controls if a label or only the checkbox/radiobutton can toggle layers.
        If set to `both`, `overlay` or `base` those labels can be clicked
        on to toggle the layer.
    **kwargs
        Additional (possibly inherited) options. See
        https://leafletjs.com/reference.html#control-layers

    Examples
    --------
    >>> import folium
    >>> from folium.plugins.treelayercontrol import TreeLayerControl
    >>> from folium.features import Marker

    >>> m = folium.Map(location=[46.603354, 1.8883335], zoom_start=5)

    >>> marker = Marker([48.8582441, 2.2944775]).add_to(m)

    >>> overlay_tree = {
    ...     "label": "Points of Interest",
    ...     "selectAllCheckbox": "Un/select all",
    ...     "children": [
    ...         {
    ...             "label": "Europe",
    ...             "selectAllCheckbox": True,
    ...             "children": [
    ...                 {
    ...                     "label": "France",
    ...                     "selectAllCheckbox": True,
    ...                     "children": [
    ...                         {"label": "Tour Eiffel", "layer": marker},
    ...                     ],
    ...                 }
    ...             ],
    ...         }
    ...     ],
    ... }

    >>> control = TreeLayerControl(overlay_tree=overlay_tree).add_to(m)
    """

    default_js = [
        (
            "L.Control.Layers.Tree.min.js",
            "https://cdn.jsdelivr.net/npm/leaflet.control.layers.tree@1.1.0/L.Control.Layers.Tree.min.js",  # noqa
        ),
    ]
    default_css = [
        (
            "L.Control.Layers.Tree.min.css",
            "https://cdn.jsdelivr.net/npm/leaflet.control.layers.tree@1.1.0/L.Control.Layers.Tree.min.css",  # noqa
        )
    ]

    _template = Template(
        """
        {% macro script(this,kwargs) %}
            L.control.layers.tree(
                {{this.base_tree|tojavascript}},
                {{this.overlay_tree|tojavascript}},
                {{this.options|tojson}}
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """
    )

    def __init__(
        self,
        base_tree: Union[dict, list, None] = None,
        overlay_tree: Union[dict, list, None] = None,
        closed_symbol: str = "+",
        opened_symbol: str = "-",
        space_symbol: str = "&nbsp;",
        selector_back: bool = False,
        named_toggle: bool = False,
        collapse_all: str = "",
        expand_all: str = "",
        label_is_selector: str = "both",
        **kwargs
    ):
        super().__init__()
        self._name = "TreeLayerControl"
        kwargs["closed_symbol"] = closed_symbol
        kwargs["openened_symbol"] = opened_symbol
        kwargs["space_symbol"] = space_symbol
        kwargs["selector_back"] = selector_back
        kwargs["named_toggle"] = named_toggle
        kwargs["collapse_all"] = collapse_all
        kwargs["expand_all"] = expand_all
        kwargs["label_is_selector"] = label_is_selector
        self.options = parse_options(**kwargs)
        self.base_tree = base_tree
        self.overlay_tree = overlay_tree
