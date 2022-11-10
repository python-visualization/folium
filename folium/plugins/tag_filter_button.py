from folium.elements import JSCSSMixin

from folium.map import Layer
from folium.utilities import parse_options

from jinja2 import Template


class TagFilterButton(JSCSSMixin, Layer):
    """
    Creates a Tag Filter Button to filter markers based on criteria
    (https://github.com/maydemirx/leaflet-tag-filter-button)

    Parameters
    ----------
    data: list, of strings.
        The tags to filter for this filter button.
    name: string, default None
        The name of the Layer, as it will appear in LayerControls.
    icon: string, default 'fa-filter'
        The icon for the filter button
    clear_text: string, default 'clear'
        Text of the clear button
    filter_on_every_click: bool, default True
        if True, the plugin will filter on every click event on checkbox.
    open_popup_on_hover: bool, default False
        if True, popup that contains tags will be open at mouse hover time
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.control.tagFilterButton(
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)

    default_js = [
        ('tag-filter-button.js',
         'https://cdn.jsdelivr.net/npm/leaflet-tag-filter-button/src/leaflet-tag-filter-button.js'),
        ('easy-button.js',
         'https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.js'),
    ]
    default_css = [
        ('tag-filter-button.css',
         'https://cdn.jsdelivr.net/npm/leaflet-tag-filter-button/src/leaflet-tag-filter-button.css'),
        ('easy-button.css',
         'https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.css'),
        ('ripples.min.css',
         'https://cdn.jsdelivr.net/npm/css-ripple-effect@1.0.5/dist/ripple.min.css'),
    ]

    def __init__(self, data, name=None, icon="fa-filter",
                 clear_text='clear', filter_on_every_click=True,
                 open_popup_on_hover=False,
                 overlay=True, control=True, show=True, **kwargs):
        super(TagFilterButton, self).__init__(name=name, overlay=overlay,
                                              control=control, show=show)
        self._name = 'TagFilterButton'
        self.options = parse_options(
            data=data,
            icon=icon,
            clear_text=clear_text,
            filter_on_every_click=filter_on_every_click,
            open_popup_on_hover=open_popup_on_hover,
            **kwargs
        )
