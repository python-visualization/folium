# -*- coding: utf-8 -*-

from folium.elements import JSCSSMixin
from folium.map import Layer
from folium.raster_layers import WmsTileLayer
from folium.utilities import parse_options

from jinja2 import Template


class TimestampedWmsTileLayers(JSCSSMixin, Layer):
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
    >>> w0 = WmsTileLayer(
    ...          'http://this.wms.server/ncWMS/wms',
    ...          name='Test WMS Data',
    ...          styles='',
    ...          fmt='image/png',
    ...          transparent=True,
    ...          layers='test_data',
    ...          COLORSCALERANGE='0,10',
    ...)
    >>> w0.add_to(m)
    >>> w1 = WmsTileLayer(
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
    >>> time = TimestampedWmsTileLayers([w0, w1])
    >>> time.add_to(m)

    See https://github.com/socib/Leaflet.TimeDimension for more information.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            {{ this._parent.get_name() }}.timeDimension = L.timeDimension(
                {{ this.options|tojson }}
            );
            {{ this._parent.get_name() }}.timeDimensionControl =
                L.control.timeDimension(
                    {{ this.options_control|tojson }}
                );
            {{ this._parent.get_name() }}.addControl(
                {{ this._parent.get_name() }}.timeDimensionControl
            );

            {% for layer in this.layers %}
            var {{ layer.get_name() }} = L.timeDimension.layer.wms(
                {{ layer.get_name() }},
                {
                    updateTimeDimension: false,
                    wmsVersion: {{ layer.options['version']|tojson }},
                }
            ).addTo({{ this._parent.get_name() }});
            {% endfor %}
        {% endmacro %}
        """)

    default_js = [
        ('jquery2.0.0',
         'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js'),
        ('jqueryui1.10.2',
         'https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js'),
        ('iso8601',
         'https://cdn.jsdelivr.net/npm/iso8601-js-period@0.2.1/iso8601.min.js'),
        ('leaflet.timedimension',
         'https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.min.js'),
    ]
    default_css = [
        ('highlight.js_css',
         'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css'),
        ('leaflet.timedimension_css',
         'https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.control.css')
    ]

    def __init__(self, data, transition_time=200, loop=False, auto_play=False,
                 period='P1D', time_interval=False, name=None):
        super(TimestampedWmsTileLayers, self).__init__(name=name,
                                                       overlay=True,
                                                       control=False,
                                                       show=True)
        self._name = 'TimestampedWmsTileLayers'
        self.options = parse_options(
            period=period,
            time_interval=time_interval,
        )
        self.options_control = parse_options(
            position='bottomleft',
            auto_play=auto_play,
            player_options={
                'transitionTime': int(transition_time),
                'loop': loop,
            },
        )
        if isinstance(data, WmsTileLayer):
            self.layers = [data]
        else:
            self.layers = data  # Assume iterable
