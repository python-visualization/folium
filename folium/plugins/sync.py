

class Sync:
    """

    https://github.com/jieter/Leaflet.Sync
    """
    def __init__(self):
        pass


"""
https://github.com/jieter/Leaflet.Sync/blob/master/examples/dual.html

<style type="text/css">
    html, body { width: 100%; height: 100%; margin: 0; }
    #map1, #map2 { width: 49.5%; height: 100%; }
    #map1 { float: left; }
    #map2 { float: right; }
</style>

var map1 = L.map('map1', {
    layers: [layer1],
    center: [59.336, 5.967],
    zoom: 14            
});

var map2 = L.map('map2', {
    layers: [layer2],
    center: [59.336, 5.967],
    zoom: 14,
    zoomControl: false                     
});

map1.sync(map2);
map2.sync(map1);
"""