# -*- coding: utf-8 -*-

from branca.element import MacroElement

from folium.elements import JSCSSMixin

from jinja2 import Template


class Terminator(JSCSSMixin, MacroElement):
    """
    Leaflet.Terminator is a simple plug-in to the Leaflet library to
    overlay day and night regions on maps.

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            L.terminator().addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)

    default_js = [
        ('terminator',
         'https://unpkg.com/@joergdietrich/leaflet.terminator')
    ]

    def __init__(self):
        super(Terminator, self).__init__()
        self._name = 'Terminator'
