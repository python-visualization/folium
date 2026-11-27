from selenium.webdriver.support.ui import WebDriverWait

import folium
from folium.utilities import temp_html_filepath


def test_fit_bounds_on_hidden_map(driver):
    """fit_bounds must apply once a map that was hidden while loading is shown.

    A map without a size, for example in a notebook cell outside the
    viewport, can't be fitted. Leaflet then zooms all the way out, and the
    map stays like that when it becomes visible.

    https://github.com/python-visualization/folium/issues/2080
    """
    m = folium.Map()
    m.get_root().header.add_child(
        folium.Element("<style id='hide'>.folium-map { display: none; }</style>")
    )
    m.fit_bounds([[41.85, 12.40], [41.95, 12.60]])

    html = m.get_root().render()
    with temp_html_filepath(html) as filepath:
        driver.get_file(filepath)
        driver.verify_js_logs()
        name = m.get_name()
        get_zoom = f"return {name}.getZoom();"
        # While hidden the map can't be fitted and is zoomed out completely.
        assert driver.execute_script(get_zoom) == 0

        driver.execute_script("document.getElementById('hide').remove();")
        driver.wait_until(".folium-map")
        WebDriverWait(driver, timeout=10).until(
            lambda d: d.execute_script(get_zoom) > 0
        )
        expected_zoom = driver.execute_script(
            f"return {name}.getBoundsZoom([[41.85, 12.40], [41.95, 12.60]]);"
        )
        assert driver.execute_script(get_zoom) == expected_zoom
        driver.verify_js_logs()
