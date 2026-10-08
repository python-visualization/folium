"""
Tests for issue #2278: Font Awesome brand icons do not render.

Leaflet.awesome-markers emits a `fa` class, which Font Awesome 6 maps to
the solid webfont. Brand glyphs such as bluetooth live in fa-brands-400,
so the rendered marker HTML must include the `fa-brands` class.
"""

import folium


def test_fontawesome_brand_icon_html_includes_fa_brands():
    m = folium.Map(location=[41, -71], zoom_start=4)
    folium.Marker(
        location=[41, -75],
        icon=folium.Icon(prefix="fa", icon="fa-bluetooth"),
    ).add_to(m)

    html = m.get_root().render()
    assert "fa-brands" in html
