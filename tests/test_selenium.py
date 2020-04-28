import glob
import os
import subprocess
from contextlib import contextmanager

import nbconvert
from parameterized import parameterized

from selenium.webdriver import Chrome, ChromeOptions


def test_selenium_chrome():
    options = ChromeOptions()
    print(subprocess.run(['which', 'google-chrome']))
    print(subprocess.run(['which', 'chromium-browser']))
    options.add_argumetn('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')  # overcome limited resource problems
    options.add_argument('--no-sandbox')  # Bypass OS security model
    driver = Chrome(options=options)
    driver.get("http://www.python.org")
    assert "Python" in driver.title


# from seleniumbase import BaseCase
# class TestNotebooks(BaseCase):
#
#     @parameterized.expand(glob.glob('examples/*.ipynb'))
#     def test_notebook(self, filepath):
#         with get_notebook_html(filepath) as filepath_html:
#             self.open('file://' + filepath_html)
#             self.assert_element('iframe')
#             iframes = self.find_elements('iframe')
#             for iframe in iframes:
#                 self.switch_to_frame(iframe)
#                 self.assert_element('.folium-map')
#                 self.switch_to_default_content()
#             # logs don't work in firefox, use chrome
#             logs = self.driver.get_log("browser")
#             for log in logs:
#                 if log['level'] == 'SEVERE':
#                     msg = ' '.join(log['message'].split()[2:])
#                     raise RuntimeError('Javascript error: "{}".'.format(msg))


@contextmanager
def get_notebook_html(filepath_notebook, run=True):
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
    try:
        yield filepath_html
    finally:
        os.remove(filepath_html)
