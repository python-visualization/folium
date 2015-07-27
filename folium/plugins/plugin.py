# -*- coding: utf-8 -*-
"""
Plugin
------

A generic class for creating plugins.
Basic plugin object that does nothing.
Other plugins may inherit from this one.
"""
from uuid import uuid4

class Plugin(object):
    """Basic plugin object that does nothing.
    Other plugins may inherit from this one."""
    def __init__(self):
        """Creates a plugin to append into a map with Map.add_plugin. """
        self.plugin_name = 'Plugin'
        self.object_name = uuid4().hex

    def add_to_map(self, map):
        """Adds the plugin on a folium.map object."""
        map.plugins.setdefault(self.plugin_name,[]).append(self)
        self.map = map

    def render_html(self, nb):
        """Generates the HTML part of the plugin."""
        return ""

    def render_css(self, nb):
        """Generates the CSS part of the plugin."""
        return ""

    def render_js(self, nb):
        """Generates the Javascript part of the plugin."""
        return ""
    def render_header(self, nb):
        """Generates the Header part of the plugin."""
        return ""