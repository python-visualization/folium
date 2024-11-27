from typing import Optional

from jinja2 import Template

from folium.elements import Element, JSCSSMixin, MacroElement
from folium.map import Marker
from folium.utilities import parse_options


class OverlappingMarkerSpiderfier(JSCSSMixin, MacroElement):
    """
    A plugin that handles overlapping markers on a map by spreading them out in a spiral or circle pattern when clicked.

    This plugin is useful when you have multiple markers in close proximity that would otherwise be difficult to interact with.
    When a user clicks on a cluster of overlapping markers, they spread out in a 'spider' pattern, making each marker
    individually accessible.

    Markers are automatically identified and managed by the plugin, so there is no need to add them separately.
    Simply add the plugin to the map using `oms.add_to(map)`.

    Parameters
    ----------
    keep_spiderfied : bool, default True
        If true, markers stay spiderfied after clicking.
    nearby_distance : int, default 20
        Pixels away from a marker that is considered overlapping.
    leg_weight : float, default 1.5
        Weight of the spider legs.
    circle_spiral_switchover : int, default 9
        Number of markers at which to switch from circle to spiral pattern.

    Example
    -------
    >>> oms = OverlappingMarkerSpiderfier(
    ...     keep_spiderfied=True, nearby_distance=30, leg_weight=2.0
    ... )
    >>> oms.add_to(map)
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
        (function () {
            try {
                var oms = new OverlappingMarkerSpiderfier(
                    {{ this._parent.get_name() }},
                    {{ this.options|tojson }}
                );

                oms.addListener('spiderfy', function() {
                    {{ this._parent.get_name() }}.closePopup();
                });

                {%- for marker in this.markers %}
                    oms.addMarker({{ marker.get_name() }});
                {%- endfor %}
            } catch (error) {
                console.error('Error initializing OverlappingMarkerSpiderfier:', error);
            }
        })();
        {% endmacro %}
        """
    )

    default_js = [
        (
            "overlappingmarkerjs",
            "https://cdnjs.cloudflare.com/ajax/libs/OverlappingMarkerSpiderfier-Leaflet/0.2.6/oms.min.js",
        )
    ]

    def __init__(
        self,
        keep_spiderfied: bool = True,
        nearby_distance: int = 20,
        leg_weight: float = 1.5,
        circle_spiral_switchover: int = 9,
        **kwargs
    ):
        super().__init__()
        self._name = "OverlappingMarkerSpiderfier"
        self.options = parse_options(
            keep_spiderfied=keep_spiderfied,
            nearby_distance=nearby_distance,
            leg_weight=leg_weight,
            circle_spiral_switchover=circle_spiral_switchover,
            **kwargs
        )

    def add_to(
        self, parent: Element, name: Optional[str] = None, index: Optional[int] = None
    ) -> Element:
        self._parent = parent
        self.markers = self._get_all_markers(parent)
        super().add_to(parent, name=name, index=index)

    def _get_all_markers(self, element: Element) -> list:
        markers = []
        for child in element._children.values():
            if isinstance(child, Marker):
                markers.append(child)
            elif hasattr(child, "_children"):
                markers.extend(self._get_all_markers(child))
        return markers
