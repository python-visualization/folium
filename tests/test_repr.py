# -*- coding: utf-8 -*-

""""
Folium _repr_*_ Tests
---------------------

"""

import io
import sys

import PIL.Image

import folium

import pytest


@pytest.fixture
def m():
    yield folium.Map(png_enabled=False)


@pytest.fixture
def m_png():
    yield folium.Map(png_enabled=True)


def test__repr_html_is_str(m):
    html = m._repr_html_()
    assert isinstance(html, str)


def test_valid_html(m):
    html = m._repr_html_()
    parts = html.split('><')
    assert len(parts) == 6
    assert parts[0].lstrip('<div ') == 'style="width:100%;"'
    assert parts[1].lstrip('<div ') == 'style="position:relative;width:100%;height:0;padding-bottom:60%;"'  # noqa
    assert parts[2].startswith('iframe')
    assert parts[3] == '/iframe'
    assert parts[4] == '/div'
    assert parts[5] == '/div>'


def test__repr_png_no_image(m):
    png = m._repr_png_()
    assert png is None


def test__repr_png_is_bytes(m_png):
    png = m_png._repr_png_()
    assert isinstance(png, bytes)


@pytest.mark.skipif(sys.version_info < (3, 0),
                    reason="Doesn't work on Python 2.7.")
def test_valid_png(m_png):
    png = m_png._repr_png_()
    img = PIL.Image.open(io.BytesIO(png))
    isinstance(img, PIL.PngImagePlugin.PngImageFile)
