"""Verify behavior of Jinja2's `tojson` template filter"""

import jinja2
import pytest


@pytest.mark.parametrize(
    "obj, expected",
    [
        (True, "true"),
        (1, "1"),
        (3.14, "3.14"),
        ("hi", '"hi"'),
        (
            '<div style="something">content</div>',
            '"\\u003cdiv style=\\"something\\"\\u003econtent\\u003c/div\\u003e"',
        ),
        ("Mus\u00e9e d'Orsay", '"Mus\\u00e9e d\\u0027Orsay"'),
        ([1, 2, 3], "[1, 2, 3]"),
        ([1, "hi", False], '[1, "hi", false]'),
        ([[0, 0], [1, 1]], "[[0, 0], [1, 1]]"),
        ([(0, 0), (1, 1)], "[[0, 0], [1, 1]]"),
        ({"hi": "there"}, '{"hi": "there"}'),
        ({"hi": {"there": 1, "what": "up"}}, '{"hi": {"there": 1, "what": "up"}}'),
    ],
)
def test_jinja2_tojson(obj, expected):
    res = jinja2.Template("{{ obj|tojson }}").render(obj=obj)
    assert res == expected


@pytest.mark.parametrize(
    "obj, expected",
    [
        (
            {
                "hi": "there",
                "what": "isup",
            },
            '{\n  "hi": "there",\n  "what": "isup"\n}',
        ),
        (
            [(0, 0), (1, 1)],
            "[\n  [\n    0,\n    0\n  ],\n  [\n    1,\n    1\n  ]\n]",
        ),
    ],
)
def test_jinja2_tojson_indented(obj, expected):
    res = jinja2.Template("{{ obj|tojson(2) }}").render(obj=obj)
    assert res == expected
