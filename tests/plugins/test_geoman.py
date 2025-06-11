"""
Test GeoMan
----------------

"""

import folium
from folium import plugins
from folium.template import Template
from folium.utilities import normalize


def test_geoman():
    m = folium.Map([47, 3], zoom_start=1)
    fs = plugins.GeoMan().add_to(m)

    out = normalize(m._parent.render())

    # verify that the GeoMan plugin was added to
    # the map
    tmpl = Template(
        """
        {{this.get_name()}}.addControls(
            {{this.options|tojavascript}}
        )
    """
    )

    assert normalize(tmpl.render(this=fs)) in out
