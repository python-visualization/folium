
import os

import folium
from folium.plugins.heat_map import HeatMap
from folium.utilities import temp_html_filepath


def test_heat_map_with_weights(driver):
    """Verify that HeatMap uses weights in data correctly.

    This test will fail in non-headless mode because window size will be different.

    """
    m = folium.Map((0.5, 0.5), zoom_start=8, tiles=None)
    HeatMap(
        # make four dots with different weights: 1, 1, 1.5 and 2.
        data=[
            (0, 0, 1.5),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 2),
        ],
        radius=70,
        blur=50,
    ).add_to(m)
    html = m.get_root().render()
    with temp_html_filepath(html) as filepath:
        driver.set_window_size(600, 600)
        driver.get_file(filepath)
        assert driver.wait_until('.folium-map')
        driver.verify_js_logs()
    assert driver.wait_until('canvas.leaflet-heatmap-layer')
    screenshot = driver.get_screenshot_as_png()
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'test_heat_map_selenium_screenshot.png'), 'rb') as f:
        screenshot_expected = f.read()
    assert hash(screenshot) == hash(screenshot_expected)
