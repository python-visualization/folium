import glob
import os
import subprocess
from contextlib import contextmanager

import nbconvert
from parameterized import parameterized
from seleniumbase import BaseCase
from selenium.webdriver import Chrome, ChromeOptions


def test_selenium_chrome():
    options = ChromeOptions()
    # print(subprocess.run(['which', 'google-chrome'], capture_output=True))
    # print(subprocess.run(['which', 'chromium-browser'], capture_output=True))
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    driver = Chrome(options=options)
    driver.get("http://www.python.org")
    assert "Python" in driver.title


def find_notebooks():
    """Return a list of filenames of the example notebooks."""
    path = os.path.dirname(__file__)
    search_patterns = [
        os.path.join(path, '..', '..', 'examples', '*.ipynb'),
    ]
    for pattern in search_patterns:
        files = glob.glob(pattern)
        if files:
            return files[:3]
    else:
        raise IOError('Could not find the notebooks')


class TestNotebooks(BaseCase):

    @parameterized.expand(find_notebooks())
    def test_notebook(self, filepath):
        with get_notebook_html(filepath) as filepath_html:
            self.open('file://' + filepath_html)
            self.assert_element('iframe')
            iframes = self.find_elements('iframe')
            print('Checking', len(iframes), 'iframes')
            for iframe in iframes:
                self.switch_to_frame(iframe)
                self.assert_element('.folium-map')
                self.switch_to_default_content()
            # logs don't work in firefox, use chrome
            print('Checking JS logs')
            logs = self.driver.get_log("browser")
            for log in logs:
                if log['level'] == 'SEVERE':
                    msg = ' '.join(log['message'].split()[2:])
                    raise RuntimeError('Javascript error: "{}".'.format(msg))


@contextmanager
def get_notebook_html(filepath_notebook, run=False):
    if run:
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute',
                        '--inplace', filepath_notebook])
    html_exporter = nbconvert.HTMLExporter()
    html_exporter.template_file = 'basic'
    body, _ = html_exporter.from_filename(filepath_notebook)
    html = ('<!DOCTYPE html><html><head><meta charset="UTF-8"></head>'
            '<body>{}</body></html>').format(body)
    filepath_html = filepath_notebook.replace('.ipynb', '.html')
    filepath_html = os.path.abspath(filepath_html)
    with open(filepath_html, 'w', encoding="utf-8") as f:
        f.write(html)
    print('Created file', filepath_html)
    try:
        yield filepath_html
    finally:
        os.remove(filepath_html)
