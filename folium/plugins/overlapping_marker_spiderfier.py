from jinja2 import Template

from folium.elements import JSCSSMixin, MacroElement
from folium.utilities import parse_options


class OverlappingMarkerSpiderfier(JSCSSMixin, MacroElement):
    """
    A plugin that handles overlapping markers on a map by spreading them out in a spiral or circle pattern when clicked.

    This plugin is useful when you have multiple markers in close proximity that would otherwise be difficult to interact with.
    When a user clicks on a cluster of overlapping markers, they spread out in a 'spider' pattern, making each marker
    individually accessible.

    Markers must be added to the map **before** calling `oms.add_to(map)`.
    The plugin identifies and manages all markers already present on the map.

    Parameters
    ----------
    options : dict, optional
        The options to configure the spiderfier behavior:
        - keepSpiderfied : bool, default True
            If true, markers stay spiderfied after clicking
        - nearbyDistance : int, default 20
            Pixels away from a marker that is considered overlapping
        - legWeight : float, default 1.5
            Weight of the spider legs
        - circleSpiralSwitchover : int, optional
            Number of markers at which to switch from circle to spiral pattern

    Example
    -------
    >>> oms = OverlappingMarkerSpiderfier(
    ...     options={"keepSpiderfied": True, "nearbyDistance": 30, "legWeight": 2.0}
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
        default_options = {
            "keepSpiderfied": True,
            "nearbyDistance": 20,
            "legWeight": 1.5,
        }
        if options:
            default_options.update(options)
        self.options = parse_options(**default_options, **kwargs)
