# -*- coding: utf-8 -*-
"""
TimestampedGeoJson plugin
--------------

Add a timestamped geojson feature collection on a folium map.
This is based on Leaflet.TimeDimension.

https://github.com/socib/Leaflet.TimeDimension

A geo-json is timestamped if:
    * it contains only features of types LineString, MultiPoint,
      MultiLineString and MultiPolygon.
    * each feature has a "times" property with the same length as the
      coordinates array.
    * each element of each "times" property is a timestamp in ms since epoch,
     or in ISO string.  Eventually, you may have Point features with a
     "times" property being an array of length 1.

"""

from jinja2 import Template

from ..map import Layer


class TimestampedWmsTileLayer(Layer):
    def __init__(self, data, transition_time=200, loop=False, auto_play=False,
                 period="P1D"):
        """Creates a TimestampedWmsTileLayer subclass of Layer that takes a
        WmsTileLayer and adds time control with the Leaflet.TimeDimension
        plugin.

        Parameters
        ----------
        data: WmsTileLayer.
           The WmsTileLayer that you want to add time support to.

           * Should be created like a typical WmsTileLayer and added to the map
             before being passed to this class.

           examples :
              # Create WmsTileLayer
              w = features.WmsTileLayer(
                  "http://this.wms.server/ncWMS/wms",
                  name="Test WMS Data",
                  styles="",
                  format="image/png",
                  transparent=True,
                  layers="test_data",
                  COLORSCALERANGE="0,10",
                  )
              # Add to map
              w.add_to(m)

              # Add WmsTileLayer to time control
              time = plugins.TimestampedWmsTileLayer(w)
              time.add_to(m)

        transition_time : int, default 200.
            The duration in ms of a transition from between timestamps.
        loop : bool, default False
            Whether the animation shall loop, default is to reduce load on WMS
            services.
        auto_play : bool, default False
            Whether the animation shall start automatically at startup, default
            is to reduce load on WMS services.
        period : str, default "P1D"
            Used to construct the array of available times starting
            from the first available time. Format: ISO8601 Duration
            ex: "P1M" -> 1/month
                "P1D"  -> 1/day
                "PT1H"  -> 1/hour
                "PT1M"  -> 1/minute
            Note: this seems to be overridden by the WMS Tile Layer
            GetCapabilities.
        """
        super(TimestampedWmsTileLayer, self).__init__(overlay=True,
                                                      control=data.control,
                                                      name=data.layer_name)
        self._name = 'TimestampedWmsTileLayer'

        self.transition_time = int(transition_time)
        self.loop = bool(loop)
        self.auto_play = bool(auto_play)
        self.period = period
        self.layer = data
        self._template = Template("""
        print kwargs
        {% macro script(this, kwargs) %}
            {{this._parent.get_name()}}.timeDimension = L.timeDimension({period:"{{this.period}}"});
            {{this._parent.get_name()}}.timeDimensionControl = L.control.timeDimension({
                position: 'bottomleft',
                autoPlay: {{'true' if this.auto_play else 'false'}},
                playerOptions: {
                    transitionTime: {{this.transition_time}},
                    loop: {{'true' if this.loop else 'false'}}}
                    });
            {{this._parent.get_name()}}.addControl({{this._parent.get_name()}}.timeDimensionControl);


            var {{this.get_name()}} = L.timeDimension.layer.wms({{ this.layer.get_name() }},
                {updateTimeDimension: true,
                 wmsVersion: '{{ this.layer.version }}',
                }
                ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)


    def render(self, **kwargs):
        super(TimestampedWmsTileLayer, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js"),  # noqa
            name='jquery2.0.0')

        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js"),  # noqa
            name='jqueryui1.10.2')

        figure.header.add_child(
            JavascriptLink("https://rawgit.com/nezasa/iso8601-js-period/master/iso8601.min.js"),  # noqa
            name='iso8601')

        figure.header.add_child(
            JavascriptLink("https://rawgit.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.min.js"),  # noqa
            name='leaflet.timedimension')

        figure.header.add_child(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css"),  # noqa
            name='highlight.js_css')

        figure.header.add_child(
            CssLink("http://apps.socib.es/Leaflet.TimeDimension/dist/leaflet.timedimension.control.min.css"),  # noqa
            name='leaflet.timedimension_css')
