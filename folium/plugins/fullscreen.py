from branca.element import MacroElement

from folium.elements import JSCSSMixin
from folium.template import Template
from folium.utilities import remove_empty


class Fullscreen(JSCSSMixin, MacroElement):
    """
    Adds a fullscreen button to your map.

    Parameters
    ----------
    position : str
        change the position of the button can be:
        'topleft', 'topright', 'bottomright' or 'bottomleft'
        default: 'topleft'
    title : str
        change the title of the button,
        default: 'Full Screen'
    title_cancel : str
        change the title of the button when fullscreen is on,
        default: 'Exit Full Screen'
    force_separate_button : bool, default False
        force separate button to detach from zoom buttons,

    See https://github.com/brunob/leaflet.fullscreen for more information.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            L.control.fullscreen(
                {{ this.options|tojavascript }}
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """
    )  # noqa

    default_js = [
        (
            "Control.Fullscreen.js",
            "https://cdn.jsdelivr.net/npm/leaflet.fullscreen@3.0.0/Control.FullScreen.min.js",
        )
    ]
    default_css = [
        (
            "Control.FullScreen.css",
            "https://cdn.jsdelivr.net/npm/leaflet.fullscreen@3.0.0/Control.FullScreen.css",
        )
    ]

    def __init__(
        self,
        position="topleft",
        title="Full Screen",
        title_cancel="Exit Full Screen",
        force_separate_button=False,
        **kwargs
    ):
        super().__init__()
        self._name = "Fullscreen"
        self.options = remove_empty(
            position=position,
            title=title,
            title_cancel=title_cancel,
            force_separate_button=force_separate_button,
            **kwargs
        )
