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
    """

    def __init__(self):
        """Add button to take your Folium map fullscreen"""
        super(Fullscreen, self).__init__()
        self._name = 'Fullscreen'

        self._template = Template("""
        {% macro script(this, kwargs) %}
            L.control.fullscreen().addTo({{this._parent.get_name()}});
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
