import pandas as pd
import json

df=pd.read_excel("/home/jovyan/data-vol-1/ODA/processing/valid_sources.xlsx")
OA_PATH = "/home/jovyan/data-vol-1/ODA/openaddresses_mod/sources/ca"

Dates=list(df['Date'].str.strip("'"))
names=list(df['JSON_NAME'])
provs=list(df['GEO_PROV'])

f_out='run_all.sh'
f = open(f_out, 'w')
for i in range(len(df)):
    pr=provs[i].lower()
    date=Dates[i]
    s=names[i]
    json_source_file = "{}/{}/{}.json".format(OA_PATH,pr,s)
    with open(json_source_file, 'r') as fin:
        source_json = json.load(fin)
        layer = source_json['layers']['addresses'][0]['name']
    
    line1="mc cp standard/deil-lode/deil-lode/ODA/OA_Processing/Output/{}/{}/{}_{}/data/data/addresses/{}/out.csv /home/jovyan/data-vol-1/ODA/processing/temporary_files/{}.csv \n".format(date,pr,pr,s,layer,s)
    line2="python standardise.py {} {}.csv {} {}_1.csv\n".format(pr,s,json_source_file,s)
    line3="mc cp /home/jovyan/data-vol-1/ODA/processing/temporary_files/{}_1.csv standard/deil-lode/deil-lode/ODA/OA_PostProcessing/1_Parsing/{}/{}_out.csv\n".format(s,pr,s)
    line4="rm /home/jovyan/data-vol-1/ODA/processing/temporary_files/*.csv \n"

    f.write(line1)
    f.write(line2)
    f.write(line3)
    f.write(line4)

f.close()