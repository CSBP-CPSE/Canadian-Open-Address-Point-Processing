"""
This is the final processing step. It does the following:
1. Assign the "Provider" field to the individual source files
2. Merge all individual level files into one monster address database
3. Loop through by CSDUIDs, and within each CSD drop duplicates and assign group ids
4. Assign unique ID using hashlib
"""
import pandas as pd
from hashlib import blake2b

#convenience function to apply to pandas column
def GetHash(x):
    h=blake2b(digest_size=10)
    h.update(x.encode())
    return h.hexdigest()
sources=pd.read_excel("/home/jovyan/data-vol-1/ODA/processing/valid_sources.xlsx")

names=list(sources['JSON_NAME'])
provs=list(sources['GEO_PROV'].str.lower())
providers=list(sources['Attribution_Name'])

DFS=[]
print('reading in csvs...')
for i in range(len(sources)):
    pr=provs[i]
    s=names[i]
    print(pr, s)
    #1. Assign provider
    provider=providers[i]
    df=pd.read_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/3_Spatial/{}/{}_out.csv".format(pr,s),low_memory=False, dtype='str')
    df["Provider"]=provider
    df['NUMBER']=df['NUMBER'].str.replace('.0','', regex=False)

    cols=['LAT','LON']
    df[cols] = df[cols].astype(float).applymap(lambda x: '{:.5f}'.format(x))

    df['temp']=df['LAT'].astype(str)+df['LON'].astype(str)+df['NUMBER'].astype(str)+df['STR_NAME_PCS'].astype(str)+df['UNIT'].astype(str)
    df['ODA_ID']=df['temp'].apply(GetHash)
    #df=df.drop(columns=['temp'])
    DFS.append(df)

#2. Merge into one dataframe
print('merging dataframes...')
DF=pd.concat(DFS, ignore_index=True)

#3a. Drop duplicates
print('Dropping duplicates')
L=['LON','LAT','UNIT','NUMBER','STR_NAME_PCS','STR_TYPE_PCS','STR_DIR_PCS']
for l in L:
    DF[l]=DF[l].fillna('')
    DF[l]=DF[l].astype(str)
    
#first dedupe using STR_NAME_PCS
DF['duplicate']=DF.duplicated(subset=['LON','LAT','UNIT','NUMBER','STR_NAME_PCS'], keep='first')
DF.loc[DF['duplicate']==True].to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_dupe_test1.csv",index=False)
DF=DF.drop(DF.loc[DF['duplicate']==True].index)
#Then drop using STREET
DF['duplicate2']=DF.duplicated(subset=['LON','LAT','UNIT','NUMBER','STREET'], keep='first')
DF.loc[DF['duplicate2']==True].to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_dupe_test2.csv",index=False)
DF=DF.drop(DF.loc[DF['duplicate2']==True].index)

#3b. Assign group ids
print('Assigning Duplicates')
DF['GROUP_ID'] = DF.groupby(['CSDUID', 'NUMBER', 'STR_NAME_PCS', 'STR_TYPE_PCS', 'STR_DIR_PCS']).ngroup()

DF=DF.rename(columns={'ID':'SOURCE_ID'})

DF=DF[["LON",	"LAT",	"NUMBER",	"STREET",	"STR_NAME",	"STR_TYPE",	"STR_DIR",	"FULL_ADDR",
       "UNIT",	"CITY",	"POSTCODE",	"STR_NAME_PCS",	"STR_DIR_PCS",	"STR_TYPE_PCS",	"CITY_PCS",	"CSDUID",
       "CSDNAME",	"PRUID",	"Provider",	"ODA_ID",	"SOURCE_ID",	"GROUP_ID"]]#,  "temp"]]

print(len(DF), 'records')
DF.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_v1.csv",index=False)

#split into province level files



#DF=pd.read_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_v1.csv", low_memory=False)

DF=pd.read_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_v1.csv", low_memory=False, dtype=str)
DF=DF[["LON",	"LAT",	"NUMBER",	"STREET",	"STR_NAME",	"STR_TYPE",	"STR_DIR",	"FULL_ADDR",
       "UNIT",	"CITY",	"POSTCODE",	"STR_NAME_PCS",	"STR_DIR_PCS",	"STR_TYPE_PCS",	"CITY_PCS",	"CSDUID",
       "CSDNAME",	"PRUID",	"Provider",	"ODA_ID",	"SOURCE_ID",	"GROUP_ID"]]
DF.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_v1.csv",index=False)



"""
Separate out entries with missing CSD/PRUID info
"""
DF_null=DF.copy()
DF_null=DF.loc[DF.PRUID.isnull()]
DF_null.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_v1_null.csv",index=False)
DF=DF.dropna(subset=['PRUID'])
pr_dict={'NL': '10',
        'PE': '11',
        'NS': '12',
        'NB': '13',
        'QC': '24',
        'ON': '35',
        'MB': '46',
        'SK': '47',
        'AB': '48',
        'BC': '59',
        'YT': '60',
        'NT': '61',
        'NU': '62'
        }

#invert dictionary

inv_dict = {v: k for k, v in pr_dict.items()}
DF['PRUID']=DF['PRUID'].astype(str).str.replace('.0','')
for pruid in list(DF.PRUID.unique()):
    temp=DF.copy()
    temp=temp.loc[temp.PRUID==pruid]
    temp.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_{}_v1.csv".format(inv_dict[pruid]),index=False)
