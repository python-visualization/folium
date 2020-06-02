#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from branca.element import Figure, JavascriptLink, CssLink

from folium.map import Layer
from folium.utilities import (
    parse_options,
    if_pandas_df_convert_to_numpy
)

from jinja2 import Template


class TagFilterButton(Layer):
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
    on_selection_complete: func, default None
        Callback function for the selected tags
    clear_text: string, default 'clear'
        Text of the clear button
    filter_on_every_click: bool, default True
        if True, the plugin will filter on every click event on checkbox.
    open_popup_on_hover:bool, default False
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

    def __init__(self, data, name=None, icon="fa-filter",
                 on_selection_complete=None,
                 clear_text='clear', filter_on_every_click=True,
                 open_popup_on_hover=False, 
                 overlay=True, control=True, show=True, **kwargs):
        super(TagFilterButton, self).__init__(name=name, overlay=overlay,
                                      control=control, show=show)
        self._name = 'TagFilterButton'
        data = if_pandas_df_convert_to_numpy(data)
        self.options = parse_options(
            data=data,
            icon=icon,
            on_selection_complete=on_selection_complete,
            clear_text=clear_text,
            filter_on_every_click=filter_on_every_click,
            open_popup_on_hover=open_popup_on_hover,
            **kwargs
        )

    def render(self, **kwargs):
        super(TagFilterButton, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdn.jsdelivr.net/npm/leaflet-tag-filter-button@0.0.4/src/leaflet-tag-filter-button.js'),
            name='tag-filter-button.js')
            # JavascriptLink('https://raw.githubusercontent.com/maydemirx/leaflet-tag-filter-button/master/src/leaflet-tag-filter-button.js'),  # noqa

        figure.header.add_child(
            JavascriptLink('https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.js'),  # noqa
            name='easy-button.js')
        
        figure.header.add_child(
            CssLink('https://cdn.jsdelivr.net/npm/leaflet-tag-filter-button@0.0.4/src/leaflet-tag-filter-button.css'),
            name='tag-filter-button.css')
        # CssLink('https://raw.githubusercontent.com/maydemirx/leaflet-tag-filter-button/master/src/leaflet-tag-filter-button.css'),  # noqa

        figure.header.add_child(
            CssLink('https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.css'),
            name='easy-button.css')
        
        figure.header.add_child(
            CssLink('https://cdn.jsdelivr.net/npm/css-ripple-effect@1.0.5/dist/ripple.min.css'),
            name='ripples.min.css')

