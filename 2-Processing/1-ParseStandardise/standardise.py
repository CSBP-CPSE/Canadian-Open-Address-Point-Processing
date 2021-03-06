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

    df['TEMP']=df['UNIT']+' '+df['NUMBER']+' '+df['STREET']
    df['TEMP']=df['TEMP'].str.replace(' +',' ',regex=True)
    df['TEMP']=df['TEMP'].str.strip()
    df['FULL_ADDR']=df['FULL_ADDR'].fillna(df['TEMP'])
    df['FULL_ADDR'] = df[['FULL_ADDR', 'TEMP']].apply(lambda x: x[0] if x[0] else x[1], axis=1)
    df=df.drop(columns=['TEMP'])
    return df
    
def city_name(df,cols):
    #if the city column is not filled in, attempt to fill in city_pcs from the file name
    if 'city' not in cols:
        df['CITY_PCS'] = df['CITY'].str.upper()
        return df
    else:
        city_name=s.replace('city_of_','').replace('_',' ')
        df['CITY_PCS'] = city_name.upper().strip()
        return df

def specific_fix(df, PR, s):
    """
    This function does string replacements and other operations for specific input files when issues are found.
    So far, this function deals with French addresses in Ottawa that are formatted differently than expected,
    replaces ";" with "l" in New Brunswick, and removes some weird things like "\r", "\s", etc 
    removes "Saskatoon, SK" from addresses in Saskatoon,
    Courtenay in BC contains asterixes in the NUMBER column,
    parses "unite: ##" from street column in Quebec City
    
    """
    #case 1, Ottawa
    if PR=="ON" and s=="city_of_ottawa":
        street=list(df['STREET'])
        for i in range(len(street)):
            split=street[i].split(',')
            if len(split)==2:
                new_street=split[1]+' '+split[0]
                new_street=new_street.strip()
                #replace a space after an apostrophe with just the apostrophe (so L' Eglise becomes L'Eglise)
                new_street=new_street.replace("' ", "'")
                street[i]=new_street
        df["STREET"] = street
                
    #case 2, NB
    if PR=="NB" and s=="province":
        print('province of NB')
        df["STREET"]=df["STREET"].str.replace(";","l",regex=False)
        df["STR_NAME"]=df["STR_NAME"].str.replace(";","l",regex=False)

        remove_list = [r"\s", r"\r", r"\n", r"\w"]
        
        for i in remove_list:
            df["STREET"]=df["STREET"].str.replace(i,'',regex=False)
            df["STR_NAME"]=df["STR_NAME"].str.replace(i,'',regex=False)
    
    #case 3, Saskatoon
    if PR=="SK" and s=="saskatoon":
        df["STREET"]=df["STREET"].str.replace(", SASKATOON","",regex=False)
        df["STREET"]=df["STREET"].str.replace(", Saskatoon, SK, Canad","",regex=False)
        df["STREET"]=df["STREET"].str.replace(", Saskatoon, SK Canad","",regex=False)

    #case 4, Courtenay
    if PR=="BC" and s=="city_of_courtenay":
        df["NUMBER"]=df["NUMBER"].str.replace("*","",regex=False)
        df["FULL_ADDR"]=df["FULL_ADDR"].str.replace("*","",regex=False)
        
        #some numbers have a hyphen which seem to designate UNIT - NUMBER
        number=list(df['NUMBER'])
        unit=list(df["UNIT"])
        for i in range(len(number)):
            split=number[i].split('-')
            if len(split)==2:
                new_num = split[1]
                new_unit = split[0]
                
                new_num = new_num.strip()
                new_unit = new_unit.strip()


                number[i] = new_num
                unit[i] = new_unit
        df["NUMBER"] = number
        df["UNIT"] = unit
        
    if PR=="QC" and s=="quebec_city":
        street=list(df['STREET'])
        unit=list(df["UNIT"])
        for i in range(len(street)):
            split=street[i].split('unite :')
            if len(split)==2:
                new_street=split[0]
                new_unit = split[1]
                new_street=new_street.strip()  
                new_unit=new_unit[1]
                street[i] = new_street
                unit[i] = new_unit
        df["STREET"] = street
        df["UNIT"] = unit
        
    if PR=="SK" and s=="regina":
        df.loc[df["STREET"]=="A NORTH RAILWAY STREET", "STR_DIR"] = "N"
        df.loc[df["STREET"]=="A NORTH RAILWAY STREET", "UNIT"] = "A"
        df.loc[df["STREET"]=="A NORTH RAILWAY STREET", "STREET"] = "NORTH RAILWAY STREET"
        df.loc[df["STREET"]=="B NORTH RAILWAY STREET", "STR_DIR"] = "N"
        df.loc[df["STREET"]=="B NORTH RAILWAY STREET", "UNIT"] = "B"
        df.loc[df["STREET"]=="B NORTH RAILWAY STREET", "STREET"] = "NORTH RAILWAY STREET"

    return df

def remove_nulltext(df):
    for c in ["NUMBER","STREET", "STR_DIR", "STR_TYPE", "STR_NAME", "FULL_ADDR", "UNIT"]:
        #if the whole cell is "nan"
        df[c]=df[c].str.replace(r"^nan$","",regex=True)
        #if the cell contains "null" in brackets
        df[c]=df[c].str.replace(r"[Null]","",regex=False)
        df[c]=df[c].str.replace(r"[NULL]","",regex=False)
        df[c]=df[c].str.replace(r"[null]","",regex=False)
        df[c]=df[c].str.replace(r"<Null>","",regex=False)
        df[c]=df[c].str.replace(r"<NULL>","",regex=False)
    
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

    df['STR_NAME_PCS'] = NAME
    df['STR_NAME_PCS'] = df['STR_NAME_PCS'].str.upper()
    df['STR_DIR_PCS'] = DIR
    df['STR_DIR_PCS'] = df['STR_DIR_PCS'].str.upper()
    df['STR_TYPE_PCS'] = TYPE
    df['STR_TYPE_PCS'] = df['STR_TYPE_PCS'].str.upper()

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
    df_in = pd.read_csv("/home/jovyan/Canadian-Open-Address-Point-Processing/2-Processing/temporary_files/"+name_in, dtype='str', low_memory=False)
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
    df_out = remove_nulltext(df_in)
    df_out = specific_fix(df_out, PR, s)
    df_out = full_addr(df_out,cols)
    df_out = parse_with_rask(df_out, cols)
    df_out = city_name(df_out, cols)
    df_out.to_csv("/home/jovyan/Canadian-Open-Address-Point-Processing/2-Processing/temporary_files/"+name_out, index=False)