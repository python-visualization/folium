"""
Test ScrollZoomToggler
----------------------
"""

import folium
from folium import plugins
from folium.template import Template
from folium.utilities import normalize


def test_scroll_zoom_toggler():
    m = folium.Map([45.0, 3.0], zoom_start=4)
    szt = plugins.ScrollZoomToggler()
    m.add_child(szt)

    out = normalize(m._parent.render())

    # Verify that the div has been created.
    tmpl = Template(
        """
        <img id="{{this.get_name()}}" alt="scroll"
        src="https://cdnjs.cloudflare.com/ajax/libs/ionicons/2.0.1/png/512/arrow-move.png"
        style="z-index: 999999"
        onclick="{{this._parent.get_name()}}.toggleScroll()"></img>
    """
    )
    assert "".join(tmpl.render(this=szt).split()) in "".join(out.split())

    # Verify that the style has been created
    tmpl = Template(
        """
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
    """
    )
    expected = normalize(tmpl.render(this=szt))
    assert expected in out

    # Verify that the script is okay.
    tmpl = Template(
        """
        {{this._parent.get_name()}}.scrollEnabled = true;

        {{this._parent.get_name()}}.toggleScroll = function() {
            if (this.scrollEnabled) {
                this.scrollEnabled = false;
                this.scrollWheelZoom.disable();
            } else {
                this.scrollEnabled = true;
                this.scrollWheelZoom.enable();
            }
        };

        {{this._parent.get_name()}}.toggleScroll();
    """
    )
    expected = normalize(tmpl.render(this=szt))
    assert expected in out

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds
