import folium
from folium import GeoJson, GeoJsonTooltip, Map
from folium.utilities import temp_html_filepath

# Selenium's pointer actions do not reliably reach Leaflet's SVG paths in
# headless Chrome, so the hover is dispatched as a DOM event instead. It
# bubbles through Map._handleDOMEvent exactly as a real pointer hover does.
HOVER = """
    const el = arguments[0];
    const rect = el.getBoundingClientRect();
    const opts = {
        bubbles: true,
        clientX: rect.x + rect.width / 2,
        clientY: rect.y + rect.height / 2,
    };
    el.dispatchEvent(new MouseEvent('mouseover', opts));
    el.dispatchEvent(new MouseEvent('mousemove', opts));
"""


def build() -> Map:
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "multipoint"},
                "geometry": {"type": "MultiPoint", "coordinates": [[0.0, 0.0]]},
            }
        ],
    }
    m = Map((0, 0), zoom_start=10)
    GeoJson(
        data,
        marker=folium.CircleMarker(radius=20),
        tooltip=GeoJsonTooltip(fields=["name"], labels=False),
    ).add_to(m)
    return m


def test_geojson_multipoint_tooltip(driver):
    """A GeoJsonTooltip must render for MultiPoint geometry.

    Leaflet returns a FeatureGroup for MultiPoint and assigns `feature` to
    that group only, while the tooltip resolves its source to the child
    layer that fired the event. Without the feature on the children, the
    tooltip's content function throws and nothing renders.

    https://github.com/python-visualization/folium/issues/1520
    """
    html = build().get_root().render()
    with temp_html_filepath(html) as filepath:
        driver.get_file(filepath)
        driver.wait_until(".folium-map")

        marker = driver.wait_until("path.leaflet-interactive")
        driver.execute_script(HOVER, marker)

        tooltip = driver.wait_until(".leaflet-tooltip.foliumtooltip")
        assert "multipoint" in tooltip.text

        driver.verify_js_logs()
