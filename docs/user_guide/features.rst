Features
--------------------------

.. toctree::
  :maxdepth: 1

  features/fit_overlays
  features/click_related_classes

Text Elements
=============

Folium supports several ways to display text on maps.

**1. DivIcon Labels**
To add always-visible text labels on the map:

.. code-block:: python

    from folium import Map, Marker, DivIcon

    m = Map(location=[40.7128, -74.0060], zoom_start=13)
    Marker(
        location=[40.7128, -74.0060],
        icon=DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html='<div style="font-size: 12pt; color : black">Hello World!</div>',
        )
    ).add_to(m)
    m.save("map.html")

**2. Tooltip and Popup Text**

Use tooltips for hover text or popups for clickable text.
