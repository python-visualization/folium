from branca.element import MacroElement
from jinja2 import Template

from folium.elements import JSCSSMixin


class Terminator(JSCSSMixin, MacroElement):
    """
    Leaflet.Terminator is a simple plug-in to the Leaflet library to
    overlay day and night regions on maps.

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            L.terminator().addTo({{this._parent.get_name()}});
        {% endmacro %}
        """
    )

    default_js = [("terminator", "https://unpkg.com/@joergdietrich/leaflet.terminator")]

    def __init__(self):
        super().__init__()
        self._name = "Terminator"
