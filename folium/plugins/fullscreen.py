# -*- coding: utf-8 -*-
"""
Fullscreen
--------------

https://github.com/brunob/leaflet.fullscreen

Adds fullscreen button to your maps.
"""
from jinja2 import Template

from branca.element import MacroElement, Figure, JavascriptLink, CssLink


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
    titleCancel : str
          change the title of the button when fullscreen is on,
          default: 'Exit Full Screen'
    forceSeparateButton : boolean
          force seperate button to detach from zoom buttons,
          default: False
    """

    def __init__(self, position='topleft', title='Full Screen',
                 titleCancel='Exit Full Screen', forceSeparateButton=False):
        """Add button to take your Folium map fullscreen"""
        super(Fullscreen, self).__init__()
        self._name = 'Fullscreen'
        self.position = position
        self.title = title
        self.titleCancel = titleCancel
        self.forceSeparateButton = str(forceSeparateButton).lower()

        self._template = Template("""
        {% macro script(this, kwargs) %}
            L.control.fullscreen({
                position: '{{this.position}}',
                title: '{{this.title}}',
                titleCancel: '{{this.titleCancel}}',
                forceSeparateButton: {{this.forceSeparateButton}},
                }).addTo({{this._parent.get_name()}});
            {{this._parent.get_name()}}.on('enterFullscreen', function(){
                console.log('entered fullscreen');
            });

        {% endmacro %}
        """)  # noqa

    def render(self, **kwargs):
        super(Fullscreen, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_child(
            JavascriptLink(
                "https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.js"),  # noqa
            name='Control.Fullscreen.js'
        )

        figure.header.add_child(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.css"),  # noqa
            name='Control.FullScreen.css'
        )
