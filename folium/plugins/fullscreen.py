# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template


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
    force_separate_button : boolean
          force seperate button to detach from zoom buttons,
          default: False
    See https://github.com/brunob/leaflet.fullscreen for more information.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            L.control.fullscreen({
                position: '{{this.position}}',
                title: '{{this.title}}',
                titleCancel: '{{this.title_cancel}}',
                forceSeparateButton: {{this.force_separate_button}},
                }).addTo({{this._parent.get_name()}});
            {{this._parent.get_name()}}.on('enterFullscreen', function(){
                console.log('entered fullscreen');
            });

        {% endmacro %}
        """)  # noqa

    def __init__(self, position='topleft', title='Full Screen',
                 title_cancel='Exit Full Screen', force_separate_button=False):
        super(Fullscreen, self).__init__()
        self._name = 'Fullscreen'
        self.position = position
        self.title = title
        self.title_cancel = title_cancel
        self.force_separate_button = str(force_separate_button).lower()

    def render(self, **kwargs):
        super(Fullscreen, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.js'),  # noqa
            name='Control.Fullscreen.js'
        )

        figure.header.add_child(
            CssLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet.fullscreen/1.4.2/Control.FullScreen.min.css'),  # noqa
            name='Control.FullScreen.css'
        )
