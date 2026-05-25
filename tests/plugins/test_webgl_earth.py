import pytest

import folium
from folium.plugins.webgl_earth import (
    WebGLEarth,
    WebGLEarthMarker,
    WebGLEarthRealtime,
    WebGLEarthTileLayer,
)
from folium.utilities import JsCode

# ─────────────────────────── WebGLEarth ───────────────────────────


class TestWebGLEarth:
    def test_default(self):
        globe = WebGLEarth()
        assert globe._name == "WebGLEarth"
        assert list(globe.center) == [20, 0]
        assert globe.zoom == 2.5
        assert globe.height == 600

    def test_custom_params(self):
        globe = WebGLEarth(
            center=[48.2, 16.4],
            zoom=5,
            height=400,
            atmosphere=False,
        )
        assert list(globe.center) == [48.2, 16.4]
        assert globe.zoom == 5
        assert globe.height == 400
        assert globe.options["atmosphere"] is False

    def test_custom_tile_url(self):
        url = "https://tiles.example.com/{z}/{x}/{y}.png"
        globe = WebGLEarth(tile_url=url)
        assert globe.tile_url == url

    def test_tile_subdomains(self):
        globe = WebGLEarth(tile_subdomains="1234")
        assert globe.tile_subdomains == ["1", "2", "3", "4"]

    def test_invalid_center(self):
        with pytest.raises(Exception):
            WebGLEarth(center=[999, 999])

    def test_add_to_map(self):
        m = folium.Map()
        globe = WebGLEarth()
        globe.add_to(m)
        html = m._repr_html_()
        assert "webglearth" in html.lower() or "WE.map" in html

    def test_renders_js_dependency(self):
        m = folium.Map()
        globe = WebGLEarth()
        globe.add_to(m)
        html = m._repr_html_()
        assert "webglearth.com/v2/api.js" in html

    def test_container_id_unique(self):
        g1 = WebGLEarth()
        g2 = WebGLEarth()
        assert g1.container_id != g2.container_id

    def test_renders_reset_button(self):
        m = folium.Map()
        globe = WebGLEarth()
        globe.add_to(m)
        html = m._repr_html_()
        assert "Reset View" in html


# ─────────────────────────── WebGLEarthMarker ────────────────────


class TestWebGLEarthMarker:
    def test_default(self):
        marker = WebGLEarthMarker(location=[48.2, 16.4])
        assert marker._name == "WebGLEarthMarker"
        assert list(marker.location) == [48.2, 16.4]
        assert marker.popup is None

    def test_with_popup(self):
        marker = WebGLEarthMarker(location=[48.2, 16.4], popup="Vienna")
        assert marker.popup == "Vienna"

    def test_invalid_location(self):
        with pytest.raises(Exception):
            WebGLEarthMarker(location=[999, 999])

    def test_renders_on_globe(self):
        m = folium.Map()
        globe = WebGLEarth()
        globe.add_to(m)
        WebGLEarthMarker(location=[48.2, 16.4], popup="Test").add_to(globe)
        html = m._repr_html_()
        assert "WE.marker" in html
        assert "Test" in html

    def test_marker_references_parent(self):
        m = folium.Map()
        globe = WebGLEarth()
        globe.add_to(m)
        marker = WebGLEarthMarker(location=[0, 0])
        marker.add_to(globe)
        html = m._repr_html_()
        assert f".addTo({globe.get_name()})" in html


# ─────────────────────────── WebGLEarthTileLayer ─────────────────


