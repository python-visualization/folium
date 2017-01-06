# -*- coding: utf-8 -*-
"""
Test Fullscreen
-----------------------
"""
import folium
from folium import plugins
from jinja2 import Template


def test_fullscreen():
    m = folium.Map([47, 3], zoom_start=1)
    fs = plugins.Fullscreen()
    m.add_child(fs)
    m._repr_html_()

    out = m._parent.render()

    # verify that the fullscreen control was rendered
    tmpl = Template("""
        L.control.fullscreen({
            position: '{{this.position}}',
            title: '{{this.title}}',
            titleCancel: '{{this.titleCancel}}',
            forceSeparateButton: {{this.forceSeparateButton}},
            }).addTo({{this._parent.get_name()}});
        {{this._parent.get_name()}}.on('enterFullscreen', function(){
            console.log('entered fullscreen');
        });
    """)

    assert ''.join(tmpl.render(this=fs).split()) in ''.join(out.split())
