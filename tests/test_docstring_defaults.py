"""
Check that documented defaults match the signature defaults.

Several classes override a default inherited from ``Layer`` or from a sibling
class but keep the parameter description they were copied from, so the
docstring ends up stating the old default.  Scoped to the boolean flags whose
documented value is a plain ``True``/``False`` literal, which is what makes the
comparison unambiguous.
"""

import inspect
import pkgutil
import re
from importlib import import_module

import pytest

import folium

FLAGS = ("overlay", "control", "show", "localize")


def _classes():
    modules = [folium]
    for mod in pkgutil.walk_packages(folium.__path__, folium.__name__ + "."):
        try:
            modules.append(import_module(mod.name))
        except ImportError:  # optional dependency
            continue
    seen = set()
    for module in modules:
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__.startswith("folium.") and obj not in seen:
                seen.add(obj)
                yield obj


def _documented_default(obj, flag):
    for source in (obj.__init__.__doc__, obj.__doc__):
        if not source:
            continue
        match = re.search(
            rf"^\s*{flag}\s*:[^\n]*default[ =:]+(True|False)\b",
            source,
            re.MULTILINE,
        )
        if match:
            return match.group(1) == "True"
    return None


@pytest.mark.parametrize("cls", sorted(_classes(), key=lambda c: c.__qualname__))
def test_documented_boolean_defaults_match_signature(cls):
    try:
        signature = inspect.signature(cls.__init__)
    except (TypeError, ValueError):
        pytest.skip("no introspectable signature")
    for flag in FLAGS:
        parameter = signature.parameters.get(flag)
        if parameter is None or not isinstance(parameter.default, bool):
            continue
        documented = _documented_default(cls, flag)
        if documented is None:
            continue
        assert documented == parameter.default, (
            f"{cls.__qualname__}.{flag} is documented as default "
            f"{documented} but defaults to {parameter.default}"
        )


def test_the_check_can_actually_fail():
    """Guard against the check passing because it never reads anything."""

    class Example:
        """
        Parameters
        ----------
        overlay : bool, default False
            Doc and signature disagree on purpose.
        """

        def __init__(self, overlay: bool = True):
            pass

    assert _documented_default(Example, "overlay") is False
    assert inspect.signature(Example.__init__).parameters["overlay"].default is True
