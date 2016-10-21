# -*- coding: utf-8 -*-
"""
Test ScrollZoomToggler
----------------------
"""

from jinja2 import Template

import folium
from folium import plugins


def test_scroll_zoom_toggler():
    m = folium.Map([45., 3.], zoom_start=4)
    szt = plugins.ScrollZoomToggler()
    m.add_child(szt)
    m._repr_html_()

    out = m._parent.render()

    # Verify that the div has been created.
    tmpl = Template("""
        <img id="{{this.get_name()}}" alt="scroll"
        src="https://cdnjs.cloudflare.com/ajax/libs/ionicons/2.0.1/png/512/arrow-move.png"
        style="z-index: 999999"
        onclick="{{this._parent.get_name()}}.toggleScroll()"></img>
    """)
    assert ''.join(tmpl.render(this=szt).split()) in ''.join(out.split())

    # Verify that the style has been created
    tmpl = Template("""
        <style>
            #{{this.get_name()}} {
                position:absolute;
                width:35px;
                bottom:10px;
                height:35px;
                left:10px;
                background-color:#fff;
                text-align:center;
                line-height:35px;
                vertical-align: middle;
                }
        </style>
    """)
    assert ''.join(tmpl.render(this=szt).split()) in ''.join(out.split())

    # Verify that the script is okay.
    tmpl = Template("""
        {{this._parent.get_name()}}.scrollEnabled = true;

        {{this._parent.get_name()}}.toggleScroll = function() {
            if (this.scrollEnabled) {
                this.scrollEnabled = false;
                this.scrollWheelZoom.disable();
                }
            else {
                this.scrollEnabled = true;
                this.scrollWheelZoom.enable();
                }
            };

        {{this._parent.get_name()}}.toggleScroll();
    """)
    assert ''.join(tmpl.render(this=szt).split()) in ''.join(out.split())

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds
