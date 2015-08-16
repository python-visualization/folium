# -*- coding: utf-8 -*-
"""
Plugin
------

A generic class for creating plugins.
Basic plugin object that does nothing.
Other plugins may inherit from this one.
"""
from uuid import uuid4

from jinja2 import Environment, PackageLoader, Template
ENV = Environment(loader=PackageLoader('folium', 'plugins'))

class Plugin(object):
    """Basic plugin object that does nothing.
    Other plugins may inherit from this one."""
    def __init__(self):
        """Creates a plugin to append into a map with Map.add_plugin. """
        self.plugin_name = 'Plugin'
        self.object_name = uuid4().hex
        self.env = ENV

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
    def render(self, nb=0, **kwargs):
        self.map.figure.header[self.object_name] = Template(self.render_header(nb))
        self.map.figure.css   [self.object_name] = Template(self.render_css(nb))
        self.map.figure.body  [self.object_name] = Template(self.render_html(nb))
        self.map.figure.script[self.object_name] = Template(self.render_js(nb))
