# -*- coding: utf-8 -*-
"""
Links
-----

Plugins to add links into the header of the file.

"""

#from six import Module_six_moves_urllib as urllib
#urlopen = urllib.request.urlopen
import sys, urllib
PY3 = sys.version_info[0] == 3
urlopen = urllib.request.urlopen if PY3 else urllib.urlopen

from .plugin import Plugin

class Link(Plugin):
    def __init__(self, url, download=False):
        """Create a link object based on a url.
        Parameters
        ----------
            url : str
                The url to be linked
            download : bool, default False
                Whether the target document shall be loaded right now.
        """
        self.url = url
        self.code = None
        if download:
            self.code = urlopen(self.url).read()
    def render_header(self, nb, embedded=False):
        """Generates the Header part of the plugin."""
        return self.render(embedded=embedded)

class JavascriptLink(Link):
    def render(self, embedded=False, **kwargs):
        """Renders the object.
        
        Parameters
        ----------
            embedded : bool, default False
                Whether the code shall be embedded explicitely in the render.
        """
        if embedded:
            if self.code is None:
                self.code = urlopen(self.url).read()
            return '<script>{}</script>'.format(self.code)
        else:
            return '<script src="{}"></script>'.format(self.url)

class CssLink(Link):
    def render(self, embedded=False, **kwargs):
        """Renders the object.
        
        Parameters
        ----------
            embedded : bool, default False
                Whether the code shall be embedded explicitely in the render.
        """
        if embedded:
            if self.code is None:
                self.code = urlopen(self.url).read()
            return '<style>{}</style>'.format(self.code)
        else:
            return '<link rel="stylesheet" href="{}" />'.format(self.url)
            

            