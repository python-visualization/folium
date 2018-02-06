# -*- coding: utf-8 -*-

"""
Test BeautifyMarker
---------------

"""

from __future__ import (absolute_import, division, print_function)

import folium

from folium import plugins

from jinja2 import Template


def test_beautify_marker():
    m = folium.Map([30., 0.], zoom_start=3)
    bm1 = plugins.BeautifyMarker(
        location=[46, -122],
        icon='plane',
        border_color='#b3334f',
        text_color='#b3334f',
        popup='Portland, OR'
    ).add_to(m)

    bm2 = plugins.BeautifyMarker(
        location=[50, -121],
        border_color='#00ABDC',
        text_color='#00ABDC',
        number=10,
        inner_icon_style='margin-top:0;'
    ).add_to(m)

    m.add_child(bm1)
    m.add_child(bm2)
    m._repr_html_()

    out = m._parent.render()

    # We verify that the script import is present.
    script = '<script src="https://cdn.rawgit.com/marslan390/BeautifyMarker/master/leaflet-beautify-marker-icon.js"></script>'  # noqa
    assert script in out
    # print(out)
    # We verify that the css import is present.
    css = '<link rel="stylesheet" href="https://cdn.rawgit.com/marslan390/BeautifyMarker/master/leaflet-beautify-marker-icon.css" />'  # noqa
    assert css in out

    # We verify that the Beautiful Markers are rendered correctly
    tmpl = Template(u"""
            var options = {
                {% if this.icon %}
                icon: '{{ this.icon }}',
                {% endif %}
                {% if this.icon_shape %}
                iconShape: '{{ this.icon_shape }}',
                {% endif %}
                borderWidth: {{ this.border_width }},
                borderColor: '{{ this.border_color }}',
                textColor: '{{ this.text_color }}',
                backgroundColor: '{{ this.background_color }}',
                innerIconStyle: '{{ this.inner_icon_style }}',
                spin: {{ this.spin }},
                {% if this.has_number %}
                isAlphaNumericIcon: {{ this.is_alpha_numeric_icon }},
                text: {{ this.number }},
                {% endif %}
            };
            var {{this.get_name()}} = L.marker(
                [{{this.location[0]}}, {{this.location[1]}}],
                {
                    icon: new L.BeautifyIcon.icon(options),
                    draggable: {{ this.is_draggable }},
                    }
                )
                {% if this.tooltip %}.bindTooltip("{{this.tooltip.__str__()}}"){% endif %}
                .addTo({{this._parent.get_name()}});
            """)  # noqa

    assert tmpl.render(this=bm1) in out
    assert tmpl.render(this=bm2) in out

    bounds = m.get_bounds()
    assert bounds == [[46, -122], [50, -121]], bounds
