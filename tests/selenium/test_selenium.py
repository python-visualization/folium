
import base64
import glob
from html.parser import HTMLParser
import os
import subprocess

import nbconvert
import pytest
from selenium.common.exceptions import UnexpectedAlertPresentException

from folium.utilities import temp_html_filepath


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
        driver.get_file(filepath_html)
        try:
            assert driver.wait_until('.folium-map')
        except UnexpectedAlertPresentException:
            # in Plugins.ipynb we get an alert about geolocation permission
            # for some reason it cannot be closed or avoided, so just ignore it
            print('skipping', filepath_html, 'because of alert')
            continue
        driver.verify_js_logs()


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

    for iframe in iframes:
        with temp_html_filepath(iframe) as filepath_html:
            yield filepath_html


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
