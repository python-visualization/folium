"""
Test Draw
---------
"""

import re

import folium
from folium import plugins
from folium.template import Template
from folium.utilities import normalize


def test_draw():
    m = folium.Map([45.0, 3.0], zoom_start=4)
    draw = plugins.Draw(export=True, filename="my_data.geojson")
    m.add_child(draw)

    out = normalize(m._parent.render())

    # Verify that the export button has been created with a unique id.
    tmpl = Template("<a href='#' id='export_{{this.get_name()}}'>Export</a>")
    assert normalize(tmpl.render(this=draw)) in out

    # Verify that the style targets that same id.
    assert normalize(f"#export_{draw.get_name()} {{") in out

    # Verify that the click handler is wired to that same id.
    assert (
        normalize(f"document.getElementById('export_{draw.get_name()}').onclick") in out
    )


def test_draw_no_export():
    m = folium.Map([45.0, 3.0], zoom_start=4)
    draw = plugins.Draw()
    m.add_child(draw)

    out = normalize(m._parent.render())

    assert "Export</a>" not in out
    assert f"export_{draw.get_name()}" not in out


def test_two_draw_controls_get_unique_export_ids():
    """Each Draw gets its own export button, wired to its own layers.

    A hard-coded ``id='export'`` made the second button dead and pointed the
    first at the wrong FeatureGroup.
    """
    m = folium.Map([45.0, 3.0], zoom_start=4)
    first = plugins.Draw(export=True, filename="first.geojson")
    second = plugins.Draw(export=True, filename="second.geojson")
    m.add_child(first)
    m.add_child(second)

    out = m._parent.render()

    ids = re.findall(r"id='(export_[^']+)'", out)
    assert len(ids) == 2
    assert len(set(ids)) == 2, f"export button ids are not unique: {ids}"

    # Each handler must reference its own element, layers and filename.
    for draw, filename in ((first, "first.geojson"), (second, "second.geojson")):
        element_id = f"export_{draw.get_name()}"
        assert f"id='{element_id}'" in out
        start = out.index(f"document.getElementById('{element_id}').onclick")
        handler = out[start : out.index("}", start) + 1]
        assert f"drawnItems_{draw.get_name()}.toGeoJSON()" in handler
        assert filename in handler
