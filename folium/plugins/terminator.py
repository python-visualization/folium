# -*- coding: utf-8 -*-
"""
Terminator plugin
-----------------

Leaflet.Terminator is a simple plug-in to the Leaflet library to overlay day and night regions on maps.
"""
try:
    from urllib.request import urlopen as _urlopen
except:
    from urllib import urlopen as _urlopen

from .plugin import Plugin

# As LO.Terminator.js is not served on both HTTP and HTTPS, we need to embed it explicitely into the code.
_request = _urlopen("http://rawgithub.com/joergdietrich/Leaflet.Terminator/master/L.Terminator.js")
assert _request.getcode()==200, "Error while loading Leaflet.terminator.js"
_terminator_script = _request.read().decode('utf8')

class Terminator(Plugin):
    """Leaflet.Terminator is a simple plug-in to the Leaflet library to overlay day and night regions on maps."""
    def __init__(self):
        """Creates a Terminator plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
        """
        super(Terminator, self).__init__()
        self.plugin_name = 'Terminator'

    def render_header(self, nb):
        """Generates the header part of the plugin."""
        return '<script type="text/javascript">'+_terminator_script+'</script>' if nb==0 else ""

    def render_js(self, nb):
        """Generates the Javascript part of the plugin."""
        return "L.terminator().addTo(map);" if nb==0 else ""
