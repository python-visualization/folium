# -*- coding: utf-8 -*-

"""
Test TagFilterButton
------------
"""

import folium
from folium import plugins
from folium.utilities import normalize

from jinja2 import Template

import random

import numpy as np


def test_tag_filter_button():
    np.random.seed(3141592)

    # Generate base data
    initial_data = (np.random.normal(size=(100, 2)) * np.array([[1, 1]]) +
                    np.array([[48, 5]]))
    # Generate the data to segment by (levels of another categorical pandas column in practical usage)
    n = 5
    categories = ['category{}'.format(i+1) for i in range(n)]
    category_column = [random.choice(categories)
                       for i in range(len(initial_data))]
    # Create map and add the data with additional parameter tags as the segmentation
    m = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)
    for i, latlng in enumerate(initial_data):
        category = category_column[i]
        folium.Marker(
            tuple(latlng),
            tags=[category]
        ).add_to(m)

    hm = plugins.TagFilterButton(categories).add_to(m)
    out = normalize(m._parent.render())

    # We verify that the script imports are present.
    script = '<script src="https://cdn.jsdelivr.net/npm/leaflet-tag-filter-button/src/leaflet-tag-filter-button.js"></script>'  # noqa
    assert script in out
    script = '<script src="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.js"></script>'  # noqa
    assert script in out
    script = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet-tag-filter-button/src/leaflet-tag-filter-button.css"/>'  # noqa
    assert script in out
    script = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.css"/>'  # noqa
    assert script in out
    script = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/css-ripple-effect@1.0.5/dist/ripple.min.css"/>'  # noqa
    assert script in out

    # We verify that the script part is correct.
    tmpl = Template("""
            var {{this.get_name()}} = L.control.tagFilterButton(
                {
                    data: {{this.options.data}},
                    icon: "{{this.options.icon}}",
                    clearText: {{this.options.clear_text}},
                    filterOnEveryClick: {{this.options.filter_on_every_click}},
                    openPopupOnHover: {{this.options.open_popup_on_hover}}
                    })
                .addTo({{this._parent.get_name()}});
    """)
    assert normalize(tmpl.render(this=hm))
