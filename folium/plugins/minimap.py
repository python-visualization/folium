# -*- coding: utf-8 -*-

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from folium.raster_layers import TileLayer
from folium.utilities import parse_options

from jinja2 import Template


class MiniMap(MacroElement):
    """Add a minimap (locator) to an existing map.

    Uses the Leaflet plugin by Norkart under BSD 2-Clause "Simplified" License.
    https://github.com/Norkart/Leaflet-MiniMap

    Parameters
    ----------
    tile_layer : folium TileLayer object or str, default None
        Provide a folium TileLayer object or the wanted tiles as string.
        If not provided it will use the default of 'TileLayer', currently
        OpenStreetMap.
    position : str, default 'bottomright'
        The standard Control position parameter for the widget.
    width : int, default 150
        The width of the minimap in pixels.
    height : int, default 150
        The height of the minimap in pixels.
    collapsed_width : int, default 25
        The width of the toggle marker and the minimap when collapsed in pixels.
    collapsed_height : int, default 25
        The height of the toggle marker and the minimap when collapsed
    zoom_level_offset : int, default -5
        The offset applied to the zoom in the minimap compared to the zoom of
        the main map. Can be positive or negative.
    zoom_level_fixed : int, default None
        Overrides the offset to apply a fixed zoom level to the minimap
        regardless of the main map zoom.
        Set it to any valid zoom level, if unset zoom_level_offset is used
        instead.
    center_fixed : bool, default False
        Applies a fixed position to the minimap regardless of the main map's
        view / position. Prevents panning the minimap, but does allow zooming
        (both in the minimap and the main map).
        If the minimap is zoomed, it will always zoom around the centerFixed
        point. You can pass in a LatLng-equivalent object.
    zoom_animation : bool, default False
        Sets whether the minimap should have an animated zoom.
        (Will cause it to lag a bit after the movement of the main map.)
    toggle_display : bool, default False
        Sets whether the minimap should have a button to minimise it.
    auto_toggle_display : bool, default False
        Sets whether the minimap should hide automatically
        if the parent map bounds does not fit within the minimap bounds.
        Especially useful when 'zoomLevelFixed' is set.
    minimized : bool, default False
        Sets whether the minimap should start in a minimized position.

    Examples
    --------
    >>> MiniMap(tile_layer='Stamen WaterColor', position='bottomleft')
    """

    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{ this.tile_layer.get_name() }} = L.tileLayer(
                {{ this.tile_layer.tiles|tojson }},
                {{ this.tile_layer.options|tojson }}
            );
            var {{ this.get_name() }} = new L.Control.MiniMap(
                {{ this.tile_layer.get_name() }},
                {{ this.options|tojson }}
            );
            {{ this._parent.get_name() }}.addControl({{ this.get_name() }});
        {% endmacro %}
    """)  # noqa

    def __init__(self, tile_layer=None, position='bottomright', width=150,
                 height=150, collapsed_width=25, collapsed_height=25,
                 zoom_level_offset=-5, zoom_level_fixed=None,
                 center_fixed=False, zoom_animation=False,
                 toggle_display=False, auto_toggle_display=False,
                 minimized=False, **kwargs):

        super(MiniMap, self).__init__()
        self._name = 'MiniMap'

        if tile_layer is None:
            self.tile_layer = TileLayer()
        elif isinstance(tile_layer, TileLayer):
            self.tile_layer = tile_layer
        else:
            self.tile_layer = TileLayer(tile_layer)

        self.options = parse_options(
            position=position,
            width=width,
            height=height,
            collapsed_width=collapsed_width,
            collapsed_height=collapsed_height,
            zoom_level_offset=zoom_level_offset,
            zoom_level_fixed=zoom_level_fixed,
            center_fixed=center_fixed,
            zoom_animation=zoom_animation,
            toggle_display=toggle_display,
            auto_toggle_display=auto_toggle_display,
            minimized=minimized,
            **kwargs
        )

    def render(self, **kwargs):
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')
        super(MiniMap, self).render()

        figure.header.add_child(JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet-minimap/3.6.1/Control.MiniMap.js'))  # noqa

        figure.header.add_child(CssLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet-minimap/3.6.1/Control.MiniMap.css'))  # noqa
