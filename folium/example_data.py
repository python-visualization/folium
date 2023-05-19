import ast
import json
import os


def get_path(filename):
    package_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(package_path, "example_data", filename)


def us_states_geojson():
    with open(get_path("us_states.json")) as f:
        return json.load(f)


def world_countries_geojson():
    with open(get_path("world_countries.json")) as f:
        return json.load(f)


def antarctic_ice_shelf_topojson():
    with open(get_path("antarctic_ice_shelf_topo.json")) as f:
        return json.load(f)


def new_york_boroughs_geodataframe():
    import geopandas

    return geopandas.read_file(get_path("new_york_boroughs.zip"))


def subway_stations_geodataframe():
    import geopandas

    return geopandas.read_file(get_path("subway_stations.geojson"))


def us_unemployment_pandas_dataframe():
    import pandas

    return pandas.read_csv(get_path("us_unemployment_oct_2012.csv"))


def us_labor_force_pandas_dataframe():
    import pandas

    return pandas.read_csv(get_path("us_labor_force_2011.csv"))


def language_coordinates_and_stats_pandas_dataframe():
    import pandas

    return pandas.read_csv(
        get_path("consonants_vowels.csv"),
        # To ensure that tuples are read as tuples
        converters={"coordinates": ast.literal_eval},
    )
