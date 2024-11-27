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
