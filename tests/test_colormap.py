# -*- coding: utf-8 -*-

""""
Folium Colormap Module
----------------------

"""

from __future__ import (absolute_import, division, print_function)

import folium.colormap as cm


def test_simple_step():
    step = cm.StepColormap(['green', 'yellow', 'red'],
                           vmin=3., vmax=10.,
                           index=[3, 4, 8, 10], caption='step')
    step = cm.StepColormap(['r', 'y', 'g', 'c', 'b', 'm'])
    step._repr_html_()


def test_simple_linear():
    linear = cm.LinearColormap(['green', 'yellow', 'red'], vmin=3., vmax=10.)
    linear = cm.LinearColormap(['red', 'orange', 'yellow', 'green'],
                               index=[0, 0.1, 0.9, 1.])
    linear._repr_html_()


def test_linear_to_step():
    some_list = [30.6, 50, 51, 52, 53, 54, 55, 60, 70, 100]
    lc = cm.linear.YlOrRd
    lc.to_step(n=12)
    lc.to_step(index=[0, 2, 4, 6, 8, 10])
    lc.to_step(data=some_list, n=12)
    lc.to_step(data=some_list, n=12, method='linear')
    lc.to_step(data=some_list, n=12, method='log')
    lc.to_step(data=some_list, n=30, method='quantiles')
    lc.to_step(data=some_list, quantiles=[0, 0.3, 0.7, 1])
    lc.to_step(data=some_list, quantiles=[0, 0.3, 0.7, 1], round_method='int')
    lc.to_step(data=some_list, quantiles=[0, 0.3, 0.7, 1],
               round_method='log10')


def test_step_to_linear():
    step = cm.StepColormap(['green', 'yellow', 'red'],
                           vmin=3., vmax=10.,
                           index=[3, 4, 8, 10], caption='step')
    step.to_linear()


def test_linear_object():
    cm.linear.OrRd._repr_html_()
    cm.linear.PuBu.to_step(12)
    cm.linear.YlGn.scale(3, 12)
    cm.linear._repr_html_()
