from selenium.webdriver.common.by import By

import folium
import folium.plugins
from folium.utilities import temp_html_filepath


def test_geojson(driver):
    """Verify that loading data in GeoJson works well for different use cases.

    Prevent two regressions:
    - https://github.com/python-visualization/folium/pull/1190
    - https://github.com/python-visualization/folium/pull/1289

    """
    data_url = "https://cdn.jsdelivr.net/gh/python-visualization/folium@main/examples/data/search_bars_rome.json"

    m = folium.Map((41.9, 12.5), zoom_start=10, tiles="cartodbpositron")
    marker_cluster = folium.plugins.MarkerCluster(name="cluster").add_to(m)
    folium.GeoJson(data_url, embed=False).add_to(marker_cluster)
    folium.GeoJson(data_url, embed=False, show=False, name="geojson").add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    html = m.get_root().render()
    with temp_html_filepath(html) as filepath:
        driver.get_file(filepath)
        assert driver.wait_until(".folium-map")
        driver.verify_js_logs()
    # Verify the marker cluster is shown, it's a yellow icon with '18' in it.
    icon = driver.wait_until(".leaflet-marker-icon.marker-cluster > div > span")
    assert icon.text == "18"
    # Verify the second GeoJson layer is not shown, because we used show=False.
    control_label = driver.wait_until(
        ".leaflet-control-layers-overlays > label:nth-of-type(2)"
    )
    assert control_label.text == "geojson"
    control_input = control_label.find_element(By.CSS_SELECTOR, value="input")
    assert control_input.get_attribute("checked") is None


def test_geojson_null_properties(driver):
    """A feature with "properties": null must not break the map.

    RFC 7946 allows null properties. The default style callback read
    feature.properties.style, which threw a TypeError and stopped the rest
    of the map script, so nothing after it was drawn.
    """
    square = [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": None,
                "geometry": {"type": "Polygon", "coordinates": square},
            },
            {
                "type": "Feature",
                "properties": {"style": {"color": "red"}},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[x + 20, y] for x, y in square[0]]],
                },
            },
        ],
    }
    m = folium.Map((5, 15), zoom_start=4)
    folium.GeoJson(data).add_to(m)
    folium.Marker((5, 15)).add_to(m)

    html = m.get_root().render()
    with temp_html_filepath(html) as filepath:
        driver.get_file(filepath)
        assert driver.wait_until(".folium-map")
        driver.verify_js_logs()
    paths = driver.find_elements(By.CSS_SELECTOR, "path.leaflet-interactive")
    assert len(paths) == 2
    assert paths[1].get_attribute("stroke") == "red"
    assert driver.find_elements(By.CSS_SELECTOR, ".leaflet-marker-icon")
