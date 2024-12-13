from folium.elements import JSCSSMixin
from folium.map import Marker
from folium.template import Template
from folium.utilities import remove_empty
from folium.vector_layers import path_options


class SemiCircle(JSCSSMixin, Marker):
    """Add a marker in the shape of a semicircle, similar to the Circle class.

    Use (direction and arc) or (start_angle and stop_angle), not both.

    Parameters
    ----------
    location: tuple[float, float]
        Latitude and Longitude pair (Northing, Easting)
    radius: float
        Radius of the circle, in meters.
    direction: int, default None
        Direction angle in degrees
    arc: int, default None
        Arc angle in degrees.
    start_angle: int, default None
        Start angle in degrees
    stop_angle: int, default None
        Stop angle in degrees.
    popup: str or folium.Popup, optional
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, optional
        Display a text when hovering over the object.
    **kwargs
        For additional arguments see :func:`folium.vector_layers.path_options`

    Uses Leaflet plugin https://github.com/jieter/Leaflet-semicircle

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.semiCircle(
                {{ this.location|tojson }},
                {{ this.options|tojavascript }}
                )
                {%- if this.direction %}
                    .setDirection({{ this.direction[0] }}, {{ this.direction[1] }})
                {%- endif %}
                .addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """
    )

    default_js = [
        (
            "semicirclejs",
            "https://cdn.jsdelivr.net/npm/leaflet-semicircle@2.0.4/Semicircle.min.js",
        )
    ]

    def __init__(
        self,
        location,
        radius,
        direction=None,
        arc=None,
        start_angle=None,
        stop_angle=None,
        popup=None,
        tooltip=None,
        **kwargs
    ):
        super().__init__(location, popup=popup, tooltip=tooltip)
        self._name = "SemiCircle"
        self.direction = (
            (direction, arc) if direction is not None and arc is not None else None
        )
        self.options = path_options(line=False, radius=radius, **kwargs)
        self.options.update(
            dict(
                start_angle=start_angle,
                stop_angle=stop_angle,
            )
        )
        self.options = remove_empty(**self.options)

        if not (
            (direction is None and arc is None)
            and (start_angle is not None and stop_angle is not None)
            or (direction is not None and arc is not None)
            and (start_angle is None and stop_angle is None)
        ):
            raise ValueError(
                "Invalid arguments. Either provide direction and arc OR start_angle and stop_angle"
            )
