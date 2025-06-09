import importlib
import io
import os
import shutil

import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from selenium import webdriver

options = webdriver.chrome.options.Options()
options.add_argument("--headless")


paths = os.listdir("tests/snapshots/modules")
paths = [p.replace(".py", "") for p in paths if p.endswith(".py")]


@pytest.mark.parametrize("path", paths)
def test_screenshot(path: str):
    driver = webdriver.Chrome(options=options)
    m = importlib.import_module(f"tests.snapshots.modules.{path}").m
    img_data = m._to_png(3, driver=driver, size=(800, 800))
    img_a = Image.open(io.BytesIO(img_data))
    img_a.save(f"/tmp/screenshot_new_{path}.png")

    if os.path.exists(f"tests/snapshots/screenshots/screenshot_{path}.png"):
        img_b = Image.open(f"tests/snapshots/screenshots/screenshot_{path}.png")

        img_diff = Image.new("RGBA", img_a.size)
        # note how there is no need to specify dimensions
        mismatch = pixelmatch(img_a, img_b, img_diff, threshold=0.2, includeAA=False)

        img_diff.save(f"/tmp/screenshot_diff_{path}.png")
        m.save(f"/tmp/folium_map_{path}.html")
        assert mismatch < 200

    else:  # pragma: no cover
        shutil.copy(
            f"/tmp/screenshot_new_{path}.png",
            f"tests/snapshots/screenshots/screenshot_{path}.png",
        )
        raise Exception("no screenshot available, generating new")
