# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 09:07:15 2021
The NB shapefile download has encoding issues (accents appear as "?" and reading in with different
 encodings does not seem to help). This script just reads in the CSV (which can't be read
  by the open addresses processing script) and outputs a new one in a standard encoding.

@author: Joseph Kuchar (joseph.kuchar@canada.ca)
"""

import geopandas as gpd
from shapely import wkt
import pandas as pd


df = pd.read_csv(r"C:/Users/josep/Downloads/Civic_Addresses_data (1).csv",
                 low_memory=False)

print(list(df))
df['geometry'] = gpd.GeoSeries.from_wkt(df['the_geom'])

gdf=gpd.GeoDataFrame(df, geometry=df['geometry'], crs="EPSG:4326")

gdf["longitude"]=gdf.geometry.x
gdf["latitude"]=gdf.geometry.y

df=pd.DataFrame(gdf)
df.to_csv("NB_addresses.csv",index=False, encoding="utf-8")

