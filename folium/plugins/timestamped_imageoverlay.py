# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import CssLink, Figure, JavascriptLink, MacroElement
from folium.utilities import image_to_url, mercator_transform

from jinja2 import Template


class TimestampedImageOverlay(MacroElement):
    """
    Creates a TimestampedImageOverlay plugin from urls/images to append
    into a map with Map.add_child.


    Eventually, you may have Point features with a 'times' property being an
    array of length 1.

    Parameters
    ----------
    image: string, file or array-like object
        The data you want to draw on the map.
        * If string, it will be written directly in the output file.
        * If file, it's content will be converted as embedded in the output file.
        * If array-like, it will be converted to PNG base64 string and embedded in the output.
    bounds: list
        Image bounds on the map in the form [[lat_min, lon_min],
        [lat_max, lon_max]]
    opacity: float, default Leaflet's default (1.0)
    alt: string, default Leaflet's default ('')
    origin: ['upper' | 'lower'], optional, default 'upper'
        Place the [0,0] index of the array in the upper left or
        lower left corner of the axes.
    colormap: callable, used only for `mono` image.
        Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
        for transforming a mono image into RGB.
        It must output iterables of length 3 or 4,
        with values between 0 and 1.
        Hint: you can use colormaps from `matplotlib.cm`.
    mercator_project: bool, default False.
        Used only for array-like image.  Transforms the data to
        project (longitude, latitude) coordinates to the
        Mercator projection.
        Beware that this will only work if `image` is an array-like
        object.
    pixelated: bool, default True
        Sharp sharp/crips (True) or aliased corners (False).
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    transition_time: int, default 200.
        The duration in ms of a transition from between timestamps.
    loop: bool, default True
        Whether the animation shall loop.
    auto_play: bool, default True
        Whether the animation shall start automatically at startup.
    add_last_point: bool, default True
        Whether a point is added at the last valid coordinate of a LineString.
    period: str, default "P1D"
        Used to construct the array of available times starting
        from the first available time. Format: ISO8601 Duration
        ex: 'P1M' 1/month, 'P1D' 1/day, 'PT1H' 1/hour, and 'PT1M' 1/minute
    duration: str, default None
        Period of time which the features will be shown on the map after their
        time has passed. If None, all previous times will be shown.
        Format: ISO8601 Duration
        ex: 'P1M' 1/month, 'P1D' 1/day, 'PT1H' 1/hour, and 'PT1M' 1/minute

    Examples
    --------



    See https://github.com/socib/Leaflet.TimeDimension for more information.

    """
    _template = Template("""
            {% macro script(this, kwargs) %}
            
            L.TimeDimension.Layer.ImageOverlay = L.TimeDimension.Layer.extend({
    
                initialize: function(layer, options) {
                    L.TimeDimension.Layer.prototype.initialize.call(this, layer, options);
                    this._layers = {};
                    this._defaultTime = 0;
                    this._timeCacheBackward = this.options.cacheBackward || this.options.cache || 0;
                    this._timeCacheForward = this.options.cacheForward || this.options.cache || 0;
                    this._getUrlFunction = this.options.getUrlFunction;
            
                    this._baseLayer.on('load', (function() {
                        this._baseLayer.setLoaded(true);
                        this.fire('timeload', {
                            time: this._defaultTime
                        });
                    }).bind(this));
                },
            
                eachLayer: function(method, context) {
                    for (var prop in this._layers) {
                        if (this._layers.hasOwnProperty(prop)) {
                            method.call(context, this._layers[prop]);
                        }
                    }
                    return L.TimeDimension.Layer.prototype.eachLayer.call(this, method, context);
                },
            
                _onNewTimeLoading: function(ev) {
                    var layer = this._getLayerForTime(ev.time);
                    if (!this._map.hasLayer(layer)) {
                        this._map.addLayer(layer);
                    }
                },
            
                isReady: function(time) {
                    var layer = this._getLayerForTime(time);
                    return layer.isLoaded();
                },
            
                _update: function() {
                    if (!this._map)
                        return;
                    var time = map.timeDimension.getCurrentTime();
                    var layer = this._getLayerForTime(time);
                    if (this._currentLayer == null) {
                        this._currentLayer = layer;
                    }
                    if (!this._map.hasLayer(layer)) {
                        this._map.addLayer(layer);
                    } else {
                        this._showLayer(layer, time);
                    }
                },
            
                _showLayer: function(layer, time) {
                    if (this._currentLayer && this._currentLayer !== layer) {
                        this._currentLayer.hide();
                        this._map.removeLayer(this._currentLayer);
                    }
                    layer.show();
                    if (this._currentLayer && this._currentLayer === layer) {
                        return;
                    }
                    this._currentLayer = layer;
                    // Cache management
                    var times = this._getLoadedTimes();
                    var strTime = String(time);
                    var index = times.indexOf(strTime);
                    var remove = [];
                    // remove times before current time
                    if (this._timeCacheBackward > -1) {
                        var objectsToRemove = index - this._timeCacheBackward;
                        if (objectsToRemove > 0) {
                            remove = times.splice(0, objectsToRemove);
                            this._removeLayers(remove);
                        }
                    }
                    if (this._timeCacheForward > -1) {
                        index = times.indexOf(strTime);
                        var objectsToRemove = times.length - index - this._timeCacheForward - 1;
                        if (objectsToRemove > 0) {
                            remove = times.splice(index + this._timeCacheForward + 1, objectsToRemove);
                            this._removeLayers(remove);
                        }
                    }
                },
            
                _getLayerForTime: function(time) {
                    if (time == 0 || time == this._defaultTime) {
                        return this._baseLayer;
                    }
                    if (this._layers.hasOwnProperty(time)) {
                        return this._layers[time];
                    }
                    var url = this._getUrlFunction(this._baseLayer.getURL(), time);
                    imageBounds = this._baseLayer._bounds;
            
                    var newLayer = L.imageOverlay(url, imageBounds, this._baseLayer.options);
                    this._layers[time] = newLayer;
                    newLayer.on('load', (function(layer, time) {
                        layer.setLoaded(true);
                        if (map.timeDimension && time == map.timeDimension.getCurrentTime() && !map.timeDimension.isLoading()) {
                            this._showLayer(layer, time);
                        }
                        this.fire('timeload', {
                            time: time
                        });
                    }).bind(this, newLayer, time));
            
                    // Hack to hide the layer when added to the map.
                    // It will be shown when timeload event is fired from the map (after all layers are loaded)
                    newLayer.onAdd = (function(map) {
                        Object.getPrototypeOf(this).onAdd.call(this, map);
                        this.hide();
                    }).bind(newLayer);
                    return newLayer;
                },
            
                _getLoadedTimes: function() {
                    var result = [];
                    for (var prop in this._layers) {
                        if (this._layers.hasOwnProperty(prop)) {
                            result.push(prop);
                        }
                    }
                    return result.sort();
                },
            
                _removeLayers: function(times) {
                    for (var i = 0, l = times.length; i < l; i++) {
                        this._map.removeLayer(this._layers[times[i]]);
                        delete this._layers[times[i]];
                    }
                },
            
            });
            
            L.timeDimension.layer.imageOverlay = function(layer, options) {
            return new L.TimeDimension.Layer.ImageOverlay(layer, options);
            };
            
            L.ImageOverlay.include({
                _visible: true,
                _loaded: false,
                
                _originalUpdate: L.imageOverlay.prototype._update,
                
                _update: function() {
                    if (!this._visible && this._loaded) {
                        return;
                    }
                    this._originalUpdate();
            },
            
                setLoaded: function(loaded) {
                    this._loaded = loaded;
            },
            
                isLoaded: function() {
                    return this._loaded;
            },
            
                hide: function() {
                    this._visible = false;
                    if (this._image && this._image.style)
                        this._image.style.display = 'none';
            },
            
                show: function() {
                    this._visible = true;
                    if (this._image && this._image.style)
                        this._image.style.display = 'block';
            },
            
                getURL: function() {
                    return this._url;
            },
            
            });
            
            var map = L.map('map', {
            timeDimension: true,
            timeDimensionOptions: {
                timeInterval: "{{ this.time_interval }}",
                period: "{{ this.period }}",
                validTimeRange: "{{ this.valid_time_range }}",
            },
            timeDimensionControl: false,
            timeDimensionControlOptions: {
                position: 'bottomleft',
                autoPlay: {{'true' if this.auto_play else 'false'}}
                playerOptions: {
                    transitionTime: {{this.transition_time}},
                    loop: {{'true' if this.loop else 'false'}}},
            });
            
            var {{this._parent.get_name()}} = L.imageOverlay(
                    '{{ this.url }}',
                    {{ this.bounds }},
                    {{ this.options }}
            );
            
        
            
            var getRadarImageUrl = function(baseUrl, time) {
                var beginUrl = "/home/d.lassahn/projects/ewb-projects/src/radar/data/";
                beginUrl = beginUrl + new Date(time).format('YYYY/MM/DD');
                var filePostfix = ".png";
                var centerUrl = "/radar_de_";
                centerUrl = centerUrl + new Date(time).format('HHmm');
                url = beginUrl + centerUrl + filePostfix;
                return url;
            };
            
            var testImageTimeLayer = L.timeDimension.layer.imageOverlay({{this._parent.get_name()}}, {
                getUrlFunction: getRadarImageUrl
            });

            testImageTimeLayer.addTo(map);

        {% endmacro %}
        """)  # noqa

    def __init__(self, data, time_interval, bounds, origin='upper',
                 colormap=None,
                 mercator_project=False, pixelated=True,
                 transition_time=200, loop=True, valid_time_range='00:00/23:59',
                 auto_play=True, add_last_point=True, period='PT5M',
                 min_speed=0.1, max_speed=10, loop_button=False,
                 date_options='YYYY-MM-DD HH:mm:ss',
                 time_slider_drag_update=False, duration=None,
                 **kwargs):
        super(TimestampedImageOverlay, self).__init__()
        # period = 'PT5M'
        self._name = 'ImageOverlay'
        self.pixelated = pixelated
        self.time_interval = time_interval
        if mercator_project:
            images = [mercator_transform(
                image,
                [bounds[0][0],
                 bounds[1][0]],
                origin=origin) for image in data]
        else:
            images = data

        self.urls = [image_to_url(img, origin=origin, colormap=colormap) for img
                     in images]

        self.bounds = json.loads(json.dumps(bounds))
        self.valid_time_range = valid_time_range
        self.add_last_point = bool(add_last_point)
        self.period = period
        self.date_options = date_options
        self.duration = 'undefined' if duration is None else "\"" + duration + "\""

        options = {
            'position': 'bottomleft',
            'minSpeed': min_speed,
            'maxSpeed': max_speed,
            'autoPlay': auto_play,
            'loopButton': loop_button,
            'timeSliderDragUpdate': time_slider_drag_update,
            'playerOptions': {
                'transitionTime': int(transition_time),
                'loop': loop,
                'startOver': True

            },
            'opacity': kwargs.pop('opacity', 1.),
            'alt': kwargs.pop('alt', ''),
            'interactive': kwargs.pop('interactive', False),
            'crossOrigin': kwargs.pop('cross_origin', False),
            'errorOverlayUrl': kwargs.pop('error_overlay_url', ''),
            'zIndex': kwargs.pop('zindex', 1),
            'className': kwargs.pop('class_name', ''),

        }
        self.options = json.dumps(options, sort_keys=True, indent=2)

    def render(self, **kwargs):
        super(TimestampedImageOverlay, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink(
                'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js'),
            # noqa
            name='jquery2.0.0')

        figure.header.add_child(
            JavascriptLink(
                'https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js'),
            # noqa
            name='jqueryui1.10.2')

        figure.header.add_child(
            JavascriptLink(
                'https://rawgit.com/nezasa/iso8601-js-period/master/iso8601.min.js'),
            # noqa
            name='iso8601')

        figure.header.add_child(
            JavascriptLink(
                'https://rawgit.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.min.js'),
            # noqa
            name='leaflet.timedimension')

        figure.header.add_child(
            CssLink(
                'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css'),
            # noqa
            name='highlight.js_css')

        figure.header.add_child(
            CssLink(
                "http://apps.socib.es/Leaflet.TimeDimension/dist/leaflet.timedimension.control.min.css"),
            # noqa
            name='leaflet.timedimension_css')

        figure.header.add_child(
            JavascriptLink(
                'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js'),
            name='moment')

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].
        """
        return self.bounds
