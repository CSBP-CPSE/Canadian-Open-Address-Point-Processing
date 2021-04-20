"""
This script reads in a csv with coordinates, and
1. drops entries with empty coordinates
2. drops entries with empty street names
3. truncates all coordinates to 5 decimal places
4. Deduplicate the file (same coordinates, unit, street number, street name)

All dropped entries (either empty values or duplicates) are recorded

-Joseph
"""

import pandas as pd
from math import trunc
import sys


s = sys.argv[1]


df = pd.read_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/{}_in.csv".format(s), low_memory=False, dtype='str')
N=len(df)

"""
replace truncation with rounding and keep everything as a string, don't need this function
def truncate(x,n=5):
    #truncate coordinates to 5 decimal places
    return trunc(x*10**n)/10**n
"""


df_null=df.copy()
df_null=(df_null.loc[(df['LAT'].isnull())|(df['STREET'].isnull())|(df['STR_NAME_PCS']=="NULL")|(df['STREET']=="<Null>")])
N_null=len(df_null)
df_null.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/{}_null.csv".format(s),index=False)
df=df.drop(df.loc[df['STR_NAME_PCS']=="NULL"].index)
df=df.drop(df.loc[df['STREET']=="<Null>"].index)

df=df.dropna(subset=['LAT','LON','STREET'])


#df['LON']=df['LON'].astype(float).apply(truncate)
#df['LAT']=df['LAT'].astype(float).apply(truncate)

cols=['LAT','LON']
df[cols] = df[cols].astype(float).applymap(lambda x: '{:.5f}'.format(x))


#simple deduplication
if 'STR_NAME_PCS' in list(df):
    df['duplicate']=df.duplicated(subset=['LON','LAT','UNIT','NUMBER','STR_NAME_PCS'], keep='first')
else:
    df['duplicate']=df.duplicated(subset=['LON','LAT','UNIT','NUMBER','STREET'], keep='first')
N_dupe=len(df.loc[df['duplicate']==True])

df.loc[df['duplicate']==True].to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/{}_dupe.csv".format(s),index=False)

df=df.loc[df['duplicate']==False]
N_f=len(df)
print(s, N, N_null, N_dupe, N_f, N==N_f+N_dupe+N_null )


df.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/{}_out.csv".format(s),index=False)

