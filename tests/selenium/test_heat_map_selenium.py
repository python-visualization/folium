import base64
import io
import os

from PIL import Image

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
        driver.get_file(filepath)
        assert driver.wait_until(".folium-map")
        driver.verify_js_logs()
    canvas = driver.wait_until("canvas.leaflet-heatmap-layer")
    assert canvas
    # get the canvas as a PNG base64 string
    canvas_base64 = driver.execute_script(
        "return arguments[0].toDataURL('image/png').substring(21);", canvas
    )
    screenshot_bytes = base64.b64decode(canvas_base64)
    screenshot = Image.open(io.BytesIO(screenshot_bytes))
    path = os.path.dirname(__file__)
    with open(os.path.join(path, "test_heat_map_selenium_screenshot.png"), "rb") as f:
        screenshot_expected = Image.open(f)
        if list(screenshot.getdata()) != list(screenshot_expected.getdata()):
            assert False, "screenshot is not as expected"
