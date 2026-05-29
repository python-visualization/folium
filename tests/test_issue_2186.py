"""
Tests for issue #2186: Add better control for height when browser window
is not maximized.

Validates that:
1. Percentage heights/widths emit vh/vw viewport units instead of %
2. Pixel heights/widths emit min-height/min-width to prevent collapse
3. The dead `#map { position:absolute; ... }` CSS rule is removed
4. All existing size formats (int, px string, % string) still parse correctly

"""


import folium
import re


def _get_map_css(m: folium.Map) -> str:
    """Return the CSS block for the map's own ID selector."""
    html = m.get_root().render()
    match = re.search(r"(#map_[a-f0-9]+ \{.*?\})", html, re.DOTALL)
    assert match, "Could not find map CSS block in rendered HTML"
    return match.group(1)


# ---------------------------------------------------------------------------
# Percentage → viewport units
# ---------------------------------------------------------------------------


class TestPercentageUsesViewportUnits:
    def test_height_100_percent_emits_vh(self):
        """The default height='100%' should use 100vh, not 100%."""
        m = folium.Map(location=[0, 0], height="100%")
        css = _get_map_css(m)
        assert "100.0vh" in css, f"Expected vh unit, got:\n{css}"
        assert (
            "100.0%" not in css.split("position")[1]
        ), "Should not emit bare % for height when using viewport units"

    def test_width_100_percent_emits_vw(self):
        """width='100%' should use 100vw."""
        m = folium.Map(location=[0, 0], width="100%")
        css = _get_map_css(m)
        assert "100.0vw" in css, f"Expected vw unit, got:\n{css}"

    def test_partial_percentage_height(self):
        """height='80%' should emit 80vh."""
        m = folium.Map(location=[0, 0], height="80%", width="60%")
        css = _get_map_css(m)
        assert "80.0vh" in css, f"Expected 80vh, got:\n{css}"
        assert "60.0vw" in css, f"Expected 60vw, got:\n{css}"

    def test_percentage_height_no_min_height(self):
        """Viewport-unit heights don't need min-height (it's implicit via vh)."""
        m = folium.Map(location=[0, 0], height="100%")
        css = _get_map_css(m)
        assert "min-height" not in css


# ---------------------------------------------------------------------------
# Pixel values → min-height / min-width guards
# ---------------------------------------------------------------------------


class TestPixelValuesGetMinConstraints:
    def test_pixel_string_height_gets_min_height(self):
        """height='1000px' should also emit min-height: 1000px."""
        m = folium.Map(location=[0, 0], height="1000px")
        css = _get_map_css(m)
        assert "height: 1000.0px" in css
        assert "min-height: 1000.0px" in css, f"min-height missing:\n{css}"

    def test_integer_height_gets_min_height(self):
        """height=500 (integer) should emit min-height: 500px."""
        m = folium.Map(location=[0, 0], height=500, width=750)
        css = _get_map_css(m)
        assert "min-height: 500.0px" in css, f"min-height missing:\n{css}"
        assert "min-width: 750.0px" in css, f"min-width missing:\n{css}"

    def test_pixel_string_width_gets_min_width(self):
        """width='400px' should emit min-width: 400px."""
        m = folium.Map(location=[0, 0], width="400px")
        css = _get_map_css(m)
        assert "min-width: 400.0px" in css, f"min-width missing:\n{css}"


# ---------------------------------------------------------------------------
# Dead CSS rule removal
# ---------------------------------------------------------------------------


class TestDeadMapRuleRemoved:
    def test_dead_map_id_rule_absent(self):
        """The stale `#map { position:absolute; ... }` block must not appear."""
        m = folium.Map(location=[0, 0])
        html = m.get_root().render()
        # The old rule targeted the literal id="map" which never matched the
        # hashed IDs folium actually generates.
        assert (
            "<style>#map {" not in html
        ), "Dead `#map { position:absolute; }` CSS rule should have been removed"


# ---------------------------------------------------------------------------
# Backwards-compatibility: all existing call signatures still work
# ---------------------------------------------------------------------------


class TestBackwardsCompatibility:
    def test_default_call(self):
        """folium.Map() with no size args still renders."""
        m = folium.Map(location=[0, 0])
        assert m.get_root().render()

    def test_integer_sizes(self):
        m = folium.Map(location=[0, 0], width=750, height=500)
        css = _get_map_css(m)
        assert "750.0px" in css
        assert "500.0px" in css

    def test_px_string_sizes(self):
        m = folium.Map(location=[0, 0], width="800px", height="600px")
        css = _get_map_css(m)
        assert "800.0px" in css
        assert "600.0px" in css

    def test_percent_string_sizes_parse(self):
        """Percentage strings are accepted without raising."""
        m = folium.Map(location=[0, 0], width="90%", height="75%")
        css = _get_map_css(m)
        assert "90.0vw" in css
        assert "75.0vh" in css

    def test_flags_set_correctly(self):
        m_pct = folium.Map(location=[0, 0], height="100%", width="100%")
        assert m_pct._height_is_percent is True
        assert m_pct._width_is_percent is True

        m_px = folium.Map(location=[0, 0], height=500, width=750)
        assert m_px._height_is_percent is False
        assert m_px._width_is_percent is False
