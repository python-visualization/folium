"""
Folium Tests
-------

"""

import json
import os

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
import xyzservices.providers as xyz
from jinja2.utils import htmlsafe_json_dumps

import folium
from folium import TileLayer
from folium.features import Choropleth, GeoJson
from folium.template import Template

rootpath = os.path.abspath(os.path.dirname(__file__))

# For testing remote requests
remote_url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"  # noqa


def setup_data():
    """Import economic data for testing."""
    with open(os.path.join(rootpath, "us-counties.json")) as f:
        get_id = json.load(f)

    county_codes = [x["id"] for x in get_id["features"]]
    county_df = pd.DataFrame({"FIPS_Code": county_codes}, dtype=str)

    # Read into Dataframe, cast to string for consistency.
    df = pd.read_csv(os.path.join(rootpath, "us_county_data.csv"), na_values=[" "])
    df["FIPS_Code"] = df["FIPS_Code"].astype(str)

    # Perform an inner join, pad NA's with data from nearest county.
    merged = pd.merge(df, county_df, on="FIPS_Code", how="inner")
    return merged.fillna(method="pad")


def test_location_args():
    """Test some data types for a location arg."""
    location = np.array([45.5236, -122.6750])
    m = folium.Map(location)
    assert m.location == [45.5236, -122.6750]

    df = pd.DataFrame({"location": [45.5236, -122.6750]})
    m = folium.Map(df["location"])
    assert m.location == [45.5236, -122.6750]


