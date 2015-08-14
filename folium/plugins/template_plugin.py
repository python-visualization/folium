# -*- coding: utf-8 -*-
"""
Template Plugin

A generic class to create plugins based on jinja2 templates.
"""
from .plugin import Plugin
from jinja2 import Template
from uuid import uuid4


class TemplatePlugin(Plugin):
    """Generates a plugin out of a jinja2 template."""
    def __init__(self):
        """Creates a TemplatePlugin plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
            template: jinja2.Template
                The template that will be used to generate the plugin.
        """
        super(TemplatePlugin, self).__init__()
        assert 'template' in dir(self), 'template attibute does not exist ; you have to define one.'
        self.template = self.template if self.template.__class__ is Template else Template(self.template)
        self.plugin_name = self.template.module.__dict__.get('plugin_name','Unknown_'+uuid4().hex)

    def render_header(self, nb):
        """Generates the header part of the plugin."""
        header = self.template.module.__dict__.get('header',None)
        if header is None:
            return super(TemplatePlugin, self).render_header(nb)
        else:
            return header(nb)

    def render_css(self, nb):
        """Generates the CSS part of the plugin."""
        css = self.template.module.__dict__.get('css',None)
        if css is None:
            return super(TemplatePlugin, self).render_css(nb)
        else:
            return css(nb)

    def render_html(self, nb):
        """Generates the HTML part of the plugin."""
        html = self.template.module.__dict__.get('html',None)
        if html is None:
            return super(TemplatePlugin, self).render_html(nb)
        else:
            return html(nb)

    def render_js(self, nb):
        """Generates the Javascript part of the plugin."""
        js = self.template.module.__dict__.get('js',None)
        if js is None:
            return super(TemplatePlugin, self).render_js(nb)
        else:
            return js(nb)
