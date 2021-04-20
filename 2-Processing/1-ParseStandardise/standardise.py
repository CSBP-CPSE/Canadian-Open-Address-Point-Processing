"""
This script reads in output from the openaddresses pipeline, and if the type, direction, and name don't exist then they are determined using modified RASK
arguments:
pr: province (eg, AB, BC)
csv_in: path to input csv
json_in: path to input json
name_out: path for output csv
-Joseph
"""
import pandas as pd
from modified_rask import RASK

import json
import os.path
from os import path
import argparse



def full_addr(df,cols):
    #fill empty entries in full address with a concatenation of unit, number, and street.
#    if 'full_addr' not in cols:
#        return df
#    else:
#        if 'unit' in cols:
#            df['FULL_ADDR']=df['UNIT']+' '+df['NUMBER']+' '+df['STREET']
    df['TEMP']=df['UNIT']+' '+df['NUMBER']+' '+df['STREET']
    df['TEMP']=df['TEMP'].str.replace(' +',' ',regex=True)
    df['TEMP']=df['TEMP'].str.strip()
    df['FULL_ADDR']=df['FULL_ADDR'].fillna(df['TEMP'])
    df['FULL_ADDR'] = df[['FULL_ADDR', 'TEMP']].apply(lambda x: x[0] if x[0] else x[1], axis=1)
    df=df.drop(columns=['TEMP'])
    return df
    
def city_name(df,cols):
    if 'city' not in cols:
        df['CITY_PCS'] = df['CITY'].str.upper()
        return df
    else:
        city_name=s.replace('city_of_','').replace('_',' ')
        df['CITY_PCS'] = city_name.upper().strip()
        return df

def parse_with_rask(df, cols):
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


    STREET=list(df['STREET'])
    STREET_DIR=list(df['STR_DIR'])
    STREET_TYPE=list(df['STR_TYPE'])
    STREET_NAME=list(df['STR_NAME'])
        

    DIR=[]
    TYPE=[]
    NAME=[]
    processing=[]
    for i in range(len(STREET)):
        street=STREET[i]
        if street=='':
            DIR.append('')
            NAME.append('')
            TYPE.append('')
        else:
            if ('str_name' not in cols) and ('str_type' not in cols) and (STREET_NAME[i]!=''): #if there's already a name and type column, then we will use those
                std_add = RASK(STREET_NAME[i], str_typ=STREET_TYPE[i], str_dir=STREET_DIR[i], pr_uid=pr_dict[pr.upper()])
            else:
                std_add = RASK(street, pr_uid=pr_dict[pr.upper()])

            std_add.run()

            NAME.append(std_add.srch_nme)
            DIR.append(std_add.srch_dir)
            TYPE.append(std_add.srch_typ)

    #if 'str_name' in cols:
    df['STR_NAME_PCS'] = NAME
    df['STR_NAME_PCS'] = df['STR_NAME_PCS'].str.upper()
     #   processing.append('N')
    #if 'str_dir' in cols:
    df['STR_DIR_PCS'] = DIR
    df['STR_DIR_PCS'] = df['STR_DIR_PCS'].str.upper()
      #  processing.append('D')
    #if 'str_type' in cols:
    df['STR_TYPE_PCS'] = TYPE
    df['STR_TYPE_PCS'] = df['STR_TYPE_PCS'].str.upper()
       # processing.append('T')
        #Add a column that indicates which of Name, Type, and Direction were inferred from the street column
    #process_str=''
    #for i in processing:
    #    process_str+=i
    #df['PROCESSING']=process_str
    return df
    


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Apply modified RASK and other standardization steps to OpenAddresses output')
    parser.add_argument('prov_in',
                        help='province name (caps)')
    parser.add_argument('csv_in',
                        help='Name/Path of input csv file')
    parser.add_argument('json_in',
                        help='name/path to json file')
    parser.add_argument('name_out',
                        help='Name/Path of output csv file')
    args = parser.parse_args()
    
    pr = args.prov_in.lower()
    PR = args.prov_in.upper()

    name_in = args.csv_in
    json_in = args.json_in
    name_out = args.name_out
    #read in csv
    df_in = pd.read_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/"+name_in, dtype='str', low_memory=False)
    s=name_in.replace(".csv","")

    cols_master=['str_name','str_type','str_dir','full_addr', 'unit','city']
    cols=cols_master.copy()
    """
    Check the json file to see what columns were processed and which weren't.
    The idea is to start with a list of the columns we want to make sure are filled,
    and pop them out of the list if they are in the json (so that they've already been incorporated)
    then we can process the street column to fill the ones that are left.
    """
    with open(json_in, 'r') as fin:
        source_json = json.load(fin)
        layer = source_json['layers']['addresses'][0]['name']
        conform = source_json['layers']['addresses'][0]['conform']
        print(conform.keys())
        for col in cols_master:
            if col in conform.keys():
                cols.remove(col)


            
    df_in=df_in.fillna('')
    df_out = full_addr(df_in,cols)
    df_out = parse_with_rask(df_out, cols)
    df_out = city_name(df_out, cols)
    df_out.to_csv("/home/jovyan/data-vol-1/ODA/processing/temporary_files/"+name_out, index=False)