class TestFolium:
    """Test class for the Folium library."""

    def setup_method(self):
        """Setup Folium Map."""
        attr = "http://openstreetmap.org"
        self.m = folium.Map(
            location=[45.5236, -122.6750],
            width=900,
            height=400,
            max_zoom=20,
            zoom_start=4,
            max_bounds=True,
            font_size="1.5rem",
            attr=attr,
        )
        self.fit_bounds_template = Template(
            """
            {% if autobounds %}
            var autobounds = L.featureGroup({{ features }}).getBounds()
            {% if not bounds %}
            {% set bounds = "autobounds" %}
            {% endif %}
            {% endif %}
            {% if bounds %}
            {{this._parent.get_name()}}.fitBounds({{ bounds }},
                {{ fit_bounds_options }}
            );
            {% endif %}
        """
        )

    def test_init(self):
        """Test map initialization."""

        assert self.m.get_name().startswith("map_")
        assert self.m.get_root() == self.m._parent
        assert self.m.location == [45.5236, -122.6750]
        assert self.m.options["zoom"] == 4
        assert self.m.options["max_bounds"] == [[-90, -180], [90, 180]]
        assert self.m.position == "relative"
        assert self.m.height == (400, "px")
        assert self.m.width == (900, "px")
        assert self.m.left == (0, "%")
        assert self.m.top == (0, "%")
        assert self.m.global_switches.no_touch is False
        assert self.m.global_switches.disable_3d is False
        assert self.m.font_size == "1.5rem"
        assert self.m.to_dict() == {
            "name": "Map",
            "id": self.m._id,
            "children": {
                "openstreetmap": {
                    "name": "TileLayer",
                    "id": self.m._children["openstreetmap"]._id,
                    "children": {},
                }
            },
        }

    @pytest.mark.parametrize(
        "tiles,provider",
        [
            ("OpenStreetMap", xyz.OpenStreetMap.Mapnik),
            ("CartoDB positron", xyz.CartoDB.Positron),
            ("CartoDB dark_matter", xyz.CartoDB.DarkMatter),
        ],
    )
    def test_builtin_tile(self, tiles, provider):
        """Test custom maptiles."""

        m = folium.Map(location=[45.5236, -122.6750], tiles=tiles)
        tiles = "".join(tiles.lower().strip().split())
        url = provider.build_url(fill_subdomain=False, scale_factor="{r}")
        attr = provider.html_attribution

        assert m._children[tiles.replace("_", "")].tiles == url
        assert htmlsafe_json_dumps(attr) in m._parent.render()

        bounds = m.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_custom_tile(self):
        """Test custom tile URLs."""

        url = "http://{s}.custom_tiles.org/{z}/{x}/{y}.png"
        attr = "Attribution for custom tiles"

        with pytest.raises(ValueError):
            folium.Map(location=[45.5236, -122.6750], tiles=url)

        m = folium.Map(location=[45.52, -122.67], tiles=url, attr=attr)
        assert m._children[url].tiles == url
        assert attr in m._parent.render()

        bounds = m.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_tilelayer_object(self):
        url = "http://{s}.custom_tiles.org/{z}/{x}/{y}.png"
        attr = "Attribution for custom tiles"
        m = folium.Map(location=[45.52, -122.67], tiles=TileLayer(url, attr=attr))
        assert next(iter(m._children.values())).tiles == url
        assert attr in m._parent.render()

    def test_feature_group(self):
        """Test FeatureGroup."""

        m = folium.Map()
        feature_group = folium.FeatureGroup()
        feature_group.add_child(folium.Marker([45, -30], popup=folium.Popup("-30")))
        feature_group.add_child(folium.Marker([45, 30], popup=folium.Popup("30")))
        m.add_child(feature_group)
        m.add_child(folium.LayerControl())

        m._repr_html_()

        bounds = m.get_bounds()
        assert bounds == [[45, -30], [45, 30]], bounds

    def test_topo_json_smooth_factor(self):
        """Test topojson smooth factor method."""
        self.m = folium.Map([43, -100], zoom_start=4)

        # Adding TopoJSON as additional layer.
        with open(os.path.join(rootpath, "or_counties_topo.json")) as f:
            choropleth = Choropleth(
                f, topojson="objects.or_counties_geo", smooth_factor=0.5
            ).add_to(self.m)

        out = self.m._parent.render()

        # Verify TopoJson
        topo_json = choropleth.geojson
        topojson_str = topo_json._template.module.script(topo_json)
        assert "".join(topojson_str.split())[:-1] in "".join(out.split())

    def test_choropleth_features(self):
        """Test to make sure that Choropleth function doesn't allow
        values outside of the domain defined by bins.

        It also tests that all parameters work as expected regarding
        nan and missing values.
        """
        with open(os.path.join(rootpath, "us-counties.json")) as f:
            geo_data = json.load(f)
        data = {"1001": -1}
        fill_color = "BuPu"
        key_on = "id"

        with pytest.raises(ValueError):
            Choropleth(
                geo_data=geo_data,
                data=data,
                key_on=key_on,
                fill_color=fill_color,
                bins=[0, 1, 2, 3],
            ).add_to(self.m)
            self.m._parent.render()

        Choropleth(
            geo_data=geo_data,
            data={"1001": 1, "1003": float("nan")},
            key_on=key_on,
            fill_color=fill_color,
            fill_opacity=0.543212345,
            nan_fill_color="a_random_color",
            nan_fill_opacity=0.123454321,
        ).add_to(self.m)

        out = self.m._parent.render()
        out_str = "".join(out.split())
        assert '"fillColor":"a_random_color","fillOpacity":0.123454321' in out_str
        assert '"fillOpacity":0.543212345' in out_str

    def test_choropleth_key_on(self):
        """Test to make sure that Choropleth function doesn't raises
        a ValueError when the 'key_on' field is set to a column that might
        have 0 as a value.
        """
        with open(os.path.join(rootpath, "geo_grid.json")) as f:
            geo_data = json.load(f)
        data = pd.DataFrame(
            {
                "idx": {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5},
                "value": {
                    "0": 78.0,
                    "1": 39.0,
                    "2": 0.0,
                    "3": 81.0,
                    "4": 42.0,
                    "5": 68.0,
                },
            }
        )
        fill_color = "BuPu"
        columns = ["idx", "value"]
        key_on = "feature.properties.idx"

        Choropleth(
            geo_data=geo_data,
            data=data,
            key_on=key_on,
            fill_color=fill_color,
            columns=columns,
        )

    def test_choropleth_geopandas_numeric(self):
        """Test to make sure that Choropleth function does complete the lookup
        between a GeoJSON generated from a GeoDataFrame and data from the GeoDataFrame itself.

        key_on field is dtype = str, while column 0 is dtype = int
        All geometries have matching values (no nan_fill_color allowed)
        """
        with open(os.path.join(rootpath, "geo_grid.json")) as f:
            geo_data = json.load(f)

        geo_data_frame = gpd.GeoDataFrame.from_features(geo_data["features"])
        geo_data_frame = geo_data_frame.set_crs("epsg: 4326")
        fill_color = "BuPu"
        key_on = "feature.id"

        Choropleth(
            geo_data=geo_data_frame.geometry,
            data=geo_data_frame.value,
            key_on=key_on,
            fill_color=fill_color,
            fill_opacity=0.543212345,
            nan_fill_color="a_random_color",
            nan_fill_opacity=0.123454321,
        ).add_to(self.m)

        out = self.m._parent.render()
        out_str = "".join(out.split())

        assert '"fillColor":"a_random_color","fillOpacity":0.123454321' not in out_str
        assert '"fillOpacity":0.543212345' in out_str

    def test_choropleth_geopandas_mixed(self):
        """Test to make sure that Choropleth function does complete the lookup
        between a GeoJSON generated from a GeoDataFrame and data from a DataFrame.

        key_on field is dtype = str, while column 0 is dtype = object (mixed int and str)
        All geometries have matching values (no nan_fill_color allowed)
        """
        with open(os.path.join(rootpath, "geo_grid.json")) as f:
            geo_data = json.load(f)

        geo_data_frame = gpd.GeoDataFrame.from_features(geo_data["features"])
        geo_data_frame = geo_data_frame.set_crs("epsg: 4326")
        data = pd.DataFrame(
            {
                "idx": {"0": 0, "1": "1", "2": 2, "3": 3, "4": 4, "5": 5},
                "value": {
                    "0": 78.0,
                    "1": 39.0,
                    "2": 0.0,
                    "3": 81.0,
                    "4": 42.0,
                    "5": 68.0,
                },
            }
        )
        fill_color = "BuPu"
        columns = ["idx", "value"]
        key_on = "feature.id"

        Choropleth(
            geo_data=geo_data_frame.geometry,
            data=data,
            key_on=key_on,
            columns=columns,
            fill_color=fill_color,
            fill_opacity=0.543212345,
            nan_fill_color="a_random_color",
            nan_fill_opacity=0.123454321,
        ).add_to(self.m)

        out = self.m._parent.render()
        out_str = "".join(out.split())

        assert '"fillColor":"a_random_color","fillOpacity":0.123454321' not in out_str
        assert '"fillOpacity":0.543212345' in out_str

    def test_choropleth_geopandas_str(self):
        """Test to make sure that Choropleth function does complete the lookup
        between a GeoJSON generated from a GeoDataFrame and data from a DataFrame.

        key_on field and column 0 from data are both strings.
        All geometries have matching values (no nan_fill_color allowed)
        """
        with open(os.path.join(rootpath, "geo_grid.json")) as f:
            geo_data = json.load(f)

        geo_data_frame = gpd.GeoDataFrame.from_features(geo_data["features"])
        geo_data_frame = geo_data_frame.set_crs("epsg: 4326")
        data = pd.DataFrame(
            {
                "idx": {"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5"},
                "value": {
                    "0": 78.0,
                    "1": 39.0,
                    "2": 0.0,
                    "3": 81.0,
                    "4": 42.0,
                    "5": 68.0,
                },
            }
        )
        fill_color = "BuPu"
        columns = ["idx", "value"]
        key_on = "feature.id"

        Choropleth(
            geo_data=geo_data_frame.geometry,
            data=data,
            key_on=key_on,
            columns=columns,
            fill_color=fill_color,
            fill_opacity=0.543212345,
            nan_fill_color="a_random_color",
            nan_fill_opacity=0.123454321,
        ).add_to(self.m)

        out = self.m._parent.render()
        out_str = "".join(out.split())

        assert '"fillColor":"a_random_color","fillOpacity":0.123454321' not in out_str
        assert '"fillOpacity":0.543212345' in out_str

    def test_tile_attr_unicode(self):
        """Test tile attribution unicode"""
        m = folium.Map(location=[45.5236, -122.6750], tiles="test", attr="юникод")
        m._parent.render()

    def test_fit_bounds(self):
        """Test fit_bounds."""
        bounds = ((52.193636, -2.221575), (52.636878, -1.139759))
        self.m.fit_bounds(bounds)
        fitbounds = [
            val
            for key, val in self.m._children.items()
            if isinstance(val, folium.FitBounds)
        ][0]
        out = self.m._parent.render()

        fit_bounds_rendered = self.fit_bounds_template.render(
            {
                "bounds": json.dumps(bounds),
                "this": fitbounds,
                "fit_bounds_options": {},
            }
        )

        assert "".join(fit_bounds_rendered.split()) in "".join(out.split())

    def test_fit_bounds_2(self):
        bounds = ((52.193636, -2.221575), (52.636878, -1.139759))
        self.m.fit_bounds(bounds, max_zoom=15, padding=(3, 3))
        fitbounds = [
            val
            for key, val in self.m._children.items()
            if isinstance(val, folium.FitBounds)
        ][0]
        out = self.m._parent.render()

        fit_bounds_rendered = self.fit_bounds_template.render(
            {
                "bounds": json.dumps(bounds),
                "fit_bounds_options": json.dumps(
                    {
                        "maxZoom": 15,
                        "padding": (3, 3),
                    },
                    sort_keys=True,
                ),
                "this": fitbounds,
            }
        )

        assert "".join(fit_bounds_rendered.split()) in "".join(out.split())

        bounds = self.m.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_custom_icon(self):
        """Test CustomIcon."""
        icon_image = "http://leafletjs.com/docs/images/leaf-green.png"
        shadow_image = "http://leafletjs.com/docs/images/leaf-shadow.png"

        self.m = folium.Map([45, -100], zoom_start=4)
        i = folium.features.CustomIcon(
            icon_image,
            icon_size=(38, 95),
            icon_anchor=(22, 94),
            shadow_image=shadow_image,
            shadow_size=(50, 64),
            shadow_anchor=(4, 62),
            popup_anchor=(-3, -76),
        )
        mk = folium.Marker([45, -100], icon=i, popup=folium.Popup("Hello"))
        self.m.add_child(mk)
        self.m._parent.render()

        bounds = self.m.get_bounds()
        assert bounds == [[45, -100], [45, -100]], bounds

    def test_global_switches(self):
        m = folium.Map(prefer_canvas=True)
        out = m._parent.render()
        out_str = "".join(out.split())
        assert '"preferCanvas":true' in out_str
        assert not m.global_switches.no_touch
        assert not m.global_switches.disable_3d

        m = folium.Map(no_touch=True)
        out = m._parent.render()
        out_str = "".join(out.split())
        assert '"preferCanvas":false' in out_str
        assert m.global_switches.no_touch
        assert not m.global_switches.disable_3d

        m = folium.Map(disable_3d=True)
        out = m._parent.render()
        out_str = "".join(out.split())
        assert '"preferCanvas":false' in out_str
        assert not m.global_switches.no_touch
        assert m.global_switches.disable_3d

        m = folium.Map(prefer_canvas=True, no_touch=True, disable_3d=True)
        out = m._parent.render()
        out_str = "".join(out.split())
        assert '"preferCanvas":true' in out_str
        assert m.global_switches.no_touch
        assert m.global_switches.disable_3d

    def test_json_request(self):
        """Test requests for remote GeoJSON files."""
        self.m = folium.Map(zoom_start=4)

        # Adding remote GeoJSON as additional layer.
        GeoJson(remote_url, smooth_factor=0.5).add_to(self.m)

        self.m._parent.render()
        bounds = self.m.get_bounds()
        np.testing.assert_allclose(
            bounds, [[18.948267, -178.123152], [71.351633, 173.304726]]
        )

    def test_control_typecheck(self):
        m = folium.Map(
            location=[39.949610, -75.150282], zoom_start=5, zoom_control=False
        )
        tiles = TileLayer(
            tiles="OpenStreetMap",
            show=False,
            control=False,
        )
        tiles.add_to(m)

        with pytest.raises(TypeError) as excinfo:
            minimap = folium.Control("MiniMap", tiles, position="downunder")
            minimap.add_js_link(
                "minimap_js",
                "https://cdnjs.cloudflare.com/ajax/libs/leaflet-minimap/3.6.1/Control.MiniMap.min.js",
            )
            minimap.add_css_link(
                "minimap_css",
                "https://cdnjs.cloudflare.com/ajax/libs/leaflet-minimap/3.6.1/Control.MiniMap.css",
            )
            minimap.add_to(m)
        assert "position must be one of ('bottomright', 'bottomleft'" in str(
            excinfo.value
        )
