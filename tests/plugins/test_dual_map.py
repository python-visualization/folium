"""
Test DualMap
------------
"""

import folium
import folium.plugins
from folium.template import Template
from folium.utilities import normalize


def test_dual_map():
    m = folium.plugins.DualMap((0, 0))

    folium.FeatureGroup(name="both").add_to(m)
    folium.FeatureGroup(name="left").add_to(m.m1)
    folium.FeatureGroup(name="right").add_to(m.m2)

    figure = m.get_root()
    assert isinstance(figure, folium.Figure)
    out = normalize(figure.render())

    script = '<script src="https://cdn.jsdelivr.net/gh/jieter/Leaflet.Sync/L.Map.Sync.min.js"></script>'  # noqa
    assert script in out

    tmpl = Template(
        """
        {{ this.m1.get_name() }}.sync({{ this.m2.get_name() }});
        {{ this.m2.get_name() }}.sync({{ this.m1.get_name() }});
    """
    )

    assert normalize(tmpl.render(this=m)) in out
