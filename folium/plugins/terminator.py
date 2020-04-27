# -*- coding: utf-8 -*-

from branca.element import Figure, JavascriptLink, MacroElement

from jinja2 import Template

_default_js = [
    ('terminator',
     'https://unpkg.com/@joergdietrich/leaflet.terminator')
    ]


class Terminator(MacroElement):
    """
    Leaflet.Terminator is a simple plug-in to the Leaflet library to
    overlay day and night regions on maps.

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            L.terminator().addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)

    def __init__(self):
        super(Terminator, self).__init__()
        self._name = 'Terminator'

    def render(self, **kwargs):
        super(Terminator, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        # Import Javascripts
        for name, url in _default_js:
            figure.header.add_child(JavascriptLink(url), name=name)
