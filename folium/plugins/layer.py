# -*- coding: utf-8 -*-
"""
Layer plugin
------------

Add layers and layer control to the map.
"""
from .plugin import Plugin

class Layer(Plugin):
    """Adds a layer to the map."""
    def __init__(self, url=None, layer_name = None, min_zoom=1, max_zoom=18, attribution=''):
        """Crates a layer object to be added on a folium map.
        
        Parameters
        ----------
            url : str
                The url of the layer service, in the classical leaflet form.
                    example: url='//otile1.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png'
            layer_name : str
                Tha name of the layer that will be displayed in the layer control.
                If None, a random hexadecimal string will be created.
            min_zoom : int, default 1
                The minimal zoom allowed for this layer
            max_zoom : int, default 18
                The maximal zoom allowed for this layer
            attribution : str, default ''
                Tha atribution string for the layer.
        """
        super(Layer, self).__init__()
        self.plugin_name = 'Layer'
        self.tile_url = url
        self.attribution = attribution
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.object_id = self.object_name
        if layer_name is not None:
            self.object_name = layer_name

    def render_js(self, nb):
        """Generates the JS part of the plugin."""
        return """
        var layer_"""+self.object_id+""" = L.tileLayer('"""+self.tile_url+"""', {
            maxZoom: """+str(self.max_zoom)+""",
            minZoom: """+str(self.min_zoom)+""",
            attribution: '"""+str(self.attribution)+"""'
            });
        layer_"""+self.object_id+""".addTo(map);
        """

class LayerControl(Plugin):
    """Adds a layer control to the map."""
    def __init__(self, base_layer_name="Base Layer"):
        """Creates a LayerControl object to be added on a folium map.
        
        Parameters
        ----------
            base_layer_name : str, default "Base Layer"
                The name of the base layer that you want to see on the control.
        """
        super(LayerControl, self).__init__()
        self.plugin_name = 'LayerControl'
        self.base_layer_name = base_layer_name

    def render_js(self, nb):
        """Generates the JS part of the plugin."""
        return """
        var baseLayer = {
          "%s": base_tile,"""% self.base_layer_name+\
        ",".join(['"%s" : layer_%s ' % (x.object_name,x.object_id) for x in self.map.plugins['Layer']])+\
        """};

        L.control.layers(baseLayer, layer_list).addTo(map);
        """
    
    
    