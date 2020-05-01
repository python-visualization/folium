
import base64
import glob
from html.parser import HTMLParser
import os
import subprocess

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
        for filepath_html in get_notebook_html(filepath):
            self.open('file://' + filepath_html)
            self.assert_element('.folium-map')
            # logs don't work in firefox, use chrome
            print('Checking JS logs')
            logs = self.driver.get_log("browser")
            for log in logs:
                if log['level'] == 'SEVERE':
                    msg = ' '.join(log['message'].split()[2:])
                    raise RuntimeError('Javascript error: "{}".'.format(msg))


def get_notebook_html(filepath_notebook, run=False):
    if run:
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute',
                        '--inplace', filepath_notebook])
    html_exporter = nbconvert.HTMLExporter()
    html_exporter.template_file = 'basic'
    body, _ = html_exporter.from_filename(filepath_notebook)

    parser = IframeParser()
    parser.feed(body)
    iframes = parser.iframes

    for i, iframe in enumerate(iframes):
        filepath_html = filepath_notebook.replace('.ipynb', '_{}.html'.format(i))
        filepath_html = os.path.abspath(filepath_html)
        with open(filepath_html, 'wb') as f:
            f.write(iframe)
        print('Created file', filepath_html)
        try:
            yield filepath_html
        finally:
            os.remove(filepath_html)


class IframeParser(HTMLParser):

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