class TestWebGLEarthTileLayer:
    def test_default(self):
        tiles = WebGLEarthTileLayer(url="https://example.com/{z}/{x}/{y}.png")
        assert tiles._name == "WebGLEarthTileLayer"
        assert tiles.url == "https://example.com/{z}/{x}/{y}.png"

    def test_with_options(self):
        tiles = WebGLEarthTileLayer(
            url="https://example.com/{z}/{x}/{y}.png",
            attribution="Test",
            opacity=0.5,
        )
        assert tiles.options["attribution"] == "Test"
        assert tiles.options["opacity"] == 0.5

    def test_renders_on_globe(self):
        m = folium.Map()
        globe = WebGLEarth()
        globe.add_to(m)
        WebGLEarthTileLayer(url="https://example.com/{z}/{x}/{y}.png").add_to(globe)
        html = m._repr_html_()
        assert "WE.tileLayer" in html
        assert "example.com" in html


# ─────────────────────────── WebGLEarthRealtime ──────────────────


class TestWebGLEarthRealtime:
    def _make_callback(self):
        return JsCode("""
            function(data, earth) {
                WE.marker([data.lat, data.lng]).addTo(earth);
            }
            """)

    def test_default(self):
        rt = WebGLEarthRealtime(
            source_url="https://api.example.com/data",
            on_update=self._make_callback(),
        )
        assert rt._name == "WebGLEarthRealtime"
        assert rt.source_url == "https://api.example.com/data"
        assert rt.interval == 5000

    def test_custom_interval(self):
        rt = WebGLEarthRealtime(
            source_url="https://api.example.com/data",
            interval=2000,
            on_update=self._make_callback(),
        )
        assert rt.interval == 2000

    def test_requires_on_update(self):
        with pytest.raises(ValueError, match="on_update is required"):
            WebGLEarthRealtime(source_url="https://api.example.com/data")

    def test_accepts_string_callback(self):
        rt = WebGLEarthRealtime(
            source_url="https://api.example.com/data",
            on_update="function(data, earth) {}",
        )
        assert isinstance(rt.on_update, JsCode)

    def test_renders_on_globe(self):
        m = folium.Map()
        globe = WebGLEarth()
        globe.add_to(m)
        WebGLEarthRealtime(
            source_url="https://api.example.com/data",
            interval=3000,
            on_update=self._make_callback(),
        ).add_to(globe)
        html = m._repr_html_()
        assert "api.example.com/data" in html
        assert "setInterval" in html

    def test_renders_fetch_call(self):
        m = folium.Map()
        globe = WebGLEarth()
        globe.add_to(m)
        WebGLEarthRealtime(
            source_url="https://api.example.com/data",
            on_update=self._make_callback(),
        ).add_to(globe)
        html = m._repr_html_()
        assert "fetch(" in html


# ─────────────────────────── Integration ─────────────────────────


class TestIntegration:
    def test_full_setup(self):
        """Full globe with markers, tiles, and realtime — must render."""
        m = folium.Map()
        globe = WebGLEarth(center=[0, 0], zoom=2)
        globe.add_to(m)

        WebGLEarthMarker(location=[48.8, 2.3], popup="Paris").add_to(globe)
        WebGLEarthMarker(location=[35.7, 139.7], popup="Tokyo").add_to(globe)

        WebGLEarthTileLayer(
            url="https://tiles.example.com/{z}/{x}/{y}.png",
            opacity=0.5,
        ).add_to(globe)

        WebGLEarthRealtime(
            source_url="https://api.example.com/live",
            interval=5000,
            on_update=JsCode("function(d, e) {}"),
        ).add_to(globe)

        html = m._repr_html_()
        assert "WE.map" in html
        assert "WE.marker" in html
        assert "WE.tileLayer" in html
        assert "setInterval" in html
        assert "Paris" in html
        assert "Tokyo" in html

    def test_save_html(self, tmp_path):
        """Must produce a valid HTML file."""
        m = folium.Map()
        globe = WebGLEarth()
        globe.add_to(m)
        WebGLEarthMarker(location=[0, 0], popup="Origin").add_to(globe)

        path = tmp_path / "globe.html"
        m.save(str(path))
        content = path.read_text()
        assert "<!DOCTYPE html>" in content
        assert "WE.map" in content
        assert "Origin" in content
