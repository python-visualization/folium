"""
Test Timeline
-----------------------

"""

import json

from jinja2 import Template

import folium
from folium import plugins
from folium.features import GeoJsonPopup
from folium.utilities import normalize


def test_timeline():
    m = folium.Map()

    data = json.load(open("./examples/data/historical_country_borders.json"))
    timeline = plugins.Timeline(
        data,
    ).add_to(m)
    GeoJsonPopup(fields=["name"], labels=True).add_to(timeline)
    slider = (
        plugins.TimelineSlider(
            auto_play=False,
            show_ticks=True,
            enable_keyboard_controls=True,
            playback_duration=30000,
        )
        .add_timelines(timeline)
        .add_to(m)
    )

    out = normalize(m._parent.render())

    # Verify the imports.
    assert (
        '<script src="https://cdn.jsdelivr.net/npm/leaflet.timeline@1.6.0/dist/leaflet.timeline.min.js"></script>'
        in out
    )
    assert (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js"></script>'
        in out
    )

    # Verify that the script is okay.
    tmpl = Template(
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
    )  # noqa
    expected = normalize(tmpl.render(this=slider))
    assert expected in out
