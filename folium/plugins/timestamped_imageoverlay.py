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
        {{this._parent.get_name()}}.timeDimension = L.timeDimension({
                period:"{{this.period}}",
                {% if this.time_interval %}
                timeInterval: "{{ this.time_interval }}",
                validTimeRange: "{{ this.valid_time_range }}",
                {% endif %}
                });
            {{this._parent.get_name()}}.timeDimensionControl = L.control.timeDimension({
                position: 'bottomleft',
                autoPlay: {{'true' if this.auto_play else 'false'}},
                playerOptions: {
                    transitionTime: {{this.transition_time}},
                    loop: {{'true' if this.loop else 'false'}}}
                    });

            {{this._parent.get_name()}}.addControl({{this._parent.get_name()}}.timeDimensionControl);

            console.log("{{this.marker}}");

            L.timeDimension.layer.imageOverlay = function(layer, options) {
                return new L.TimeDimension.Layer.ImageOverlay(layer, options);
            };

            {% for url in this.urls %}
            var ImageOverlayLayer = L.imageOverlay(
                    '{{ url }}',
                    {{ this.bounds }},
                    {{ this.options }}
                    ).addTo({{this._parent.get_name()}});

            var {{this.get_name()}} = L.timeDimension.layer.imageOverlay(ImageOverlayLayer,
                {updateTimeDimension: true,
                 addlastPoint: {{'true' if this.add_last_point else 'false'}},
                 duration: {{ this.duration }},
                }).addTo({{this._parent.get_name()}});
            {% endfor %}

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