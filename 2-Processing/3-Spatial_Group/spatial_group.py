"""
This script uses geopandas to place all addresses into CSDs.
This uses the digital boundary files, which extend into the water. This is deliberate so that addresses on coastlines are not accidentally dropped.
"""

import pandas as pd
import geopandas as gpd
from hashlib import blake2b

import sys

name_in = sys.argv[1]
name_out = sys.argv[2]
print(name_in)
prefix="/home/jovyan/data-vol-1/ODA/processing/temporary_files/"
df = pd.read_csv("{}{}".format(prefix,name_in), low_memory=False, dtype='str')

N1=len(df)
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.LON.astype(float), df.LAT.astype(float)))
gdf.crs="EPSG:4326"

#read in Statcan boundary file

CSD = gpd.read_file("/home/jovyan/data-vol-1/ODA/processing/3-Spatial_Group/CSD/fixed_CSD.shp")
CSD=CSD[['CSDUID', 'CSDNAME','PRUID', 'geometry']]
#convert geometry of addresses to statcan geometry

gdf=gdf.to_crs(CSD.crs)


#perform spatial merge

gdf_csd=gpd.sjoin(gdf,CSD, op='within', how='left')

df=pd.DataFrame(gdf_csd)
df=df.drop(columns=['geometry', 'index_right', 'duplicate', 'REGION', 'HASH', 'DISTRICT'])

df_null=df.copy()
df_null=df_null.loc[df_null.CSDUID.isnull()]
df_null.to_csv('{}NULL_{}'.format(prefix,name_out),index=False)

df=df.dropna(subset=['CSDUID'])

print(name_in, N1==len(df_null)+len(df))
df.to_csv("{}{}".format(prefix,name_out),index=False)




