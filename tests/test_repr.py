# -*- coding: utf-8 -*-

""""
Folium _repr_*_ Tests
---------------------

"""

from __future__ import (absolute_import, division, print_function)

import io

import PIL.Image

import folium

import pytest


@pytest.fixture
def make_map(png_enabled=False):
    m = folium.Map(png_enabled=png_enabled)
    return m


def test__repr_html_is_str():
    html = make_map()._repr_html_()
    assert isinstance(html, str)


def test_valid_html():
    html = make_map()._repr_html_()
    parts = html.split('><')
    assert len(parts) == 6
    assert parts[0].lstrip('<div ') == 'style="width:100%;"'
    assert parts[1].lstrip('<div ') == 'style="position:relative;width:100%;height:0;padding-bottom:60%;"'  # noqa
    assert parts[2].startswith('iframe')
    assert parts[3] == '/iframe'
    assert parts[4] == '/div'
    assert parts[5] == '/div>'


def test__repr_png_no_image():
    png = make_map(png_enabled=False)._repr_png_()
    assert png is None


def test__repr_png_is_bytes():
    png = make_map(png_enabled=True)._repr_png_()
    assert isinstance(png, bytes)


def test_valid_png():
    png = make_map(png_enabled=True)._repr_png_()
    img = PIL.Image.open(io.BytesIO(png))
    isinstance(img, PIL.PngImagePlugin.PngImageFile)
