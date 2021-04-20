mc cp standard/deil-lode/deil-lode/ODA/OA_PostProcessing/3_Spatial /home/jovyan/data-vol-1/ODA/processing/temporary_files/ --recursive
python merge.py
#rm -r /home/jovyan/data-vol-1/ODA/processing/temporary_files/3_Spatial
mc cp /home/jovyan/data-vol-1/ODA/processing/temporary_files/ODA*.csv standard/deil-lode/deil-lode/ODA/OA_PostProcessing/4_Merge/
#rm /home/jovyan/data-vol-1/ODA/processing/temporary_files/*
