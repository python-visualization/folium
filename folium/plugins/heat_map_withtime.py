# -*- coding: utf-8 -*-
"""
Heat Map with time dimension
--------

Create a HeatMapWithTime layer

"""
import json
from jinja2 import Template

from branca.element import JavascriptLink, Figure, CssLink, Element
from branca.utilities import none_min, none_max

from folium.map import TileLayer

class HeatMapWithTime(TileLayer):
    def __init__(self, data, index=None, times=None, name=None, radius=15, max_opacity=0.6, scale_radius=False,
                 use_local_extrema=False, default_weight=1, overlay=True,
                 auto_play=False, backward_button=True, display_date=True,
                 forward_button=True, limit_minimum_range=5, limit_sliders=False,
                 loop_button=False, min_speed=0.1, max_speed=10, play_button=True,
                 play_reverse_button=False, position="bottomleft", speed_slider=True,
                 speed_step=0.1, style_NS = "leaflet-control-timecontrol", time_slider=True,
                 time_slider_drap_update=False, time_steps=1, time_control_title="Time Control"
                 ):
        """Create a HeatMapWithTime layer

        Parameters
        ----------

        """
        super(TileLayer, self).__init__(name=name)
        self._name = 'HeatMap'
        self._control_name = self.get_name() + 'Control'
        self.tile_name = name if name is not None else self.get_name()

        # input data
        self.data = data
        self.index = index if index is not None else [str(i) for i in range(1, len(data)+1)]
        self.times = times if times is not None else range(1, len(data)+1)

        # heatmap settings
        self.radius = radius
        self.max_opacity = max_opacity
        self.scale_radius = "true" if scale_radius else "false"
        self.use_local_extrema = "true" if use_local_extrema else "false"
        self.default_weight = default_weight
        self.overlay = overlay

        # time dimension settings
        self.auto_play = "true" if auto_play else "false"
        self.backward_button = "true" if backward_button else "false"
        self.display_date = "true" if display_date else "false"
        self.forward_button = "true" if forward_button else "false"
        self.limit_minimum_range = "true" if limit_minimum_range else "false"
        self.limit_sliders = "true" if limit_sliders else "false"
        self.loop_button = "true" if loop_button else "false"
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.play_button = "true" if play_button else "false"
        self.play_reverse_button = "true" if play_reverse_button else "false"
        self.position = position
        self.speed_slider = "true" if speed_slider else "false"
        self.speed_step = speed_step
        self.style_NS = style_NS
        self.time_slider = "true" if time_slider else "false"
        self.time_slider_drap_update = "true" if time_slider_drap_update else "false"
        self.time_steps = time_steps
        self.time_control_title = time_control_title

        self._template = Template(u"""
        {% macro script(this, kwargs) %}

            var times = {{this.times}};

            {{this._parent.get_name()}}.timeDimension = L.timeDimension({times : times, currentTime: new Date(1)});

            var {{this._control_name}} = new L.Control.TimeDimensionCustom({{this.index}}, {
                autoPlay: {{this.auto_play}},
                backwardButton: {{this.backward_button}},
                displayDate: {{this.display_date}},
                forwardButton: {{this.forward_button}},
                limitMinimumRange: {{this.limit_minimum_range}},
                limitSliders: {{this.limit_sliders}},
                loopButton: {{this.loop_button}},
                maxSpeed: {{this.max_speed}},
                minSpeed: {{this.min_speed}},
                playButton: {{this.play_button}},
                playReverseButton: {{this.play_reverse_button}},
                position: "{{this.position}}",
                speedSlider: {{this.speed_slider}},
                speedStep: {{this.speed_step}},
                styleNS: "{{this.style_NS}}",
                timeSlider: {{this.time_slider}},
                timeSliderDrapUpdate: {{this.time_slider_drap_update}},
                timeSteps: {{this.time_steps}},
                title: "{{this.time_control_title}}"
                })
                .addTo({{this._parent.get_name()}});

                var {{this.get_name()}} = new TDHeatmap({{this.data}},
                {heatmapOptions: {
                        radius: {{this.radius}},
                        maxOpacity: {{this.max_opacity}},
                        scaleRadius: {{this.scale_radius}},
                        useLocalExtrema: {{this.use_local_extrema}},
                        defaultWeight: {{this.default_weight}}
                    }
                })
                .addTo({{this._parent.get_name()}});

        {% endmacro %}
        """)

    def render(self, **kwargs):
        super(TileLayer, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_child(
            JavascriptLink("https://rawgit.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.min.js"),
            name='leaflet.timedimension.min.js')

        figure.header.add_child(
            JavascriptLink(
                "https://cdnjs.cloudflare.com/ajax/libs/heatmap.js/2.0.2/heatmap.min.js"),
            name='heatmap.min.js')

        figure.header.add_child(
            JavascriptLink(
                "https://rawgit.com/pa7/heatmap.js/develop/plugins/leaflet-heatmap/leaflet-heatmap.js"),
            name='leaflet-heatmap.js')

        figure.header.add_child(
            CssLink("http://apps.socib.es/Leaflet.TimeDimension/dist/leaflet.timedimension.control.min.css"),  # noqa
            name='leaflet.timedimension.control.min.css')

        figure.header.add_child(
            Element(
                """
            <script>
                var TDHeatmap = L.TimeDimension.Layer.extend({

            initialize: function(data, options) {
                var heatmapCfg = {
                    radius: 15,
                    maxOpacity: 1.,
                    scaleRadius: false,
                    useLocalExtrema: false,
                    latField: 'lat',
                    lngField: 'lng',
                    valueField: 'count',
                    defaultWeight : 1,
                };
                heatmapCfg = $.extend({}, heatmapCfg, options.heatmapOptions || {});
                var layer = new HeatmapOverlay(heatmapCfg);
                L.TimeDimension.Layer.prototype.initialize.call(this, layer, options);
                this._currentLoadedTime = 0;
                this._currentTimeData = {
                    data: []
                    };
                this.data= data;
                this.defaultWeight = heatmapCfg.defaultWeight || 1;
            },
            onAdd: function(map) {
                L.TimeDimension.Layer.prototype.onAdd.call(this, map);
                map.addLayer(this._baseLayer);
                if (this._timeDimension) {
                    this._getDataForTime(this._timeDimension.getCurrentTime());
                }
            },
            _onNewTimeLoading: function(ev) {
                this._getDataForTime(ev.time);
                return;
            },
            isReady: function(time) {
                return (this._currentLoadedTime == time);
            },
            _update: function() {
                this._baseLayer.setData(this._currentTimeData);
                return true;
            },
            _getDataForTime: function(time) {
                    delete this._currentTimeData.data;
                    this._currentTimeData.data = [];
                    var data = this.data[time-1];
                    for (var i = 0; i < data.length; i++) {
                        this._currentTimeData.data.push({
                                lat: data[i][0],
                                lng: data[i][1],
                                count: data[i].length>2 ? data[i][2] : this.defaultWeight
                            });
                        }
                    this._currentLoadedTime = time;
                    if (this._timeDimension && time == this._timeDimension.getCurrentTime() && !this._timeDimension.isLoading()) {
                        this._update();
                    }
                    this.fire('timeload', {
                        time: time
                    });
                }
        });

        L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
            initialize: function(index, options) {
                var playerOptions = {
                    buffer: 1,
                    minBufferReady: -1
                    };
                options.playerOptions = $.extend({}, playerOptions, options.playerOptions || {});
                L.Control.TimeDimension.prototype.initialize.call(this, options);
                this.index = index;
                },
            _getDisplayDateFormat: function(date){
                return this.index[date.getTime()-1];
                }
            });
            </script>
                """,
                template_name="timeControlScript"
            )
        )

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """
        bounds = [[None, None], [None, None]]
        for point in self.data:
            bounds = [
                [
                    none_min(bounds[0][0], point[0]),
                    none_min(bounds[0][1], point[1]),
                ],
                [
                    none_max(bounds[1][0], point[0]),
                    none_max(bounds[1][1], point[1]),
                ],
            ]
        return bounds
