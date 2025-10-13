Text Elements
=============

Folium allows you to add text to your maps in several ways, beyond the standard
marker popups and tooltips. This section covers the most common approaches.

Adding Text with DivIcon
------------------------

The simplest way to display static text on a map is by using a `DivIcon`.
A `DivIcon` creates a marker that shows HTML content directly on the map.

Example:

.. code-block:: python

    import folium
    from folium.features import DivIcon

    m = folium.Map(location=[40, -100], zoom_start=4)

    folium.Marker(
        location=[40, -100],
        icon=DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html='<div style="font-size: 16pt; color: red;">Hello Map!</div>',
        )
    ).add_to(m)

    m

Other Approaches
----------------

- **Leaflet text layers**: You can directly use the underlying Leaflet `L.divIcon` or
  `L.tooltip` via Folium's `CustomPane` or plugins.
- **Branca HTML templates**: For more advanced formatting, you can inject HTML
  elements into your map using Branca's `Element` class.

Tips
----

- DivIcon text is always visible, unlike tooltips or popups.
- Use HTML/CSS for styling text size, color, and position.
