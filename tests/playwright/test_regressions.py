from __future__ import annotations

import os
import shutil
from contextlib import contextmanager
from time import sleep

import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
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
    # page.goto(f"localhost:{PORT}")
    page.set_viewport_size({"width": 1200, "height": 800})
    expect.set_options(timeout=5_000)


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
                "tests/playwright/regressions/main.py",
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


paths = os.listdir("tests/playwright/regressions/pages")
paths = [p.replace(".py", "") for p in paths]


@pytest.mark.parametrize("path", paths)
def test_screenshot(page: Page, path: str):
    page.goto(f"localhost:{PORT}/{path}")

    # set the viewport to be big enough for the full screenshot
    # otherwise there will be differences between headed and headless
    # mode
    sleep(3)
    page.locator('[data-testid="stCustomComponentV1"]').screenshot(
        path=f"/tmp/screenshot_new_{path}.png",
    )

    img_a = Image.open(f"/tmp/screenshot_new_{path}.png")

    if os.path.exists(f"tests/playwright/screenshots/screenshot_{path}.png"):
        img_b = Image.open(f"tests/playwright/screenshots/screenshot_{path}.png")

        img_diff = Image.new("RGBA", img_a.size)
        # note how there is no need to specify dimensions
        mismatch = pixelmatch(img_a, img_b, img_diff, threshold=0.2, includeAA=False)

        img_diff.save(f"/tmp/screenshot_diff_{path}.png")
        assert mismatch < 50

    else:
        shutil.copy(
            f"/tmp/screenshot_new_{path}.png",
            f"tests/playwright/screenshots/screenshot_{path}.png",
        )
        raise Exception("no screenshot available, generating new")
