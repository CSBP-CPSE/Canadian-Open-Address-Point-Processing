"""
This script checks to make sure every source processed in the open addresses pipeline resulted in a final out.csv file,
and logs those that did not so that they can be fixed and re-run.
-Joseph Kuchar
13-01-2021
"""

import pandas as pd
import os
import json

date='2021-01-15'
OA_path = "/home/jovyan/data-vol-1/ODA/openaddresses_mod/sources/ca"
minio_bucket_name = 'deil-lode'

sources_file="/home/jovyan/minio/minimal-tenant1/private/ODA/OA_Processing/Output/{}/valid_sources.xlsx".format(date)
sources = pd.read_excel(sources_file)
sources["GEO_PROV"]=sources["GEO_PROV"].str.lower()

provs=list(sources["GEO_PROV"])
s_list=list(sources["JSON_NAME"])
temp=list(zip(provs,s_list))
skip=False
for pr, s in temp:
    if skip==False:
        
        json_source_file = "{}/{}/{}.json".format(OA_path,pr,s)
        with open(json_source_file, 'r') as fin:
            source_json = json.load(fin)
            layer = source_json['layers']['addresses'][0]['name']
            
            outdir = "/home/jovyan/minio/minimal-tenant1/private/ODA/OA_Processing/Output/{}/{}/{}_{}/data/data/addresses/{}".format(date, pr, pr, s, layer)
            if "out.csv" not in os.listdir(outdir):
                print("{} {} invalid run".format(pr, s))