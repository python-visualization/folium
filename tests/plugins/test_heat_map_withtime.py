# -*- coding: utf-8 -*-
"""
Test HeatMapWithTime
------------
"""

from jinja2 import Template
import numpy as np

import folium
from folium import plugins


def test_heat_map_with_time():
    np.random.seed(3141592)
    initial_data = (np.random.normal(size=(100, 2)) * np.array([[1, 1]]) +
                    np.array([[48, 5]]))
    move_data = np.random.normal(size=(100, 2)) * 0.01
    data = [(initial_data + move_data * i).tolist() for i in range(100)]
    m = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)
    hm = plugins.HeatMapWithTime(data)
    m.add_child(hm)
    m._repr_html_()

    out = m._parent.render()

    # We verify that the script imports are present.
    script = '<script src="https://rawgit.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.min.js"></script>'  # noqa
    assert script in out
    script = '<script src="https://cdnjs.cloudflare.com/ajax/libs/heatmap.js/2.0.2/heatmap.min.js"></script>'  # noqa
    assert script in out
    script = '<script src="https://rawgit.com/pa7/heatmap.js/develop/plugins/leaflet-heatmap/leaflet-heatmap.js"></script>'  # noqa
    assert script in out
    script = '<link rel="stylesheet" href="http://apps.socib.es/Leaflet.TimeDimension/dist/leaflet.timedimension.control.min.css" />'  # noqa
    assert script in out

    # We verify that the script part is correct.
    tmpl = Template("""
            var times = {{this.times}};

            {{this._parent.get_name()}}.timeDimension = L.timeDimension({times : times, currentTime: new Date(1)});

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
                        minOpacity: {{this.min_opacity}},
                        maxOpacity: {{this.max_opacity}},
                        scaleRadius: {{this.scale_radius}},
                        useLocalExtrema: {{this.use_local_extrema}},
                        defaultWeight: 1 ,
                    }
                })
                .addTo({{this._parent.get_name()}});
    """)

    assert tmpl.render(this=hm)
