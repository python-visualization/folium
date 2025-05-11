import geopandas as gpd
import pandas as pd

import folium

data = {
    "warehouses": {
        1: ("Allentown", "Allentown", "PA", "18101", 40.602812, -75.470433),
        2: ("Atlanta", "Atlanta", "GA", "30301", 33.753693, -84.389544),
        3: ("Baltimore", "Baltimore", "MD", "21201", 39.294398, -76.622747),
        4: ("Boston", "Boston", "MA", "02101", 42.36097, -71.05344),
        5: ("Chicago", "Chicago", "IL", "60602", 41.88331, -87.624713),
    },
    "customers": {
        1: ("Akron", "Akron", "OH", "  ", 41.08, -81.52),
        2: ("Albuquerque", "Albuquerque", "NM", "  ", 35.12, -106.62),
        3: ("Alexandria", "Alexandria", "VA", "  ", 38.82, -77.09),
        4: ("Amarillo", "Amarillo", "TX", "  ", 35.2, -101.82),
        5: ("Anaheim", "Anaheim", "CA", "  ", 33.84, -117.87),
        6: ("Brownfield", "Brownfield", "TX", "  ", 33.18101, -102.27066),
        7: ("Arlington", "Arlington", "TX", "  ", 32.69, -97.13),
        8: ("Arlington", "Arlington", "VA", "  ", 38.88, -77.1),
        9: ("Atlanta", "Atlanta", "GA", "  ", 33.76, -84.42),
        10: ("Augusta-Richmond", "Augusta-Richmond", "GA", "  ", 33.46, -81.99),
    },
}

df_customer = pd.DataFrame(
    list(data["customers"].values()),
    columns=["Facility Name", "City", "State", "Zip", "Latitude", "Longitude"],
)
df_customer["Facility Name"] = (
    "CUST_" + df_customer["Facility Name"] + "_" + df_customer["State"]
)

df_customer_geometry = gpd.points_from_xy(df_customer.Longitude, df_customer.Latitude)
gdf_customer = gpd.GeoDataFrame(
    df_customer, crs="EPSG:4326", geometry=df_customer_geometry
)
gdf_customer["Facility Type"] = "Customer"

df_warehouse = pd.DataFrame(
    list(data["warehouses"].values()),
    columns=["Facility Name", "City", "State", "Zip", "Latitude", "Longitude"],
)
df_warehouse["Facility Name"] = (
    "WH_" + df_warehouse["Facility Name"] + "_" + df_customer["State"]
)

df_warehouse_geometry = gpd.points_from_xy(
    df_warehouse.Longitude, df_warehouse.Latitude
)
gdf_warehouse = gpd.GeoDataFrame(
    df_warehouse, crs="EPSG:4326", geometry=df_warehouse_geometry
)
gdf_warehouse["Facility Type"] = "Warehouse"

m = folium.Map([40, -100.0], zoom_start=5, tiles=None)

gdf_warehouse.explore(
    m=m,
    marker_type="marker",
    marker_kwds=dict(icon=folium.Icon(color="red", icon="warehouse", prefix="fa")),
    name="Warehouse",
)

gdf_customer.explore(
    m=m,
    marker_type="marker",
    marker_kwds=dict(icon=folium.Icon(color="green", icon="tent", prefix="fa")),
    name="Customers",
)

folium.LayerControl().add_to(m)
