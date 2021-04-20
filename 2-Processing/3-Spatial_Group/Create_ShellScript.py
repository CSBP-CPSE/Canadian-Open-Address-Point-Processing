import pandas as pd

df=pd.read_excel("/home/jovyan/data-vol-1/ODA/processing/valid_sources.xlsx")

Dates=list(df['Date'].str.strip("'"))
names=list(df['JSON_NAME'])
provs=list(df['GEO_PROV'])

f_out='run_all.sh'
f = open(f_out, 'w')
for i in range(len(df)):
    pr=provs[i].lower()
    date=Dates[i]
    s=names[i]

    line1="mc cp standard/deil-lode/deil-lode/ODA/OA_PostProcessing/2_Dedupe/{}/{}_out.csv /home/jovyan/data-vol-1/ODA/processing/temporary_files/{}_in.csv \n".format(pr,s,s)
    line2="python spatial_group.py {}_in.csv {}_out.csv \n".format(s,s)
    line3="rm /home/jovyan/data-vol-1/ODA/processing/temporary_files/*_in.csv \n"

    line4="mc cp /home/jovyan/data-vol-1/ODA/processing/temporary_files/*_out.csv standard/deil-lode/deil-lode/ODA/OA_PostProcessing/3_Spatial/{}/ \n".format(pr)
    line5="rm /home/jovyan/data-vol-1/ODA/processing/temporary_files/*.csv \n"

    f.write(line1)
    f.write(line2)
    f.write(line3)
    f.write(line4)
    f.write(line5)

f.close()