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

DF=DF[["LAT", "LON",	"SOURCE_ID", "ODA_ID",	"GROUP_ID", "NUMBER",	"STREET",	"STR_NAME",	"STR_TYPE",	"STR_DIR",	"UNIT", 
       "CITY", "POSTCODE", "FULL_ADDR",	 "CITY_PCS", "STR_NAME_PCS", "STR_TYPE_PCS", "STR_DIR_PCS",
       "CSDUID", "CSDNAME",	"PRUID",	"Provider"	]]#,  "temp"]]

print(len(DF), 'records')



"""
Separate out entries with missing CSD/PRUID info
"""
DF_null=DF.copy()
DF_null=DF.loc[DF.PRUID.isnull()]
DF_null.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_v1_null.csv",index=False)
DF=DF.dropna(subset=['PRUID'])


name_map={'LAT': "latitude",
         "LON": "longitude",
         "NUMBER": "street_no",
         "STREET": "street",
         "STR_NAME": "str_name",
         "STR_TYPE": "str_type",
         "STR_DIR": "str_dir",
         "FULL_ADDR": "full_addr",
         "UNIT": "unit",
         "CITY": "city",
         "POSTCODE": "postal_code",
         "STR_NAME_PCS": "str_name_pcs",
         "STR_DIR_PCS": "str_dir_pcs",
         "STR_TYPE_PCS": "str_type_pcs",
         "CITY_PCS": "city_pcs",
         "CSDUID": "csduid",
         "CSDNAME": "csdname",
         "PRUID": "pruid",
         "Provider": "provider",
         "ODA_ID": "id",
         "SOURCE_ID": "source_id",
         "GROUP_ID": "group_id"
         }

fr_map={
         "street_no": "numero_rue",
         "street": "rue",
         "str_name": "nom_rue",
         "str_type": "type_rue",
         "str_dir": "dir_rue",
         "full_addr": "adr_complete",
         "unit": "unite",
         "city": "ville",
         "postal_code": "code_postal",
         "str_name_pcs": "nom_rue_pcs",
         "str_dir_pcs": "dir_rue_pcs",
         "str_type_pcs": "type_rue_pcs",
         "city_pcs": "ville_pcs",
         "csduid": "sdridu",
         "csdname": "sdrnom",
         "pruid": "pridu",
         "provider": "fournisseur",
         "source_id": "id_source",
         "group_id": "id_group"
         }

DF.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_v1.csv",index=False)

DF=DF.rename(columns=name_map)
#split into province level files


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
DF['pruid']=DF['pruid'].astype(str).str.replace('.0','')
for pruid in list(DF.pruid.unique()):
    temp=DF.copy()
    temp=temp.loc[temp['pruid']==pruid]
    temp.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA_{}_v1.csv".format(inv_dict[pruid]),index=False, encoding="utf-8")
    temp=temp.rename(columns=fr_map)
    temp.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/BDOA_{}_v1.csv".format(inv_dict[pruid]),index=False, encoding="utf-8")
