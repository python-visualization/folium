# -*- coding: utf-8 -*-

from collections import Iterable, OrderedDict

from branca.element import Element, Figure, JavascriptLink, MacroElement

from folium import Map
from folium.map import FeatureGroup

from jinja2 import Template


class StoryMap(FeatureGroup):
    """
    A specialisation of the FeatureGroup for creating interactive story maps. By passing it an iterable of labelled
    features, a timeline is produced.

    Parameter
    ---------
    data : Iterable of the form [(label 1, layer 1), (label 2, layer 2)]
        The set of labels and layers that will make up the story.
        The label values will appear in the timeline slider. The layer is what will be added to the map when that
        label has been selected.
    name : string, default None,
        The name of the Layer, as it will appear in LayerControls.
    overlay : bool, default True,
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default False,
        Whether the Layer will be included in LayerControls.
    show : bool, default True
        Whether the layer will be shown on opening (only for overlays).
    pan_zoom : int, default 10
        The zoom level applied when changing the timeline slider.
        If set to None, the map's current zoom is used.
    timeslider_options : dict, default {}
        Extra options which may be passed along to leaflet timeline slider.
        See https://github.com/svitkin/leaflet-timeline-slider#options for the various options available.
        *NB* 'changeMap', 'timelineItems', 'initializeChange' are reserved for use by this module.
    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{ this.get_name() }} = L.featureGroup(
                    {{ this.options|tojson }}
                ).addTo({{ this._parent.get_name() }});

                {{this.get_name()}}_clearStoryMap = function (map) {
                    // Remove all story map layers
                    {%- for feature in this.story_steps.values() %}
                    {{this.get_name()}}.removeLayer({{ feature.get_name() }});
                    {%- endfor %}
                }

                {{this.get_name()}}_changeStoryMap = function( {label, value, map} ) {
                    {{this.get_name()}}_clearStoryMap(map);
                    switch(label) {
                      {%- for story_step, feature in this.story_steps.items() %}
                        case ("{{ story_step }}"):
                            {{this.get_name()}}.addLayer({{ feature.get_name() }});
                            var story_step_centre = map.getCenter();
                            var story_step_zoom = {% if this.pan_zoom is none %} map.getZoom()
                                                  {% else %} {{ this.pan_zoom }}
                                                  {%- endif %};
                            try {
                                var story_step_bounds = {{this.get_name()}}.getBounds();
                                story_step_centre = story_step_bounds.getCenter();
                                {%- if this.pan_zoom is none %}
                                story_step_zoom = map.getBoundsZoom(story_step_bounds);
                                {%- endif %}
                            }
                            catch(err) {
                                console.log("Received the following error when trying to pan: " + err);
                                console.log("This is probably because the Leaflet FeatureGroup doesn't know how to " +
                                            "get the bounds of the underlying feature."
                                );
                            }
                            map.flyTo(story_step_centre, story_step_zoom);
                            break;
                      {%- endfor %}
                    }
                }

            {% endmacro %}
            """)

    _after_children_template = Template(u"""
            {% macro after_children_script(this, kwargs) %}
                var {{this.get_name()}}_timeline_slider = L.control.timelineSlider({
                    changeMap: {{this.get_name()}}_changeStoryMap,
                    timelineItems: {{this._story_steps_list|safe}},
                    {% for name, value in this.timeslider_options.items() %}
                    {{ name }}: {{ value|tojson }},
                    {% endfor %}
                    initializeChange: true
                }).addTo({{this._parent.get_name()}});

                {{ this.get_name() }}.on('remove', function(){
                    {{this.get_name()}}_timeline_slider.remove()
                });
                {{ this.get_name() }}.on('add', function(){
                    {{this.get_name()}}_timeline_slider.addTo({{this._parent.get_name()}})
                });
            {% endmacro %}
            """)

    _reserved_timeslider_options = {'changeMap', 'timelineItems', 'initializeChange'}

    def __init__(self, data, name=None, overlay=True, control=False, show=True, pan_zoom=None, timeslider_options={}):
        # Creating the feature group
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = 'story_map'
        self.pan_zoom = pan_zoom

        for reserved_opt in self._reserved_timeslider_options:
            assert (reserved_opt not in timeslider_options), (
                'Sorry, the "{}" keyword is reserved for use by this module.'.format(reserved_opt)
            )
        self.timeslider_options = timeslider_options

        # Constructing ordered dictionary
        assert isinstance(data, Iterable), 'Step data has to be an Iterable'
        self.story_steps = data if isinstance(data, OrderedDict) else OrderedDict([
            (key, feature)
            for key, feature in data
        ])

        # Verifying all of the features passed in are map features
        for key, feature in self.story_steps.items():
            assert isinstance(feature, MacroElement), ('Feature "{}" for step "{}" is not a MacroElement,'
                                                       'or a child class thereof'.format(feature, key))

        # Convenience list because (dict key) -> list conversions are a pain in Jinja
        self._story_steps_list = list(self.story_steps.keys())

        # Adding children to the underlying feature group
        for feature in self.story_steps.values():
            super().add_child(feature)

    def render(self, **kwargs):
        super().render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        # Adding JS header
        figure.header.add_child(
            JavascriptLink('https://svitkin.github.io/leaflet-timeline-slider/dist/leaflet-timeline-slider.min.js'),
            # noqa
            name='leaflet-timeline-slider.min.js')

        # Adding the time slider control *after* the children have been added
        # Otherwise it will try refer to one of the kids when it first runs
        after_children_script = self._after_children_template.module.__dict__['after_children_script']
        figure.script.add_child(Element(after_children_script(self, kwargs)),
                                name=self.get_name() + '_bootstrap')

    def add_to(self, parent, name=None, index=None):
        assert isinstance(parent, Map), 'The Story Map has to be added to a Map instance'
        super().add_to(parent, name, index)

    def add_child(self, child, name=None, index=None):
        raise RuntimeError('Children may only be added to StoryMap class via the constructor.')

    def add_children(self, child, name=None, index=None):
        raise RuntimeError('Children may only be added to StoryMap class via the constructor.')
