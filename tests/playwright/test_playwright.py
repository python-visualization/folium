from __future__ import annotations

from contextlib import contextmanager
from time import sleep

import pytest
from playwright.sync_api import Page, expect

LOCAL_TEST = False

PORT = "8503" if LOCAL_TEST else "8699"


@pytest.fixture(scope="module", autouse=True)
def _before_module():
    # Run the streamlit app before each module
    with run_streamlit():
        yield


@pytest.fixture(autouse=True)
def _before_test(page: Page):
    page.goto(f"localhost:{PORT}")
    page.set_viewport_size({"width": 2000, "height": 2000})
    expect.set_options(timeout=5_000)


# Take screenshot of each page if there are failures for this session
@pytest.fixture(autouse=True)
def _after_test(page: Page, request):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"screenshot-{request.node.name}.png", full_page=True)


@contextmanager
def run_streamlit():
    """Run the streamlit app at examples/streamlit_app.py on port 8599"""
    import subprocess

    if LOCAL_TEST:
        try:
            yield 1
        finally:
            pass
    else:
        p = subprocess.Popen(
            [
                "streamlit",
                "run",
                "examples/streamlit/main.py",
                "--server.port",
                PORT,
                "--server.headless",
                "true",
            ]
        )

        sleep(5)

        try:
            yield 1
        finally:
            p.kill()


def click_button_or_marker(page: Page, nth: int = 0, locator: str | None = None):
    """For some reason, there's a discrepancy between how the map markers are
    selectable locally and on github actions, perhaps related some error in loading
    the actual marker images. This tries both ways to select a marker"""

    frame = page.frame_locator('iframe[title="streamlit_folium\\.st_folium"]')
    if locator is not None:
        frame = frame.locator(locator)
    try:
        frame.get_by_role("button", name="Marker").nth(nth).click(timeout=5_000)
    except Exception:
        frame.get_by_role("img").nth(nth).click(timeout=5_000)


def test_draw(page: Page):
    # Test draw support
    page.get_by_role("link", name="draw feature group").click()

    # This is the marker that was drawn beforehand
    expect(
        page.locator('[data-testid="stCustomComponentV1"]').content_frame.get_by_role(
            "button", name="Marker"
        )
    ).to_be_visible()

    # Start drawing a rectangle
    page.locator('[data-testid="stCustomComponentV1"]').content_frame.get_by_role(
        "link", name="Draw a rectangle"
    ).click()

    # I could not record this
    # so some trickery to get the mouse movements correct
    bbox = page.locator('[data-testid="stCustomComponentV1"]').bounding_box()

    # One of the few times I miss javascript
    x = bbox["x"]
    y = bbox["y"]
    width = bbox["width"]
    height = bbox["height"]

    # careful, my first click attempt triggered the zoom button
    page.mouse.click(x + 100, y + 100)
    page.mouse.click(x + width - 100, y + height - 100)

    # Now check if streamlit shows a Polygon result
    expect(page.get_by_text('"Polygon"').first).to_be_visible()
