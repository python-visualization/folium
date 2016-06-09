# -*- coding: utf-8 -*-
"""
Terminator plugin
-----------------

Leaflet.Terminator is a simple plug-in to the Leaflet library to overlay day
and night regions on maps.

"""
from jinja2 import Template

from branca.element import JavascriptLink, MacroElement, Figure


class Terminator(MacroElement):
    """Leaflet.Terminator is a simple plug-in to the Leaflet library to
    overlay day and night regions on maps.

    """
    def __init__(self):
        """
        Creates a Terminator plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------

        """
        super(Terminator, self).__init__()
        self._name = 'Terminator'

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                L.terminator().addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def render(self, **kwargs):
        super(Terminator, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_child(
            JavascriptLink("https://rawgithub.com/joergdietrich/Leaflet.Terminator/master/L.Terminator.js"),  # noqa
            name='markerclusterjs')
