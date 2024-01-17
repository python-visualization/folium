import json
from typing import Optional, TextIO, Union

from branca.element import MacroElement
from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.folium import Map
from folium.utilities import JsCode, camelize, get_bounds, parse_options


class TimestampedGeoJson(JSCSSMixin, MacroElement):
    """
      Creates a TimestampedGeoJson plugin from timestamped GeoJSONs to append
      into a map with Map.add_child.

      There are two main modes this plugin can run:
      1. Timestamp mode, in which features only have start times
      2. Interval mode, in which features have start and end times

      These modes require different layout of the GeoJson

      Timestamp mode
      ----------
      For Timestamp mode you need a GeoJson with the following conditions

      * it contains only features of types LineString, MultiPoint, MultiLineString,
        Polygon and MultiPolygon.
      * each feature has a 'times' property with the same length as the
        coordinates array.
      * each element of each 'times' property is a timestamp in ms since epoch,
        or in ISO string.

      Eventually, you may have Point features with a 'times' property being an
      array of length 1.

      Interval mode
      -------------
      For Interval mode, you need a GeoJson with the following conditions.

      * Each feature contains a 'start' and 'end' property. The start and end
        can be any comparable item.


      Alternatively, you can trigger Interval mode by providing
      a `get_interval` function.

      * This function should be a JsCode object and take as parameter
        a GeoJson feature and return a dict containing values for
        'start', 'end', 'startExclusive' and 'endExcusive' (or false if no
        data could be extracted from the feature).
      * 'start' and 'end' can be any comparable items
      * 'startExclusive' and 'endExclusive' should be boolean values.

      Parameters
      ----------
      data: file, dict or str.
          The timestamped geo-json data you want to plot.

          * If file, then data will be read in the file and fully embedded in
            Leaflet's javascript.
          * If dict, then data will be converted to json and embedded in the
            javascript.
          * If str, then data will be passed to the javascript as-is.

      auto_play: bool, default True
          Whether the animation shall start automatically at startup.

      Timestamp mode parameters
      ------------------------
      transition_time: int, default 200.
          The duration in ms of a transition from between timestamps.
      loop: bool, default True
          Whether the animation shall loop.
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

      Interval mode parameters
      -------------------
      get_interval: JsCode
          Called for each feature, and should return either a time range for the
          feature or `false`, indicating that it should not be included in the
          timeline. The time range object should have 'start' and 'end' properties.
          Optionally, the boolean keys 'startExclusive' and 'endExclusive' allow the
          interval to be considered exclusive.

          If `get_interval` is not provided, 'start' and 'end' properties are
          assumed to be present on each feature.
      start: str, int or float, default earliest 'start' in GeoJson
          The beginning/minimum value of the timeline.
      end: str, int or float, default latest 'end' in GeoJSON
          The end/maximum value of the timeline.
      enable_playback: bool, default True
          Show playback controls (i.e. prev/play/pause/next).
      enable_keyboard_controls: bool, default False
          Allow playback to be controlled using the spacebar (play/pause) and
          right/left arrow keys (next/previous).
      show_ticks: bool, default True
          Show tick marks on the slider
      steps: int, default 1000
          How many steps to break the timeline into.
          Each step will then be (end-start) / steps. Only affects playback.
      playback_duration: int, default 10000
          Minimum time, in ms, for the playback to take. Will almost certainly
          actually take at least a bit longer -- after each frame, the next
          one displays in playback_duration/steps ms, so each frame really
          takes frame processing time PLUS step time.

    Example of Timestamp mode
    --------
    >>> TimestampedGeoJson(
    ...     {
    ...         "type": "FeatureCollection",
    ...         "features": [
    ...             {
    ...                 "type": "Feature",
    ...                 "geometry": {
    ...                     "type": "LineString",
    ...                     "coordinates": [[-70, -25], [-70, 35], [70, 35]],
    ...                 },
    ...                 "properties": {
    ...                     "times": [1435708800000, 1435795200000, 1435881600000],
    ...                     "tooltip": "my tooltip text",
    ...                 },
    ...             }
    ...         ],
    ...     }
    ... )

    See https://github.com/socib/Leaflet.TimeDimension for more information.

    Example of Interval mode
    --------

    >>> data = requests.get(
    ...     "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/borders.json"
    ... ).json()
    >>> TimestampedGeoJson(
    ...     data,
    ...     show_ticks=True,
    ...     style=JsCode(
    ...         '''
    ...        function (data) {
    ...            function getColorFor(str) {
    ...                // java String#hashCode
    ...                var hash = 0;
    ...                for (var i = 0; i < str.length; i++) {
    ...                    hash = str.charCodeAt(i) + ((hash << 5) - hash);
    ...                }
    ...                var red = (hash >> 24) & 0xff;
    ...                var grn = (hash >> 16) & 0xff;
    ...                var blu = (hash >> 8) & 0xff;
    ...                return "rgb(" + red + "," + grn + "," + blu + ")";
    ...            }
    ...            return {
    ...                stroke: false,
    ...                color: getColorFor(data.properties.name),
    ...                fillOpacity: 0.5,
    ...            };
    ...        }
    ...    '''
    ...     ),
    ... ).add_to(m)

    Other keyword arguments are passed to the GeoJson layer, so you can pass
      `style`, `point_to_layer` and/or `on_each_feature`.

    """

    _template = Template(
        """
        {% macro header(this,kwargs) %}
            <style>
                .leaflet-bottom.leaflet-left {
                    width: 100%;
                }
                .leaflet-control-container .leaflet-timeline-controls {
                    box-sizing: border-box;
                    width: 100%;
                    margin: 0;
                    margin-bottom: 15px;
                }
            </style>
        {% endmacro %}

        {% macro script(this, kwargs) %}
          var {{ this.get_name() }}_options = {{ this.options|tojson }};
          {% for key, value in this.functions.items() %}
            {{ this.get_name() }}_options["{{key}}"] = {{ value }};
          {% endfor %}

          {% if this.type == "Timedimension" %}
            L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
                _getDisplayDateFormat: {{ this._getDisplayDateFormat }}
            });
            {{this._parent.get_name()}}.timeDimension = L.timeDimension(
                {
                    period: {{ this.period|tojson }},
                }
            );
            var {{this.get_name()}}_timeDimensionControl = new L.Control.TimeDimensionCustom(
                {{ this.get_name() }}_options
            );
            {{this._parent.get_name()}}.addControl({{this.get_name()}}_timeDimensionControl);

            var {{this.get_name()}}_geoJsonLayer = L.geoJson({{this.data}},
                {{ this.get_name() }}_options
            })

            var {{this.get_name()}} = L.timeDimension.layer.geoJson(
                {{this.get_name()}}_geoJsonLayer,
                {
                    updateTimeDimension: true,
                    addlastPoint: {{ this.add_last_point|tojson }},
                    duration: {{ this.duration }},
                }
            ).addTo({{this._parent.get_name()}});

          {% else %}

            var {{ this.get_name() }} = L.timeline(
                {{ this.data|tojson }},
                {{ this.get_name() }}_options
            );
            var {{ this.get_name() }}_control = L.timelineSliderControl(
              {{ this.get_name() }}_options
            );
            {{ this.get_name() }}_control.addTo({{ this._parent.get_name() }});

            {{ this._parent.get_name() }}.addControl(control);
            {{ this.get_name() }}.addTo({{ this._parent.get_name() }});

            {{ this.get_name() }}_control.addTimelines({{ this.get_name() }});

          {% endif %}
        {% endmacro %}
    """
    )

    default_js = [
        (
            "timeline",
            "https://skeate.dev/Leaflet.timeline/examples/leaflet.timeline.js",
        ),
        (
            "jquery3.7.1",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js",
        ),
        (
            "jqueryui1.10.2",
            "https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
        ),
        (
            "iso8601",
            "https://cdn.jsdelivr.net/npm/iso8601-js-period@0.2.1/iso8601.min.js",
        ),
        (
            "leaflet.timedimension",
            "https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.min.js",
        ),
        (
            "moment",
            "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js",
        ),
    ]

    default_css = [
        (
            "highlight.js_css",
            "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css",
        ),
        (
            "leaflet.timedimension_css",
            "https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.control.css",
        ),
    ]

    style = JsCode(
        """
        function (feature) {
            return feature.properties.style;
        }
    """
    )

    on_each_feature = JsCode(
        """
        function(feature, layer) {
            if (feature.properties.popup) {
                layer.bindPopup(feature.properties.popup);
            }
            if (feature.properties.tooltip) {
                layer.bindTooltip(feature.properties.tooltip);
            }
        }
    """
    )

    point_to_layer = JsCode(
        """
        function (feature, latLng) {
            if (feature.properties.icon == 'marker') {
                if(feature.properties.iconstyle) {
                    return new L.Marker(latLng, {
                       icon: L.icon(feature.properties.iconstyle)});
                };
                //else
                return new L.Marker(latLng);
            };
            if (feature.properties.icon == 'circle') {
                if (feature.properties.iconstyle) {
                    return new L.circleMarker(latLng,
                        feature.properties.iconstyle)
                };
                //else
                return new L.circleMarker(latLng);
            };
            //else
            return new L.Marker(latLng);
          };
    """
    )

    def __init__(
        self,
        data: Union[dict, str, TextIO],
        # arguments relevant to both interval and timestamp mode
        auto_play: bool = True,
        date_options: str = "YYYY-MM-DD HH:mm:ss",
        point_to_layer: Optional[JsCode] = point_to_layer,
        style: Optional[JsCode] = style,
        on_each_feature: Optional[JsCode] = on_each_feature,
        # arguments relevant to interval mode
        get_interval: Optional[JsCode] = None,
        start: Optional[Union[str, int, float]] = None,
        end: Optional[Union[str, int, float]] = None,
        enable_playback: bool = True,
        enable_keyboard_controls: bool = False,
        show_ticks: bool = True,
        steps: int = 1000,
        playback_duration: int = 10000,
        # arguments relevant to timestamp mode
        duration: Optional[str] = None,
        add_last_point: bool = True,
        transition_time: int = 200,
        loop: bool = True,
        period: str = "P1D",
        min_speed: float = 0.1,
        max_speed: float = 10,
        loop_button: bool = False,
        time_slider_drag_update: bool = False,
        speed_slider: bool = True,
        **kwargs
    ):
        super().__init__()
        self._name = "Timeline"

        if "read" in dir(data):
            self.data = json.load(data)  # type: ignore
        elif type(data) is dict:
            self.data = data
        else:
            self.data = json.loads(data)  # type: ignore

        self.data = _convert_to_feature_collection(self.data)

        if get_interval:
            self.type = "Timeline"
        elif any(
            "times" in f["properties"]
            or "coordTimes" in f["properties"]
            or "linestringTimestamps" in f["properties"]
            or "time" in f["properties"]
            for f in self.data["features"]
        ):
            self.type = "Timedimension"
        elif any(
            "start" in f["properties"] and "end" in f["properties"]
            for f in self.data["features"]
        ):
            self.type = "Timeline"
        else:
            pass
            # Should not happen

        self._getDisplayDateFormat = JsCode(
            """
            function(date) {
                var newdate = new moment(date);
                return newdate.format(\""""
            + date_options
            + """\");
            }
        """
        )

        kwargs["auto_play"] = auto_play
        kwargs["point_to_layer"] = point_to_layer
        kwargs["on_each_feature"] = on_each_feature
        kwargs["style"] = style

        if self.type == "Timeline":
            kwargs["start"] = start
            kwargs["end"] = end
            kwargs["enable_playback"] = enable_playback
            kwargs["enable_keyboard_controls"] = enable_keyboard_controls
            kwargs["show_ticks"] = show_ticks
            kwargs["steps"] = steps
            kwargs["duration"] = playback_duration
            kwargs["format_output"] = self._getDisplayDateFormat
            if get_interval is not None:
                kwargs["get_interval"] = get_interval

        elif self.type == "Timedimension":
            self.add_last_point = bool(add_last_point)
            self.period = period
            self.date_options = date_options
            self.duration = "undefined" if duration is None else '"' + duration + '"'

            kwargs["position"] = "bottomleft"
            kwargs["min_speed"] = min_speed
            kwargs["max_speed"] = max_speed
            kwargs["loop_button"] = loop_button
            kwargs["time_slider_drag_update"] = time_slider_drag_update
            kwargs["speed_slider"] = speed_slider
            kwargs["player_options"] = (
                {
                    "transitionTime": int(transition_time),
                    "loop": loop,
                    "startOver": True,
                },
            )

        # extract JsCode objects
        self.functions = {}
        for key, value in list(kwargs.items()):
            if isinstance(value, JsCode):
                self.functions[camelize(key)] = value.js_code
                kwargs.pop(key)

        self.options = parse_options(**kwargs)

    def render(self, **kwargs):
        assert isinstance(
            self._parent, Map
        ), "TimestampedGeoJson can only be added to a Map object."
        super().render(**kwargs)

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """
        return get_bounds(self.data, lonlat=True)


def _convert_to_feature_collection(obj) -> dict:
    """Convert data into a FeatureCollection if it is not already."""
    if obj["type"] == "FeatureCollection":
        return obj
    # Catch case when GeoJSON is just a single Feature or a geometry.
    if "geometry" not in obj.keys():
        # Catch case when GeoJSON is just a geometry.
        return {"type": "Feature", "geometry": obj}
    return {"type": "FeatureCollection", "features": [obj]}
