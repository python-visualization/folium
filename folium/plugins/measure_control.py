from branca.element import MacroElement
from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.utilities import parse_options


class MeasureControl(JSCSSMixin, MacroElement):
    """Add a measurement widget on the map.

    Parameters
    ----------
    position: str, default 'topright'
        Location of the widget.
    primary_length_unit: str, default 'meters'
    secondary_length_unit: str, default 'miles'
    primary_area_unit: str, default 'sqmeters'
    secondary_area_unit: str, default 'acres'

    See https://github.com/ljagis/leaflet-measure for more information.

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = new L.Control.Measure(
                {{ this.options|tojson }});
            {{this._parent.get_name()}}.addControl({{this.get_name()}});

        {% endmacro %}
        """
    )  # noqa

    default_js = [
        (
            "leaflet_measure_js",
            "https://cdn.jsdelivr.net/gh/ljagis/leaflet-measure@2.1.7/dist/leaflet-measure.min.js",
        )
    ]

    default_css = [
        (
            "leaflet_measure_css",
            "https://cdn.jsdelivr.net/gh/ljagis/leaflet-measure@2.1.7/dist/leaflet-measure.min.css",
        )
    ]

    def __init__(
        self,
        position="topright",
        primary_length_unit="meters",
        secondary_length_unit="miles",
        primary_area_unit="sqmeters",
        secondary_area_unit="acres",
        **kwargs
    ):

        super().__init__()
        self._name = "MeasureControl"

        self.options = parse_options(
            position=position,
            primary_length_unit=primary_length_unit,
            secondary_length_unit=secondary_length_unit,
            primary_area_unit=primary_area_unit,
            secondary_area_unit=secondary_area_unit,
            **kwargs
        )
