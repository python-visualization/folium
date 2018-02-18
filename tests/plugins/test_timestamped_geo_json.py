# -*- coding: utf-8 -*-

"""
Test TimestampedGeoJson
-----------------------

"""

from __future__ import (absolute_import, division, print_function)

import folium

from folium import plugins

from jinja2 import Template

import numpy as np


def test_timestamped_geo_json():
    coordinates = [[[[lon-8*np.sin(theta), -47+6*np.cos(theta)] for
                     theta in np.linspace(0, 2*np.pi, 25)],
                    [[lon-4*np.sin(theta), -47+3*np.cos(theta)] for theta
                     in np.linspace(0, 2*np.pi, 25)]] for
                   lon in np.linspace(-150, 150, 7)]
    data = {
        'type': 'FeatureCollection',
        'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [0, 0],
                        },
                    'properties': {
                        'times': [1435708800000+12*86400000]
                        }
                    },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[lon, -25] for
                                        lon in np.linspace(-150, 150, 49)],
                        },
                    'properties': {
                        'times': [1435708800000+i*86400000 for
                                  i in np.linspace(0, 25, 49)]
                        }
                    },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': [[lon, 25] for
                                        lon in np.linspace(-150, 150, 25)],
                        },
                    'properties': {
                        'times': [1435708800000+i*86400000 for
                                  i in np.linspace(0, 25, 25)],
                        'style': {
                            'color': 'red'
                            },
                        },
                    },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[lon-4*np.sin(theta),
                                          47+3*np.cos(theta)] for theta
                                         in np.linspace(0, 2*np.pi, 25)]
                                        for lon in
                                        np.linspace(-150, 150, 13)],
                        },
                    'properties': {
                        'times': [1435708800000+i*86400000 for
                                  i in np.linspace(0, 25, 13)]
                        }
                    },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': coordinates,
                        },
                    'properties': {
                        'times': [1435708800000+i*86400000 for
                                  i in np.linspace(0, 25, 7)]
                        }
                    },
            ],
        }

    m = folium.Map([47, 3], zoom_start=1)
    tgj = plugins.TimestampedGeoJson(data)
    m.add_child(tgj)
    m._repr_html_()

    out = m._parent.render()

    # Verify the imports.
    assert ('<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/'
            'jquery.min.js"></script>'
            ) in out
    assert ('<script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/'
            '1.10.2/jquery-ui.min.js"></script>'
            ) in out
    assert ('<script src="https://rawgit.com/nezasa/'
            'iso8601-js-period/master/iso8601.min.js"></script>'
            ) in out
    assert ('<script src="https://rawgit.com/socib/Leaflet.'
            'TimeDimension/master/dist/leaflet.timedimension.min.js">'
            '</script>'
            ) in out
    assert ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/'
            'libs/highlight.js/8.4/styles/default.min.css" />'
            ) in out
    assert ('<link rel="stylesheet" href="http://apps.socib.es/Leaflet.'
            'TimeDimension/dist/leaflet.timedimension.control.min.css" />'
            ) in out
    assert ('<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js">'
            '</script>'
            ) in out

    # Verify that the script is okay.
    tmpl = Template("""
            L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
                _getDisplayDateFormat: function(date){
                    var newdate = new moment(date);
                    console.log(newdate)
                    return newdate.format("{{this.date_options}}");
                }
            });
            {{this._parent.get_name()}}.timeDimension = L.timeDimension({period:"{{this.period}}"});
            var timeDimensionControl = new L.Control.TimeDimensionCustom({{ this.options }});
            {{this._parent.get_name()}}.addControl(this.timeDimensionControl);
             
            function __propagateProperties(props) {
                if(!props) { return {}; }
            
                var propertiesToExtract = {{ this.propagate_properties }},
                    ps = {};
                
                if(propertiesToExtract.length == 0) { return {}; }
                
                for(var i = 0, p = null;i < propertiesToExtract.length;i++) {
                    var p = propertiesToExtract[i];
                    if(props[p]) { ps[p] = props[p]; }
                }
                
                return ps;
            }
            
            function __merge(first, second) {
                var merged = {};
                first = first || {};
                second = second || {};
                
                for (var attrname in first)  { merged[attrname] = first[attrname]; }
                for (var attrname in second) { merged[attrname] = second[attrname]; }
                
                return merged;
            }

            console.log("{{this.marker}}");

            var geoJsonLayer = L.geoJson({{this.data}}, {
                    pointToLayer: function (feature, latLng) {
                        if (feature.properties.icon == 'marker') {
                            if(feature.properties.iconstyle){
                                return new L.Marker(latLng, __merge(__propagateProperties(feature.properties), {
                                    icon: L.icon(feature.properties.iconstyle)}));
                            }
                            //else
                            return new L.Marker(latLng, __propagateProperties(feature.properties));
                        }
                        if (feature.properties.icon == 'circle') {
                            if (feature.properties.iconstyle) {
                                return new L.circleMarker(latLng, __merge(__propagateProperties(feature.properties), feature.properties.iconstyle))
                            }
                            //else
                            return new L.circleMarker(latLng, __propagateProperties(feature.properties));
                        }
                        //else

                        return new L.Marker(latLng, __propagateProperties(feature.properties));
                    },
                    style: function (feature) {
                        return feature.properties.style;
                    },
                    onEachFeature: function(feature, layer) {
                        if (feature.properties.popup) {
                        layer.bindPopup(feature.properties.popup);
                        }
                    }
                })

            var {{this.get_name()}} = L.timeDimension.layer.geoJson(geoJsonLayer,
                {updateTimeDimension: true,addlastPoint: {{'true' if this.add_last_point else 'false'}}}
                ).addTo({{this._parent.get_name()}});
    """)  # noqa

    assert ''.join(tmpl.render(this=tgj).split()) in ''.join(out.split())

    bounds = m.get_bounds()
    assert bounds == [[-53.0, -158.0], [50.0, 158.0]], bounds


