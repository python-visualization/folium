# -*- coding: utf-8 -*-

"""
Test StoryMap
------------
"""

import folium
from folium.plugins import StoryMap
from folium.utilities import normalize

import pytest


def test_story_map_rendering():
    # Rendering tests
    step_data = [
        ("My First Scene", folium.Marker(name="Marker 1", location=(-34.25, 18.44), popup="This is the 1st marker")),
        ("My Second Scene", folium.Marker(name="Marker 2", location=(-34.18, 18.42), popup="This is the 2nd marker")),
    ]
    m = folium.Map([-34.19, 18.43], max_zoom=12)
    sm = StoryMap(step_data)
    m.add_child(sm)
    m._repr_html_()

    out = normalize(m._parent.render())

    # Verifying that the script import is present.
    script = '<script src="https://svitkin.github.io/leaflet-timeline-slider/dist/leaflet-timeline-slider.min.js"></script>'  # noqa
    assert script in out

    # Verifying that we can render the key bits of the two templates.
    assert StoryMap._template.render(this=sm)
    assert StoryMap._after_children_template.render(this=sm)

    sm.save("/home/gordon/workspace/scratch/map_test.html")


def test_story_map_data():
    # The happy case
    step_data = [
        ("My First Scene", folium.Marker(name="Marker 1", location=(-34.25, 18.44), popup="This is the 1st marker")),
        ("My Second Scene", folium.Marker(name="Marker 2", location=(-34.18, 18.42), popup="This is the 2nd marker")),
    ]
    sm = StoryMap(step_data)
    for label, feature in step_data:
        assert label in sm.story_steps, "Label '{}' is not being passed in!".format(label)
        assert feature is sm.story_steps[label], "Feature '{}' is not being passed in!".format(feature)

    # testing the unhappy case where a non-iterable is passed in
    bad_step_data_1 = 10
    with pytest.raises(AssertionError):
        StoryMap(bad_step_data_1)

    # testing the unhappy case where a non-macro element is passed in
    bad_step_data_2 = [
        ("My First Scene", "This is a marker, I promise"),
        ("My Second Scene", folium.Marker(name="Marker 2", location=(-34.25, 18.44), popup="This is the 2nd marker")),
    ]
    with pytest.raises(AssertionError):
        StoryMap(bad_step_data_2)


def test_story_map_parameter_handling():
    # Testing the blocking of reserved keys
    extra_keywords = {'changeMap': True}
    step_data = []
    with pytest.raises(AssertionError):
        StoryMap(step_data, timeslider_options=extra_keywords)


def test_story_map_no_child_policy():
    step_data = [
        ("My First Scene", folium.Marker(name="Marker 1", location=(-34.25, 18.44), popup="This is the 1st marker")),
        ("My Second Scene", folium.Marker(name="Marker 2", location=(-34.18, 18.42), popup="This is the 2nd marker")),
    ]
    sm = StoryMap(step_data)
    with pytest.raises(RuntimeError):
        sm.add_child(
            folium.Marker(name="Marker 3", location=(-34.28, 18.52), popup="This is the 3rd marker")
        )
