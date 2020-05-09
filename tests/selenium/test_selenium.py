
import base64
import glob
from html.parser import HTMLParser
import os
import subprocess

import nbconvert
import pytest
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located


def create_driver():
    """Create a Selenium WebDriver instance."""
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    driver = Chrome(options=options)
    return driver


@pytest.fixture(scope='module')
def driver():
    """Pytest fixture that yields a Selenium WebDriver instance"""
    driver = create_driver()
    try:
        yield driver
    finally:
        driver.quit()


def clean_window(driver):
    # open new tab
    driver.execute_script('window.open();')
    # close old tab
    driver.close()
    # switch to new tab
    driver.switch_to.window(driver.window_handles[0])


def find_notebooks():
    """Return a list of filenames of the example notebooks."""
    path = os.path.dirname(__file__)
    pattern = os.path.join(path, '..', '..', 'examples', '*.ipynb')
    files = glob.glob(pattern)
    files = [f for f in files if not f.endswith('.nbconvert.ipynb')]
    if files:
        return files
    else:
        raise IOError('Could not find the notebooks')


@pytest.mark.parametrize('filepath', find_notebooks())
def test_notebook(filepath, driver):
    for filepath_html in get_notebook_html(filepath):
        clean_window(driver)
        driver.get('file://' + filepath_html)
        wait = WebDriverWait(driver, timeout=10)
        map_is_visible = visibility_of_element_located((By.CSS_SELECTOR, '.folium-map'))
        try:
            assert wait.until(map_is_visible)
        except UnexpectedAlertPresentException:
            # in Plugins.ipynb we get an alert about geolocation permission
            # for some reason it cannot be closed or avoided, so just ignore it
            print('skipping', filepath_html, 'because of alert')
            continue
        logs = driver.get_log('browser')
        for log in logs:
            if log['level'] == 'SEVERE':
                msg = ' '.join(log['message'].split()[2:])
                raise RuntimeError('Javascript error: "{}".'.format(msg))


def get_notebook_html(filepath_notebook, execute=True):
    """Store iframes from a notebook in html files, remove them when done."""
    if execute:
        subprocess.run([
            'jupyter', 'nbconvert', '--to', 'notebook', '--execute', filepath_notebook,
        ])
        filepath_notebook = filepath_notebook.replace('.ipynb', '.nbconvert.ipynb')

    html_exporter = nbconvert.HTMLExporter()
    html_exporter.template_file = 'basic'
    body, _ = html_exporter.from_filename(filepath_notebook)

    parser = IframeParser()
    parser.feed(body)
    iframes = parser.iframes

    for i, iframe in enumerate(iframes):
        filepath_html = filepath_notebook.replace('.ipynb', '.{}.html'.format(i))
        filepath_html = os.path.abspath(filepath_html)
        with open(filepath_html, 'wb') as f:
            f.write(iframe)
        try:
            yield filepath_html
        finally:
            os.remove(filepath_html)


class IframeParser(HTMLParser):
    """Extract the iframes from an html page."""

    def __init__(self):
        super().__init__()
        self.iframes = []

    def handle_starttag(self, tag, attrs):
        if tag == 'iframe':
            attrs = dict(attrs)
            if 'data-html' in attrs:
                html_base64 = attrs['data-html']
            else:  # legacy, can be removed when all notebooks have `data-html`.
                src = attrs['src']
                html_base64 = src.split(',')[-1]
            html_bytes = base64.b64decode(html_base64)
            self.iframes.append(html_bytes)
