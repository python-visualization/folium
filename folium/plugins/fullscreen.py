# -*- coding: utf-8 -*-

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from folium.utilities import parse_options

from jinja2 import Template

_default_js = [
    ('Control.Fullscreen.js',
     'https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.js')
    ]

_default_css = [
    ('Control.FullScreen.css',
     'https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.css')
    ]


class Fullscreen(MacroElement):
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
        force seperate button to detach from zoom buttons,

    See https://github.com/brunob/leaflet.fullscreen for more information.
    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            L.control.fullscreen(
                {{ this.options|tojson }}
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)  # noqa

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

    def render(self, **kwargs):
        super(Fullscreen, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        # Import Javascripts
        for name, url in _default_js:
            figure.header.add_child(JavascriptLink(url), name=name)

        # Import Css
        for name, url in _default_css:
            figure.header.add_child(CssLink(url), name=name)
