from folium.elements import JSCSSMixin
from folium.map import Layer

from jinja2 import Template


class FeatureGroupSubGroup(JSCSSMixin, Layer):
    """
    Creates a Feature Group that adds its child layers into a parent group when
    added to a map (e.g. through LayerControl). Useful to create nested groups,
    or cluster markers from multiple overlays. From [0].

    [0] https://github.com/ghybs/Leaflet.FeatureGroup.SubGroup

    Parameters
    ----------
    group : Layer
        The MarkerCluster or FeatureGroup containing this subgroup.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).

    Examples
    -------

    Nested groups
    =============
    >>> fg = folium.FeatureGroup()                          # Main group
    >>> g1 = folium.plugins.FeatureGroupSubGroup(fg, 'g1')  # First subgroup of fg
    >>> g2 = folium.plugins.FeatureGroupSubGroup(fg, 'g2')  # Second subgroup of fg
    >>> m.add_child(fg)
    >>> m.add_child(g1)
    >>> m.add_child(g2)
    >>> g1.add_child(folium.Marker([0,0]))
    >>> g2.add_child(folium.Marker([0,1]))
    >>> folium.LayerControl().add_to(m)

    Multiple overlays part of the same cluster group
    =====================================================
    >>> mcg = folium.plugins.MarkerCluster(control=False)   # Marker Cluster, hidden in controls
    >>> g1 = folium.plugins.FeatureGroupSubGroup(mcg, 'g1') # First group, in mcg
    >>> g2 = folium.plugins.FeatureGroupSubGroup(mcg, 'g2') # Second group, in mcg
    >>> m.add_child(mcg)
    >>> m.add_child(g1)
    >>> m.add_child(g2)
    >>> g1.add_child(folium.Marker([0,0]))
    >>> g2.add_child(folium.Marker([0,1]))
    >>> folium.LayerControl().add_to(m)
    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.featureGroup.subGroup(
                {{ this._group.get_name() }}
            );
            {{ this.get_name() }}.addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)

    default_js = [
        ('featuregroupsubgroupjs',
         'https://unpkg.com/leaflet.featuregroup.subgroup@1.0.2/dist/leaflet.featuregroup.subgroup.js'),
    ]

    def __init__(self, group, name=None, overlay=True, control=True, show=True):
        super(FeatureGroupSubGroup, self).__init__(name=name, overlay=overlay,
                                                   control=control, show=show)

        self._group = group
        self._name = 'FeatureGroupSubGroup'