def test_propagates_named_feature_properties_when_asked():
    data = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [0, 0],
                },
                'properties': {
                    'times': [1435708800000 + 12 * 86400000]
                }
            },
        ]
    }
    data['features'][0]['properties']['rotationAngle'] = 45

    m = folium.Map([47, 3], zoom_start=1)
    tgj = plugins.TimestampedGeoJson(data, propagate_properties=['rotationAngle'])
    m.add_child(tgj)

    out = m._parent.render()

    # language=js
    tmpl = Template("""
            L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
                _getDisplayDateFormat: function(date){
                    var newdate = new moment(date);
                    console.log(newdate)
                    return newdate.format("{{this.date_options}}");
                }
            });
            {{this._parent.get_name()}}.timeDimension = L.timeDimension({period:"{{this.period}}"});
            var timeDimensionControl = new L.Control.TimeDimensionCustom({{ this.options }});
            {{this._parent.get_name()}}.addControl(this.timeDimensionControl);
             
            function __propagateProperties(props) {
                if(!props) { return {}; }
            
                var propertiesToExtract = ["rotationAngle"],
                    ps = {};
                
                if(propertiesToExtract.length == 0) { return {}; }
                
                for(var i = 0, p = null;i < propertiesToExtract.length;i++) {
                    var p = propertiesToExtract[i];
                    if(props[p]) { ps[p] = props[p]; }
                }
                
                return ps;
            }
            
            function __merge(first, second) {
                var merged = {};
                first = first || {};
                second = second || {};
                
                for (var attrname in first)  { merged[attrname] = first[attrname]; }
                for (var attrname in second) { merged[attrname] = second[attrname]; }
                
                return merged;
            }

            console.log("{{this.marker}}");

            var geoJsonLayer = L.geoJson({{this.data}}, {
                    pointToLayer: function (feature, latLng) {
                        if (feature.properties.icon == 'marker') {
                            if(feature.properties.iconstyle){
                                return new L.Marker(latLng, __merge(__propagateProperties(feature.properties), {
                                    icon: L.icon(feature.properties.iconstyle)}));
                            }
                            //else
                            return new L.Marker(latLng, __propagateProperties(feature.properties));
                        }
                        if (feature.properties.icon == 'circle') {
                            if (feature.properties.iconstyle) {
                                return new L.circleMarker(latLng, __merge(__propagateProperties(feature.properties), feature.properties.iconstyle))
                            }
                            //else
                            return new L.circleMarker(latLng, __propagateProperties(feature.properties));
                        }
                        //else

                        return new L.Marker(latLng, __propagateProperties(feature.properties));
                    },
                    style: function (feature) {
                        return feature.properties.style;
                    },
                    onEachFeature: function(feature, layer) {
                        if (feature.properties.popup) {
                        layer.bindPopup(feature.properties.popup);
                        }
                    }
                })

            var {{this.get_name()}} = L.timeDimension.layer.geoJson(geoJsonLayer,
                {updateTimeDimension: true,addlastPoint: {{'true' if this.add_last_point else 'false'}}}
                ).addTo({{this._parent.get_name()}});
    """)  # noqa

    assert tmpl.render(this=tgj) in out
