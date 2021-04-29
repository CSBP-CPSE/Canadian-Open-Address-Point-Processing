# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 2021
@author: Joseph Kuchar
Combine all the municipal address data from the Alberta Municipal Data Sharing Partnership (AMDSP) into a single shapefile
The civic_id column is meant to be the city/municipality field, but some entries contain blanks or numbers (particularly rural).
This script reads in the metadata csv for each file to extract the municipality name providing the data, and use that to fill gaps 
or replace the civic_id value if it's a number.
"""

import geopandas as gpd
import pandas as pd
import re
import os

path="/home/jovyan/data-vol-1/ODA/pre-processing/Alberta"

files=os.listdir(path)

f_list=[x for x in files if x.endswith('.shp')]
DFS=[]
for f in f_list:
    print(f)

    test=gpd.read_file(path+'/'+f)
    csv_name=f.replace('maddress_','').replace('.shp','.csv')
    df=pd.read_csv(path+'/'+csv_name)
    
    test=test[['record_id', 'civic_id', 'name', 'road_name', 'dir_pref', 'name_pref', 'main_name', 'road_type', 'dir_sufx', 'house_id', 'access_num', 'unit_num', 'geometry']]
    Municipality_Name=df['Municipality name '].iloc[0]
    print(Municipality_Name)
    test['civic_id']=test['civic_id'].fillna(Municipality_Name)
    pat=re.compile(r"^\d+$")
    test['civic_id']=test['civic_id'].str.replace(pat,Municipality_Name,regex=True)

    crs="EPSG:4326"
    test=test.to_crs(crs)

    test['lat']=test.geometry.y
    test['lon']=test.geometry.x

    test=pd.DataFrame(test)
    test=test.drop(columns=['geometry'])

    DFS.append(test)

DF=pd.concat(DFS)
GDF=gpd.GeoDataFrame(DF, geometry=gpd.points_from_xy(DF.lon, DF.lat), crs=crs)

GDF.to_file('alberta_AMDSP_2021-03.shp')