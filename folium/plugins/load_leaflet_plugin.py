# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import Element, Figure, JavascriptLink


class LoadLeafletPlugin(Element):
    """
    Includes Leaflet plugins to the current map from passed URLs.

    Parameters
    ----------
    *urls : str
        Links to Leaflet plugins to include for the map
    """

    def __init__(self, *plugin_urls):
        super(LoadLeafletPlugin, self).__init__()
        self._name = 'LoadLeafletPlugin'
        self.plugins = plugin_urls

    def render(self, **kwargs):
        super(LoadLeafletPlugin, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        for plugin in self.plugins:
            js_link = JavascriptLink(plugin)
            figure.header.add_child(
                js_link,
                name='loadleafletplugin-{}'.format(plugin),  # to load each plugin once
            )
