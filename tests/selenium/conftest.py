import pytest
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located


@pytest.fixture(scope='session')
def driver():
    """Pytest fixture that yields a Selenium WebDriver instance"""
    driver = DriverFolium()
    try:
        yield driver
    finally:
        driver.quit()


class DriverFolium(Chrome):
    """Selenium WebDriver wrapper that adds folium test specific features."""

    def __init__(self):
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        options.add_argument("--window-size=1024,768")
        super().__init__(options=options)

    def get_file(self, filepath):
        self.clean_window()
        super().get('file://' + filepath)

    def clean_window(self):
        """Make sure we have a fresh window (without restarting the browser)."""
        # open new tab
        self.execute_script('window.open();')
        # close old tab
        self.close()
        # switch to new tab
        self.switch_to.window(self.window_handles[0])

    def verify_js_logs(self):
        """Raise an error if there are errors in the browser JS console."""
        logs = self.get_log('browser')
        for log in logs:
            if log['level'] == 'SEVERE':
                msg = ' '.join(log['message'].split()[2:])
                raise RuntimeError('Javascript error: "{}".'.format(msg))

    def wait_until(self, css_selector, timeout=10):
        """Wait for and return the element(s) selected by css_selector."""
        wait = WebDriverWait(self, timeout=timeout)
        is_visible = visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        return wait.until(is_visible)
