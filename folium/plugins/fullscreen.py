from branca.element import MacroElement

from folium.elements import JSCSSMixin
from folium.utilities import parse_options

from jinja2 import Template


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
    _template = Template("""
        {% macro script(this, kwargs) %}
            L.control.fullscreen(
                {{ this.options|tojson }}
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)  # noqa

    default_js = [
        ('Control.Fullscreen.js',
         'https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.js')
    ]
    default_css = [
        ('Control.FullScreen.css',
         'https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.css')
    ]

    def __init__(self, position='topleft', title='Full Screen',
                 title_cancel='Exit Full Screen', force_separate_button=False,
                 **kwargs):
        super(Fullscreen, self).__init__()
        self._name = 'Fullscreen'
        self.options = parse_options(
            position=position,
            title=title,
            title_cancel=title_cancel,
            force_separate_button=force_separate_button,
            **kwargs
        )
