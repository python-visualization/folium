""""
Folium _repr_*_ Tests
---------------------

"""

import io

import PIL.Image
import pytest

import folium


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
    parts = html.split("><")
    assert len(parts) == 7
    assert parts[0].lstrip("<div ") == 'style="width:100%;"'
    assert (
        parts[1].lstrip("<div ")
        == 'style="position:relative;width:100%;height:0;padding-bottom:60%;"'
    )  # noqa
    assert "make this notebook trusted" in parts[2].lower()
    assert parts[3].startswith("iframe")
    assert parts[4] == "/iframe"
    assert parts[5] == "/div"
    assert parts[6] == "/div>"


def test__repr_png_no_image(m):
    png = m._repr_png_()
    assert png is None


def test__repr_png_is_bytes(m_png):
    png = m_png._repr_png_()
    assert isinstance(png, bytes)


def test_valid_png(m_png):
    png = m_png._repr_png_()
    img = PIL.Image.open(io.BytesIO(png))
    assert isinstance(img, PIL.PngImagePlugin.PngImageFile)


def test_valid_png_size(m_png):
    from folium.utilities import _parse_size

    w = h = 500
    m_png.width = _parse_size(w)
    m_png.height = _parse_size(h)
    png = m_png._repr_png_()
    img = PIL.Image.open(io.BytesIO(png))
    assert img.size == (w, h)
