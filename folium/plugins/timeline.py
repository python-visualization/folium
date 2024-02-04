from typing import List, Optional, TextIO, Union

from branca.element import MacroElement
from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.features import GeoJson
from folium.folium import Map
from folium.utilities import JsCode, camelize, get_bounds, parse_options


class Timeline(GeoJson):
    """
      Creates a layer from GeoJSON with time data to append
      into a map with Map.add_child.

      To add time data, you need to do one of the following:

      * Add a 'start' and 'end' property to each feature. The start and end
        can be any comparable item.


      Alternatively, you can provide
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
          The geojson data you want to plot.

      auto_play: bool, default True
          Whether the animation shall start automatically at startup.

      get_interval: JsCode
          Called for each feature, and should return either a time range for the
          feature or `false`, indicating that it should not be included in the
          timeline. The time range object should have 'start' and 'end' properties.
          Optionally, the boolean keys 'startExclusive' and 'endExclusive' allow the
          interval to be considered exclusive.

          If `get_interval` is not provided, 'start' and 'end' properties are
          assumed to be present on each feature.

    Examples
    --------

    >>> data = requests.get(
    ...     "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/borders.json"
    ... ).json()
    >>> timeline = Timeline(
    ...     data,
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
    >>> GeoJsonPopup(fields=["name"], labels=True).add_to(timeline)
    >>> TimelineSlider(
    ...     auto_play=False,
    ...     enable_keyboard_controls=True,
    ...     playback_duration=60000,
    ... ).addTimelines(timeline).add_to(m)

    Other keyword arguments are passed to the GeoJson layer, so you can pass
      `style`, `point_to_layer` and/or `on_each_feature`.

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
          var {{ this.get_name() }}_options = {{ this.options|tojson }};
          {% for key, value in this.functions.items() %}
            {{ this.get_name() }}_options["{{key}}"] = {{ value }};
          {% endfor %}

          var {{ this.get_name() }} = L.timeline(
              {{ this.data|tojson }},
              {{ this.get_name() }}_options
          );
          {{ this.get_name() }}.addTo({{ this._parent.get_name() }});
        {% endmacro %}
    """
    )

    default_js = [
        (
            "timeline",
            "https://skeate.dev/Leaflet.timeline/examples/leaflet.timeline.js",
        ),
        (
            "moment",
            "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js",
        ),
    ]

    def __init__(
        self,
        data: Union[dict, str, TextIO],
        date_options: str = "YYYY-MM-DD HH:mm:ss",
        point_to_layer: Optional[JsCode] = None,
        style: Optional[JsCode] = None,
        on_each_feature: Optional[JsCode] = None,
        get_interval: Optional[JsCode] = None,
        **kwargs
    ):
        super().__init__(data)
        self._name = "Timeline"

        kwargs["point_to_layer"] = point_to_layer
        kwargs["on_each_feature"] = on_each_feature
        kwargs["style"] = style

        if get_interval is not None:
            kwargs["get_interval"] = get_interval

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
        ), "Timeline can only be added to a Map object."
        super().render(**kwargs)

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """
        return get_bounds(self.data, lonlat=True)


class TimelineSlider(JSCSSMixin, MacroElement):
    """
      Creates a timeline slider for timeline layers.

      Parameters
      ----------
      auto_play: bool, default True
          Whether the animation shall start automatically at startup.

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

    Examples
    --------
    See the documentation for Timeline

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

          var {{ this.get_name() }} = L.timelineSliderControl(
              {{ this.get_name() }}_options
          );
          {{ this.get_name() }}.addTo({{ this._parent.get_name() }});

          {% for timeline in this.timelines %}
              {{ this.get_name() }}.addTimelines({{ timeline.get_name() }});
          {% endfor %}

        {% endmacro %}
    """
    )

    default_js = [
        (
            "timeline",
            "https://skeate.dev/Leaflet.timeline/examples/leaflet.timeline.js",
        ),
        (
            "moment",
            "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js",
        ),
    ]

    def __init__(
        self,
        # arguments relevant to both interval and timestamp mode
        auto_play: bool = True,
        date_options: str = "YYYY-MM-DD HH:mm:ss",
        start: Optional[Union[str, int, float]] = None,
        end: Optional[Union[str, int, float]] = None,
        enable_playback: bool = True,
        enable_keyboard_controls: bool = False,
        show_ticks: bool = True,
        steps: int = 1000,
        playback_duration: int = 10000,
        speed_slider: bool = True,
        **kwargs
    ):
        super().__init__()
        self._name = "TimelineSlider"
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
        kwargs["start"] = start
        kwargs["end"] = end
        kwargs["enable_playback"] = enable_playback
        kwargs["enable_keyboard_controls"] = enable_keyboard_controls
        kwargs["show_ticks"] = show_ticks
        kwargs["steps"] = steps
        kwargs["duration"] = playback_duration
        kwargs["format_output"] = self._getDisplayDateFormat

        # extract JsCode objects
        self.functions = {}
        for key, value in list(kwargs.items()):
            if isinstance(value, JsCode):
                self.functions[camelize(key)] = value.js_code
                kwargs.pop(key)

        self.timelines: List[Timeline] = []
        self.options = parse_options(**kwargs)

    def add_timelines(self, *args):
        """Add timelines to the control"""
        self.timelines += args  # we do not check for duplicates
        return self

    def render(self, **kwargs):
        assert isinstance(
            self._parent, Map
        ), "TimelineSlider can only be added to a Map object."
        super().render(**kwargs)

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """
        return get_bounds(self.data, lonlat=True)
