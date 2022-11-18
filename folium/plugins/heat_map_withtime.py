from branca.element import Element, Figure
from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.map import Layer
from folium.utilities import none_max, none_min


class HeatMapWithTime(JSCSSMixin, Layer):
    """
    Create a HeatMapWithTime layer

    Parameters
    ----------
    data: list of list of points of the form [lat, lng] or [lat, lng, weight]
        The points you want to plot. The outer list corresponds to the various time
        steps in sequential order. (weight is in (0, 1] range and defaults to 1 if
        not specified for a point)
    index: Index giving the label (or timestamp) of the elements of data. Should have
        the same length as data, or is replaced by a simple count if not specified.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls.
    radius: default 15.
        The radius used around points for the heatmap.
    blur: default 0.8.
        Blur strength used for the heatmap. Must be between 0 and 1.
    min_opacity: default 0
        The minimum opacity for the heatmap.
    max_opacity: default 0.6
        The maximum opacity for the heatmap.
    scale_radius: default False
        Scale the radius of the points based on the zoom level.
    gradient: dict, default None
        Match point density values to colors. Color can be a name ('red'),
        RGB values ('rgb(255,0,0)') or a hex number ('#FF0000').
    use_local_extrema: default False
        Defines whether the heatmap uses a global extrema set found from the input data
        OR a local extrema (the maximum and minimum of the currently displayed view).
    auto_play: default False
        Automatically play the animation across time.
    display_index: default True
        Display the index (usually time) in the time control.
    index_steps: default 1
        Steps to take in the index dimension between animation steps.
    min_speed: default 0.1
        Minimum fps speed for animation.
    max_speed: default 10
        Maximum fps speed for animation.
    speed_step: default 0.1
        Step between different fps speeds on the speed slider.
    position: default 'bottomleft'
        Position string for the time slider. Format: 'bottom/top'+'left/right'.
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}

            var times = {{this.times}};

            {{this._parent.get_name()}}.timeDimension = L.timeDimension(
                {times : times, currentTime: new Date(1)}
            );

            var {{this._control_name}} = new L.Control.TimeDimensionCustom({{this.index}}, {
                autoPlay: {{this.auto_play}},
                backwardButton: {{this.backward_button}},
                displayDate: {{this.display_index}},
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
                timeSteps: {{this.index_steps}}
                })
                .addTo({{this._parent.get_name()}});

                var {{this.get_name()}} = new TDHeatmap({{this.data}},
                {heatmapOptions: {
                        radius: {{this.radius}},
                        blur: {{this.blur}},
                        minOpacity: {{this.min_opacity}},
                        maxOpacity: {{this.max_opacity}},
                        scaleRadius: {{this.scale_radius}},
                        useLocalExtrema: {{this.use_local_extrema}},
                        defaultWeight: 1,
                        {% if this.gradient %}gradient: {{ this.gradient }}{% endif %}
                    }
                })
                .addTo({{this._parent.get_name()}});

        {% endmacro %}
        """
    )

    default_js = [
        (
            "iso8601",
            "https://cdn.jsdelivr.net/npm/iso8601-js-period@0.2.1/iso8601.min.js",
        ),
        (
            "leaflet.timedimension.min.js",
            "https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.min.js",
        ),
        (
            "heatmap.min.js",
            "https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/pa7_hm.min.js",
        ),
        (
            "leaflet-heatmap.js",
            "https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/pa7_leaflet_hm.min.js",
        ),
    ]
    default_css = [
        (
            "leaflet.timedimension.control.min.css",
            "https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.control.css",
        )
    ]

    def __init__(
        self,
        data,
        index=None,
        name=None,
        radius=15,
        blur=0.8,
        min_opacity=0,
        max_opacity=0.6,
        scale_radius=False,
        gradient=None,
        use_local_extrema=False,
        auto_play=False,
        display_index=True,
        index_steps=1,
        min_speed=0.1,
        max_speed=10,
        speed_step=0.1,
        position="bottomleft",
        overlay=True,
        control=True,
        show=True,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "HeatMap"
        self._control_name = self.get_name() + "Control"

        # Input data.
        self.data = data
        self.index = (
            index if index is not None else [str(i) for i in range(1, len(data) + 1)]
        )
        if len(self.data) != len(self.index):
            raise ValueError(
                "Input data and index are not of compatible lengths."
            )  # noqa
        self.times = list(range(1, len(data) + 1))

        # Heatmap settings.
        self.radius = radius
        self.blur = blur
        self.min_opacity = min_opacity
        self.max_opacity = max_opacity
        self.scale_radius = "true" if scale_radius else "false"
        self.use_local_extrema = "true" if use_local_extrema else "false"
        self.gradient = gradient

        # Time dimension settings.
        self.auto_play = "true" if auto_play else "false"
        self.display_index = "true" if display_index else "false"
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.position = position
        self.speed_step = speed_step
        self.index_steps = index_steps

        # Hard coded defaults for simplicity.
        self.backward_button = "true"
        self.forward_button = "true"
        self.limit_sliders = "true"
        self.limit_minimum_range = 5
        self.loop_button = "true"
        self.speed_slider = "true"
        self.time_slider = "true"
        self.play_button = "true"
        self.play_reverse_button = "true"
        self.time_slider_drap_update = "false"
        self.style_NS = "leaflet-control-timecontrol"

    def render(self, **kwargs):
        super().render(**kwargs)

        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."

        figure.header.add_child(
            Element(
                """
            <script>
                var TDHeatmap = L.TimeDimension.Layer.extend({

            initialize: function(data, options) {
                var heatmapCfg = {
                    radius: 15,
                    blur: 0.8,
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
                """,  # noqa
                template_name="timeControlScript",
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
