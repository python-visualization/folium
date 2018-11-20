# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import CssLink, Figure, JavascriptLink

from folium.map import Layer
from folium.raster_layers import WmsTileLayer

from jinja2 import Template


class TimestampedWmsTileLayers(Layer):
    """
    Creates a TimestampedWmsTileLayer that takes a WmsTileLayer and adds time
    control with the Leaflet.TimeDimension plugin.

    Parameters
    ----------
    data: WmsTileLayer.
        The WmsTileLayer that you want to add time support to.
        Must  be created like a typical WmsTileLayer and added to the map
        before being passed to this class.

    transition_time: int, default 200.
        The duration in ms of a transition from between timestamps.
    loop: bool, default False
        Whether the animation shall loop, default is to reduce load on WMS
        services.
    auto_play: bool, default False
        Whether the animation shall start automatically at startup, default
        is to reduce load on WMS services.
    period: str, default 'P1D'
        Used to construct the array of available times starting
        from the first available time. Format: ISO8601 Duration
        ex: 'P1M' -> 1/month, 'P1D' -> 1/day, 'PT1H' -> 1/hour, and 'PT1M' -> 1/minute
        Note: this seems to be overridden by the WMS Tile Layer GetCapabilities.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls.
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).

    Examples
    --------
    >>> w0 = features.WmsTileLayer(
    ...          'http://this.wms.server/ncWMS/wms',
    ...          name='Test WMS Data',
    ...          styles='',
    ...          fmt='image/png',
    ...          transparent=True,
    ...          layers='test_data',
    ...          COLORSCALERANGE='0,10',
    ...)
    >>> w0.add_to(m)
    >>> w1 = features.WmsTileLayer(
    ...          'http://this.wms.server/ncWMS/wms',
    ...          name='Test WMS Data',
    ...          styles='',
    ...          fmt='image/png',
    ...          transparent=True,
    ...          layers='test_data_2',
    ...          COLORSCALERANGE='0,5',
    ...)
    >>> w1.add_to(m)
    >>> # Add WmsTileLayers to time control.
    >>> time = plugins.TimestampedWmsTileLayers([w0, w1])
    >>> time.add_to(m)

    See https://github.com/socib/Leaflet.TimeDimension for more information.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            {{this._parent.get_name()}}.timeDimension = L.timeDimension({
                period:"{{this.period}}",
                {% if this.time_interval %}
                timeInterval: "{{ this.time_interval }}",
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

            {% for layer in this.layers %}
            var {{ layer.get_name() }} = L.timeDimension.layer.wms({{ layer.get_name() }},
                {updateTimeDimension: false,
                 wmsVersion: '{{ layer.version }}',
                }
                ).addTo({{this._parent.get_name()}});
            {% endfor %}
        {% endmacro %}
        """)

    def __init__(self, data, transition_time=200, loop=False, auto_play=False,
                 period='P1D', time_interval=False, name=None,
                 overlay=True, control=True, show=True):
        super(TimestampedWmsTileLayers, self).__init__(name=name,
                                                       overlay=overlay,
                                                       control=control,
                                                       show=show)
        self._name = 'TimestampedWmsTileLayers'

        self.transition_time = int(transition_time)
        self.loop = bool(loop)
        self.auto_play = bool(auto_play)
        self.period = period
        self.time_interval = time_interval
        if isinstance(data, WmsTileLayer):
            self.layers = [data]
        else:
            self.layers = data  # Assume iterable

    def render(self, **kwargs):
        super(TimestampedWmsTileLayers, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js'),  # noqa
            name='jquery2.0.0')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js'),  # noqa
            name='jqueryui1.10.2')

        figure.header.add_child(
            JavascriptLink('https://rawcdn.githack.com/nezasa/iso8601-js-period/master/iso8601.min.js'),  # noqa
            name='iso8601')

        figure.header.add_child(
            JavascriptLink('https://rawcdn.githack.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.min.js'),  # noqa
            name='leaflet.timedimension')

        figure.header.add_child(
            CssLink('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css'),  # noqa
            name='highlight.js_css')

        figure.header.add_child(
            CssLink('http://apps.socib.es/Leaflet.TimeDimension/dist/leaflet.timedimension.control.min.css'),  # noqa
            name='leaflet.timedimension_css')
