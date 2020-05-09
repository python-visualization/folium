
import base64
import glob
from html.parser import HTMLParser
import os
import subprocess

import nbconvert
from parameterized import parameterized
from seleniumbase import BaseCase


def find_notebooks():
    """Return a list of filenames of the example notebooks."""
    path = os.path.dirname(__file__)
    pattern = os.path.join(path, '..', '..', 'examples', '*.ipynb')
    files = glob.glob(pattern)
    if files:
        return files
    else:
        raise IOError('Could not find the notebooks')


class TestNotebooks(BaseCase):

    @parameterized.expand(find_notebooks())
    def test_notebook(self, filepath):
        for filepath_html in get_notebook_html(filepath):
            self.open('file://' + filepath_html)
            self.assert_element('.folium-map')
            # logs don't work in firefox, use chrome
            self.assert_no_js_errors()


def get_notebook_html(filepath_notebook, execute=True):
    """Store iframes from a notebook in html files, remove them when done.

    If run is True the notebook will first be executed.

    """
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
